from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ProfileForm

User = get_user_model()


def profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {'user': user})


def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.save()
            messages.success(request, f'Thank you for updating your details')
            return redirect(reverse('profile'))

    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})
