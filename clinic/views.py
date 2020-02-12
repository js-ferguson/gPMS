from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
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
    profile = Profile.objects.all()
    search_vector = SearchVector('practitioner__first_name', 'description',
                                 'street', 'city')
    qs = Clinic.objects.annotate(search=search_vector).filter(
        search='tuina').values()
    # print(qs)
    if not qs:

        ## get a list of mods belonging to each practitioner
        #and return each practioner_id that contains that mod
        # then get all clinics belonging to those practitoners
        count = profile.count()
        p_prac = []  # list of practitioners matching the search
        for id in range(count):  # for each profile_id in range
            prac = Profile.objects.filter(
                mods=id)  # find the profile with the id
            r_list = []
            for i in prac:
                r_list.append({
                    'pk': i.id,
                    'mods': []
                })  # append pk:profile_id and list of dicts with mods
                for mod in i.mods.all().values("name"):  #  for each mod
                    r_list[0]['mods'].append(
                        mod)  # append name: mod to r_list mods:[]
                print(r_list[0]['mods'])
                for k in r_list[0]['mods']:
                    if 'Tuina' in k.values():
                        prac_id = r_list[0]['pk']
                        p_prac.append(Profile.objects.filter(pk=prac_id))
        print(p_prac)

        #    if 'Massage' in k.values():
        #        prac_id = r_list[0]['pk']
        #       print(prac_id)
        #       p_prac = Profile.objects.filter(pk=prac_id)
        #       print(p_prac)
        # print(r_list)

    #mods = Modalities.objects.filter(profile__clinics__in=qs[0]['id'])
    #print(mods)

    #def search(request):
    #    clinics = Clinic.objects.all()
    #    search_vector = SearchVector('practitioner__first_name', 'description',
    #                                 'street', 'city')
    #    results = Clinic.objects.annotate(search=search_vector).filter(
    #        search='Göteborg').values_list('name',
    #                                       'street',
    #                                       'city',
    #                                       'lat',
    #                                       'lng',
    #                                       'pk',
    #                                       flat=False)

    #    # Modalities.objects.filter(profile__clinics__in=results)
    #
    #    def list_of_results(results):
    #        print(results)
    #        key_list = ['name', 'street', 'city', 'lat', 'lng', 'clinic_id']
    #        r_list = []
    #        object = []
    #        for p in results:
    #            r_list.append([p[0], p[1], p[2], p[3], p[4], p[5]])
    #        # print(r_list)
    #        for array in r_list:
    #            object.append(dict(zip(key_list, array)))
    #        print(object)
    #        id_list = []

    #        def get_id():
    #            for clinic in object:
    #                id = clinic['clinic_id']
    #                id_list.append(id)
    #            mods = Modalities.objects.filter(profile__clinics__in=id_list)
    #            return mods
    #
    #        print(get_id)
    #        return object
    #
    #    search_result = list_of_results(results)

    return render(
        request,
        'clinic_listing.html',
        {
            'api_key': api_key,
            #            'latlng': search_result,
            #            'clinic': clinics,
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
