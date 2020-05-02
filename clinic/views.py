from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, reverse
from geopy.geocoders import GoogleV3

from accounts.forms import UserProfileForm
from accounts.models import Profile
from djGoannaPMS import settings

from .forms import RegisterClinicForm, ReviewForm
from .models import Clinic, Reviews

User = get_user_model()
api_key = settings.GOOGLE_MAPS_API_KEY


@login_required
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


def search(request):

    # else:  # user = User.objects.get(user=request.user)
    #     messages.warning(
    #         request,
    #         "Please consider signing up... It's free and you can leave comments!"
    #     )
    search_result = []
    result = []
    is_search = False

    def search(search_term):
        search_vector = SearchVector('name', 'practitioner__first_name',
                                     'description', 'street', 'city')
        qs = Clinic.objects.annotate(search=search_vector).filter(
            search=search_term).values()
        # if qs:
        for i in qs:
            search_result.append(
                Clinic.objects.get(
                    practitioner=i['practitioner_id']).get_clinic_details())
            # else:
        mods_vector = SearchVector('mods__name')

        mqs = Profile.objects.annotate(search=mods_vector).filter(
            search=search_term).values()
        if mqs:
            for i in mqs:
                result.append(i)

    def find_clinics(result):
        r_array = []
        for i in result:
            r_array.append(
                Clinic.objects.get(
                    practitioner=i['user_id']).get_clinic_details())
        return (r_array)

    def colate_results(search_result, find_clinics_result):
        seen_names = set()
        search_results = []
        for obj in search_result:
            if obj['name'] not in seen_names:
                search_results.append(obj)
                seen_names.add(obj['name'])

        for obj in find_clinics_result:
            if obj['name'] not in seen_names:
                search_results.append(obj)
                seen_names.add(obj['name'])
        return search_results

    def get_coords(search_result):
        coords = []
        for i in search_result:
            coords.append({
                "lat": i['lat'],
                "lng": i['lng'],
                "url": f"clinic/{i['id']}"
            })
        return coords

    if request.method == 'POST':
        is_search = True
        search_term = request.POST['search_term']
        search(search_term)

        return render(
            request, 'clinic_listing.html', {
                'api_key':
                api_key,
                'is_search':
                is_search,
                'result':
                colate_results(search_result, find_clinics(result)),
                'latlng':
                get_coords(colate_results(search_result,
                                          find_clinics(result))),
            })
    else:
        if request.user.is_authenticated:
            print("Authenticated")
            user = User.objects.get(email=request.user.email)

            # if user is authenticated but not finished registration:
            if not user.completed_signup:
                try:
                    user.profile.city
                except Profile.DoesNotExist:
                    return redirect(reverse('create_profile'))
                # and not user.profile.city:
                # return redirect(reverse('create_profile'))

            # if user has no profile:
            # redirect to create_profile
            # else if user has no sub:
            # redirect to sub
            # else if user has no clinic
            # redirect to create_clinic

        else:
            print("Not authenticated")
        search(user.profile.city)
        form = UserProfileForm()
    return render(
        request, 'clinic_listing.html', {
            'api_key':
            api_key,
            'user':
            user,
            'form':
            form,
            'is_search':
            is_search,
            'result':
            colate_results(search_result, find_clinics(result)),
            'latlng':
            get_coords(colate_results(search_result, find_clinics(result)))
        })


@login_required
def clinic_profile(request, clinic_id):

    clinic = Clinic.objects.filter(pk=clinic_id)

    if clinic.count() == 0:
        messages.warning(
            request,
            "The clinic you are looking for does not exist",
        )
        return redirect('index')

    form = ReviewForm()
    clinic_reviews = Reviews.objects.filter(clinic=clinic_id)

    # Test if clinic_id in session['initial'] matches the current clinic_id
    # if not, remove 'initial' from request.session
    if 'initial' in request.session:
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


@login_required
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


@login_required
def edit_review(request, review_id):
    try:
        review = Reviews.objects.get(pk=review_id)
    except Reviews.DoesNotExist:
        raise Http404("This review does not exist")

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


@login_required
def delete_review(request, review_id):
    try:
        review = Reviews.objects.get(pk=review_id)
    except Reviews.DoesNotExist:
        raise Http404("This review does not exist")

    clinic_id = review.clinic.id
    if review.author == request.user:
        review.delete()
    return redirect('clinic_profile', clinic_id=clinic_id)
