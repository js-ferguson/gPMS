from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterClinicForm
from geopy.geocoders import Nominatim

User = get_user_model()


def register_clinic(request):
    form = RegisterClinicForm(request.POST)
    nominatim = Nominatim(user_agent="gPMS")
    if request.method == 'POST':
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.practitioner = request.user

            #clinic.save()

            coords_query = {"street": form.cleaned_data.get("street"), "city": form.cleaned_data.get("city")}

            def get_coords(query):
                coords = nominatim.geocode(query)
                return coords
            print(get_coords(coords_query))

            clinic.save()
            messages.success(request, f'Thank you for registering your clinic with us!')
            return redirect(reverse('profile'))

    else:
        form = RegisterClinicForm()
    return render(request, 'register_clinic.html', {'form': form})


#def clinic_listing(request):
    #clinics = Clinic.objects.all()
 #   return render(request, 'profile.html', {'user': user})

