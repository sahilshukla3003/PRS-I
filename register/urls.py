from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('forgot', views.forgot_password, name='forgot'),
]