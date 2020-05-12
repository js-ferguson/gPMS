from datetime import datetime

import stripe
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from django.shortcuts import redirect, render, reverse
from geopy.geocoders import GoogleV3

from accounts.models import Profile
from clinic.forms import RegisterClinicForm
from clinic.models import Clinic
from djGoannaPMS import settings
from payments.models import Customer, Subscription
from payments.views import get_subscription

from .forms import (ModsUpdateForm, ProfileForm, ProfileUpdateForm,
                    UserProfileForm, UserUpdateForm)
from .models import Modalities

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


def is_active(request):
    status = "Not active"
    customer = Customer.objects.get(user=request.user)
    try:
        subscription = Subscription.objects.get(customer=customer)
        if subscription.active:
            status = "Active"

    except Subscription.DoesNotExist:
        status = "No subscription"

    return status


@login_required
def profile(request):
    """
    Displays the practitioners profile and allows them to
    update both personal and clinic details. It also provides
    a place for subscription management
    """

    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        raise Http404("This user does not exit")

    # Redirect regular users to user_profile
    if not user.is_practitioner:
        return redirect(reverse('user_profile'))

    mods = user.profile.mods.all()

    latlng = {
        "lat": user.clinic.lat,
        "lng": user.clinic.lng,
        "name": user.clinic.name,
        "url": "clinic/" + str(user.clinic.id),
        "clinic_id": user.clinic.id
    }

    profile_form_initial = {
        'bio': user.profile.bio,
        'phone': user.profile.phone,
        'street': user.profile.street,
        'city': user.profile.city
    }

    profile_form = ProfileUpdateForm(initial=profile_form_initial)

    user_form_initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    user_form = UserUpdateForm(initial=user_form_initial)

    clinic_form_initial = {
        'name': user.clinic.name,
        'description': user.clinic.description,
        'phone': user.clinic.phone,
        'web': user.clinic.web,
        'street': user.clinic.street,
        'city': user.clinic.city,
        'facebook': user.clinic.facebook,
        'instagram': user.clinic.instagram,
        'twitter': user.clinic.twitter,
        'linkedin': user.clinic.linkedin,
    }

    clinic_form = RegisterClinicForm(initial=clinic_form_initial)
    password_form = PasswordChangeForm(request.user)

    mod_list = []
    for mod in mods:
        mod_list.append(str(mod))
    mod_string = ', '.join(mod_list)
    mods_form_initial = {'mods': mod_string}

    mods_form = ModsUpdateForm(initial=mods_form_initial)

    def subscription_end_date():
        subscription = get_subscription(request)
        if subscription:
            try:
                stripesub = stripe.Subscription.retrieve(
                    subscription.stripe_subscription_id)
                return datetime.fromtimestamp(stripesub['current_period_end'])
            except stripesub.DoesNotExist:
                return "No Subscription"

    def allow_new_sub():
        '''
        Test if todays date has exceded the users subscription end date.
        Determins whether a new subscription can be created.
        '''
        today = datetime.now()
        end_date = subscription_end_date()
        if today >= end_date:
            return True

    def is_active():
        status = "Not active"
        customer = Customer.objects.get(user=request.user)
        try:
            subscription = Subscription.objects.get(customer=customer)
            if subscription.active:
                status = "Active"
        except Subscription.DoesNotExist:
            status = "No subscription"

        return status

    return render(
        request, 'profile.html', {
            'user': user,
            'mods': mods,
            'latlng': latlng,
            'api_key': api_key,
            'profile_form': profile_form,
            'user_form': user_form,
            'clinic_form': clinic_form,
            'mods_form': mods_form,
            'password_form': password_form,
            'period_ends': subscription_end_date().strftime("%B %-d, %Y"),
            'sub_is_active': is_active(),
            'allow_new_sub': allow_new_sub(),
        })


@login_required
def update_location(request, lat, lng, clinic_id):
    '''
    Takes a latitude, longitude and clinic_id and updates the position of
    a clinics map marker
    '''
    try:
        clinic = Clinic.objects.get(pk=clinic_id)
    except Clinic.DoesNotExist:
        raise Http404("This clinic does not exist")

    clinic.lat = lat
    clinic.lng = lng
    clinic.save()
    return redirect('profile')


@login_required
def user_profile(request):
    '''
    Displays the logged in users profile and allows them to
    update their details.
    '''
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        raise Http404("This user does not exist")

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("This clinic does not exist")

    # Redirect practitioners to profile
    if user.is_practitioner:
        return redirect(reverse('profile'))

    clinics = Clinic.objects.all()

    if request.method == "POST":
        form = UserUpdateForm(request.POST)
        city_form = UserProfileForm(request.POST)
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        profile.city = request.POST['city']
        user.save()
        profile.save()

        return redirect(reverse('user_profile'))
    else:

        def list_of_clinics():
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

        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        initial_profile = {'city': user.profile.city}

        form = UserUpdateForm(initial=initial)
        city_form = UserProfileForm(initial=initial_profile)
        password_form = PasswordChangeForm(request.user)

        return render(
            request, 'user_profile.html', {
                'user': user,
                'form': form,
                'latlng': list_of_clinics,
                'api_key': api_key,
                'password_form': password_form,
                'city_form': city_form
            })


