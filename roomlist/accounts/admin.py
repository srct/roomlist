# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Major

admin.site.register(Major)
admin.site.register(Student)
