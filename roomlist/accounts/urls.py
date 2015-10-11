# core django imports
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailStudent, UpdateStudent, DetailStudentSettings,\
    DetailCurrentStudent, DetailCurrentStudentSettings, ListMajors,\
    DetailMajor, WelcomeName, WelcomePrivacy, WelcomeMajor, WelcomeSocial


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

    url(r'^settings/$',
        cache_page(4)(DetailCurrentStudentSettings.as_view()),
        name='currentStudentSettings'),

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
