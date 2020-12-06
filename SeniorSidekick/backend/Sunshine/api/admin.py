from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Service)
# admin.site.register(Address)
admin.site.register(TestVolunteer, OSMGeoAdmin)
admin.site.register(Elder, OSMGeoAdmin)
admin.site.register(Feedback)
