from django.urls import path, re_path

from . import views

# from accounts import views as account_views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    re_path(
        r'^profile/(?P<lat>\d+\.\d{7})/(?P<lng>\d+\.\d{7})/(?P<clinic_id>\d+)/$',
        views.update_location,
        name='update_location'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    # path('register_user', account_views.register_user, name='register_user'),
    # path('login', account_views.login, name='login'),
]
