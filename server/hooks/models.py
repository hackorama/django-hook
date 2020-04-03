from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Webhook(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.url)
