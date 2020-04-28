from django.urls import path

from .views import cancel_sub, subscription, update_plan

app_name = 'payments'

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('cancel_sub/<int:user_id>', cancel_sub, name='cancel_sub'),
    path('update_plan/<int:user_id>', update_plan, name='update_plan'),
]
