from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('elderregister/', RegisterElderAPI.as_view(), name='elderregister'),
    path('elderlogin/', LoginElderAPI.as_view(), name='elderlogin'),
    path('currentuser/', current_user, name='current_user'),
    path('token/', views.obtain_auth_token, name='token'),
    path('services/', ServicesAPIView.as_view(), name ='get_post_services'),
    path('service/<int:id>/', ServicesDetailsView.as_view(), name='get_delete_update_service'),
    # path('profiles/', ProfileAPIView.as_view()),
    # path('profile/<int:id>/', ProfileDetailsView.as_view()),
    path('elders/',ElderListView.as_view(),name ='get_post_elder_profiles'),
    path('elder/<int:id>/',ElderDetailView.as_view(),name ='get_delete_update_elder_profile'),
    path('feedback/',FeedbackSubmitAPIView.as_view(),name ='get_post_feedback'),
    path('test_volunteers/',TestVolunteerView.as_view(), name ='get_post_profiles'),
    path('test_volunteer/<int:id>/',TestVolunteerDetailView.as_view(),name='get_delete_update_profile'),
    path('custom_users/',UsersAPIView.as_view()),
    path('volunteers/<int:id>/',GetVolunteers.as_view())
]