from django.urls import path

from .views import cancel_sub, subscription

app_name = 'payments'

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('cancel_sub/<int:user_id>', cancel_sub, name='cancel_sub'),
]
