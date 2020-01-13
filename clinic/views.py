from django.shortcuts import render
from .models import Clinic


def listing(request):
    clinic = Clinic.objects.all()
    return render(request, 'profile.html', {'user': user})
