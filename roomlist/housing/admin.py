# core django imports
from django.contrib import admin
# imports from your apps
from .models import Building, Floor, Room


admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
