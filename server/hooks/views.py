import datetime
import logging
from collections import defaultdict

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from huey import RetryTask
from huey.contrib.djhuey import task

from .forms import WebhookForm
from .models import Event
from .models import Webhook

logger = logging.getLogger(__name__)

# TODO Pick ideal default and make it configurable
HTTP_POST_REQUEST_RETRY_DELAY = 3


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    webhooks = Webhook.objects.all()
    events = Event.objects.all()
    webhooks_events = defaultdict(list)
    for event in events.all():
        for hook in Webhook.objects.filter(events__name=event):
            webhooks_events[event.name].append(hook.name)
    context = {
        'webhooks': webhooks,
        'events': events,
        'webhooks_events': webhooks_events
    }
    return render(request, 'hooks/index.html', context)


def trigger(request, name):
    event = Event.objects.filter(name=name).first()  # Avoiding DoesNotExist handling
    if event is None:
        logger.error("Cannot trigger invalid event=%s", name)
    else:
        schedule_webhooks_for_event(event)
    return render(request, 'hooks/trigger.html', {'name': name, 'event': event})


def schedule_webhooks_for_event(event):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    payload = {'event': event.name, 'time': now}
    for webhook in Webhook.objects.filter(events__name=event.name):
        logger.info("Adding webhook \"%s\" (%s) with payload \"%s\" to task queue", webhook.name, webhook.url, payload)
        post_url(webhook.url, payload)


@task(retry_delay=HTTP_POST_REQUEST_RETRY_DELAY)
def post_url(url, payload):
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


def webhook_view(request, pk):
    webhook = get_object_or_404(Webhook, pk=pk)
    events = webhook.events.all()  # TODO Optimize related lookup query
    return render(request, 'hooks/webhook_view.html', {'webhook': webhook, 'events': events})


def webhook_new(request):
    if request.method == "POST":
        form = WebhookForm(request.POST)
        if form.is_valid():
            webhook = form.save(commit=False)
            webhook.save()
            form.save_m2m()
            return redirect('webhook_view', pk=webhook.pk)
    else:
        form = WebhookForm()
    return render(request, 'hooks/webhook_edit.html', {'form': form})


def webhook_edit(request, pk):
    webhook = get_object_or_404(Webhook, pk=pk)
    if request.method == "POST":
        form = WebhookForm(request.POST, instance=webhook)
        if form.is_valid():
            webhook = form.save(commit=False)
            webhook.save()
            form.save_m2m()
            return redirect('webhook_view', pk=webhook.pk)
    else:
        form = WebhookForm(instance=webhook)
    return render(request, 'hooks/webhook_edit.html', {'form': form})
