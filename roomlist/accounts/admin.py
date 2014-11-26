from django.contrib import admin
from accounts.models import Student, Major

# Register your models here.
admin.site.register(Major)
admin.site.register(Student)
