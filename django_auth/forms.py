from django.forms import ModelForm
from accounts.models import Profile
#from django.contrib.auth import get_user_model

#User = get_user_model()

# Create the form class.
class SignUpForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone', 'personnummer',]

    def save(self, commit=True):
        # save the users details to the db
         
