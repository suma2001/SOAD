from rest_framework import serializers
# import serializers.u
from .models import *
from django.contrib.auth.models import User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'description']


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Volunteer
        fields = ['username', 'email', 'name','volunteer_age',
                  'phone_no', 'address', 'biography', 'availability', 'services_available', 'experience', 'location']

    # def update(self, instance, validated_data):
    #     # First, update the User
    #     user_data = validated_data.pop('user', {})
    #     for attr, value in user_data.items():
    #             setattr(instance.user, attr, value)
    #     # Then, update UserProfile
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.user.save()
    #     return instance

    # def create(self, validated_data):

    #     user_data = validated_data.pop('user', {})
    #     print(user_data)
    #     user = User.objects.create(username=user_data['username'], email=user_data['email'], password=user_data['password'])
    #     user.save()
    #     # user
    #     profile = Volunteer.objects.create(user = user, **validated_data)
    #     print(profile)
    #     profile.save()
    #     return user


class ElderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['username', 'email', 'name', 'elder_age',
                  'phone_no', 'address', 'location']


class FeedbackSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d-%m-%Y %H:%m')
    class Meta:
        model = Feedback
        fields = ['volunteer_name', 'service_done', 'time', 'rating', 'custom_feedback']
