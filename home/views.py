from django.shortcuts import render
from django.http import HttpResponse
#from accounts.models import Clinic

def index(request):
    return render(request, "index.html")



