from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Modalities
from .forms import ProfileForm


User = get_user_model()


def profile(request):
    user = User.objects.get(email=request.user.email)

    mods = user.profile.mods.all()
    matches = [val for val in user.profile.mods.all()]
    print(matches)
    for mod in mods:
        print(mod.name)
    #mods = user.profile.mods
    #print(user.is_practitioner)

    #mod_list = []
    #for word in mods.split():
    #    mod_list.append(word)
    #print(mod_list)

    return render(request, 'profile.html', {'user': user, 'mods': mods}) 


def create_profile(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            profile.save()

            mod_list = []
            mods = form.cleaned_data.get('mods')
            for word in mods.split(", "):
                mod_list.append(word)
                print("This is the list of mods: " + str(mod_list))

            # def save_mods(mods):
            #     for mod in mods:
            #         m = Modalities(name=mod)
            #         m.save()
            #         user.profile.mods.add(m)
            # save_mods(mod_list)
            
            def add_modalities(mods):
                for mod in mods:
                    if Modalities.objects.filter(name=str(mod)).exists():
                        #user.profile.mods.add(mod)
                        e = Modalities.objects.get(name=mod)
                        print(e)
                        user.profile.mods.add(e)
                    else:
                        print("creating that shit anyway")
                        user.profile.mods.create(name=str(mod))
            add_modalities(mod_list)

            if user.is_practitioner:
                messages.success(request, f'Now register your clinic')
                return redirect(reverse('register_clinic'))

            messages.success(request, f'Thank you for updating your details')
            return redirect(reverse('profile'))

    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})
