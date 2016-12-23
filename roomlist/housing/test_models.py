# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import TestCase
from django.contrib.auth.models import User
# imports from your apps
from accounts.models import Student
from housing.models import Building, Floor, Room


class HousingTest(TestCase):

    def setUp(self):

        self.wilson = Building.objects.create(name='Wilson', neighbourhood='sh',
                                              campus='ff')
        self.wilson_third = Floor.objects.create(building=self.wilson, number=3)
        self.wilson_313 = Room.objects.create(floor=self.wilson_third, number=313)

        self.wilson.save()
        self.wilson_third.save()
        self.wilson_313.save()

        self.harrison = Building.objects.create(name='Harrison', neighbourhood='sh',
                                                campus='ff')
        self.harrison_third = Floor.objects.create(building=self.harrison, number=3)
        self.harrison_313 = Room.objects.create(floor=self.harrison_third, number=313)

        self.harrison.save()
        self.harrison_third.save()
        self.harrison_313.save()

        self.gmason = User.objects.create_user(username='gmason',
                                               first_name='George',
                                               last_name='Mason',
                                               email='gmason@masonlive.gmu.edu',
                                               password='eagle_bank')

        self.george = Student.objects.create(user=self.gmason, room=self.wilson_313)

        self.george.save()


class BuildingTest(HousingTest):

    def test_building_contains_room(self):
        self.assertTrue(self.wilson_313 in self.wilson)
        self.assertFalse(self.harrison_313 in self.wilson)

    def test_building_contains_floor(self):
        self.assertTrue(self.wilson_third in self.wilson)
        self.assertFalse(self.harrison_third in self.wilson)

    def test_building_contains_student(self):
        self.assertTrue(self.george in self.wilson)
        self.assertFalse(self.george in self.harrison)


class FloorTest(HousingTest):

    def test_floor_contains_room(self):
        self.assertTrue(self.wilson_313 in self.wilson_third)
        self.assertFalse(self.harrison_313 in self.wilson_third)

    def test_floor_contains_student(self):
        self.assertTrue(self.george in self.wilson_third)
        self.assertFalse(self.george in self.harrison_third)


class RoomTest(HousingTest):

    def test_room_contains_student(self):
        self.assertTrue(self.george in self.wilson_313)
        self.assertFalse(self.george in self.harrison_313)
