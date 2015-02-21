from django.contrib import admin
from housing.models import Class, Building, Floor, Room

# Register your models here.
admin.site.register(Class)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
