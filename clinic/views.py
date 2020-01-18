from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterClinicForm

User = get_user_model()


def register_clinic(request):
    form = RegisterClinicForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.practitioner = request.user

            clinic.save()
            messages.success(request, f'Thank you for registering your clinic with us!')
            return redirect(reverse('profile'))

    else:
        form = RegisterClinicForm()
    return render(request, 'register_clinic.html', {'form': form})


#def clinic_listing(request):
    #clinics = Clinic.objects.all()
 #   return render(request, 'profile.html', {'user': user})

