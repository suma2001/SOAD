# from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models as models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class VolunteerAccountManager(BaseUserManager):
    def create_user(self, email, username, phone_number, volunteer_age, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.username = username
        user.phone_number = phone_number
        user.volunteer_age = volunteer_age
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, volunteer_age, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            volunteer_age=volunteer_age,
            password=password,
            phone_number=phone_number,
        )

        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user

class ElderAccountManager(BaseUserManager):
    def create_user(self, email, username, phone_no, elder_age, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.username = username
        user.phone_no = phone_no
        user.elder_age = elder_age
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, elder_age, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            elder_age=elder_age,
            password=password,
            phone_no=phone_no,
        )

        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Address(models.Model):
    address_id = models.AutoField(primary_key=True, auto_created=True)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


class Experience(models.Model):
    experience_id = models.AutoField(primary_key=True, auto_created=True)
    date_of_service = models.DateTimeField(auto_now_add=True)
    type_of_service = models.ForeignKey('Service', on_delete=models.CASCADE)


class Volunteer(AbstractBaseUser):
    profile_id = models.AutoField(primary_key=True, auto_created=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=200, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    volunteer_name = models.CharField(max_length=50, default="name")
    volunteer_age = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(100)])
    phone_number = models.CharField(max_length=13)
    address = models.ForeignKey('Address', on_delete=models.PROTECT, null=True)
    location = models.PointField(null=True)
    biography = models.TextField(default="biography")
    availability = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    services_available = models.ForeignKey('Service', on_delete=models.CASCADE, null=True)
    experience = ArrayField(
        models.IntegerField(), null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'volunteer_age']

    objects = VolunteerAccountManager()

    def __str__(self):
        return str(self.profile_id) + str(self.volunteer_name)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender=settings.AUTH_USER_MODEL, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Elder(AbstractBaseUser):
    elder_id = models.AutoField(primary_key=True, auto_created=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=200, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    elder_name = models.CharField(max_length=50, null=True)
    elder_age = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(110)])
    phone_no = models.CharField(max_length=14)
    location = models.PointField(null=True)
    address = models.ForeignKey('Address', on_delete=models.PROTECT, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_no', 'elder_age']

    objects = ElderAccountManager()

    def __str__(self):
        return str(self.elder_id) + str(self.elder_name)