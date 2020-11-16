from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path('token/', views.obtain_auth_token, name='token'),
    path('services/', ServicesAPIView.as_view()),
    path('service/<int:id>/', ServicesDetailsView.as_view()),
    path('profiles/', ProfileAPIView.as_view()),
    path('profile/<int:id>/', ProfileDetailsView.as_view()),
    path('elders/',ElderListView.as_view()),
    path('elders/<int:id>/',ElderDetailView.as_view()),
    path('feedback/',FeedbackSubmitAPIView.as_view()),
    # path('volunteers/<int:id>/',GetVolunteers.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)