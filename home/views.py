from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render, reverse

from accounts.forms import ProfileForm, UserProfileForm
from accounts.models import Profile
from clinic.models import Clinic
from home.forms import SignUpForm
from payments.models import Customer, Subscription

User = get_user_model()

api_key = settings.GOOGLE_MAPS_API_KEY
clinics = Clinic.objects.all()


def list_of_clinics():
    '''
    Return a dict containing clinic details.
    '''
    c_list = []
    for clinic in clinics:
        if clinic.lat:
            c_list.append({
                'lat': clinic.lat,
                'lng': clinic.lng,
                'name': clinic.name,
                'url': "clinic/" + str(clinic.id)
            })
    return c_list


def index(request):
    '''
    Route for the landing/signup page.
    '''
    if not request.user.is_anonymous and request.user.is_practitioner:
        try:
            Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect(reverse('create_profile'))

        try:
            customer = Customer.objects.get(user=request.user)
            try:
                Subscription.objects.get(customer=customer)
            except Subscription.DoesNotExist:
                return redirect(reverse('payments:subscription'))
        except Customer.DoesNotExist:
            pass

        try:
            Clinic.objects.get(practitioner=request.user)
        except Clinic.DoesNotExist:
            return redirect(reverse('register_clinic'))

    if request.user.is_authenticated:
        return redirect(reverse('search'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            if user.is_practitioner:
                messages.success(
                    request,
                    f'Your account has been created. Please update your personal details'
                )

                return render(request, "create_profile.html", {
                    "form": profile_form,
                    "user": user
                })

            else:
                form = UserProfileForm()
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()

                user.complete_signup = True
                user.save()

                messages.success(
                    request,
                    f'You can now update your details or begin your search')
                return redirect(reverse("search"))

    else:
        form = SignUpForm(request.POST or None)

    return render(request, "index.html", {
        "form": form,
        "api_key": api_key,
        "c_list": list_of_clinics()
    })
