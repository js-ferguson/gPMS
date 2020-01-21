from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterClinicForm
from geopy.geocoders import Nominatim
from djGoannaPMS import settings
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
            address = form.cleaned_data.get("street") + " " + form.cleaned_data.get("city")
            coords = locator.geocode(address)
            print(f'Latitude = {coords.latitude}, Longitude = {coords.longitude}')

            model.lat = coords.latitude
            model.lng = coords.longitude
            model.save() 

            messages.success(request, f'Thank you for registering your clinic with us!')
            return redirect(reverse('profile'))

    else:
        form = RegisterClinicForm()
    return render(request, 'register_clinic.html', {'form': form})


def clinic_listing(request):
    clinics = Clinic.objects.all()

    for clinic in clinics:
        print(clinic)
    return render(request, 'clinic_listing.html', {'clinics': clinics}) 
