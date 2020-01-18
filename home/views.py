from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from home.forms import SignUpForm
from accounts.forms import ProfileForm
from django.conf import settings

User = get_user_model()


# from accounts.models import Clinic


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, f'Your account has been created. Please update your details')
            # return redirect('index')
            return render(request, "create_profile.html",
                          {"form": profile_form, "user": user})
    else:
        form = SignUpForm()
        api_key = settings.GOOGLE_MAPS_API_KEY
    return render(request, "index.html", {"form": form, "api_key": api_key})
