from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model
#from django_auth.forms import 

User = get_user_model()


#class SignUpForm(ModelForm):

#    password2 = forms.CharField(label='Confirm password', max_length=128,
#                                widget=forms.PasswordInput())

#    class Meta:
#        model = User
#        fields = ['first_name', 'last_name', 'email', 'password', 'password2',
#                  'practitioner', ]

class SignUpForm(forms.ModelForm):
    """
    Form to allow creating new users
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

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
