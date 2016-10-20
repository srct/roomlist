# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


class ListBuildingsTest(TestCase):

    # tests that the view does not 404
    def test_list_buildings_ok(self):
        # not passing in anything special because it's not login-protected
        client = Client()
        response = client.get(reverse('list_buildings'))
        self.assertEqual(response.status_code, 200)
