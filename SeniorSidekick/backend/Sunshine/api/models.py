# from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models as models
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Service(models.Model):
    # service_id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Address(models.Model):
    # address_id = models.AutoField(primary_key=True, auto_created=True)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


class Experience(models.Model):
    date_of_service = models.DateTimeField(auto_now_add=True)
    type_of_service = models.ForeignKey('Service', on_delete=models.CASCADE)


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


class Volunteer(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    # volunteer_id = models.AutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    volunteer_age = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
    phone_no = models.CharField(max_length=10)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)
    location = models.PointField(default=None)
    biography = models.TextField(blank=True)
    availability = models.BooleanField(default=False)
    services_available = models.ForeignKey('Service', on_delete=models.CASCADE)
    experience = ArrayField(
        models.IntegerField()
    )

    # USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.username)


# @receiver(post_save,sender=User)
# def update_volunteer_signal(sender,instance,created,**kwargs):
#     if created:
#         Volunteer.objects.create(user=instance)
#     instance.profile.save()

class Elder(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    # elder_id = models.AutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    elder_age = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(110)])
    phone_no = models.CharField(max_length=10)
    location = models.PointField(default=None)
    address = models.ForeignKey('Address', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.username)

# @receiver(post_save,sender=User)
# def update_elder_signal(sender,instance,created,**kwargs):
#     if created:
#         Elder.objects.create(user=instance)
#     instance.elder.save()