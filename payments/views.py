from datetime import datetime

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, reverse

# from accounts.views import is_active
from clinic.models import Clinic

from .forms import MakePaymentForm
from .models import Customer, Plans, Subscription

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET
api_key = settings.GOOGLE_MAPS_API_KEY


def get_customer(request):
    try:
        customer = Customer.objects.filter(user=request.user)
    except Customer.DoesNotExist:
        raise Http404("This customer does not exist")

    if customer.exists():
        return customer.first()
    return None


def get_subscription(request):
    try:
        subscription = Subscription.objects.filter(
            customer=get_customer(request))
    except Subscription.DoesNotExist:
        raise Http404("Subscription does not exist")

    if subscription.exists():
        subscription = subscription.first()
        return subscription
    return None


def get_plan(request):
    plan_type = request.session['selected_plan_type']

    try:
        selected_plan = Plans.objects.filter(plan_type=plan_type)
    except Plans.DoesNotExist:
        raise Http404("This plan does not exit")

    if selected_plan.exists():
        return selected_plan.first()
    return None


def create_sub(request, *args):
    token = args[0]
    customer = get_customer(request)
    selected_plan = get_plan(request)

    stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
    stripe_customer.source = token
    stripe_customer.save()

    subscription = stripe.Subscription.create(customer=customer,
                                              items=[{
                                                  "plan":
                                                  selected_plan.stripe_plan_id
                                              }])

    def subscription_end_date():
        subscription = get_subscription(request)
        if subscription:
            stripesub = stripe.Subscription.retrieve(
                subscription.stripe_subscription_id)
            return datetime.fromtimestamp(stripesub['current_period_end'])

    # Update customer with the selected subscription
    customer.sub = selected_plan
    customer.save()

    sub, created = Subscription.objects.get_or_create(customer=customer)
    sub.stripe_subscription_id = subscription.id
    sub.end_billing_period = subscription_end_date()
    sub.active = True
    sub.save()


@login_required
def subscription(request):
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        messages.warning(request,
                         "Create an account before you try to subscribe.")
        return redirect(reverse('index'))

    if get_subscription(request):
        try:
            clinic = Clinic.objects.get(practitioner=request.user)
            print(clinic)
        except Clinic.DoesNotExist:
            return redirect(reverse('register_clinic'))

    # if is_active(request) == "Active" and not clinic:

    plans = Plans.objects.all()

    if request.method == "POST":
        token = request.POST['stripeToken']
        request.session['selected_plan_type'] = request.POST['sublist']
        create_sub(request, token)

        amount = 1000
        if request.POST.get('sublist') == 'yearly':
            amount = 10000

        intent = stripe.PaymentIntent.create(amount=amount,
                                             currency='sek',
                                             payment_method_types=['card'],
                                             setup_future_usage='off_session',
                                             customer=user.customer)

        request.session['payment_intent_id'] = intent.id
        stripe.PaymentIntent.confirm(intent.id, payment_method="pm_card_visa")
        if request.POST['stripeToken']:
            messages.success(
                request,
                "Thank you for subscribing to gCMS. You can now register your clinic"
            )
            if user.complete_signup:
                return redirect(reverse('profile'))
            else:
                return redirect(reverse('register_clinic'))

        return render(
            request, "subscription.html", {
                'api-key': api_key,
                'key': settings.STRIPE_SECRET,
                'user': user,
                'plans': plans,
                'publishable': settings.STRIPE_PUBLISHABLE,
                'client_secret': intent.client_secret
            })
    else:
        form = MakePaymentForm(initial={'full_name': user.get_full_name()})
    return render(
        request, "subscription.html", {
            'form': form,
            'api-key': api_key,
            'user': user,
            'plans': plans,
            'publishable': settings.STRIPE_PUBLISHABLE,
        })


@login_required
def cancel_sub(request, user_id):
    subscription = get_subscription(request)
    subscription.active = False
    subscription.terminated_on = datetime.today()
    # print(datetime.date())
    subscription.save()

    # cancel sub with stripe
    stripe.Subscription.delete(subscription.stripe_subscription_id)
    messages.success(request, "Your subscription has been cancelled")
    return redirect('profile')
