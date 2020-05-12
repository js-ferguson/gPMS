from django import forms


class MakePaymentForm(forms.Form):
    '''
    Form to take payment for service subscription. 
    '''
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2017, 2036)]

    SUB_LEVELS = [
        ('montly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('three years', 'Three years'),
    ]

    full_name = forms.CharField(max_length=100)

    sub_type = forms.ChoiceField(choices=SUB_LEVELS)

    credit_card_number = forms.CharField(label='Credit Card Number',
                                         required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month',
                                     choices=MONTH_CHOICES,
                                     required=False)
    expiry_year = forms.ChoiceField(label='Year',
                                    choices=YEAR_CHOICES,
                                    required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
