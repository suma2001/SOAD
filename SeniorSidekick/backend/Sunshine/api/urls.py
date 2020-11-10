from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    # path('article/', article_list),
    path('services/', ServicesAPIView.as_view()),
    path('service/<int:id>/', ServicesDetailsView.as_view()),
    path('profiles/', ProfileAPIView.as_view()),
    path('profile/<int:id>/', ProfileDetailsView.as_view()),
    path('elders/',ElderListView.as_view()),
    path('elder/<int:id>/',ElderDetailView.as_view()),
    path('volunteers/<int:id>/',GetVolunteers.as_view()),
    path('signup/', UserList.as_view()),
    path('login/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    
]