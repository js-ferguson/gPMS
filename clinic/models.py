from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Clinic(models.Model):
    practitioner = models.OneToOneField(User,
                                        on_delete=models.CASCADE)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=128, )
    phone = PhoneNumberField()
    description = models.TextField(max_length=5000)
    street = models.CharField(max_length=128, )
    city = models.CharField(max_length=128, )

    def __str__(self):
        return self.name

    def save(self):
        super().save()

    def get_clinic_details(self):
        from accounts.models import Profile
        phone = str(self.phone)
        name = self.practitioner.get_full_name()
        profile = Profile.objects.get(user=Clinic.objects.get(pk=self.id).practitioner)
        mods = profile.mods.all().values('name') if profile else []
        mods = [(q['name']) for q in mods]

        return {"lat": self.lat,
                "lng": self.lng, "name": self.name,
                "prac_name": name, "phone": phone,
                "mods": mods, "description": self.description,
                "street": self.street,
                "city": self.city}
