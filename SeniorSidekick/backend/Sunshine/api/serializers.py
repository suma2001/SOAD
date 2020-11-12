from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


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


class VolunteerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Volunteer
        fields = ['email', 'username', 'password', 'volunteer_age', 'phone_number']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        volunteer_age = attrs.get('volunteer_age', '')
        phone_number = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        if not phone_number.isnumeric():
            raise serializers.ValidationError('Phone number should only consist of numbers')
        if volunteer_age < 15:
            raise serializers.ValidationError('You must be at least 15 years to volunteer')
        if len(password) < 6:
            raise serializers.ValidationError('Minimum required password length is 6')
        return attrs

    def create(self, validated_data):
        return Volunteer.objects.create_user(**validated_data)

class ElderRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['email', 'username', 'password', 'elder_age', 'phone_no']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        elder_age = attrs.get('elder_age', '')
        phone_no = attrs.get('phone_no', '')
        if not phone_no.isnumeric():
            raise serializers.ValidationError('Phone number should only consist of numbers')
        if elder_age < 40:
            raise serializers.ValidationError('Sorry! We currently offer services for people above 40 years')
        if len(password) < 6:
            raise serializers.ValidationError('Minimum required password length is 6')
        return attrs

    def create(self, validated_data):
        return Elder.objects.create_user(**validated_data)

class VolunteerLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=6, write_only=True)
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = Volunteer
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                raise AuthenticationFailed('Account disabled')
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return attrs


class ElderLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                raise AuthenticationFailed('Account disabled')
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return attrs

class VolunteerResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        user = Volunteer.objects.get(email=email)
        if not user:
            raise AuthenticationFailed('Email does not exist, please check again')
        return attrs

class ElderResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elder
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        user = Elder.objects.get(email=email)
        if not user:
            raise AuthenticationFailed('Email does not exist, please check again')
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        fields = ['password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1', '')
        password2 = attrs.get('password2', '')

        if password1 == password2:
            return attrs
        elif password1 != password2:
            raise serializers.ValidationError("Passwords don't match")

