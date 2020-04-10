from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register('events', api.EventViewSet)
router.register('webhooks', api.WebhookViewSet)

urlpatterns = [
    # Web interface endpoints
    path('', views.index, name='index'),
    path('view/<int:pk>', views.webhook_view, name='webhook_view'),
    path('edit/<int:pk>', views.webhook_edit, name='webhook_edit'),
    path('new', views.webhook_new, name='webhook_new'),
    path('trigger/<str:name>', views.trigger, name='trigger'),
    # REST API endpoints
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
