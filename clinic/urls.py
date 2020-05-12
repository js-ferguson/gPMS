from django.urls import path

from .views import (clinic_profile, create_review, delete_review, edit_review,
                    register_clinic, search)

urlpatterns = [
    path('register_clinic/', register_clinic, name='register_clinic'),
    path('search/', search, name='search'),
    path('clinic/<int:clinic_id>/', clinic_profile, name='clinic_profile'),
    path('clinic/<int:clinic_id>/create_review/',
         create_review,
         name='create_review'),
    path('clinic/edit_review/<int:review_id>', edit_review,
         name='edit_review'),
    path('clinic/delete_review/<int:review_id>',
         delete_review,
         name='delete_review')
]
