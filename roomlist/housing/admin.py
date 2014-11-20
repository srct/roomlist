from django.contrib import admin
from api.models import Class, Building, Address, Room

# Register your models here.
admin.site.register(Class)
admin.site.register(Building)
admin.site.register(Address)
admin.site.register(Room)
