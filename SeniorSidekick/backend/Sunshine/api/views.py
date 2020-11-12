from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import *
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


class ServicesAPIView(APIView):

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicesDetailsView(APIView):

    def get_object(self, id):
        try:
            return Service.objects.get(pk=id)
        except Service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        service = self.get_object(id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, id):
        service = self.get_object(id)
        serializer = ServiceSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileAPIView(APIView):
    def get(self, request, format=None):
        profiles = Volunteer.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileCreate(generics.GenericAPIView):
    serializer_class = VolunteerRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = Volunteer.objects.get(email=user_data['email'])
        user.id = user.profile_id
        token = Token.objects.create(user=user)
        uidb64 = urlsafe_base64_encode(smart_bytes(token.profile_id))
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify', kwargs={'uidb64': uidb64})
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi! Welcome to Senior Sunshine.\nClick on the below link to verify your email\n' + absurl
        message = {'email_body': email_body, 'email_subject': 'Email Verification for Senior Sunshine', 'to_email': (user.email, )}
        Util.send_email(message)
        user_data['token'] = token.key
        user_data['profile_id'] = user.id
        user_data['is_verified'] = user.is_verified
        return Response(user_data, status=status.HTTP_201_CREATED)


class VolunteerVerifyEmail(generics.GenericAPIView):

    def get(self, request, uidb64):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = Volunteer.objects.get(profile_id=user_id)
        if user:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                email_body = 'Your email was successfully verified. Thanks for registering.'
                message = {'email_body': email_body, 'email_subject': 'Welcome to Senior Sunshine',
                           'to_email': (user.email)}
                Util.send_email(message)
                return Response({'status': 'Successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileLogin(generics.GenericAPIView):
    serializer_class = VolunteerLoginSerializer

    def post(self, request):
        if request.session.session_key:
            return Response({'error': 'Already another user is logged in'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.data
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            account = authenticate(email=user['email'], password=user['password'])
            account.id = account.profile_id
            token = Token.objects.get(user=account)
            login(request, account)
            return Response({'success': 'Login successful', 'token': token.key, 'user_id': account.profile_id,
                             'username': account.username, 'email': account.email, 'phone_number': account.phone_number,
                             'is_verified': account.is_verified}, status=status.HTTP_200_OK)

class ElderCreate(generics.GenericAPIView):
    serializer_class = ElderRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = Elder.objects.get(email=user_data['email'])
        user.id = user.elder_id
        token = Token.objects.get(user=user)
        uidb64 = urlsafe_base64_encode(smart_bytes(token.elder_id))
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify', kwargs={'uidb64': uidb64})
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi! Welcome to Senior Sunshine.\nClick on the below link to verify your email\n' + absurl
        message = {'email_body': email_body, 'email_subject': 'Email Verification for Senior Sunshine', 'to_email': (user.email, )}
        Util.send_email(message)
        user_data['token'] = token.key
        user_data['elder_id'] = user.id
        return Response(user_data, status=status.HTTP_201_CREATED)

class ElderVerifyEmail(generics.GenericAPIView):
    def get(self, request, uidb64):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = Elder.objects.get(elder_id=user_id)
        if user:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                email_body = 'Your email was successfully verified. Thanks for registering.'
                message = {'email_body': email_body, 'email_subject': 'Welcome to Senior Sunshine',
                           'to_email': (user.email)}
                Util.send_email(message)
                return Response({'status': 'Successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

class ElderLoginAPIView(generics.GenericAPIView):
    serializer_class = ElderLoginSerializer

    def post(self, request):
        if request.session.session_key:
            return Response({'error': 'Already another user is logged in'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.data
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            account = authenticate(email=user['email'], password=user['password'])
            account.id = account.elder_id
            token = Token.objects.get(user=account)
            login(request, account)
            return Response({'success': 'Login successful', 'token': token.key, 'user_id': account.elder_id,
                             'email': account.email, 'phone_number': account.phone_number,
                             'is_verified': account.is_verified}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        if request.session.session_key:
            logout(request)
            return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "You haven't logged in yet"}, status=status.HTTP_400_BAD_REQUEST)


# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         user = UserData.objects.get(email=user['email'])

#         if user:
#             user.id = user.user_id
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(request).domain
#             relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
#             absurl = 'http://' + current_site + relative_link
#             email_body = 'Hi ' + user.username + ', click the link below to reset your password\n' + absurl
#             message = {'email_body': email_body, 'email_subject': 'Reset Password', 'to_email': (user.email,)}
#             Util.send_email(message)
#             return Response({'success': 'We have sent you a link to reset password'}, status=status.HTTP_200_OK)


# class PasswordReset(generics.GenericAPIView):
#     serializer_class = ResetPasswordSerializer

#     def post(self, request, user_id):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         serializer.is_valid(raise_exception=True)
#         user = UserData.objects.get(user_id=user_id)
#         password = data['password1']
#         user.set_password(password)
#         user.save()
#         return redirect('login')


# class PasswordTokenCheckAPI(generics.GenericAPIView):

#     def get(self, request, uidb64, token):

#         try:
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = UserData.objects.get(user_id=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'Token is not valid, please request a new one'},
#                                 status=status.HTTP_401_UNAUTHORIZED)
#             reset_password_url = reverse('reset-password', kwargs={'user_id': user_id})

#             return redirect(reset_password_url)

#         except DjangoUnicodeDecodeError:
#             return Response({'error': 'Token is not valid, please request a new one'},
#                             status=status.HTTP_401_UNAUTHORIZED)


class ElderLogin(generics.GenericAPIView):
    serializer_class = ElderLoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        account = authenticate(email=user['email'], password=user['password'])
        login(request, account)

        return Response({'success': 'Login successful', 'user_id': account.user_id,
                         'username': account.username, 'email': account.email,
                         'phone_number': account.phone_number}, status=status.HTTP_200_OK)

class ProfileDetailsView(APIView):

    def get_object(self, id):
        try:
            return Volunteer.objects.get(pk=id)
        except Volunteer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        profile = self.get_object(id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, id):
        profile = self.get_object(id)
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        profile = self.get_object(id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElderListView(APIView):
    def get(self, request, format=None):
        Elders = Elder.objects.all()
        serializer = ElderProfileSerializer(Elders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ElderProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElderDetailView(APIView):
    def get_object(self, id):
        try:
            return Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        elder = self.get_object(id)
        serializer = ElderProfileSerializer(elder)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        elder = self.get_object(id)
        serializer = ElderProfileSerializer(elder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        elder = self.get_object(id)
        elder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetVolunteers(APIView):
    def get(self,request,id,format=None):
        try:
            elder = Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_location = elder.location
        volunteers = Volunteer.objects.filter(location__dwithin=(current_location, 1), availability=True
                                              ).annotate(distance=Distance('location', current_location))

        serializer = ProfileSerializer(volunteers, many=True)
        return Response(serializer.data)
