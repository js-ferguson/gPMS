from django.urls import path

from . import views

#from accounts import views as account_views

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
]
