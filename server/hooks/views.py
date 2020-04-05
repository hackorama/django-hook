import logging

import requests
from django.http import HttpResponse
from django.template import loader
from huey import RetryTask
from huey.contrib.djhuey import task

from .models import Webhook

logger = logging.getLogger(__name__)

# TODO Pick ideal default and make it configurable
HTTP_POST_REQUEST_RETRY_DELAY = 3


def index(request):
    template = loader.get_template('hooks/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def trigger(request, event):
    response = "Triggering event %s ..."
    schedule_webhooks_for_event(event)
    return HttpResponse(response % event)


@task(retry_delay=HTTP_POST_REQUEST_RETRY_DELAY)
def post_url(url, event):
    payload = {'event': event}
    logger.info("Requesting POST %s %s", url, payload)
    try:
        response = requests.post(url=url, data=payload)
        if response.status_code not in range(200, 299):  # TODO Better check for valid 2xx codes
            logger.warning("Unexpected response code %s from %s", response.status_code, url)
            raise RetryTask()  # Queues the task for retry
    except requests.exceptions.RequestException:
        logger.error("Failed POST request at %s", url)
        raise RetryTask()  # Queues the task for retry


def schedule_webhooks_for_event(event):
    for hook in Webhook.objects.filter(events__name=event):
        logger.info("Adding webhook=%s for event=%s to task queue", hook.name, event)
        post_url(hook.url, event)