@login_required
def create_profile(request):
    """
    Provides a profile creation form for the user to add personal
    details to their profile.
    """
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        raise Http404("This User does not exit")

    try:
        profile = Profile.objects.get(user=request.user)

        if profile and is_active(request) == "No subscription":
            return redirect(reverse('payments:subscription'))
    except Profile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.save()

            mod_list = []
            mods = form.cleaned_data.get('mods')
            for word in mods.split(", "):
                word.capitalize()
                mod_list.append(word)

            def add_modalities(mods):
                # Takes a list of modalities from the user and tests each to
                # see if it already
                # exists in the modalities table. Adds the mod to the user if
                # it exists, creates
                # a new mod and adds it to the user if it doesn't
                for mod in mods:
                    if Modalities.objects.filter(name=str(mod)).exists():
                        e = Modalities.objects.get(name=mod)
                        user.profile.mods.add(e)
                    else:
                        user.profile.mods.create(name=str(mod))

            add_modalities(mod_list)

            if user.is_practitioner:
                messages.success(request, f'Now set up your subscription')
                return redirect(reverse('payments:subscription'))

            messages.success(request, f'Thank you for updating your details')
            user.complete_signup = True
            user.save()
            return redirect(reverse('profile'))

    else:
        form = ProfileForm(None)
    return render(request, 'create_profile.html', {'form': form})


@login_required
def update_user(request, user_id):
    '''
    Provides a route to post updated user details and
    saves them to the appropriate model
    '''
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile = Profile.objects.get(user=user_id)
        profile.bio = request.POST['bio']
        profile.phone = request.POST['phone']
        profile.street = request.POST['street']
        profile.city = request.POST['city']
        profile.save()
        return redirect('profile')


@login_required
def update_city(request, user_id):
    '''
    Provides a route for a regular user to add a city to their profile
    to provide a default list of clinics on the search page
    '''
    profile = Profile.objects.get(user=user_id)
    profile.city = request.POST['city']
    profile.save()
    return redirect('search')


@login_required
def update_mods(request, user_id):
    '''
    Provides a route to post an updated list of modalities from the
    practitioners profile.
    '''
    user = User.objects.get(pk=user_id)
    mod_list = []
    mod_string = request.POST['mods']

    for word in mod_string.split(", "):
        word.capitalize()
        mod_list.append(word)

    def save_modalities(mods):
        # if the count of mod in mods does not equal count of user.profile.mods
        # create a list of mods to remove
        db_mods = list(user.profile.mods.all())
        list_of_db_mods = []

        def diff(db_mods, altered_mods):
            # return a list of mods that exist in the database that don't
            # exist in the request.POST
            return (list(set(db_mods) - set(altered_mods)))

        for mod in db_mods:
            list_of_db_mods.append(str(mod))

        removed_mods = diff(list_of_db_mods, mod_list)

        if removed_mods:
            for mod in removed_mods:
                m = Modalities.objects.get(name=mod)
                user.profile.mods.remove(m)

        for mod in mods:
            if Modalities.objects.filter(name=str(mod)).exists():
                e = Modalities.objects.get(name=mod)
                user.profile.mods.add(e)
            else:
                user.profile.mods.create(name=str(mod))

    save_modalities(mod_list)

    return redirect('profile')


@login_required
def update_clinic(request, user_id):
    '''
    Provides a route to post updated clinic details
    from the practitioners profile. A change in the clinics address
    results in the new address being geotagged.
    '''
    locator = GoogleV3(api_key=api_key)

    try:
        clinic = Clinic.objects.get(practitioner=user_id)
    except Clinic.DoesNotExist:
        raise Http404("This clinic does not exist")

    clinic.name = request.POST['name']
    clinic.web = request.POST['web']
    clinic.phone = request.POST['phone']
    clinic.facebook = request.POST['facebook']
    clinic.instagram = request.POST['instagram']
    clinic.twitter = request.POST['twitter']
    clinic.linkedin = request.POST['linkedin']
    clinic.description = request.POST['description']
    clinic.street = request.POST['street']
    clinic.city = request.POST['city']

    address = request.POST['street'] + " " + request.POST['city']
    coords = locator.geocode(address)

    clinic.lat = coords.latitude
    clinic.lng = coords.longitude

    clinic.save()
    return redirect('profile')


@login_required
def change_password(request):
    '''
    Provides a route to update password.
    '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated')
            return redirect('profile')
        else:
            messages.error(request, 'Please corrct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return redirect(reverse('profile'))
