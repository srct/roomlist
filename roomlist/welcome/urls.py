# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
# imports from your apps
from .views import WelcomeName, WelcomePrivacy, WelcomeMajor, WelcomeSocial


urlpatterns = patterns('',

    # first welcome page
    # let's verify your name and optionally select a gender
    url(r'^1/$',
        WelcomeName.as_view(), name='welcomeName'),

    # thought it made sense to redirect without the number
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('welcomeName'), permanent=True)),

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
