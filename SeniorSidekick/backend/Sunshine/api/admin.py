from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
admin.site.register(Service)
admin.site.register(Address)
admin.site.register(Experience)
admin.site.register(Elder, OSMGeoAdmin)
admin.site.register(Volunteer, OSMGeoAdmin)

# @admin.register(Elder)
# class ElderAdmin(OSMGeoAdmin):
#     list_display = ('email', 'password', 'elder_name', 'elder_age', 'phone_no',
#                     'address', 'location')


# @admin.register(Volunteer)
# class VolunteerAdmin(OSMGeoAdmin):
#     list_display = ('email', 'password', 'volunteer_name', 'volunteer_age', 'phone_number',
#                     'address', 'location', 'biography', 'availability', 'services_available',
#                     'experience')
