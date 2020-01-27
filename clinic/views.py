from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import Nominatim

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
                latlng.append({'lat': clinic.lat, 'lng': clinic.lng})
        return latlng

    print(str(list_of_coords()))

    return render(request, 'clinic_listing.html', {
        'clinics': clinics,
        'api_key': api_key,
        'latlng': list_of_coords()
    })
