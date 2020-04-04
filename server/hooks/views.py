from concurrent.futures.thread import ThreadPoolExecutor

import requests
from django.http import HttpResponse

from .models import Webhook

# TODO Pick ideal defaults and make them configurable
HTTP_POST_REQUEST_POOL_SIZE = 10
HTTP_POST_REQUEST_RETRIES = 3
HTTP_POST_REQUEST_BACKOFF_FACTOR_SECONDS = 0.3

executor = ThreadPoolExecutor(max_workers=HTTP_POST_REQUEST_POOL_SIZE)


def index(request):
    return HttpResponse("Webhooks Manager")


def trigger(request, event):
    response = "Triggering event %s ..."
    schedule_webhooks_for_event(event)
    return HttpResponse(response % event)


def enqueue(url, event):
    print("TODO: Add to retry queue url = {}, event = {}".format(url, event))


def post_url(url, event):
    payload = {'event': event}
    print("Making POST request at {} with body {}".format(url, payload))
    try:
        response = requests.post(url=url, data=payload)
        if response.status_code not in range(200, 299):  # TODO Better check for valid 2xx codes
            enqueue(url, event)
    except requests.exceptions.RequestException:
        print("ERROR: Failed POST request at {}".format(url))
        enqueue(url, event)


def schedule_webhooks_for_event(event):
    for hook in Webhook.objects.filter(events__name=event):
        print("Submitting webhook {} for event {} ...".format(hook.name, event))
        executor.submit(post_url, hook.url, event)
