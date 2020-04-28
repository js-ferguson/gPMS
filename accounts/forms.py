from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, Select, Textarea, TextInput

from django_auth.models import CustomUser

from .models import Modalities, Profile

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
            'street',
            'city',
            'consent',
        )
        labels = {
            'consent':
            "Do you consent to have your clinic's details listed publically",
        }
        widgets = {
            'phone':
            TextInput(
                attrs={'placeholder': "Phone number in international format"}),
            'bio':
            Textarea(attrs={'placeholder': "Tell us a little about your self"})
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


class ModsUpdateForm(forms.Form):
    mods = forms.CharField(label='Modalities', max_length=500)


PLAN_CHOICES = [('monthly', 'Monthly'), ('yearly', 'Yearly')]


class SubUpdateForm(forms.Form):
    sub = forms.CharField(label="Change plan",
                          widget=forms.Select(choices=PLAN_CHOICES))
