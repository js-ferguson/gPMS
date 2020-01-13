from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    personnummer = models.CharField(max_length=12)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    consent = models.BooleanField()

    def __str__(self):
        return self.user.email

    def save(self):
        super().save()


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
