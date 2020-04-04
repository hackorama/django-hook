from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trigger/<str:event>', views.trigger, name='trigger'),
]
