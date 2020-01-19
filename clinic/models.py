from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django_google_maps import fields as map_fields

User = get_user_model()


#class Coordinates(models.Model):
#    latitude = models.FloatField()
#    longitude = models.FloatField()


    #def __str__(self):
    #    return {"lat": self.latitude, "long": self.longitude}


class Clinic(models.Model):
    practitioner = models.OneToOneField(User, on_delete=models.CASCADE)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    name = models.CharField(max_length=128, )
    phone = PhoneNumberField()
    description = models.TextField(max_length=5000)
    street = models.CharField(max_length=128, )
    city = models.CharField(max_length=128, )

    def __str__(self):
        return self.name

    def save(self):
        super().save()
