from django.conf.urls import url
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register('events', api.EventViewSet)
router.register('webhooks', api.WebhookViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Hooks API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    # REST API documentation
    url(r'^api-help/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
