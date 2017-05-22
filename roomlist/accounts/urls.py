# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import url, include
# imports from your apps
from .views import (DetailStudent, UpdateStudent, DeleteStudent,
                    ListMajors, DetailMajor,
                    CreateConfirmation, DeleteConfirmation)
from .adapter import RemoveSocialConfirmationView


urlpatterns = [

    # social media confirmation
    url(r'', include('allauth.urls')),

    # majors pages
    url(r'^majors/$', ListMajors.as_view(), name='list_majors'),

    url(r'^majors/(?P<slug>[\w-]+)/$',
        DetailMajor.as_view(), name='detail_major'),

    # student profile pages
    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='detail_student'),

    # student settings
    url(r'^student/(?P<slug>[\w-]+)/settings/$',
        UpdateStudent.as_view(), name='update_student'),

    # delete student account
    url(r'^student/(?P<slug>[\w-]+)/delete/$',
        DeleteStudent.as_view(), name='delete_student'),

    # custom allauth page to disconnect a social media account
    url(r'^student/(?P<slug>[\w-]+)/settings/social/remove/$',
        RemoveSocialConfirmationView.as_view(),
        name='remove_social'),

    # student confirmation pages
    url(r'^student/(?P<confirmer_slug>[\w-]+)/flag/(?P<student_slug>[\w-]+)/$',
        CreateConfirmation.as_view(), name='createConfirmation'),

    # delete confirmation
    url(r'^student/(?P<confirmer_slug>[\w-]+)/flag/(?P<student_slug>[\w-]+)/remove/$',
        DeleteConfirmation.as_view(), name='deleteConfirmation'),
]
