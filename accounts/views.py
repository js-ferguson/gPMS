from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from accounts.models import Profile
from clinic.forms import RegisterClinicForm
from clinic.models import Clinic
from djGoannaPMS import settings

from .forms import ProfileForm, ProfileUpdateForm, UserUpdateForm
from .models import Modalities

User = get_user_model()


def profile(request):
    """
    Displays the users profile
    """
    user = User.objects.get(email=request.user.email)
    print(user.clinic.id)
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

    # matches = [val for val in user.profile.mods.all()]
    for mod in mods:
        print(mod.name)

    api_key = settings.GOOGLE_MAPS_API_KEY
    return render(
        request, 'profile.html', {
            'user': user,
            'mods': mods,
            'latlng': latlng,
            'api_key': api_key,
            'profile_form': profile_form,
            'user_form': user_form,
            'clinic_form': clinic_form,
        })


def update_location(request, lat, lng, clinic_id):
    print(lat, lng, clinic_id)
    clinic = Clinic.objects.get(pk=clinic_id)
    print(clinic.lat)
    clinic.lat = lat
    clinic.lng = lng
    clinic.save()
    return redirect('profile')


@login_required
def user_profile(request):
    user = User.objects.get(email=request.user.email)
    form = UserUpdateForm(request.POST)

    return render(request, 'user_profile.html', {
        'user': user,
        'form': form,
    })


def create_profile(request):
    """
    Provides a profile creation form for the user to add personal i
    details to their profile.
    """
    user = User.objects.get(email=request.user.email)
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
                messages.success(request, f'Now register your clinic')
                return redirect(reverse('register_clinic'))

            messages.success(request, f'Thank you for updating your details')
            return redirect(reverse('profile'))

    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})


def update_user(request, user_id):
    user = User.objects.get(pk=user_id)

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('profile')


def update_profile(request, user_id):
    profile = Profile.objects.get(user=user_id)
    print(request.POST)

    profile.bio = request.POST['bio']
    profile.phone = request.POST['phone']
    profile.street = request.POST['street']
    profile.city = request.POST['city']
    profile.save()
    return redirect('profile')


def update_clinic(request, user_id):
    clinic = Clinic.objects.get(practitioner=user_id)

    clinic.name = request.POST['name']
    clinic.web = request.POST['name']
    clinic.phone = request.POST['phone']
    clinic.description = request.POST['description']
    clinic.street = request.POST['street']
    clinic.city = request.POST['city']
    clinic.save()
    return redirect('profile')
