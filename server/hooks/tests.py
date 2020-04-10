import logging

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import Event, Webhook

logger = logging.getLogger(__name__)


class EventTests(APITestCase):

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


class WebhookTests(APITestCase):

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
