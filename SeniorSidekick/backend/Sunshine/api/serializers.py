from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','name','description']
        # read_only_fields = ['service_id']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['profile_id','username','email','volunteer_name','volunteer_age',
        'phone_number','address','biography','availability','services_available','experience']
        # read_only_fields = ['profile_id','experience']
