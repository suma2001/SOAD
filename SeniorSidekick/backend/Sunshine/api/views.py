from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from knox.models import AuthToken
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import logout, authenticate
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.rest import Client
from django.core.mail import send_mail
from knox.auth import TokenAuthentication
import requests
from requests.api import request
from rest_framework.reverse import reverse
from googlemaps import Client as GoogleMaps
import json 
import urllib.request

User = get_user_model()


class UsersAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicesAPIView(APIView):

    def get(self, request):
        print(request.user)
        # current_user(request)
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
            return None

    def get(self, request, id):
        service = self.get_object(id)
        if service == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
        if article == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def current_user(request, token):
    cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
    # tokens = ''
    # # print(AuthToken.objects.filter(user))
    # for token in AuthToken.objects.all():
    #     # print(type(token))
    #     RHS = str(token).split(':')[1].strip()
    #     LHS = str(token).split(':')[0].strip()
    #     print(RHS)
    #     if RHS==user:
    #         tokens=LHS
    #         break
    # print(AuthToken.objects.all())
    # x = AuthToken.objects.filter(user=user)
    # print(x)
    return Response({
        'username': cus_user.username,
        # 'token': AuthToken.objects.create(user)[0]
    })


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterTestVolunteerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user1 = serializer.validated_data.pop('user')
        username = user1['username']
        # print("User is:", user['username'])
        user = User.objects.get(username=username)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "volunteer_age": serializer.validated_data['volunteer_age'],
            "phone_no": serializer.validated_data['phone_no'],
            "location": serializer.validated_data['location'],
            "availability": serializer.validated_data['availability'],
            "address_line1": serializer.validated_data['address_line1'],
            "address_line2": serializer.validated_data['address_line2'],
            "area": serializer.validated_data['area'],
            "city": serializer.validated_data['city'],
            "state": serializer.validated_data['state'],
            "country": serializer.validated_data['country'],
            "pincode": serializer.validated_data['pincode'],
            "token": AuthToken.objects.create(user)[1],
        },status = status.HTTP_201_CREATED)


# Login API
class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        print("Hello")
        serializer = AuthTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # user = authenticate(username=username, password=password)
        user = serializer.validated_data
        Cususer = User.objects.get(username=username)
        print(Cususer)
        # login(request, user)
        # print(request.user)
        # user = User.objects.get(username=username)
        # current_user(request)
        # window.localStorage.setItem(request.user.token, request.user)

        # print(AuthToken.objects.all())
        # print(TokenAuthentication().authenticate_credentials(token=token1.encode(encoding='UTF-8',errors='strict')))
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(Cususer)[1]
        })


class LogoutAPI(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        print(AuthToken.objects.all())
        print("Logged in user is: ", request.user)
        try:
            AuthToken.objects.filter(user=request.user).delete()
        except:
            print("Error")

        logout(request)
        # request.user.token.delete()
        return Response(status=status.HTTP_200_OK)


# Elder Register API
class RegisterElderAPI(generics.GenericAPIView):
    serializer_class = RegisterElderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user1 = serializer.validated_data.pop('user')
        username = user1['username']
        # print("User is:", user['username'])
        user = User.objects.get(username=username)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "elder_age": serializer.validated_data['elder_age'],
            "phone_no": serializer.validated_data['phone_no'],
            "location": serializer.validated_data['location'],
            "address_line1": serializer.validated_data['address_line1'],
            "address_line2": serializer.validated_data['address_line2'],
            "area": serializer.validated_data['area'],
            "city": serializer.validated_data['city'],
            "state": serializer.validated_data['state'],
            "country": serializer.validated_data['country'],
            "pincode": serializer.validated_data['pincode'],
            "token": AuthToken.objects.create(user)[1]
        },status=status.HTTP_201_CREATED)


# Login API
class LoginElderAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginElderAPI, self).post(request, format=None)


