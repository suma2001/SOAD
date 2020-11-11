import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient

from .models import Address, Experience, Service, Volunteer
from .serializers import ProfileSerializer, ServiceSerializer

class Models_TestCase(TestCase):

    def setUp(self):

        # self.address_data = {"address_line1" : "H No: 16-2-398/12,Sai Colony",
        #                 "address_line2":"Opp KLM shopping mall", "area" : "Jubilee Hills", 
        #                 "city" :"Hyderabad", "state" : "Telangana",
        #                 "country" : "India", 
        #                 "pincode":"500094"
        #             }

        # self.data = {"email": "testcase@gmail.com","password" : "hello$kanna13", "volunteer_name": "test_volunteer", 
        #         "volunteer_age":"23", "phone_number":"9848000000", "address":address_data,
        #         "biography" :"I am a test case", "availability":"True",
        #         "services_available": "Groceries,Medicines",
        #         "experience": "[0,1]"
        #     }
        # response = self.client.post("api/profiles/add/",data)
        # self.assertEqual(response.status_code,status.HTTP_201_CREATED)

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
        self.volunteer_name = "test_volunteer"
        self.volunteer_age = 23
        self.phone_number = "9848000000" 
        self.address = self.address
        self.biography = "I am a test case"
        self.availability  = "True"
        self.services_available = [self.service.id]
        self.experience = [self.experience.experience_id]
        self.profile = Volunteer(username = self.username,email = self.email,volunteer_name = self.volunteer_name,volunteer_age = self.volunteer_age,
                                phone_number=self.phone_number,address = self.address,biography = self.biography,
                                availability = self.availability,services_available=self.services_available,experience=self.experience)

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
        old_count = Volunteer.objects.count()
        self.profile.save()
        new_count = Volunteer.objects.count()
        self.assertEqual(old_count+1,new_count)
        

# class Service_ViewTestCase(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.services_data = APIClient()
        # self.response = self.client.post(reverse('create_service'),self.services_data,
                                            # format="application/json/")
    
    # def test_services_post_api(self):
    #     self.assertEqual(self.response.status_code,status.HTTP_201_CREATED)
    
    # def test_services_get_api(self):
    #     service = Service.objects.get()
    #     response = self.client.get(
    #         reverse('service_detail',
    #         kwargs = {'pk':service.id}),format = "application/json/")

    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertContains(response,service)
    
    

    

