from django.contrib import admin

from .models import Customer, Plans, Products, Subscription

admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Plans)
