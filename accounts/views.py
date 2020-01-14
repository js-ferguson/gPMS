from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ProfileForm

User = get_user_model()


def profile(request):
    user = User.objects.get(email=request.user.email)
    mods = user.profile.mods
    print(user.is_practitioner)

    mod_list = []
    for word in mods.split():
        mod_list.append(word)
    print(mod_list)

    return render(request, 'profile.html', {'user': user, 'mods': mod_list})


def create_profile(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.save()
            if user.is_practitioner:
                messages.success(request, f'Now register your clinic')            
                return redirect(reverse('register_clinic'))
            
            messages.success(request, f'Thank you for updating your details')
            return redirect(reverse('profile'))

    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})
