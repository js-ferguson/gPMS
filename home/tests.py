from django.test import TestCase
from .forms import SignUpForm

class MyTests(TestCase):
    def test_forms(self):
        form_data = {'something': 'something'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
