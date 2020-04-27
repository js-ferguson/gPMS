from django.contrib import admin

from .models import Customer, Plans, Subscription

admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Plans)
