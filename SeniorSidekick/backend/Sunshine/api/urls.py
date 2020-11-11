from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    # path('article/', article_list),
    path('services/', ServicesAPIView.as_view(),name='services'),
    path('service/<int:id>/', ServicesDetailsView.as_view(), name = 'service_detail'),
    path('profiles/', ProfileAPIView.as_view(),name = 'profile'),
    path('profile/<int:id>/', ProfileDetailsView.as_view(),name = 'profile_detail'),
]