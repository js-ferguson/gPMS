from django.urls import path

from .views import (clinic_listing, clinic_profile, create_review, edit_review,
                    register_clinic, search)

# from accounts import views as account_views

urlpatterns = [
    # path('', views.index, name='home_index'),
    path('clinic_listing/', clinic_listing, name='clinic_listing'),
    path('register_clinic/', register_clinic, name='register_clinic'),
    path('search/', search, name='search'),
    path('clinic/<int:clinic_id>/', clinic_profile, name='clinic_profile'),
    path('clinic/<int:clinic_id>/create_review/',
         create_review,
         name='create_review'),
    path('clinic/edit_review/<int:review_id>', edit_review, name='edit_review')
    # path('login', account_views.login, name='login'),
]
