from django import forms

from .models import Webhook


class WebhookForm(forms.ModelForm):
    class Meta:
        model = Webhook
        fields = ('name', 'url',)
