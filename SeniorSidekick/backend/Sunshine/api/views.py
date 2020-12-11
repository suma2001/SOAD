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
def current_user(request):
    user = request.user
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
    return Response({
        'username': user.username,
        # 'token': tokens
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
            "address_line1" : serializer.validated_data['address_line1'],
            "address_line2" : serializer.validated_data['address_line2'],
            "area" : serializer.validated_data['area'],
            "city" : serializer.validated_data['city'],
            "state" : serializer.validated_data['state'],
            "country" : serializer.validated_data['country'],
            "pincode" : serializer.validated_data['pincode'],
            "token": AuthToken.objects.create(user)[1],
            })


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        print(user.id)
        login(request, user)
        print(request.user)
        # window.localStorage.setItem(request.user.token, request.user)
        return super(LoginAPI, self).post(request, format=None)

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
            "address_line1" : serializer.validated_data['address_line1'],
            "address_line2" : serializer.validated_data['address_line2'],
            "area" : serializer.validated_data['area'],
            "city" : serializer.validated_data['city'],
            "state" : serializer.validated_data['state'],
            "country" : serializer.validated_data['country'],
            "pincode" : serializer.validated_data['pincode'],
            "token": AuthToken.objects.create(user)[1]
            })

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

    def post(self, request, format=None):
        serializer = RegisterTestVolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # user = serializer.validated_data['user']
            # login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestVolunteerDetailView(APIView):
    def get_object(self, id):
        try:
            return TestVolunteer.objects.get(id=id)
        except TestVolunteer.DoesNotExist:
            return None

    def get(self, request, id):
        service = self.get_object(id)
        if service == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterTestVolunteerSerializer(service)
        print(len(serializer.data))
        return Response(serializer.data)

    def put(self, request, id):
        service = self.get_object(id)
        serializer = RegisterTestVolunteerSerializer(service, data=request.data)

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

class ElderListView(APIView):
    def get(self, request, format=None):
        elders = Elder.objects.all()
        serializer = RegisterElderSerializer(elders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegisterElderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ElderDetailView(APIView):
    def get_object(self, id):
        try:
            return Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return None

    def get(self, request, id):
        service = self.get_object(id)
        if service == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RegisterElderSerializer(service)
        print(len(serializer.data))
        return Response(serializer.data)

    def put(self, request, id):
        service = self.get_object(id)
        serializer = RegisterElderSerializer(service, data=request.data)

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


class GetVolunteers(APIView):

    def get(self,request,id,format=None):
        try:
            elder = Elder.objects.get(pk=id)
        except Elder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        current_location = elder.location
        print(elder.request_service)
        print(TestVolunteer.objects.filter(services_available=elder.request_service))
        if elder.request_service!=0:
            volunteers = TestVolunteer.objects.filter(location__dwithin=(current_location, 100), availability=True, services_available=elder.request_service
                                              ).annotate(distance=Distance('location', current_location))
        else:
            volunteers = TestVolunteer.objects.filter(location__dwithin=(current_location, 100), availability=True,
                                               ).annotate(distance=Distance('location', current_location))



        serializer = RegisterTestVolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

class RequestServiceAPIView(APIView):

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


def notifications(request):
    # print(phone_no)
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

    phone_no = "6382677337"
    account_sid = 'ACf62e531f2099e445acf3cce250fbdc6a'
    auth_token  = '2ac0f267f0e3eefea063b67013dff017'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Your service is booked",
        to="+91" + phone_no,
        from_="+12512500974",
        )
    print (message.sid)
    data = {'message': "Notifcation successfully sent !"}
    return Response(data, status=status.HTTP_200_OK)

