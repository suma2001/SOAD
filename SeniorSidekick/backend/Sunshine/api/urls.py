from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('article/', article_list),
    path('services/', ServicesAPIView.as_view()),
    path('service/<int:id>/', ServicesDetailsView.as_view()),
    path('profiles/', ProfileAPIView.as_view()),
    path('profile/<int:id>/', ProfileDetailsView.as_view()),
]