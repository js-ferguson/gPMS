from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Profile

User = get_user_model()


class ProfileForm(ModelForm):

    mods = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Profile
        fields = (
            'bio',
            'mods',
            'phone',
            'personnummer',
            'street',
            'city',
            'consent',
        )
