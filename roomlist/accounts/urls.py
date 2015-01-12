from django.conf.urls import patterns, include, url
from accounts.views import DetailStudent, CreateStudent, DetailStudentSettings, DetailCurrentStudent, DetailCurrentStudentSettings
from accounts.models import Student

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #url(r'', include('allauth.urls')),

    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(
            model=Student,
            context_object_name='student',
            template_name='detailStudent.html'),
        name='detailStudent'),

    url(r'^student/$',
        DetailCurrentStudent.as_view(
            model=Student,
            context_object_name='student',
            template_name='detailStudent.html'),
        name='detailCurrentStudent'),

    url(r'^create/$',
        CreateStudent.as_view(
            model=Student,
            template_name="createStudent.html"),
        name='createStudent'),

    url(r'^settings/$',
        DetailCurrentStudentSettings.as_view(
            model=Student,
            context_object_name='student',
            template_name="studentSettings.html"),
        name='currentStudentSettings'),
)
