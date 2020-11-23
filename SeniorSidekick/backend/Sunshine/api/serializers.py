from rest_framework import serializers
# import serializers.u
from .models import *
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
# from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()  # custom user model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        user.save()
        return user


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'description']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')


# Register Serializer
class RegisterTestVolunteerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = TestVolunteer
        fields = ['user', 'volunteer_age', 'phone_no', 'address', 'availability', 'location', 'services_available']
        read_only_fields = ('email',)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        print(user_data)
        user1 = User.objects.create_user(username=user_data['username'],
                                         email=user_data['email'],
                                         password=user_data['password'])

        volunteer = TestVolunteer()
        volunteer.user = user1
        volunteer.phone_no = validated_data['phone_no']
        volunteer.address = validated_data['address']
        volunteer.volunteer_age = validated_data['volunteer_age']
        volunteer.location = validated_data['location']
        volunteer.availability = validated_data['availability']
        volunteer.services_available = validated_data['services_available']
        volunteer.save()
        return volunteer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        each = TestVolunteer.objects.get(user=instance.user)
        cuser = instance.user
        cuser.username = user_data.get('username', cuser.username)
        cuser.password = user_data.get('password', cuser.password)
        cuser.email = user_data.get('email', cuser.email)
        cuser.save()

        each.user = cuser
        each.phone_no =  validated_data.get('phone_no', each.phone_no)
        each.address =  validated_data.get('address', each.address)
        each.volunteer_age =  validated_data.get('volunteer_age', each.volunteer_age)
        each.location =  validated_data.get('location', each.location)
        each.availability =  validated_data.get('availability', each.availability)
        each.services_available =  validated_data.get('services_available', each.services_available)
        each.save()
        return instance


class RegisterElderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Elder
        fields = ['user', 'elder_age',
                  'phone_no', 'address', 'location']
        read_only_fields = ('email',)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        print(user_data)
        user1 = User.objects.create_user(username=user_data['username'],
                                         email=user_data['email'],
                                         password=user_data['password'])

        elder = Elder()
        elder.user = user1
        elder.phone_no = validated_data['phone_no']
        elder.address = validated_data['address']
        elder.location = validated_data['location']
        elder.elder_age = validated_data['elder_age']
        elder.save()
        return elder

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        each = Elder.objects.get(user=instance.user)
        cuser = instance.user
        cuser.username = user_data.get('username', cuser.username)
        cuser.password = user_data.get('password', cuser.password)
        cuser.email = user_data.get('email', cuser.email)
        cuser.save()

        each.user = cuser
        each.phone_no =  validated_data.get('phone_no', each.phone_no)
        each.address =  validated_data.get('address', each.address)
        each.elder_age =  validated_data.get('volunteer_age', each.elder_age)
        each.location =  validated_data.get('location', each.location)
        each.save()
        return instance
    

class FeedbackSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d-%m-%Y %H:%m')
    class Meta:
        model = Feedback
        fields = ['volunteer_name', 'service_done', 'time', 'rating', 'custom_feedback']