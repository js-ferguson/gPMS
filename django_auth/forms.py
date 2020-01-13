from django import forms


class UserLoginForm(forms.Form):
    """Form to log users in"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
