from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import Nominatim

#from accounts.models import Profile
from djGoannaPMS import settings

from .forms import RegisterClinicForm
from .models import Clinic

User = get_user_model()


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
    api_key = settings.GOOGLE_MAPS_API_KEY

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
    api_key = settings.GOOGLE_MAPS_API_KEY

    search_vector = SearchVector('practitioner__first_name', 'name',
                                 'description', 'street', 'city')
    results = Clinic.objects.annotate(search=search_vector).filter(
        search='Göteborg').values_list('name',
                                       'street',
                                       'city',
                                       'lat',
                                       'lng',
                                       flat=False)

    print("These are the raw results: " + str(results))

    def list_of_results(results):
        key_list = ['name', 'street', 'city', 'lat', 'lng']
        r_list = []
        for p in results:
            r_list.append([p[0], p[1], p[2], p[3], p[4]])
            print(r_list)

        # what data structure to I want before I run zip?
        # r_list = [[gun, gunsStreet, gunsCity, gunsLat, gunsLng],
        #           [jimi, jimiStreet, jimiCity, jimiLat, Jimilng ]]

        #target_dict = defaultdict(list)
        #for i, key in enumerate(results):
        #    target_dict[k].append(values[i])

        #r_list = []
        #for r in results:
        #    for i in r:
        #        r_list.append(i)
        #print("this is r_list: " + str(r_list))
        #key_list = ['name', 'street', 'city', 'lat', 'lng']
        # r_list = [results[0], results[1], results[2], results[3], results[4]]
        #zipped = zip(key_list, r_list)
        #for r in results:
        #    print(r[3])
        #print(str(zipped))
        #return r[0]

    search_result = list_of_results(results)
    return render(request, 'clinic_listing.html', {
        'api_key': api_key,
        'result': search_result
    })


# search('Göteborg')
