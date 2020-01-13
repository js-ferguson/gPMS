from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class Clinic(models.Model):
    practitioner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, required=True)
    phone = PhoneNumberField()
    street = models.CharField(max_length=128, required=True)
    city = models.CharField(max_length=128, required=True)
