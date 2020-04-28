from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, reverse

from accounts.models import Profile
from clinic.forms import RegisterClinicForm
from clinic.models import Clinic
from djGoannaPMS import settings

from .forms import (ModsUpdateForm, ProfileForm, ProfileUpdateForm,
                    SubUpdateForm, UserUpdateForm)
from .models import Modalities

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


@login_required
def profile(request):
    """
    Displays the practitioners profile and allows them to
    update their details as well as their clinics details.
    """

    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        raise Http404("This user does not exit")

        print("clinic id: " + str(user.clinic.id))
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
        'city': user.clinic.city
    }

    clinic_form = RegisterClinicForm(initial=clinic_form_initial)
    mod_list = []
    for mod in mods:
        mod_list.append(str(mod))
    mod_string = ', '.join(mod_list)
    mods_form_initial = {'mods': mod_string}

    mods_form = ModsUpdateForm(initial=mods_form_initial)

    sub_form = SubUpdateForm()

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
            'sub_form': sub_form,
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

    form = UserUpdateForm()
    clinics = Clinic.objects.all()

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
        print(c_list)
        return c_list

    return render(request, 'user_profile.html', {
        'user': user,
        'form': form,
        'latlng': list_of_clinics,
        'api_key': api_key
    })


@login_required
def create_profile(request):
    """
    Provides a profile creation form for the user to add personal i
    details to their profile.
    """
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        raise Http404("This User does not exit")

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

            #if user.is_practitioner:
            #    messages.success(request, f'Now register your clinic')
            #    return redirect(reverse('register_clinic'))

            if user.is_practitioner:
                messages.success(request, f'Now set up your subscription')
                return redirect(reverse('subscription'))

            messages.success(request, f'Thank you for updating your details')
            user.complete_signup = True
            user.save()
            return redirect(reverse('profile'))

    else:
        form = ProfileForm(None)
    return render(request, 'create_profile.html', {'form': form})


@login_required
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('profile')


@login_required
def update_profile(request, user_id):
    profile = Profile.objects.get(user=user_id)
    profile.bio = request.POST['bio']
    profile.phone = request.POST['phone']
    profile.street = request.POST['street']
    profile.city = request.POST['city']
    profile.save()
    return redirect('profile')


@login_required
def update_mods(request, user_id):
    user = User.objects.get(pk=user_id)
    mod_list = []
    mod_string = request.POST['mods']
    for word in mod_string.split(", "):
        word.capitalize()
        mod_list.append(word)

    def save_modalities(mods):
        # if the count of mod in mods does not equal count of count of user.profile.mods
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
    try:
        clinic = Clinic.objects.get(practitioner=user_id)
    except Clinic.DoesNotExist:
        raise Http404("This clinic does not exist")

    clinic.name = request.POST['name']
    clinic.web = request.POST['web']
    clinic.phone = request.POST['phone']
    clinic.description = request.POST['description']
    clinic.street = request.POST['street']
    clinic.city = request.POST['city']
    clinic.save()
    return redirect('profile')
