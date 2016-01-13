# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import Client, TestCase
from django.contrib.auth.models import User
# imports from your apps
from accounts.models import Student, Major
from housing.models import Building, Floor, Room


class MajorTest(TestCase):

    def setUp(self):
        Major.objects.create(name='Government and International Politics, BA')

    def test_major_first_letter(self):
        govt = Major.objects.get(name='Government and International Politics, BA')
        self.assertEqual(govt.first_letter(), 'G')


class StudentTest(TestCase):

    def setUp(self):
        gmason = User.objects.create_user(username='gmason',
                                          first_name='George',
                                          last_name='Mason',
                                          email='gmason@masonlive.gmu.edu',
                                          password='eagle_bank')
        dmadison = User.objects.create_user(username='dmadison',
                                            email='dmadison@masonlive.gmu.edu',
                                            password='white_house')
        Student.objects.create(user=gmason)
        Student.objects.create(user=dmadison)

    def test_recent_changes(self):
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.recent_changes(), 0)

    def test_totally_done(self):
        # one assert per test?
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.totally_done(), False)
        george.completedName = True
        self.assertEqual(george.totally_done(), False)
        george.completedPrivacy = True
        self.assertEqual(george.totally_done(), False)
        george.completedMajor = True
        self.assertEqual(george.totally_done(), False)
        george.completedSocial = True
        self.assertEqual(george.totally_done(), True)

    def test_get_flag_count(self):
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.get_flag_count(), 0)

    def test_get_first_name_or_uname(self):
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.get_first_name_or_uname(), 'George')
        dolley = Student.objects.get(user__username='dmadison')
        self.assertEqual(dolley.get_first_name_or_uname(), 'dmadison')

    def test_get_last_name_or_uname(self):
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.get_last_name_or_uname(), 'Mason')
        dolley = Student.objects.get(user__username='dmadison')
        self.assertEqual(dolley.get_last_name_or_uname(), 'dmadison')

    def test_get_full_name_or_uname(self):
        george = Student.objects.get(user__username='gmason')
        self.assertEqual(george.get_full_name_or_uname(), 'George Mason')
        dolley = Student.objects.get(user__username='dmadison')
        self.assertEqual(dolley.get_full_name_or_uname(), 'dmadison')
