from rest_framework import serializers
from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['profile_id', 'email', 'password', 'volunteer_name', 'volunteer_age',
                  'phone_number', 'address', 'biography', 'availability', 'services_available', 'experience']


class ElderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['elder_id', 'email', 'password', 'elder_name', 'elder_age',
                  'phone_no', 'address']

class FeedbackSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d-%m-%Y %H:%m')
    class Meta:
        model = Feedback
        fields = ['volunteer_name', 'service_done', 'time', 'rating', 'custom_feedback']
