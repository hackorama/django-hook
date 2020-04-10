from rest_framework import viewsets

from .models import Event, Webhook
from .serializers import EventSerializer, WebhookSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer


class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all().order_by('name')
    serializer_class = WebhookSerializer
