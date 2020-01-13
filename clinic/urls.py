from django.urls import path
from . import views
# from accounts import views as account_views

urlpatterns = [
    # path('', views.index, name='home_index'),
    path('clinic', views.listing, name='listing'),
    # path('register_user', account_views.register_user, name='register_user'),
    # path('login', account_views.login, name='login'),
]
