from rest_framework import serializers

from .models import Event, Webhook


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name']


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ['id', 'name', 'url', 'events']
        extra_kwargs = {'events': {'required': False}}
