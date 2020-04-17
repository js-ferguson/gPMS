from django.urls import path

from .views import subscription

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('sub/', subscription, name='sub'),
]
