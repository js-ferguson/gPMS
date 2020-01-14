from django.urls import path
from .views import register_clinic
# from accounts import views as account_views

urlpatterns = [
    # path('', views.index, name='home_index'),
    # path('clinic_listing/', clinic_listing, name='listing'),
    path('register_clinic/', register_clinic, name='register_clinic'),
    # path('login', account_views.login, name='login'),
]
