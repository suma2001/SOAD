from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path('token/', views.obtain_auth_token, name='token'),
    path('services/', ServicesAPIView.as_view(),name='get_post_services'),
    path('service/<int:id>/', ServicesDetailsView.as_view(),name="get_delete_update_service"),
    path('profiles/', ProfileAPIView.as_view(),name = "get_post_profiles"),
    path('profile/<int:id>/', ProfileDetailsView.as_view(),name = "get_delete_update_profile"),
    path('elders/',ElderListView.as_view(),name = "get_post_elder_profiles"),
    path('elders/<int:id>/',ElderDetailView.as_view(),name = "get_delete_update_elder_profile"),
    path('feedback/',FeedbackSubmitAPIView.as_view()),
    # path('volunteers/<int:id>/',GetVolunteers.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)