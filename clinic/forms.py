from django import forms
from django.contrib.auth import get_user_model

from .models import Clinic, Reviews

User = get_user_model()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = (
            'title',
            'body',
        )


class RegisterClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = (
            'name',
            'phone',
            'description',
            'web',
            'street',
            'city',
        )
