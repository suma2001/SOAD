from rest_framework import serializers
# import serializers.u
from .models import *
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
# from drf_writable_nested.serializers import WritableNestedModelSerializer
from googlemaps import Client as GoogleMaps
from django.contrib.auth import logout, authenticate

User = get_user_model()  # custom user model


def getLocation(address_line1, address_line2, area, city, state, country, pincode):
    gmaps = GoogleMaps('AIzaSyBoy1plslvW_UTSM3JTWNLijJL1KjsKf60')
    address = str(address_line1) + ',' + str(address_line2) + ',' + str(area) + ',' + str(city) + ',' + str(
        state) + ',' + str(country) + ',' + str(pincode)
    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    print(lat, lon)
    location = "SRID=4326;POINT (" + str(lat) + " " + str(lon) + ")"
    print(location)
    return location


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
        fields = ['id', 'name', 'description']


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
        fields = ['id', 'user', 'volunteer_age', 'phone_no', 'availability', 'elder_ids', 'location',
                  'services_available', 'address_line1', 'address_line2',
                  'area', 'city', 'state', 'country', 'pincode']
        read_only_fields = ('email',)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        print(user_data)
        user1 = User.objects.create_user(username=user_data['username'],
                                         email=user_data['email'],
                                         password=user_data['password'])

        address_line1 = validated_data['address_line1']
        address_line2 = validated_data['address_line2']
        area = validated_data['area']
        city = validated_data['city']
        state = validated_data['state']
        country = validated_data['country']
        pincode = validated_data['pincode']

        volunteer = TestVolunteer()
        volunteer.user = user1
        volunteer.phone_no = validated_data['phone_no']
        # volunteer.address = validated_data['address']
        volunteer.volunteer_age = validated_data['volunteer_age']
        # volunteer.location = validated_data['location']
        volunteer.availability = validated_data['availability']
        volunteer.services_available = validated_data['services_available']
        volunteer.address_line1 = address_line1
        volunteer.address_line2 = address_line2
        volunteer.area = area
        volunteer.city = city
        volunteer.state = state
        volunteer.country = country
        volunteer.pincode = pincode
        volunteer.location = getLocation(address_line1, address_line2, area, city, state, country, pincode)
        volunteer.save()
        print(volunteer.location)
        return volunteer

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     each = TestVolunteer.objects.get(user=instance.user)
    #     cuser = instance.user
    #     cuser.username = user_data.get('username', cuser.username)
    #     cuser.password = user_data.get('password', cuser.password)
    #     cuser.email = user_data.get('email', cuser.email)
    #     cuser.save()

    #     each.user = cuser
    #     each.phone_no =  validated_data.get('phone_no', each.phone_no)
    #     each.address =  validated_data.get('address', each.address)
    #     each.volunteer_age =  validated_data.get('volunteer_age', each.volunteer_age)
    #     each.location =  validated_data.get('location', each.location)
    #     each.availability =  validated_data.get('availability', each.availability)
    #     each.services_available =  validated_data.get('services_available', each.services_available)
    #     each.save()
    #     return instance


class RegisterElderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Elder
        fields = ['id', 'user', 'elder_age',
                  'phone_no', 'location', 'address_line1', 'address_line2',
                  'area', 'city', 'state', 'country', 'pincode']
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
        # elder.address = validated_data['address']
        elder.location = validated_data['location']
        elder.elder_age = validated_data['elder_age']
        elder.address_line1 = validated_data['address_line1']
        elder.address_line2 = validated_data['address_line2']
        elder.area = validated_data['area']
        elder.city = validated_data['city']
        elder.state = validated_data['state']
        elder.country = validated_data['country']
        elder.pincode = validated_data['pincode']
        elder.save()
        return elder

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     each = Elder.objects.get(user=instance.user)
    #     cuser = instance.user
    #     cuser.username = user_data.get('username', cuser.username)
    #     cuser.password = user_data.get('password', cuser.password)
    #     cuser.email = user_data.get('email', cuser.email)
    #     cuser.save()

    #     each.user = cuser
    #     each.phone_no =  validated_data.get('phone_no', each.phone_no)
    #     each.address =  validated_data.get('address', each.address)
    #     each.elder_age =  validated_data.get('volunteer_age', each.elder_age)
    #     each.location =  validated_data.get('location', each.location)
    #     each.save()
    #     return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class RequestServiceSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d-%m-%Y %H:%m')

    class Meta:
        model = Service
        fields = ['name', 'time']


class AddElderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddElder
        fields = ['elder', 'volunteer']


class DeleteElderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteElder
        fields = ['elder', 'volunteer']


class FeedbackSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d-%m-%Y %H:%m')

    class Meta:
        model = Feedback
        fields = ['volunteer_name', 'service_done', 'time', 'rating', 'custom_feedback']
