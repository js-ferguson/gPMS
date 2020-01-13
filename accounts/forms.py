# from django import forms
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('phone', 'personnummer', 'street', 'city', 'consent', )
