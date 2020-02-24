from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from djGoannaPMS import settings

from .forms import ProfileForm, UserUpdateForm
from .models import Modalities

User = get_user_model()


def profile(request):
    """
    Displays the users profile
    """
    user = User.objects.get(email=request.user.email)
    mods = user.profile.mods.all()
    latlng = [user.clinic.lat, user.clinic.lng]
    # matches = [val for val in user.profile.mods.all()]
    for mod in mods:
        print(mod.name)

    api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, 'profile.html', {
        'user': user,
        'mods': mods,
        'latlng': latlng,
        'api_key': api_key
    })


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
