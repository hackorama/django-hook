from django.contrib import admin

from .models import Event
from .models import Webhook

admin.site.register(Event)
admin.site.register(Webhook)
