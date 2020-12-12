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
    path('currentuser/token/', current_user, name='current_user'),
    path('token/', views.obtain_auth_token, name='token'),
    path('services/', ServicesAPIView.as_view(), name ='get_post_services'),
    path('service/<int:id>/', ServicesDetailsView.as_view(), name='get_delete_update_service'),
    # path('profiles/', ProfileAPIView.as_view()),
    path('Addelders/', AddElderAPIView.as_view(), name="AddElders"),
    path('Deleteelders/', DeleteElderAPIView.as_view(), name="DelElders"),
    path('elders/',ElderListView.as_view(),name ='get_post_elder_profiles'),
    path('elder/id/<int:token>/', ElderDetailView.as_view(), name='get_delete_update_elder_profile_id'),
    path('elder/<token>/',ElderDetailView.as_view(),name ='get_delete_update_elder_profile_token'),
    path('requestservice/',RequestServiceAPIView.as_view(),name ='get_post_service'),
    path('feedback/',FeedbackSubmitAPIView.as_view(),name ='get_post_feedback'),
    path('test_volunteers/',TestVolunteerView.as_view(), name ='get_post_profiles'),
    path('test_volunteer/id/<int:token>/', TestVolunteerDetailView.as_view(), name='get_delete_update_profile_id'),
    path('test_volunteer/<token>/',TestVolunteerDetailView.as_view(),name='get_delete_update_profile_token'),
    path('custom_users/',UsersAPIView.as_view()),
    path('volunteers/id/<int:token>/', GetVolunteers.as_view(), name='get_near_vol_id'),
    path('volunteers/<token>/',GetVolunteers.as_view(),name='get_near_vol_token')
]