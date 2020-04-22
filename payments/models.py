from datetime import datetime

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET
PLAN_CHOICES = (('monthly', 'Monthly'), ('yearly', 'Yearly'), ('free', 'Free'))


class Products(models.Model):
    name = models.CharField(max_length=30)
    stripe_product_id = models.CharField(max_length=50)


class Plans(models.Model):  # Membership
    slug = models.SlugField()
    stripe_plan_id = models.CharField(max_length=50)
    plan_type = models.CharField(choices=PLAN_CHOICES,
                                 default='free',
                                 max_length=30)
    price = models.IntegerField(default=10)
    duration = models.CharField(max_length=20, default='ongoing')
    description = models.CharField(max_length=100, default='description')

    def __str__(self):
        return self.plan_type


class Customer(models.Model):  # UserMembership
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100)
    sub = models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.stripe_customer_id


def post_save_customer_create(sender, instance, created, *args, **kwargs):
    customer, created = Customer.objects.get_or_create(user=instance)

    if customer.stripe_customer_id is None or customer.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        free_membership = Plans.objects.get(plan_type='free')
        customer.stripe_customer_id = new_customer_id['id']
        customer.sub = free_membership
        customer.save()


post_save.connect(post_save_customer_create, sender=User)


class Subscription(models.Model):  # Subscription
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    initiated_on = models.DateField(null=True, blank=True)
    terminated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user_customer.user.email

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)
