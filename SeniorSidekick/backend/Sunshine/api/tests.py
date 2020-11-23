import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient

from .models import Address, Experience, Service, TestVolunteer,Elder, Feedback
from .serializers import CustomUserSerializer,ServiceSerializer,UserSerializer,RegisterTestVolunteerSerializer,RegisterElderSerializer,FeedbackSerializer
from django.utils import timezone
import pytz
from django.contrib.auth import get_user_model

User = get_user_model()

class Models_TestCase(TestCase):

    def setUp(self):

        #Service 
        self.name = "Groceries"
        self.description = "Delivering the groceries"
        self.service = Service(name = self.name,description = self.description)
        self.service_old_count = Service.objects.count()

        #Address
        self.address_line1 = "H No: 16-2-398/12,Sai Colony"
        self.address_line2 = "Opp KLM shopping mall"
        self.area = "Jubilee Hills"
        self.city = "Hyderabad"
        self.state = "Telangana"
        self.country = "India"
        self.pincode = "500094"
        self.address = Address(address_line1 = self.address_line1,address_line2 = self.address_line2,
                                area=self.area,city=self.city,state=self.state,country=self.country,
                                pincode = self.pincode)
        self.address_old_count = Address.objects.count()

        #Experience
    
        self.service.save()
        self.type_of_service = self.service
        self.experience = Experience(type_of_service = self.type_of_service)
        self.experience_old_count = Experience.objects.count()

        #Volunteer
        self.experience.save()
        self.address.save()
        self.username = "bugsbunny"
        self.email = "testcase@gmail.com"
        self.name = "test_volunteer"
        self.age = 23
        self.phone_no = "9848000000" 
        self.address = self.address
        self.biography = "I am a test case"
        self.availability  = True
        self.services_available = self.service
        self.location = "SRID=4326;POINT (32.43164062048556 -3.337956638610946)"
        self.password = "hi123@456"
        self.experience = [self.experience.id]

        # user 

        self.user = User.objects.create_user(username=self.username,password = self.password,email = self.email) 

        self.profile = TestVolunteer(user = self.user,volunteer_age = self.age,
                                phone_no=self.phone_no,address = self.address,
                                availability = self.availability,services_available=self.services_available,location=self.location)

        #Elder
        self.elder = Elder(user = self.user,elder_age = self.age,
                                phone_no=self.phone_no,address = self.address,location=self.location)

        #Feedback
        self.time = timezone.now()
        self.rating = 3
        self.custom_feedback = "He is very polite."
        self.feedback = Feedback(volunteer_name = self.name, service_done = self.service.name,time=self.time,
                                rating = self.rating,custom_feedback = self.custom_feedback)
        

    def test_model_can_create_an_address(self):
        new_count = Address.objects.count()
        self.assertEqual(self.address_old_count+1, new_count)
    
    def test_model_can_create_a_service(self):
        new_count = Service.objects.count()
        self.assertEqual(self.service_old_count+1, new_count)

    def test_model_can_create_an_experience(self):
        new_count = Experience.objects.count()
        self.assertEqual(self.experience_old_count+1, new_count)
    
    def test_model_can_create_a_profile(self):
        old_count = TestVolunteer.objects.count()
        self.profile.save()
        new_count = TestVolunteer.objects.count()
        self.assertEqual(old_count+1,new_count)
    
    def test_model_can_create_an_elder(self):
        old_count = Elder.objects.count()
        self.elder.save()
        new_count = Elder.objects.count()
        self.assertEqual(old_count+1,new_count)
    
    def test_model_can_create_a_feedback(self):
        old_count = Feedback.objects.count()
        self.feedback.save()
        new_count = Feedback.objects.count()
        self.assertEqual(old_count+1,new_count)
        

class GetServicesTest(TestCase):

    def setUp(self):
        Service.objects.create(name="Groceries",description="Delivering the groceries")

    def test_services_get_all_api(self):
        response = self.client.get(
            reverse('get_post_services')
        )
        services = Service.objects.all()
        serializer = ServiceSerializer(services,many=True)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)

