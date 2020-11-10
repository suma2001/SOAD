from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    # path('article/', article_list),
    path('services/', ServicesAPIView.as_view()),
    path('service/<int:id>/', ServicesDetailsView.as_view()),
    path('volunteer-signup/', ProfileCreate.as_view()),
    path('elder-signup/', ElderCreate.as_view()),
    path('profiles/', ProfileAPIView.as_view()),
    path('profile/<int:id>/', ProfileDetailsView.as_view()),
    path('elders/',ElderListView.as_view()),
    path('elders/<int:id>/',ElderDetailView.as_view()),
    path('volunteers/<int:id>/',GetVolunteers.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)