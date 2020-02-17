from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import GoogleV3, Nominatim

from accounts.models import Modalities, Profile
from djGoannaPMS import settings

from .forms import RegisterClinicForm
from .models import Clinic

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


def register_clinic(request):
    form = RegisterClinicForm(request.POST)
    locator = GoogleV3(api_key=api_key)
    if request.method == 'POST':
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.practitioner = request.user
            clinic.save()

            model = get_object_or_404(Clinic, practitioner=request.user)
            address = form.cleaned_data.get(
                "street") + " " + form.cleaned_data.get("city")
            coords = locator.geocode(address)
            print(
                f'Latitude = {coords.latitude}, Longitude = {coords.longitude}'
            )

            model.lat = coords.latitude
            model.lng = coords.longitude
            model.save()

            messages.success(
                request, f'Thank you for registering your clinic with us!')
            return redirect(reverse('profile'))

    else:
        form = RegisterClinicForm()
    return render(request, 'register_clinic.html', {'form': form})


def clinic_listing(request):
    clinics = Clinic.objects.all()

    def list_of_coords():
        latlng = []
        for clinic in clinics:
            if clinic.lat:
                latlng.append({
                    'lat': clinic.lat,
                    'lng': clinic.lng,
                    'name': clinic.name,
                })
        return latlng

    return render(request, 'clinic_listing.html', {
        'clinics': clinics,
        'api_key': api_key,
        'latlng': list_of_coords(),
    })


def search(request):
    result = []
    search_vector = SearchVector('practitioner__first_name', 'description',
                                 'street', 'city')
    qs = Clinic.objects.annotate(search=search_vector).filter(
        search='tuina').values()
    if qs:
        for i in qs[0]:
            result.append(i)
    else:

        if Modalities.objects.filter(name="Acupuncture").exists():
            s_mod = Modalities.objects.get(name="Acupuncture")
            s_users = Profile.objects.filter(
                mods__name__contains='Acupuncture').values()
            # print(s_users)
            for i in s_users:
                result.append(i)
    print(result)

    def find_clinics(result):
        r_array = []
        # l_array = []
        for i in result:
            r_array.append(Clinic.objects.get(practitioner=i['user_id']))
            # for j in r_array[0]:
            #   l_array.append(j)

        # print(l_array)
        print(r_array)
        return (r_array)

    find_clinics(result)

    return render(
        request,
        'clinic_listing.html',
        {
            'api_key': api_key,
            #'result': find_clinics(result)
            #            'latlng': search_result,
            #'clinic': find_clinics(result),
            # 'mods': get_mods
        })


def clinic_profile(request, clinic_id):

    clinic = Clinic.objects.filter(pk=clinic_id)
    latlng = {
        "lat": clinic[0].lat,
        "lng": clinic[0].lng,
        "name": clinic[0].name
    }
    print(latlng)

    def get_mods():
        profile = Profile.objects.filter(user=Clinic.objects.get(
            pk=clinic_id).practitioner)
        mods = profile[0].mods.all().values('name') if profile else []

        mods = [(q['name']) for q in mods]
        print(mods)
        return mods

    return render(request, 'clinic_profile.html', {
        'clinic': clinic,
        'mods': get_mods,
        'latlng': latlng,
        'api_key': api_key
    })
