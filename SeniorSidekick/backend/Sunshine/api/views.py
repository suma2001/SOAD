from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import *
from .models import *
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


class ProfileCreate(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerRegisterSerializer

class ElderCreate(generics.ListCreateAPIView):
    queryset = Elder.objects.all()
    serializer_class = ElderProfileSerializer

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
