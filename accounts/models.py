from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.models import Clinic

User = get_user_model()


class Modalities(models.Model):
    '''
    Model for saving a practitioners modalities
    '''
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''
    Model for saving a practitioners profile
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=5000, blank=True)
    mods = models.ManyToManyField(Modalities, blank=True)
    phone = PhoneNumberField(blank=True)
    clinics = models.ManyToManyField(Clinic, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.email

    def get_owner(self):
        return self.user.name

    def save(self):
        super().save()
