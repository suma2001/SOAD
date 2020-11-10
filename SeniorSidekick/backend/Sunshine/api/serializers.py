from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['profile_id','username', 'email','password','volunteer_name','volunteer_age',
        'phone_number','address','biography','availability','services_available','experience']

class ElderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['elder_id','username', 'email','password','elder_name','elder_age', 'phone_no','address']

class ProfileSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        # print(payload)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # if password is not None:
        #     instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Volunteer
        fields = ['token', 'profile_id','username', 'email','password','volunteer_name','volunteer_age',
        'phone_number','address','biography','availability','services_available','experience']


class ElderProfileSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        print(payload)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # if password is not None:
        #     instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Elder
        fields = ['token', 'elder_id','username', 'email','password','elder_name','elder_age', 'phone_no','address']