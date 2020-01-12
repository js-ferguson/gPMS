from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
# from django.http import HttpResponse
# from django_auth.models import CustomUser
from django.contrib.auth import get_user_model
from home.forms import SignUpForm

User = get_user_model()


# from accounts.models import Clinic


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"Ya'll have a new account to use!")
            # return redirect('index')
            return HttpResponseRedirect('/index/')
    else:
        form = SignUpForm()
    return render(request, "index.html", {"form": form})
