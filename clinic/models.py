from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from payments.models import Customer, Subscription

User = get_user_model()


class Clinic(models.Model):
    practitioner = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    web = models.CharField(null=True, blank=True, max_length=128)
    name = models.CharField(max_length=128, )
    phone = PhoneNumberField()
    description = models.TextField(max_length=5000)
    street = models.CharField(max_length=128, )
    city = models.CharField(max_length=128, )
    instagram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()

    def is_searchable(self):
        user = self.practitioner
        customer = Customer.objects.get(user=user)
        subscription = Subscription.objects.get(customer=customer)
        if subscription.end_billing_period >= datetime.today().date():
            return True

    def get_clinic_details(self):
        is_searchable = self.is_searchable()
        from accounts.models import Profile
        phone = str(self.phone)
        name = self.practitioner.get_full_name()
        profile = Profile.objects.get(user=Clinic.objects.get(
            pk=self.id).practitioner)
        mods = profile.mods.all().values('name') if profile else []
        mods = [(q['name']) for q in mods]

        return {
            "lat": self.lat,
            "lng": self.lng,
            "name": self.name,
            "id": self.id,
            "prac_name": name,
            "phone": phone,
            "mods": mods,
            "description": self.description,
            "street": self.street,
            "city": self.city,
            "is_searchable": is_searchable,
        }


class Reviews(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
