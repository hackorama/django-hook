import datetime
import logging

import requests
from huey import RetryTask
from huey.contrib.djhuey import task

from .models import Webhook

logger = logging.getLogger(__name__)

# TODO Pick ideal default and make it configurable. Using a low retry delay for dev testing.
HTTP_POST_REQUEST_RETRY_DELAY = 3


def schedule_webhooks_for_event(event):
    """
    Schedules the registered webhooks for the given event for execution
    """
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    payload = {'event': event.name, 'time': now}
    for webhook in Webhook.objects.filter(events__name=event.name):
        logger.info("Adding webhook \"%s\" (%s) with payload \"%s\" to task queue", webhook.name, webhook.url, payload)
        post_url(webhook.url, payload)


@task(retry_delay=HTTP_POST_REQUEST_RETRY_DELAY)
def post_url(url, payload):
    """
    A Huey task queue task that will be submitted to Huey task queue to be handled by Huey workers.

    On failures during the task execution raising Huey specific RetryTask exception will put the task back into the
    task queue to be retried.

    This task executes a POST request of the given payload as BODY to the given URL.
    Any failures or non-successful HTTP response code will cause re-queueing of the task.
    """
    logger.info("Requesting POST %s %s", url, payload)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.post(url=url, data=payload, headers=headers)
        if response.status_code not in range(200, 299):  # TODO Better check for valid 2xx codes
            logger.warning("Unexpected response code %s from %s", response.status_code, url)
            raise RetryTask()  # Queues the task for retry
    except requests.exceptions.RequestException:
        logger.error("Failed POST request at %s", url)
        raise RetryTask()  # Queues the task for retry
