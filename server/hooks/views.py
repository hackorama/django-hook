import requests
from django.http import HttpResponse
from huey import RetryTask
from huey.contrib.djhuey import task

from .models import Webhook

# TODO Pick ideal default and make it configurable
HTTP_POST_REQUEST_RETRY_DELAY = 3


def index(request):
    return HttpResponse("Webhooks Manager")


def trigger(request, event):
    response = "Triggering event %s ..."
    schedule_webhooks_for_event(event)
    return HttpResponse(response % event)


@task(retry_delay=HTTP_POST_REQUEST_RETRY_DELAY)
def post_url(url, event):
    payload = {'event': event}
    print("Making POST request at {} with body {}".format(url, payload))
    try:
        response = requests.post(url=url, data=payload)
        if response.status_code not in range(200, 299):  # TODO Better check for valid 2xx codes
            raise RetryTask()  # Queues the task for retry
    except requests.exceptions.RequestException:
        print("ERROR: Failed POST request at {}".format(url))
        raise RetryTask()  # Queues the task for retry


def schedule_webhooks_for_event(event):
    for hook in Webhook.objects.filter(events__name=event):
        print("Adding webhook {} for event {} to task queue".format(hook.name, event))
        post_url(hook.url, event)
