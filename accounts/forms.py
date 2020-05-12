from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, Textarea, TextInput

from django_auth.models import CustomUser

from .models import Profile

User = get_user_model()


class ProfileForm(ModelForm):
    '''
    Form for practitioner profile creation during signup
    '''
    mods = forms.CharField(
        max_length=500,
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
        )
        widgets = {
            'phone':
            TextInput(
                attrs={'placeholder': "Phone number in international format"}),
            'bio':
            Textarea(attrs={'placeholder': "Tell us a little about your self"})
        }


class UserProfileForm(ModelForm):
    '''
    Form for regular users to add their location on the search page.
    '''
    class Meta:
        model = Profile
        fields = ['city']


class UserUpdateForm(ModelForm):
    '''
    Form for regular users to update their details in their profile.
    '''
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfileUpdateForm(ModelForm):
    '''
    Form for practitioners to update their personal details in their profile.
    '''
    class Meta:
        model = Profile
        fields = ('bio', 'phone', 'street', 'city')


class ModsUpdateForm(forms.Form):
    '''
    Form for practitioners to update the list of modalities they provide.
    '''
    mods = forms.CharField(label='Modalities', max_length=500, required=False)
