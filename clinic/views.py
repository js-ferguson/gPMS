from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import GoogleV3

from accounts.models import Modalities, Profile
from djGoannaPMS import settings

from .forms import RegisterClinicForm, ReviewForm
from .models import Clinic, Reviews

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


def register_clinic(request):
    form = RegisterClinicForm(request.POST)
    locator = GoogleV3(api_key=api_key)
    if request.method == 'POST':
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.practitioner = request.user
            clinic.save()

            model = get_object_or_404(Clinic, practitioner=request.user)
            address = form.cleaned_data.get(
                "street") + " " + form.cleaned_data.get("city")
            coords = locator.geocode(address)

            model.lat = coords.latitude
            model.lng = coords.longitude
            model.save()

            user = User.objects.get(email=request.user.email)
            user.complete_signup = True
            user.save()

            messages.success(
                request, f'Thank you for registering your clinic with us!')
            return redirect(reverse('profile'))

    else:
        form = RegisterClinicForm()
    return render(request, 'register_clinic.html', {'form': form})


#     clinics = Clinic.objects.all()

#     def list_of_coords():
#         latlng = []
#         for clinic in clinics:
#             if clinic.lat:
#                 latlng.append({
#                     'lat': clinic.lat,
#                     'lng': clinic.lng,
#                     'name': clinic.name,
#                 })
#         return latlng

#     return render(request, 'clinic_listing.html', {
#         'clinics': clinics,
#         'api_key': api_key,
#         'latlng': list_of_coords(),
#     })


def search(request):
    search_term = request.POST.get('search_term')
    search_result = []
    result = []
    search_vector = SearchVector('name', 'practitioner__first_name',
                                 'description', 'street', 'city')
    qs = Clinic.objects.annotate(search=search_vector).filter(
        search=search_term).values()
    if qs:
        for i in qs:
            search_result.append(
                Clinic.objects.get(
                    practitioner=i['practitioner_id']).get_clinic_details())
    else:
        if Modalities.objects.filter(name__iexact=search_term).exists():
            s_users = Profile.objects.filter(
                mods__name__icontains=search_term).values()
            for i in s_users:
                result.append(i)

    def find_clinics(result):
        r_array = []
        for i in result:
            r_array.append(
                Clinic.objects.get(
                    practitioner=i['user_id']).get_clinic_details())
        return (r_array)

    def colate_results(sv_result, mod_result):
        search_result = sv_result + mod_result
        return search_result

    def get_coords(search_result):
        coords = []
        for i in search_result:
            coords.append({
                "lat": i['lat'],
                "lng": i['lng'],
                "url": f"clinic/{i['id']}"
            })
        return coords

    return render(
        request, 'clinic_listing.html', {
            'api_key':
            api_key,
            'result':
            colate_results(search_result, find_clinics(result)),
            'latlng':
            get_coords(colate_results(search_result, find_clinics(result))),
        })


def clinic_profile(request, clinic_id):

    clinic = Clinic.objects.filter(pk=clinic_id)

    if clinic.count() == 0:
        raise Http404("This clinic does not exist")

    form = ReviewForm()
    clinic_reviews = Reviews.objects.filter(clinic=clinic_id)

    # Test if clinic_id in session['initial'] matches the current clinic_id
    # if not, remove 'initial' from request.session
    if 'initial' in request.session:
        print(clinic_id)
        if request.session['initial']['clinic_id'] != clinic_id:
            del request.session['initial']
    edit = False

    latlng = {
        "lat": clinic[0].lat,
        "lng": clinic[0].lng,
        "name": clinic[0].name
    }

    def get_mods():
        profile = Profile.objects.filter(user=Clinic.objects.get(
            pk=clinic_id).practitioner)
        mods = profile[0].mods.all().values('name') if profile else []

        mods = [(q['name']) for q in mods]
        return mods

    if request.user.is_active:
        if 'initial' in request.session:
            print("It's in here")
            edit = True
            form = ReviewForm(initial=request.session['initial'])

            # This will populate the review form with the review to be edited
            # on, and it populates on any page... Please set a session
            # variable with the clinic_id to be edited and check that it
            # matches the page you are on before pre-filling the form.
            # Also... delete 'initial' from session when your done.

    return render(
        request, 'clinic_profile.html', {
            'clinic': clinic,
            'mods': get_mods,
            'latlng': latlng,
            'api_key': api_key,
            'reviews': clinic_reviews,
            'form': form,
            'edit': edit,
            'user': request.user
        })


def create_review(request, clinic_id):
    form = ReviewForm(request.POST)
    if request.method == 'POST':
        if request.user.is_active:
            if form.is_valid():
                r_clinic = Clinic.objects.get(pk=clinic_id)
                title = form.cleaned_data.get("title")
                body = form.cleaned_data.get("body")
                review = Reviews(title=title,
                                 body=body,
                                 author=request.user,
                                 clinic=r_clinic)
            review.save()
            messages.success(request, f'Thank you for leaving a review!')
        else:
            messages.error(request, f'You must be logged in to post a review')
            return redirect('login')
    return redirect('clinic_profile', clinic_id=clinic_id)


def edit_review(request, review_id):
    review = Reviews.objects.get(pk=review_id)
    clinic_id = review.clinic.id
    title_data = review.title
    body_data = review.body
    print(review.author)
    if request.method == 'POST' and review.author == request.user:
        review.title = request.POST['title']
        review.body = request.POST['body']
        # review.author = request.user
        review.save()
        del request.session['initial']
        messages.success(request, f"Your review has been updated")
        return redirect('clinic_profile', clinic_id=clinic_id)

    if review.author == request.user:
        request.session['initial'] = {
            "title": title_data,
            "body": body_data,
            "clinic_id": clinic_id
        }
        return redirect('clinic_profile', clinic_id=clinic_id)
    else:
        messages.error(request, f"You don't have permission to edit that")
        if 'initial' in request.session:
            del request.session['initial']
        return redirect('clinic_profile', clinic_id=clinic_id)


def delete_review(request, review_id):
    review = Reviews.objects.get(pk=review_id)
    clinic_id = review.clinic.id
    print(review.id)
    if review.author == request.user:
        review.delete()
    return redirect('clinic_profile', clinic_id=clinic_id)
