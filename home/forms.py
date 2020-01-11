from django import forms
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(AuthenticationForm):

    password2 = forms.CharField(label='Confirm password', max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'practitioner']

