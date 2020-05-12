from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class SignUpForm(ModelForm):
    '''
    Form to allow creating new users
    '''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    practitioner = forms.BooleanField(
        label='Are you signing up as a practitioner?', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'practitioner')

    def clean_password2(self):
        # Test that passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Hash the password and save it
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
