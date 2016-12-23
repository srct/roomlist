# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import SimpleTestCase, Client
from django.core.urlresolvers import reverse
# imports from your apps
from housing.test_views import RoomlistViewTest


class StaticLoadTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_load(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_about_load(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_load(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)


class LandingTest(RoomlistViewTest):

    def test_landing_ok(self):
        client = self.client_login()
        response = client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
