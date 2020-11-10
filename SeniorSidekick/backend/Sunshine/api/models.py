from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_description(self):
        return self.name + " : " + self.description

class Address(models.Model):
    address_id = models.IntegerField(primary_key=True,auto_created=True)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length = 150,blank= True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    pincode = models.BigIntegerField()

    def get_address(self):
        return self.city + ", " + self.state + ", " + self.country

class Experience(models.Model):
    experience_id = models.IntegerField(primary_key=True,auto_created=True)
    date_of_service = models.DateTimeField(auto_now_add=True)
    type_of_service = models.ForeignKey('Service',on_delete=models.CASCADE)

class Volunteer(models.Model):
    profile_id = models.IntegerField(primary_key=True,auto_created=True)
    username = models.CharField(max_length=100, default=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    volunteer_name = models.CharField(max_length=50)
    volunteer_age = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
    phone_number = models.CharField(max_length=13)
    address = models.ForeignKey('Address',on_delete=models.PROTECT)
    biography = models.TextField()
    availability = models.BooleanField(default=False)
    services_available = models.ForeignKey('Service',on_delete=models.CASCADE)
    experience = ArrayField(
            models.IntegerField()
    )
    def __str__(self):
        return str(self.profile_id)+str(self.volunteer_name)

class Elder(models.Model):
    elder_id = models.AutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=100, default=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    elder_name = models.CharField(max_length=50)
    elder_age = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(110)])
    phone_no = models.CharField(max_length=14)
    # location = models.PointField(default=None)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.elder_id) + str(self.elder_name)


 


