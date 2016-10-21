# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Student


class HousingViewTest(TestCase):
    def setUp(self):
        wilson = Building.objects.create(name='Wilson', neighbourhood='sh', campus='ff')
        wilson_third = Floor.objects.create(building=wilson, number=3)
        wilson_313 = Room.objects.create(floor=wilson_third, number=313)

        wilson.save()
        wilson_third.save()
        wilson_313.save()

        user = User.objects.create_user(username='gmason',
                                        first_name='George',
                                        last_name='Mason',
                                        email='gmason@masonlive.gmu.edu',
                                        password='eagle_bank')
        # .create_user() includes .save()

        gmason = Student.objects.create(user=user)
        gmason.save()


class ListBuildingsTest(TestCase):

    # tests that the view does not 404
    def test_list_buildings_ok(self):
        # not passing in anything special because it's not login-protected
        client = Client()
        response = client.get(reverse('list_buildings'))
        self.assertEqual(response.status_code, 200)


class DetailBuildingTest(HousingViewTest):

    def test_detail_building_ok(self):
        client = Client()
        gmason = User.objects.get(username='gmason')
        # this is only for testing purposes; we're using CAS for auth
        client.login(username='gmason', password='eagle_bank')
        response = client.get(reverse('detail_building',
                                      kwargs = {'building': 'wilson'}))
        self.assertEqual(response.status_code, 200)


class DetailFloorTest(HousingViewTest):

    def test_detail_floor_ok(self):
        client = Client()
        gmason = User.objects.get(username='gmason')
        client.login(username='gmason', password='eagle_bank')
        response = client.get(reverse('detail_floor',
                                      kwargs = {'building': 'wilson',
                                                'floor': '3'}))
        self.assertEqual(response.status_code, 200)


class DetailRoomTest(HousingViewTest):

    def test_detail_room_ok(self):
        client = Client()
        gmason = User.objects.get(username='gmason')
        client.login(username='gmason', password='eagle_bank')
        response = client.get(reverse('detail_room',
                                      kwargs = {'building': 'wilson',
                                                'floor': '3',
                                                'room': '313'}))
        self.assertEqual(response.status_code, 200)
