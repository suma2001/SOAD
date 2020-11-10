from django.test import TestCase

# Create your tests here.

from .models import Service, Address, Experience, Volunteer, Elder

# Tested
class ServiceTest(TestCase):
    def setUp(self):
        Service.objects.create(name="Pet Walk", description="Taking pets for a walk")

    def test_name(self):
        pet_walk_service = Service.objects.get(name='Pet Walk')
        self.assertEqual(
            pet_walk_service.get_description(), "Pet Walk : Taking pets for a walk")

# Tested
class AddressTest(TestCase):
    def setUp(self):
        Address.objects.create(
            address_id=1, 
            address_line1="Flat no 303, VTS MUkundan Residency",
            address_line2="B/H Archana Restaurant",
            area="Gandhinagar",
            city="Neyveli",
            state="TN",
            country="India",
            pincode=607308
            )

    def test_name(self):
        address = Address.objects.get(address_id=1)
        self.assertEqual(
            address.get_address(), "Neyveli, TN, India")

class ExperienceTest(TestCase):
    def setUp(self):
        Experience.objects.create(
            experience_id=1, 
            date_of_service="10/11/2020",
            type_of_service=1,
            )

# class VolunteerTest(TestCase):
#     def setUp(self):
#         Address.objects.create(
#             address_id=1, 
#             address_line1="Flat no 303, VTS MUkundan Residency",
#             address_line2="B/H Archana Restaurant",
#             area="Gandhinagar",
#             city="Neyveli",
#             state="TamilNadu",
#             country="India",
#             pincode=607308
#         )
#         Volunteer.objects.create(
#             profile_id=1,
#             username="suma",
#             email="suma@gmail.com",
#             password="shreya", 
#             volunteer_name="Suma",
#             volunteer_age=19,
#             phone_number="123456780",
#             # address=Address.objects.get(address_id=1).get_address(),
#             biography="Good",
#             availability=False,
#             # services_available=Service.objects.get(name=),
#             experience=[1]
#         )

#     def test_volunteer(self):
#         volunteer = Volunteer.objects.get(profile_id=1)
#         self.assertEqual(
#             volunteer, "1Suma")


            
