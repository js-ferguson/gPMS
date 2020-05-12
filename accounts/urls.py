from django.urls import path, re_path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    re_path(
        r'^profile/(?P<lat>-?\d+\.\d{7})/(?P<lng>-?\d+\.\d{7})/(?P<clinic_id>\d+)/$',
        views.update_location,
        name='update_location'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile/update_user/<int:user_id>/',
         views.update_user,
         name='update_user'),
    path('profile/update_clinic/<int:user_id>/',
         views.update_clinic,
         name='update_clinic'),
    path('profile/update_mods/<int:user_id>/',
         views.update_mods,
         name='update_mods'),
    path('profile/update_city/<int:user_id>/',
         views.update_city,
         name='update_city'),
    path('change_password', views.change_password, name='change_password')
]
