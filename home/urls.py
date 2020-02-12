from django.urls import path

from . import views

# from accounts import views as account_views

urlpatterns = [
    path('', views.index, name='home_index'),
    path('index/', views.index, name='index'),

    # path('register_user', account_views.register_user, name='register_user'),
    # path('login', account_views.login, name='login'),
]
