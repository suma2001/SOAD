from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    CHOICES = (
        (1, 'Elder'),
        (2, "Volunteer"),
    )

    # user_type = models.PositiveSmallIntegerField(choices=CHOICES, default=1)
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)


class Service(models.Model):
    # service_id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Experience(models.Model):
    date_of_service = models.DateTimeField(auto_now_add=True)
    type_of_service = models.ForeignKey('Service', on_delete=models.CASCADE)

# class Address(models.Model):
    # address_id = models.AutoField(primary_key=True, auto_created=True)
    # address_line1 = models.CharField(max_length=150)
    # address_line2 = models.CharField(max_length=150, blank=True)
    # area = models.CharField(max_length=50)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    # pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.city + ", " + self.state

class TestVolunteer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="test_volunteer", null=True)
    volunteer_age = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
    phone_no = models.CharField(max_length=10)
    # address = models.ForeignKey('Address', on_delete=models.PROTECT)
    location = models.PointField(null=True)
    availability = models.BooleanField(default=False)
    services_available = models.ForeignKey('Service', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Elder(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="elder", null=True)
    elder_age = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(110)])
    phone_no = models.CharField(max_length=10)
    location = models.PointField(null=True)
    # address = models.ForeignKey('Address', on_delete=models.PROTECT)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    volunteer_name = models.CharField(max_length=50)
    service_done = models.CharField(max_length=50)
    time = models.DateTimeField()

    class Rating(models.IntegerChoices):
        POOR = 1
        BAD = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5

    rating = models.IntegerField(choices=Rating.choices)
    custom_feedback = models.TextField(blank=True)

    def __str__(self):
        return str(self.volunteer_name) + str(self.time)
        