class TestVolunteerView(APIView):
    def get(self, request, format=None):
        T_volunteers = TestVolunteer.objects.all()
        serializer = RegisterTestVolunteerSerializer(T_volunteers, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = RegisterTestVolunteerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # user = serializer.validated_data['user']
    #         # login(request, user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestVolunteerDetailView(APIView):
    def get_object_token(self, token):
        cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
        try:
            return TestVolunteer.objects.get(user=cus_user[0])
        except TestVolunteer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_id(self, id):
        try:
            return TestVolunteer.objects.get(pk=id)
        except TestVolunteer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, token):
        if isinstance(token, int):
            service = self.get_object_id(token)
        else:
            service = self.get_object_token(token)
        if service == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterTestVolunteerSerializer(service)
        print(len(serializer.data))
        return Response(serializer.data)

    def put(self, request, token):
        if isinstance(token, int):
            service = self.get_object_id(token)
        else:
            service = self.get_object_token(token)
        serializer = RegisterTestVolunteerSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, token):
        if isinstance(token, int):
            article = self.get_object_id(token)
        else:
            article = self.get_object_token(token)
        if article == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElderListView(APIView):
    def get(self, request, format=None):
        elders = Elder.objects.all()
        serializer = RegisterElderSerializer(elders, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = RegisterElderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElderDetailView(APIView):
    def get_object_token(self, token):
        cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
        try:
            return Elder.objects.get(user=cus_user[0])
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_id(self, id):
        try:
            return Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, token):
        print(token)
        # print(AuthToken.objects.all())
        # tuser = AuthToken.objects.get(token_key=token)
        # print(tuser)
        if isinstance(token, int):
            service = self.get_object_id(token)
        else:
            service = self.get_object_token(token)
        if service == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterElderSerializer(service)
        print(len(serializer.data))
        return Response(serializer.data)

    def put(self, request, token):
        if isinstance(token, int):
            service = self.get_object_id(token)
        else:
            service = self.get_object_token(token)
        serializer = RegisterElderSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, token):
        if isinstance(token, int):
            article = self.get_object_id(token)
        else:
            article = self.get_object_token(token)
        if article == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetVolunteers(APIView):
    def get_object_token(self, token):
        cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
        try:
            return Elder.objects.get(user=cus_user[0])
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_id(self, id):
        try:
            return Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, token, format=None):
        if isinstance(token, int):
            elder = self.get_object_id(token)
        else:
            elder = self.get_object_token(token)
        current_location = elder.location
        print(elder.request_service)
        print(TestVolunteer.objects.filter(services_available=elder.request_service))
        if elder.request_service != 0:
            volunteers = TestVolunteer.objects.filter(location__dwithin=(current_location, 100), availability=True,
                                                      services_available=elder.request_service
                                                      ).annotate(distance=Distance('location', current_location))
        else:
            volunteers = TestVolunteer.objects.filter(location__dwithin=(current_location, 100), availability=True,
                                                      ).annotate(distance=Distance('location', current_location))

        serializer = RegisterTestVolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)


