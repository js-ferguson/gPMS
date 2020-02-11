from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import Nominatim

from accounts.models import Modalities, Profile
from djGoannaPMS import settings

from .forms import RegisterClinicForm
from .models import Clinic

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


def register_clinic(request):
    form = RegisterClinicForm(request.POST)
    locator = Nominatim(user_agent="gPMS")
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
    clinics = Clinic.objects.all()
    search_vector = SearchVector('practitioner__first_name', 'description',
                                 'street', 'city')
    results = Clinic.objects.annotate(search=search_vector).filter(
        search='Göteborg').values_list('name',
                                       'street',
                                       'city',
                                       'lat',
                                       'lng',
                                       'pk',
                                       flat=False)

    # Modalities.objects.filter(profile__clinics__in=results)

    def list_of_results(results):
        print(results)
        key_list = ['name', 'street', 'city', 'lat', 'lng', 'clinic_id']
        r_list = []
        object = []
        for p in results:
            r_list.append([p[0], p[1], p[2], p[3], p[4], p[5]])
        # print(r_list)
        for array in r_list:
            object.append(dict(zip(key_list, array)))
        print(object)
        id_list = []

        def get_id():
            for clinic in object:
                id = clinic['clinic_id']
                id_list.append(id)
            mods = Modalities.objects.filter(profile__clinics__in=id_list)
            return mods

        print(get_id)
        return object

    search_result = list_of_results(results)

    return render(
        request,
        'clinic_listing.html',
        {
            'api_key': api_key,
            'latlng': search_result,
            'clinic': clinics,
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
