from django import forms


class NavSearchForm(forms.Form):
    query = forms.CharField(max_length=30, required=False)
