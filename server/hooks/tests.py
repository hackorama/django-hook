import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import Event, Webhook

logger = logging.getLogger(__name__)


class EventAPITests(APITestCase):

    def test_create_event(self):
        """
        Ensure we can create a new event
        """
        url = reverse("event-list")
        data = {"name": "test-one"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().name, "test-one")


class WebhookAPITests(APITestCase):

    def test_create_webhook(self):
        """
        Ensure we can create a new webhook
        """
        url = reverse("webhook-list")
        data = {"name": "test-hook", "url": "http://localhost/test", "events": []}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Webhook.objects.count(), 1)
        self.assertEqual(Webhook.objects.get().name, "test-hook")


class WebAppTests(TestCase):

    def test_index_webhook(self):
        """
        Test the webhook listing on index page
        """
        webhook = Webhook.objects.create(name="test", url="http://test/test")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['webhooks'].count(), 1)
        self.assertEqual(response.context['webhooks'].first().name, "test")
        self.assertEqual(response.status_code, 200)

    def test_index_event(self):
        """
        Test the event listing on index page
        """
        event = Event.objects.create(name="test")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['events'].count(), 1)
        self.assertEqual(response.context['events'].first().name, "test")
        self.assertEqual(response.status_code, 200)
