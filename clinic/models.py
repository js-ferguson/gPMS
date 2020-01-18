from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


    def __str__(self):
        return {"lat": self.latitude, "long": self.longitude}


class Clinic(models.Model):
    practitioner = models.OneToOneField(User, on_delete=models.CASCADE)
   # location = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, )
    phone = PhoneNumberField()
    description = models.TextField(max_length=5000)
    street = models.CharField(max_length=128, )
    city = models.CharField(max_length=128, )

    def __str__(self):
        return self.name

    def save(self):
        super().save()
