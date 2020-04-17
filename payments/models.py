from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Products(models.Model):
    name = models.CharField(max_length=30)
    stripe_id = models.CharField(max_length=50)


class Plans(models.Model):
    nickname = models.CharField(max_length=30)
    stripe_id = models.CharField(max_length=50)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.stripe_customer_id


class Subscription(models.Model):

    plans = (('MONTHLY', 'Basic monthly plan (10kr/month)'),
             ('YEARLY', 'Two months free (100kr/year)'),
             ('THREE_YEAR', 'Four months free (280kr/3 years)'))

    stripe_subscription_id = models.CharField(max_length=50,
                                              primary_key=True,
                                              default=0)
    stripe_customer_id = models.ForeignKey('Customer',
                                           db_column='stripe_customer_id',
                                           on_delete=models.CASCADE,
                                           default=0)
    is_active = models.BooleanField(default=False)
    plan_type = models.CharField(max_length=15,
                                 choices=plans,
                                 default='MONTHLY')
    initiated_on = models.DateField(null=True, blank=True)
    terminated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.stripe_subscription_id
