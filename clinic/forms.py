from django import forms
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput

from .models import Clinic, Reviews

User = get_user_model()


class ReviewForm(forms.ModelForm):
    '''
    Form for users to submit clinic reviews.
    '''
    class Meta:
        model = Reviews
        fields = (
            'title',
            'body',
        )
        labels = {
            "title": "",
            "body": "",
        }
        widgets = {
            'title': TextInput(attrs={'placeholder': "Title"}),
            'body': Textarea(attrs={'placeholder': "Review"})
        }


class RegisterClinicForm(forms.ModelForm):
    '''
    Form for practitioners to submit their clinic details during signup.
    '''
    class Meta:
        model = Clinic
        fields = (
            'name',
            'phone',
            'description',
            'web',
            'facebook',
            'instagram',
            'twitter',
            'linkedin',
            'street',
            'city',
        )
        widgets = {
            'phone':
            TextInput(
                attrs={'placeholder': "Phone number in international format"}),
        }
