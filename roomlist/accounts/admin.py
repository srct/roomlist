# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Major, Confirmation


class StudentAdmin(admin.ModelAdmin):
    list_display = ("get_name", "room", "privacy", "get_first_major", "created")

    def get_name(self, student):
        return student.get_full_name_or_uname()

    get_name.short_description = 'Name'
    get_name.admin_order_field = 'user__username'  # ordering by callables is hard

    # We cannot use a manytomanyfield as a field in the list, so we're getting the first
    # major. If we need to see a student's second major, we can just click the student.
    # This covers nearly all students, who will have only one major.
    def get_first_major(self, student):
        return student.major.first()

    get_first_major.short_description = 'Major'
    # we're not going to give the option to sort by major for now


class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "get_major_num", )

    def get_major_num(self, major):
        student_num = Student.objects.filter(major=major).count()
        return student_num
    get_major_num.short_description = 'Number of Students'
    # ordering is hard (ditto above; rewrite queryset :-/)

admin.site.register(Student, StudentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Confirmation)
