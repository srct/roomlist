# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import (DetailStudent, UpdateStudent, DetailStudentSettings,
                    DetailCurrentStudent, DetailCurrentStudentSettings, ListMajors,
                    DetailMajor, CreateConfirmation, DeleteConfirmation)
from .adapter import RemoveSocialConfirmationView


urlpatterns = patterns('',

    # social media confirmation
    url(r'', include('allauth.urls')),

    # majors pages
    url(r'^majors/$', ListMajors.as_view(), name='list_majors'),

    url(r'^majors/(?P<slug>[\w-]+)/$',
        DetailMajor.as_view(), name='detail_major'),

    # student profile pages
    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='detail_student'),

    #url(r'^student/$',
        #cache_page(60 * 2)(DetailCurrentStudent.as_view()),
        #name='detailCurrentStudent'),

    # student settings
    url(r'^student/(?P<slug>[\w-]+)/settings/$',
        UpdateStudent.as_view(), name='update_student'),

    url(r'^student/(?P<slug>[\w-]+)/settings/social/remove/$',
        RemoveSocialConfirmationView.as_view(),
        name='remove_social'),

    #url(r'^settings/$',
        #cache_page(4)(DetailCurrentStudentSettings.as_view()),
        #name='currentStudentSettings'),

    # student confirmation pages
    url(r'^student/(?P<student_slug>[\w-]+)/flag/$',
        CreateConfirmation.as_view(), name='createConfirmation'),

    # delete
    url(r'^student/(?P<student_slug>[\w-]+)/flag/(?P<slug>[\w-]+)/$',
        DeleteConfirmation.as_view(), name='deleteConfirmation'),
)
