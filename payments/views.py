import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone

from .forms import MakePaymentForm
#from .forms import MakePaymentForm, OrderForm
from .models import Customer, Plans, Products, Subscription

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET
api_key = settings.GOOGLE_MAPS_API_KEY


def get_customer(request):
    customer = Customer.objects.filter(user=request.user)
    if customer.exists():
        return customer.first()
    return None


def get_subscription(request):
    subscription = Subscription.objects.filter(customer=get_customer(request))
    if subscription.exists():
        subscription = subscription.first()
        return subscription
    return None


def get_plan(request):
    plan_type = request.session['selected_plan_type']
    selected_plan = Plans.objects.filter(plan_type=plan_type)
    if selected_plan.exists():
        return selected_plan.first()
    return None


@login_required
def subscription(request):
    user = User.objects.get(email=request.user.email)
    plans = Plans.objects.all()
    if request.method == "POST":
        token = request.POST['stripeToken']
        request.session['selected_plan_type'] = request.POST['sublist']
        print(user.customer.sub.stripe_plan_id)
        print(request.POST)
        customer = get_customer(request)
        selected_plan = get_plan(request)

        stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
        stripe_customer.source = token
        stripe_customer.save()

        subscription = stripe.Subscription.create(
            customer=customer, items=[{
                "plan": selected_plan.stripe_plan_id
            }])

        ## Update customer with the selected subscription
        customer.sub = selected_plan
        customer.save()

        sub, created = Subscription.objects.get_or_create(customer=customer)
        sub.stripe_subscription_id = subscription.id
        sub.active = True
        sub.save()

        amount = 1000
        if request.POST.get('sublist') == 'yearly':
            amount = 10000
        print(amount)

        print(request.POST['sublist'])

        intent = stripe.PaymentIntent.create(amount=amount,
                                             currency='sek',
                                             payment_method_types=['card'],
                                             setup_future_usage='off_session',
                                             customer=user.customer)

        request.session['payment_intent_id'] = intent.id
        print(intent)
        stripe.PaymentIntent.confirm(intent.id, payment_method="pm_card_visa")
        if request.POST['stripeToken']:
            messages.success(
                request,
                "Thank you for subscribing to gCMS. You can now register your clinic"
            )
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
