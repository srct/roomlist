# standard library imports
from __future__ import absolute_import, print_function
from datetime import date
# core django imports
from django.test import TestCase
# imports from your apps
from welcome.views import get_semester

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
