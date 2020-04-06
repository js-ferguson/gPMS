from django.conf.urls import path

from .views import checkout

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
]
