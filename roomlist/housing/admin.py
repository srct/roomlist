from django.contrib import admin
from housing.models import Class, Building, Address, Room, Student

# Register your models here.
admin.site.register(Class)
admin.site.register(Building)
admin.site.register(Address)
admin.site.register(Room)
admin.site.register(Student)
