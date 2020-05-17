import json
from types import MethodType

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse
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
    '''
    Route to save clinic details and geocode the clinics address.
    '''
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
    '''
    Route for searching clinics
    '''
    is_search = False
    page_info = None

    def search(search_term):
        # Takes a search term and uses PostgreSQL full-text search
        # to return a list of dicts containing clinic details.
        search_result = []
        search_models = []  # A list of values in dicts, each
        # representing a clinic
        search_vector = SearchVector('name', 'practitioner__first_name',
                                     'description', 'street', 'city')
        mods_vector = SearchVector('mods__name')

        qs = Clinic.objects.annotate(search=search_vector).filter(
            search=search_term).values()
        mqs = Profile.objects.annotate(search=mods_vector).filter(
            search=search_term).values()

        models = Clinic.objects.annotate(search=search_vector).filter(
            search=search_term).order_by('name')

        # print(models)

        for i in qs:
            try:
                search_result.append(
                    Clinic.objects.get(practitioner=i['practitioner_id']).
                    get_clinic_details())
            except Clinic.DoesNotExist:
                return

        for i in mqs:
            try:
                search_result.append(
                    Clinic.objects.get(
                        practitioner=i['user_id']).get_clinic_details())
            except Clinic.DoesNotExist:
                return

        for i in models:
            search_models.append(i)

        seen_names = set()
        set_results = []
        for obj in search_result:
            if obj['is_searchable']:
                if obj['name'] not in seen_names:
                    set_results.append(obj)
                    seen_names.add(obj['name'])
        print(set_results)
        return [set_results, models, search_models]

    # Try returning the search results without values to the paginator
    # anything else needed, like coords can be extracted some other way
    # perhaps in a function that specifically returns the values()

    # Also... take the search funciton out of the route function.

    coords = []

    def paginate(search_term):
        # paginate the results of the search
        search_result_list = search(search_term)[0]

        #for i in search_result_list:
        #    coords.append({
        #        "lat": i['lat'],
        #        "lng": i['lng'],
        #        "url": f"clinic/{i['id']}",
        #        "name": i['name']
        #    })

        paginator = Paginator(search_result_list, 6)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            results = paginator.get_page(page)
        except PageNotAnInteger:
            results = paginator.get_page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        serializedpage = {}

        def get_page_attr():

            page_info = (
                "end_index",
                "has_next",
                "has_other_pages",
                "has_previous",
                "next_page_number",
                "number",
                "start_index",
            )

            for attr in page_info:
                v = getattr(results, attr)
                if isinstance(v, MethodType):
                    serializedpage[attr] = v()
                elif isinstance(v, (str, int)):
                    serializedpage[attr] = v
                    print(serializedpage)
                    return serializedpage

        return [serializedpage, list(results)]

    # python_serializer = serializers.get_serializer("python")()
    # serializedpage["object_list"] = python_serializer.serialize(
    #     results.object_list,
    #     fields=("name", "description", "street", "city"))

    # print(serializedpage)

    # response = HttpResponse(mimetype="application/json")
    # json.dumps(serializedpage, response, cls=DjangoJSONEncoder)
    # print(response)
    # return response

    if request.method == 'POST':
        is_search = True
        search_term = request.POST['search_term']

        return render(
            request, 'clinic_listing.html', {
                'api_key': api_key,
                'is_search': is_search,
                'result': paginate(search_term)[1],
                'page': paginate(search_term)[0],
                'latlng': coords,
            })
    else:
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user.email)

            # if user is authenticated but not finished registration:
            if not user.completed_signup:
                try:
                    user.profile.city
                except Profile.DoesNotExist:
                    return redirect(reverse('create_profile'))

        form = UserProfileForm()
    return render(
        request, 'clinic_listing.html', {
            'api_key': api_key,
            'user': user,
            'form': form,
            'is_search': is_search,
            'result': paginate(user.profile.city),
            'latlng': coords,
        })


@login_required
def clinic_profile(request, clinic_id):
    '''
    Provide a route to view the clinics public profile page.
    '''
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

    def is_searchable():
        if clinic.is_searchable():
            return

    return render(
        request, 'clinic_profile.html', {
            'clinic': clinic,
            'mods': get_mods,
            'latlng': latlng,
            'api_key': api_key,
            'reviews': clinic_reviews,
            'form': form,
            'edit': edit,
            'user': request.user,
            'is_searchable': is_searchable,
        })


@login_required
def create_review(request, clinic_id):
    '''
    Provides a route for clinic reviews to be posted and saved.
    '''
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
    '''
    Provides a route to edit a review.
    '''
    try:
        review = Reviews.objects.get(pk=review_id)
    except Reviews.DoesNotExist:
        raise Http404("This review does not exist")

    clinic_id = review.clinic.id
    title_data = review.title
    body_data = review.body

    if request.method == 'POST' and review.author == request.user:
        review.title = request.POST['title']
        review.body = request.POST['body']
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
    '''
    Provides a route for a review to be deleted by its author.
    '''
    try:
        review = Reviews.objects.get(pk=review_id)
    except Reviews.DoesNotExist:
        raise Http404("This review does not exist")

    clinic_id = review.clinic.id
    if review.author == request.user:
        review.delete()
    return redirect('clinic_profile', clinic_id=clinic_id)
