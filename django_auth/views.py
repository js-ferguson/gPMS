from django.shortcuts import render
from . import forms

def login(request):
    return render(request, "login.html")

def register(request):
    form = forms.SignUpForm
    return render(request, "register.html", {"form": form})

