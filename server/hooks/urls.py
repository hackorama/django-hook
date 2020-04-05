from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:pk>', views.webhook_view, name='webhook_view'),
    path('edit/<int:pk>', views.webhook_edit, name='webhook_edit'),
    path('new', views.webhook_new, name='webhook_new'),
    path('trigger/<str:event>', views.trigger, name='trigger'),
]
