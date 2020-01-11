from django.urls import path
from . import views
#from accounts import views as account_views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]
