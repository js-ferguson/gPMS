from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Clinic


User = get_user_model()

class RegisterClinicForm(ModelForm):

    class Meta:
        model = Clinic
        fields = ('name', 'phone', 'description', 'street', 'city', )
