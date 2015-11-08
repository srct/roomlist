# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Major, Confirmation

admin.site.register(Major)
admin.site.register(Student)
admin.site.register(Confirmation)
