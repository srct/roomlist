from django.conf.urls import patterns, include, url
from accounts.views import DetailStudent, UpdateStudent, DetailStudentSettings, DetailCurrentStudent, DetailCurrentStudentSettings, UpdateStudentMajor
from accounts.models import Student

urlpatterns = patterns('',

    url(r'', include('allauth.urls')),

    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(
            model=Student,
            context_object_name='student',
            template_name='detailStudent.html'),
        name='detail_student'),

    url(r'^student/$',
        DetailCurrentStudent.as_view(
            model=Student,
            context_object_name='student',
            template_name='detailStudent.html'),
        name='detailCurrentStudent'),

    url(r'^student/(?P<slug>[\w-]+)/welcome/$',
        UpdateStudent.as_view(
            model=Student,
            template_name="updateStudent.html"),
        name='updateStudent'),

    url(r'^(?P<slug>[\w-]+)/major/$',
        UpdateStudentMajor.as_view(
            model=Student,
            template_name="updateStudentMajor.html"),
        name='updateStudentMajor'),

    url(r'^settings/$',
        DetailCurrentStudentSettings.as_view(
            model=Student,
            context_object_name='student',
            template_name="studentSettings.html"),
        name='currentStudentSettings'),
)
