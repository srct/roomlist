# standard library imports
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta
# core django imports
from django.shortcuts import resolve_url
# third party imports
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        threshold = 90  # seconds

        assert request.user.is_authenticated()
        if ((request.user.last_login - request.user.date_joined).seconds < threshold):
            url = '/accounts/student/'
        else:
            url = '/accounts/student/'
        return resolve_url(url)
