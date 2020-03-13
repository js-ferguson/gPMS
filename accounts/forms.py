from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, TextInput

from django_auth.models import CustomUser

from .models import Profile

User = get_user_model()


class ProfileForm(ModelForm):

    mods = forms.CharField(
        max_length=50,
        required=False,
        label="Modalities",
        widget=forms.TextInput(
            attrs={
                'placeholder': "Comma separated list e.g. Massage, Acupuncture"
            }))

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
        labels = {
            'consent':
            "Do you consent to have your clinic's details listed publically"
        }
        widgets = {
            'mods': TextInput(attrs={'placeholder': "Comma separated list"}),
        }


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'phone', 'street', 'city')
