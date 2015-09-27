# core django imports
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailStudent, UpdateStudent, DetailStudentSettings,\
    DetailCurrentStudent, DetailCurrentStudentSettings, UpdateStudentMajor,\
    ListMajors, DetailMajor


urlpatterns = patterns('',

    url(r'', include('allauth.urls')),

    url(r'^majors/$',
        cache_page(60 * 15)(ListMajors.as_view()),
        name='list_majors'),

    url(r'^majors/(?P<slug>[\w-]+)/(?P<major>[\w-]+)/$',
        cache_page(60 * 2)(DetailMajor.as_view()),
        name='detail_major'),

    url(r'^student/$',
        cache_page(60 * 2)(DetailCurrentStudent.as_view()),
        name='detailCurrentStudent'),

    url(r'^student/(?P<slug>[\w-]+)/$',
        cache_page(60 * 2)(DetailStudent.as_view()),
        name='detail_student'),

    url(r'^student/(?P<slug>[\w-]+)/welcome/$',
        cache_page(60 * 15)(UpdateStudent.as_view()),
        name='updateStudent'),

    url(r'^(?P<slug>[\w-]+)/major/$',
        cache_page(4)(UpdateStudentMajor.as_view()),
        name='updateStudentMajor'),

    url(r'^settings/$',
        cache_page(4)(DetailCurrentStudentSettings.as_view()),
        name='currentStudentSettings'),

)
