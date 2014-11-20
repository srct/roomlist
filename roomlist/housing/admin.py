from django.contrib import admin
from housing.models import Class, Building, Address, Room

# Register your models here.
admin.site.register(Class)
admin.site.register(Building)
admin.site.register(Address)
admin.site.register(Room)
