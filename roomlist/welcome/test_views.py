# standard library imports
from __future__ import absolute_import, print_function
from datetime import date
# core django imports
from django.test import TestCase
from django.core.urlresolvers import reverse
# imports from your apps
from welcome.views import get_semester
from housing.test_views import RoomlistViewTest


class GetSemesterTest(TestCase):

    def test_summer_month(self):
        created = date(month=7, day=4, year=2016)  # Fourth of July
        semester = get_semester(created)
        self.assertEqual(semester, 'Summer')

    def test_fall_month(self):
        created = date(month=10, day=31, year=2016)  # Halloween
        semester = get_semester(created)
        self.assertEqual(semester, 'Fall')

    def test_spring_month(self):
        created = date(month=1, day=1, year=2016)  # New Years Day
        semester = get_semester(created)
        self.assertEqual(semester, 'Spring')


class WelcomeNameTest(RoomlistViewTest):

    def test_welcome_name_ok(self):
        client = self.client_login()
        response = client.get(reverse('welcomeName'))
        self.assertEqual(response.status_code, 200)


class WelcomePrivacyTest(RoomlistViewTest):

    def test_welcome_privacy_ok(self):
        client = self.client_login()
        response = client.get(reverse('welcomePrivacy'))
        self.assertEqual(response.status_code, 200)


class WelcomeMajorTest(RoomlistViewTest):

    def test_welcome_major_ok(self):
        client = self.client_login()
        response = client.get(reverse('welcomeMajor'))
        self.assertEqual(response.status_code, 200)


class WelcomeSocialTest(RoomlistViewTest):

    def test_welcome_social_ok(self):
        client = self.client_login()
        response = client.get(reverse('welcomeSocial'))
        self.assertEqual(response.status_code, 200)
