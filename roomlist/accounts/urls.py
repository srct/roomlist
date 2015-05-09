# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import DetailStudent, UpdateStudent, DetailStudentSettings,\
    DetailCurrentStudent, DetailCurrentStudentSettings, UpdateStudentMajor


urlpatterns = patterns('',

    url(r'', include('allauth.urls')),

    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='detail_student'),

    url(r'^student/$',
        DetailCurrentStudent.as_view(), name='detailCurrentStudent'),

    url(r'^student/(?P<slug>[\w-]+)/welcome/$',
        UpdateStudent.as_view(), name='updateStudent'),

    url(r'^(?P<slug>[\w-]+)/major/$',
        UpdateStudentMajor.as_view(), name='updateStudentMajor'),

    url(r'^settings/$',
        DetailCurrentStudentSettings.as_view(), name='currentStudentSettings'),

)
