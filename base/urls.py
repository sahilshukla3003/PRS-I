from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('payment/<str:plan>/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.history, name='history'),
    path('reviews/<str:pname>/', views.reviews, name='reviews'),
    path('customreview/', views.analyze_review ,name='custom'),
    path('about/', views.about, name='about')
]