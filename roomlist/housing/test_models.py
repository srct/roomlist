# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import TestCase
from django.contrib.auth.models import User
# imports from your apps
from accounts.models import Student
from housing.models import Building, Floor, Room


class BuildingTest(TestCase):

    def setUp(self):
        global wilson
        global wilson_third
        global wilson_313

        wilson = Building.objects.create(name='Wilson', neighbourhood='sh', campus='ff')
        wilson_third = Floor.objects.create(building=wilson, number=3)
        wilson_313 = Room.objects.create(floor=wilson_third, number=313)

        wilson.save()
        wilson_third.save()
        wilson_313.save()

        gmason = User.objects.create_user(username='gmason',
                                          first_name='George',
                                          last_name='Mason',
                                          email='gmason@masonlive.gmu.edu',
                                          password='eagle_bank')

        global george

        george = Student.objects.create(user=gmason, room=wilson_313)

        george.save()

    def test_building_contains_room(self):
        self.assertTrue(wilson_313 in wilson)

    def test_building_contains_floor(self):
        self.assertTrue(wilson_third in wilson)

    def test_building_contains_student(self):
        self.assertTrue(george in wilson)


class FloorTest(TestCase):

    def test_floor_contains_room(self):
        self.assertTrue(wilson_313 in wilson_third)

    def test_floor_contains_student(self):
        self.assertTrue(george in wilson_third)


class RoomTest(TestCase):

    def test_room_contains_student(self):
        self.assertTrue(george in wilson_313)
