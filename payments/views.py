from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone

import stripe

from .forms import MakePaymentForm
#from .forms import MakePaymentForm, OrderForm
from .models import Customer, Plans, Products, Subscription

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET
api_key = settings.GOOGLE_MAPS_API_KEY


@login_required
def subscription(request):
    user = User.objects.get(email=request.user.email)

    if request.method == "POST":
        form = MakePaymentForm()

        # yearly = Plans(nickname="yearly", stripe_id="plan_H2cPoMv9Kx449p")
        # monthly = Plans(nickname="monthly", stripe_id="plan_H2cOfdfjGlirRx")
        cust = Customer.objects.all()
        plans = Plans.objects.all()

        for plan in plans:
            print(plan.stripe_id)
        prods = Products.objects.all()

        for prod in prods:
            print(prod.stripe_id)

        # get card info and pass to backend
        # then create a customer

        def create_customer():
            #this needs to add a customer to the db one-to-one with a profile
            # using both profile model sending both profile info to stripe and adding stipe info to db

            customer = stripe.Customer.create(
                name=user.request.POST['name'],
                email=user.email,
            )

            db_cust = Customer(stripe_customer_id=customer.id, user_id=user.id)
            if Customer.objects.filter(stripe_customer_id=customer.id):
                messages(request, "customer exists")
            else:
                db_cust.save()

            return customer

        for c in cust:
            print(f'{c.user.profile.bio} {c.user_id}')
        print(request.POST)
        # print(create_customer())
        if request.POST['sublist'] == 'monthly':
            amount = 1000
        else:
            amount = 10000

        intent = stripe.PaymentIntent.create(
            amount=0,
            currency='sek',
            payment_method_types=['card'],
            setup_future_usage='off_session',
        )  #save intent_id to session
        print(intent)

        stripe.PaymentIntent.confirm(intent.id, payment_method="pm_card_visa")
        #pay_method = stripe.PaymentMethod.create(
        #    type="card",
        #    card={
        #        "number": form.cleaned_data.credit_card_number,
        #        "exp_month": form.cleaned_data.expiry_month,
        #        "exp_year": form.cleaned_data.expity_year,
        #        "cvc": form.cleaned_data.cvv,
        #    },
        #)

        #def payment():
        #    pay = stripe.PaymentIntent.create(customer=customer['id'],
        #                                      amount=1000,
        #                                      currency='sek',
        #                                      receipt_email=customer['email'])
        #    print(pay)
        #    return pay

        # payment()

        return render(
            request,
            "sub.html",
            {
                'form': form,
                'api-key': api_key,
                'key': settings.STRIPE_SECRET,
                'user': user,
                #'payment_form': payment_form,
                #'publishable': settings.STRIPE_PUBLISHABLE
            })
    else:
        form = MakePaymentForm(initial={'full_name': user.get_full_name()})
    return render(
        request, "sub.html", {
            'form': form,
            'api_key': api_key,
            'user': user,
            'client_secret': intent.client_secret,
        })
