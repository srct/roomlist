# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import DetailStudent, UpdateStudent, DetailStudentSettings,\
    DetailCurrentStudent, DetailCurrentStudentSettings, ListMajors,\
    DetailMajor, WelcomeName, WelcomePrivacy, WelcomeMajor, WelcomeSocial


urlpatterns = patterns('',

    url(r'', include('allauth.urls')),

    url(r'^majors/$', ListMajors.as_view(), name='list_majors'),

    url(r'^majors/(?P<slug>[\w-]+)/(?P<major>[\w-]+)/$', DetailMajor.as_view(),
        name='detail_major'),

    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='detail_student'),

    url(r'^student/$',
        DetailCurrentStudent.as_view(), name='detailCurrentStudent'),

    url(r'^settings/$',
        DetailCurrentStudentSettings.as_view(), name='currentStudentSettings'),

    url(r'^student/(?P<slug>[\w-]+)/update/$',
        UpdateStudent.as_view(), name='updateStudent'),

    # first welcome page
    # let's verify your name and optionally select a gender
    url(r'^welcome/(?P<slug>[\w-]+)/1/$',
        WelcomeName.as_view(), name='welcomeName'),

    # second welcome page
    # let's set your room and privacy
    url(r'^welcome/(?P<slug>[\w-]+)/2/$',
        WelcomePrivacy.as_view(), name='welcomePrivacy'),

    # third welcome page
    # let's verify your major
    url(r'^welcome/(?P<slug>[\w-]+)/3/$',
        WelcomeMajor.as_view(), name='welcomeMajor'),

    # fourth welcome page
    # set your social media links
    url(r'^welcome/(?P<slug>[\w-]+)/4/$',
        WelcomeSocial.as_view(), name='welcomeSocial'),

)
