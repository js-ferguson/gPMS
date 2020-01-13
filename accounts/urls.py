from django.urls import path
from . import views
# from accounts import views as account_views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    # path('register_user', account_views.register_user, name='register_user'),
    # path('login', account_views.login, name='login'),
]