class RequestServiceAPIView(APIView):

    def get_matching_volunteers(self,service_name,user):
        matching_volunteers = []
        # user_data = requests.get(
        #     url="http://127.0.0.1:8000/api/currentuser/"
        # )
        # user_data = user_data.json()
        # print(user_data)
        # print("Hello")
        # print(user_data['username'])
        # print(user_data[0].data['name'])
        # username = user_data['username']
        # print(username)
        # user = User.objects.get(username=username)
        elder_id = Elder.objects.filter(user=user)[0].id
        print(elder_id)
        url = "http://127.0.0.1:8000/api/volunteers/" + str(elder_id)+"/"
        nearest_volunteers = requests.get(url=url).json()
        print(nearest_volunteers)
        for volunteer in nearest_volunteers:
            service_id = volunteer['services_available']
            service = Service.objects.get(id=service_id)
            if service.name == service_name and volunteer['availability']==True:
                matching_volunteers.append(volunteer)
        return matching_volunteers

    def post(self, request, format=None):
        print("HI")
        serializer = RequestServiceSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
            service_id = serializer.data['name']
            print(service_id)
            # service_available = TestVolunteer.objects.get(pk=1).services_available
            try:
                elder = Elder.objects.get(pk=1)
            except Elder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            elder.request_service = int(service_id)
            print(elder.request_service)
            elder.save()
            print(elder.request_service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetDirections(APIView):

    def getPlaceID(self,address_line1,address_line2,area,city,state,country,pincode):
        gmaps = GoogleMaps('AIzaSyBoy1plslvW_UTSM3JTWNLijJL1KjsKf60')
        address = str(address_line1)+ ',' + str(address_line2)+ ',' + str(area) + ',' + str(city) + ',' + str(state) + ',' + str(country) + ',' + str(pincode)
        geocode_result = gmaps.geocode(address)
        print(geocode_result[0]['formatted_address'])
        place_id = geocode_result[0]['place_id']
        return place_id
    
    def get_address(self,lat,lng):
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json?"
        api_key = "AIzaSyBoy1plslvW_UTSM3JTWNLijJL1KjsKf60"
        nav_request = "latlng=" + str(lat) + "," + str(lng) + "&key=" + api_key
        request = endpoint + nav_request
        response = urllib.request.urlopen(request).read()
        results = json.loads(response)['results']
        address = results[0]['formatted_address']
        return address

    def get_Directions(self,place_id1,place_id2):
        endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
        api_key = "AIzaSyBoy1plslvW_UTSM3JTWNLijJL1KjsKf60"
        nav_request = "origin=place_id:"+place_id1+"&destination=place_id:"+place_id2+"&key="+api_key
        request = endpoint + nav_request
        response = urllib.request.urlopen(request).read()
        directions = json.loads(response)
        routes = directions['routes']
        legs = routes[0]['legs']
        steps = legs[0]['steps']
        dir_list = []
        for each in steps:
            step = {}
            step["distance"] = each['distance']['text']
            step["estimated_time"] = each['duration']['text']
            step["start_location"] = self.get_address(each['start_location']['lat'],each['start_location']['lng'])
            step["end_location"] = self.get_address(each['end_location']['lat'],each['end_location']['lng'])
            dir_list.append(step)
        return dir_list
    
    def get(self,request,id,format=None):
        try:
            elder = Elder.objects.get(id=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        volunteer = TestVolunteer.objects.get(user = request.user)

        elder_place_id = self.getPlaceID(elder.address_line1,elder.address_line2,elder.area,elder.city,elder.state,elder.country,elder.pincode)
        volunteer_place_id = self.getPlaceID(volunteer.address_line1,volunteer.address_line2,volunteer.area,volunteer.city,volunteer.state,
                                volunteer.country,volunteer.pincode)

        print(elder.location)
        print(volunteer.location)
        print(elder_place_id)
        print(volunteer_place_id)
        steps = self.get_Directions(volunteer_place_id,elder_place_id)

        serializer = DirectionsSerializer(steps, many=True)
        print(serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)


# @csrf_exempt
# def AddElders(request):
#     if request.method=="POST":
#         print("Helo")
#         print(request.POST.get('elder'))
#         # elderid = request.POST['elder']
#         # volunteerid = request.POST['volunteer']
#         # volunteer = TestVolunteer.objects.get(pk=volunteerid)
#         # if elderid not in volunteer.elder_ids:
#         #     volunteer.elder_ids.append(elderid)
#         # volunteer.save()
#         return HttpResponse("Thank you") 

class AddElderAPIView(APIView):
    def get_object_token(self, token):
        cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
        try:
            return Elder.objects.get(user=cus_user[0])
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_id(self, id):
        try:
            return Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        print("I am in")
        serializer = AddElderSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            if isinstance(data['elder'],int):
                eld = self.get_object_id(data['elder'])
            else:
                eld = self.get_object_token(data['elder'])
            vol = TestVolunteer.objects.get(pk=data['volunteer'])
            print(vol.elder_ids)
            if eld.id not in vol.elder_ids:
                vol.elder_ids.append(eld.id)
            vol.save()
            print(vol.elder_ids)
            # phone_no = "6382677337"
            # account_sid = 'ACf62e531f2099e445acf3cce250fbdc6a'
            # auth_token  = '3a620bdf57bc951d3a28b43b60c27765'
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            #     body="Your service is booked",
            #     to="+91" + phone_no,
            #     from_="+12512500974",
            #     )
            # print (message.sid)
            send_mail(
                'Regarding asking help',
                'Wait for your match!!',
                'sumashreya72@gmail.com',
                ['sumashreyatv@gmail.com'],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteElderAPIView(APIView):
    def get_object_token(self, token):
        cus_user = TokenAuthentication().authenticate_credentials(token=token.encode(encoding='UTF-8', errors='strict'))
        try:
            return TestVolunteer.objects.get(user=cus_user[0])
        except TestVolunteer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_id(self, id):
        try:
            return TestVolunteer.objects.get(pk=id)
        except TestVolunteer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        print("I am in")
        serializer = DeleteElderSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            if isinstance(data['volunteer'],int):
                vol = self.get_object_id(data['volunteer'])
            else:
                vol = self.get_object_token(data['volunteer'])
            eld = Elder.objects.get(pk=data['elder'])
            print(vol.elder_ids)
            if eld.id in vol.elder_ids:
                vol.elder_ids.remove(eld.id)
            vol.save()
            print(vol.elder_ids)
            details = ["username", "elder_age", "phone_no"]
            edetail = {
                "Username": eld.user.username,
                "Age ": eld.elder_age,
                "Phone No ": eld.phone_no,
            }
            vdetail = {
                "Username": vol.user.username,
                "Age ": vol.volunteer_age,
                "Phone No ": vol.phone_no,
            }
            send_mail(
                'Regarding asking help',
                'Elder: ' + str(edetail) + "Volunteer: " + str(vdetail),
                'sumashreya72@gmail.com',
                ['sumashreyatv@gmail.com'],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackSubmitAPIView(APIView):
    def get(self, request, format=None):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("HI")
        serializer = FeedbackSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def notifications(p1, p2):
    print(p1, p2)
    # phone_no = "6303588356"
    # account_sid = 'AC56e26320fee387bc8bcaf52128c52138'
    # auth_token  = '10925b2912913cfba8f5409ba655673d'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body="Your service is booked",
    #     to="+91" + phone_no,
    #     from_="+19105861815",
    #     )
    # print (message.sid)

    # phone_no = "6382677337"
    # account_sid = 'ACf62e531f2099e445acf3cce250fbdc6a'
    # auth_token  = '2ac0f267f0e3eefea063b67013dff017'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body="Your service is booked",
    #     to="+91" + phone_no,
    #     from_="+12512500974",
    #     )
    # print (message.sid)

    # data = {'message': "Notifcation successfully sent !"}
    return Response(status=status.HTTP_200_OK)
