# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import WelcomeName, WelcomePrivacy, WelcomeMajor, WelcomeSocial


urlpatterns = patterns('',

    # first welcome page
    # let's verify your name and optionally select a gender
    url(r'^$',
        WelcomeName.as_view(), name='welcomeName'),

    # second welcome page
    # let's set your room and privacy
    url(r'^2/$',
        WelcomePrivacy.as_view(), name='welcomePrivacy'),

    # third welcome page
    # let's verify your major
    url(r'^3/$',
        WelcomeMajor.as_view(), name='welcomeMajor'),

    # fourth welcome page
    # set your social media links
    url(r'^4/$',
        WelcomeSocial.as_view(), name='welcomeSocial'),

)