class GetSingleServiceTest(TestCase):
    def setUp(self):
        self.groceries = Service.objects.create(name="Groceries",description="Delivering the groceries")

    def test_get_valid_single_service(self):
        response = self.client.get(
            reverse('get_delete_update_service',kwargs={'id':self.groceries.id})
        )
        service = Service.objects.get(id=self.groceries.id)
        serializer = ServiceSerializer(service)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_invalid_single_service(self):
        response = self.client.get(
            reverse('get_delete_update_service',kwargs={'id':100})
        )

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class CreateNewServiceTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'name' : "Groceries",
            'description': "Delivering Groceries"
        }

        self.invalid_payload = {
            'name': '',
            'description': "Delivering Groceries"
        }
    
    def test_create_valid_service(self):
        response = self.client.post(
            reverse('get_post_services'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_invalid_service(self):
        response = self.client.post(
            reverse('get_post_services'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleServiceTest(TestCase):

    def setUp(self):
        self.groceries = Service.objects.create(name="Groceries",description="Delivering the groceries")
        print(self.groceries.id)
        self.valid_payload = {
            'name' : "Medicines",
            'description': "Delivering Medicines"
        }

        self.invalid_payload = {
            'name': '',
            'description': "Delivering Medicines"
        }

    def test_valid_update_service(self):
        response = self.client.put(
            reverse('get_delete_update_service', kwargs={'id':self.groceries.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data,self.valid_payload)

    def test_invalid_update_service(self):
        response = self.client.put(
            reverse('get_delete_update_service', kwargs={'id': self.groceries.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleServiceTest(TestCase):

    def setUp(self):
        self.groceries = Service.objects.create(name="Groceries",description="Delivering the groceries")

    def test_valid_delete_service(self):
        response = self.client.delete(
            reverse('get_delete_update_service', kwargs={'id': self.groceries.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_service(self):
        response = self.client.delete(
            reverse('get_delete_update_service', kwargs={'id': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #Profiles

class CreateProfile():
    
    def __init__(self):
        self.location = "SRID=4326;POINT (32.43164062048556 -3.337956638610946)"

        self.service = Service.objects.create(name="Groceries",description="Delivering the groceries")

        self.address = Address.objects.create(address_line1 = "H No: 16-2-398/12,Sai Colony",
                          address_line2 = "Opp KLM shopping mall", area = "Jubilee Hills", 
                           city = "Hyderabad", state = "Telangana", country = "India",pincode = "500094")

        self.experience = Experience(type_of_service=self.service)

        self.user = User.objects.create_user(username="bugsbunny",password = "hello@123",email = "bugs@bunny.com") 

        self.volunteer = TestVolunteer.objects.create(user = self.user,volunteer_age = 23,
                                phone_no="9848000000",address = self.address, availability = True,
                                services_available=self.service,location=self.location)

class Payload():

    def __init__(self):

        service = {
            'name' : "Medicines",
            'description': "Delivering Medicines"
        }
        groceries = Service.objects.create(name="Groceries",description="Delivering the groceries")
        # self.address = {
        #     'address_line1' : "H No: 16-2-398/12,Sai Colony",
        #     'address_line2' : "Opp KLM shopping mall",
        #     'area' : "Jubilee Hills",
        #     'city' : "Hyderabad",
        #     'state' : "Telangana",
        #     'country' : "India",
        #     'pincode' : "500094"
        # }
        addr = Address.objects.create(address_line1 = "H No: 16-2-398/12,Sai Colony",
                          address_line2 = "Opp KLM shopping mall", area = "Jubilee Hills", 
                           city = "Hyderabad", state = "Telangana", country = "India",pincode = "500094")

        exp = Experience.objects.create(type_of_service= groceries)
        print(exp.id)

        
        # find_user = User.objects.filter(username=username)
        # print(find_user)
        # if not find_user:
        #     print("I am in 1")
        #     create_user = User.objects.create_user(username=username,password = password,email = email)
        #     create_user.save()
        # else:
        #     create_user = find_user[0]
        self.user = {'username' : "HorridHenry",
                    'email' : "bugsbunny@gmail.com",
                    'password' : "hi123@456"
                    }
        self.address = addr.pk
        self.volunteer_age = 13
        self.phone_no = "9848000007"
        self.availability = True
        self.services_available = groceries.pk
        self.location = "SRID=4326;POINT (32.43164062048556 -3.337956638610946)"
    
    def payload_with_no_user(self):
        self.user=None
    
    # def payload_with_no_email(self):
    #     self.email = ""

    def payload_with_no_address(self):
        self.address = ""

    # def payload_with_no_name(self):
    #     self.name=""
    
    def payload_with_no_phone_number(self):
        self.phone_no=""

    def payload_with_no_location(self):
        self.location = ""
       
class GetAllProfilesTest(TestCase):
    
    def test_profile_get_all_api(self):
        response = self.client.get(
            reverse('get_post_profiles'))
        # import pdb
        # pdb.set_trace()
        profiles = TestVolunteer.objects.all()
        serializer = RegisterTestVolunteerSerializer(profiles ,many=True)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)
    
    
class GetSingleProfileTest(TestCase):
    def setUp(self):

        self.instance = CreateProfile()
        print("#"+str(self.instance.volunteer.id))

    def test_get_valid_single_profile(self):
        response = self.client.get(
            reverse('get_delete_update_profile',kwargs={'id':self.instance.volunteer.id})
        )
        profile = TestVolunteer.objects.get(id=self.instance.volunteer.id)
        serializer = RegisterTestVolunteerSerializer(profile)

        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK) 

    def test_get_invalid_single_profile(self):
        response = self.client.get(
            reverse('get_delete_update_profile',kwargs={'id':100})
        )

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

class CreateNewProfileTest(TestCase):

    def setUp(self):
        self.instance = Payload()
        # print("$"+str(self.instance))

    def test_create_valid_profile(self):
        response = self.client.post(
            reverse('get_post_profiles'),
            data=json.dumps(self.instance.__dict__),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_profile_with_no_user(self):
        invalid_payload = Payload().payload_with_no_user()
        response = self.client.post(
            reverse('get_post_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_invalid_profile_with_no_email(self):
    #     invalid_payload = Payload().payload_with_no_email()
    #     response = self.client.post(
    #         reverse('get_post_profiles'),
    #         data=json.dumps(invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_profile_with_no_address(self):
        invalid_payload = Payload().payload_with_no_address()
        response = self.client.post(
            reverse('get_post_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_invalid_profile_with_no_name(self):
    #     invalid_payload = Payload().payload_with_no_name()
    #     response = self.client.post(
    #         reverse('get_post_profiles'),
    #         data=json.dumps(invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_profile_with_no_phone_number(self):
        invalid_payload = Payload().payload_with_no_phone_number()
        response = self.client.post(
            reverse('get_post_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_profile_with_no_location(self):
        invalid_payload = Payload().payload_with_no_location()
        response = self.client.post(
            reverse('get_post_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProfileTest(TestCase):

    def setUp(self):
        self.profile = CreateProfile()
        self.instance = Payload()

    def test_valid_update_profile(self):
        response = self.client.put(
            reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
            data=json.dumps(self.instance.__dict__),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data,self.valid_payload)

    def test_update_invalid_profile_with_no_user(self):
        invalid_payload = Payload().payload_with_no_user()
        response = self.client.put(
            reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_update_invalid_profile_with_no_email(self):
    #     invalid_payload = Payload().payload_with_no_email()
    #     response = self.client.put(
    #         reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
    #         data=json.dumps(invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_invalid_profile_with_no_address(self):
        invalid_payload = Payload().payload_with_no_address()
        response = self.client.put(
            reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_invalid_profile_with_no_name(self):
    #     invalid_payload = Payload().payload_with_no_name()
    #     response = self.client.put(
    #         reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
    #         data=json.dumps(invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_invalid_profile_with_no_phone_number(self):
        invalid_payload = Payload().payload_with_no_phone_number()
        response = self.client.put(
            reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_profile_with_no_location(self):
        invalid_payload = Payload().payload_with_no_location()
        response = self.client.put(
            reverse('get_delete_update_profile', kwargs={'id':self.profile.volunteer.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleProfileTest(TestCase):

    def setUp(self):
        self.instance = CreateProfile()

    def test_valid_delete_profile(self):
        response = self.client.delete(
            reverse('get_delete_update_profile', kwargs={'id': self.instance.volunteer.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_profile(self):
        response = self.client.delete(
            reverse('get_delete_update_profile', kwargs={'id': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #Elder Profile

class Create_Elder_Profile():
    
    def __init__(self):
        self.location = "SRID=4326;POINT (32.43164062048556 -3.337956638610946)"

        self.user = User.objects.create_user(username="bugsbunny",password = "hello@123",email = "bugs@bunny.com") 

        self.address = Address.objects.create(address_line1 = "H No: 16-2-398/12,Sai Colony",
                          address_line2 = "Opp KLM shopping mall", area = "Jubilee Hills", 
                           city = "Hyderabad", state = "Telangana", country = "India",pincode = "500094")

        self.elder  = Elder.objects.create(user = self.user,elder_age = 72,phone_no="9848131313",address = self.address,location=self.location)

class Elder_Payload():

    def __init__(self):

        addr = Address.objects.create(address_line1 = "H No: 16-2-398/12,Sai Colony",
                          address_line2 = "Opp KLM shopping mall", area = "Jubilee Hills", 
                           city = "Hyderabad", state = "Telangana", country = "India",pincode = "500094")

        self.user = {'username' : "Doreamon",
                    'email' : "bugsbunny@gmail.com",
                    'password' : "hi123@456"
                    }
        self.address = addr.pk
        self.elder_age = 72
        self.phone_no = "9848000007"
        self.location = "SRID=4326;POINT (32.43164062048556 -3.337956638610946)"
    
    def elder_payload_with_no_user(self):
        self.user=""
    
    def elder_payload_with_no_address(self):
        self.address = ""
    
    def elder_payload_with_no_phone_number(self):
        self.phone_no=""

    def elder_payload_with_no_location(self):
        self.location = ""
       


class GetAll_ElderProfiles_Test(TestCase):
    
    def test_elder_profile_get_all_api(self):
        response = self.client.get(
            reverse('get_post_elder_profiles'))
        # import pdb
        # pdb.set_trace()
        elder_profiles = Elder.objects.all()
        serializer = RegisterElderSerializer(elder_profiles ,many=True)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)
    
    
class GetSingle_ElderProfile_Test(TestCase):
    def setUp(self):

        self.instance = Create_Elder_Profile()

    def test_get_valid_single_elder_profile(self):
        response = self.client.get(
            reverse('get_delete_update_elder_profile',kwargs={'id':self.instance.elder.id})
        )
        profile = Elder.objects.get(id=self.instance.elder.id)
        serializer = RegisterElderSerializer(profile)

        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK) 

    def test_get_invalid_single_elder_profile(self):
        response = self.client.get(
            reverse('get_delete_update_elder_profile',kwargs={'id':100})
        )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

class CreateNew_ElderProfile_Test(TestCase):

    def setUp(self):
        self.instance = Elder_Payload()

    def test_create_valid_elder_profile(self):
        response = self.client.post(
            reverse('get_post_elder_profiles'),
            data=json.dumps(self.instance.__dict__),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_elder_profile_with_no_user(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_user()
        response = self.client.post(
            reverse('get_post_elder_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_elder_profile_with_no_address(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_address()
        response = self.client.post(
            reverse('get_post_elder_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_elder_profile_with_no_phone_number(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_phone_number()
        response = self.client.post(
            reverse('get_post_elder_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_elder_profile_with_no_location(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_location()
        response = self.client.post(
            reverse('get_post_elder_profiles'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingle_ElderProfile_Test(TestCase):

    def setUp(self):
        self.profile = Create_Elder_Profile()
        self.instance = Elder_Payload()

    def test_valid_update_elder_profile(self):
        response = self.client.put(
            reverse('get_delete_update_elder_profile', kwargs={'id':self.profile.elder.id}),
            data=json.dumps(self.instance.__dict__),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data,self.valid_payload)

    def test_update_invalid_elder_profile_with_no_user(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_user()
        response = self.client.put(
            reverse('get_delete_update_elder_profile', kwargs={'id':self.profile.elder.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_invalid_elder_profile_with_no_address(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_address()
        response = self.client.put(
            reverse('get_delete_update_elder_profile', kwargs={'id':self.profile.elder.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_invalid_elder_profile_with_no_phone_number(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_phone_number()
        response = self.client.put(
            reverse('get_delete_update_elder_profile', kwargs={'id':self.profile.elder.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_elder_profile_with_no_location(self):
        invalid_payload = Elder_Payload().elder_payload_with_no_location()
        response = self.client.put(
            reverse('get_delete_update_elder_profile', kwargs={'id':self.profile.elder.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingle_ElderProfile_Test(TestCase):

    def setUp(self):
        self.instance = Create_Elder_Profile()

    def test_valid_delete_elder_profile(self):
        response = self.client.delete(
            reverse('get_delete_update_elder_profile', kwargs={'id': self.instance.elder.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_elder_profile(self):
        response = self.client.delete(
            reverse('get_delete_update_elder_profile', kwargs={'id': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #Feedback

class Feedback_Payload():

    def __init__(self):

        instance = CreateProfile()

        self.volunteer_name = instance.volunteer.user.username
        self.service_done = instance.service.name
        self.time = str(timezone.now())
        self.rating = 4
        self.custom_feedback = "He is down to earth"
        
    def feedback_payload_with_no_volunteer_name(self):
        self.volunteer_name=""
    
    def feedback_payload_with_no_service_name(self):
        self.service_done = ""

    def feedback_payload_with_invalid_rating(self):
        self.rating = 10

class GetAllFeedbacksTest(TestCase):
    
    def test_feedback_get_all_api(self):
        response = self.client.get(
            reverse('get_post_feedback'))
        # import pdb
        # pdb.set_trace()
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks,many=True)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)

class CreateNewFeedbackTest(TestCase):

    def setUp(self):
        self.instance = Feedback_Payload()

    def test_create_valid_feedback(self):
        response = self.client.post(
            reverse('get_post_feedback'),
            data=json.dumps(self.instance.__dict__),
            content_type='application/json'
        )
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_feedback_with_no_volunteer_name(self):
        invalid_payload = self.instance.feedback_payload_with_no_volunteer_name()
        response = self.client.post(
            reverse('get_post_feedback'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_feedback_with_no_service_name(self):
        invalid_payload = self.instance.feedback_payload_with_no_service_name()
        response = self.client.post(
            reverse('get_post_feedback'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_feedback_with_invalid_rating(self):
        invalid_payload = self.instance.feedback_payload_with_invalid_rating()
        response = self.client.post(
            reverse('get_post_feedback'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)