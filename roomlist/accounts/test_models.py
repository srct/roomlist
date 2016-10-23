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

        self.wilson = Building.objects.create(name='Wilson', neighbourhood='sh',
                                              campus='ff')
        self.wilson_third = Floor.objects.create(building=self.wilson, number=3)
        self.wilson_313 = Room.objects.create(floor=self.wilson_third, number=313)
        self.wilson_307 = Room.objects.create(floor=self.wilson_third, number=307)
        self.wilson_first = Floor.objects.create(building=self.wilson, number=1)
        self.wilson_102 = Room.objects.create(floor=self.wilson_first, number=102)

        self.wilson.save()
        self.wilson_third.save()
        self.wilson_313.save()
        self.wilson_307.save()
        self.wilson_first.save()
        self.wilson_102.save()

        self.harrison = Building.objects.create(name='Harrison', neighbourhood='sh',
                                                campus='ff')
        self.harrison_second = Floor.objects.create(building=self.harrison, number=2)
        self.harrison_207 = Room.objects.create(floor=self.harrison_second, number=207)

        self.harrison.save()
        self.harrison_second.save()
        self.harrison_207.save()

        self.gmason = User.objects.create_user(username='gmason',
                                              first_name='George',
                                              last_name='Mason',
                                              email='gmason@masonlive.gmu.edu',
                                              password='eagle_bank')
        self.tjefferson = User.objects.create_user(username='tjefferson',
                                                   first_name='Thomas',
                                                   last_name='Jefferson',
                                                   email='tjefferson@masonlive.gmu.edu',
                                                   password='louisiana')
        self.dmadison = User.objects.create_user(username='dmadison',
                                                 # note lack of first or last name!
                                                 email='dmadison@masonlive.gmu.edu',
                                                 password='white_house')
        self.jtyler = User.objects.create_user(username='jtyler',
                                               first_name='John',
                                               last_name='Tyler',
                                               email='jtyler@masonlive.gmu.edu',
                                               password='canhaztexas')
        self.hclinton = User.objects.create_user(username='hclinton',
                                                 first_name='Hillary',
                                                 last_name='Clinton',
                                                 email='hildawg@mytotallynotsketchysite.biz',
                                                 password='')
        self.spalin = User.objects.create_user(username='spalin',
                                               first_name='Sarah',
                                               last_name='Palin',
                                               email='grizzlymama@mccain08.com',
                                               password='youbetcha')
        self.cfiorina = User.objects.create_user(username='cfiorina',
                                                 first_name='Carly',
                                                 last_name='Fiorina',
                                                 email='carly@hp.com',
                                                 password='lookatthisface')

        # create_user includes .save()

        self.george = Student.objects.create(user=self.gmason, room=self.wilson_313,
                                             privacy=u'floor')
        self.thomas = Student.objects.create(user=self.tjefferson, room=self.wilson_313,
                                             privacy=u'building')
        self.dolley = Student.objects.create(user=self.dmadison, room=self.harrison_207,
                                             privacy=u'floor')
        self.sarah = Student.objects.create(user=self.spalin, room=self.wilson_307,
                                            privacy=u'building')
        self.hillary = Student.objects.create(user=self.hclinton, room=self.wilson_102,
                                              privacy=u'students')
        self.john = Student.objects.create(user=self.jtyler, room=self.wilson_313,
                                           privacy=u'students')
        self.carly = Student.objects.create(user=self.cfiorina,
                                            privacy=u'students')  # note lack of room!

        self.george.save()
        self.thomas.save()
        self.dolley.save()
        self.sarah.save()
        self.hillary.save()
        self.john.save()
        self.carly.save()

    def test_recent_changes(self):
        self.assertEqual(self.george.recent_changes(), 0)

    def test_totally_done(self):
        # one assert per test?
        self.assertEqual(self.george.totally_done(), False)
        self.george.completedName = True
        self.assertEqual(self.george.totally_done(), False)
        self.george.completedPrivacy = True
        self.assertEqual(self.george.totally_done(), False)
        self.george.completedMajor = True
        self.assertEqual(self.george.totally_done(), False)
        self.george.completedSocial = True
        self.assertEqual(self.george.totally_done(), True)

    def test_get_flag_count(self):
        self.assertEqual(self.george.get_flag_count(), 0)

    def test_get_first_name_or_uname(self):
        self.assertEqual(self.george.get_first_name_or_uname(), 'George')
        self.assertEqual(self.dolley.get_first_name_or_uname(), 'dmadison')

    def test_get_last_name_or_uname(self):
        self.assertEqual(self.george.get_last_name_or_uname(), 'Mason')
        self.assertEqual(self.dolley.get_last_name_or_uname(), 'dmadison')

    def test_get_full_name_or_uname(self):
        self.assertEqual(self.george.get_full_name_or_uname(), 'George Mason')
        self.assertEqual(self.dolley.get_full_name_or_uname(), 'dmadison')

    def test_qset_floor(self):
        students = Student.objects.all().floor()
        self.assertEqual(len(students), 2)
        self.assertTrue(self.george in students)
        self.assertTrue(self.dolley in students)

    def test_qset_building(self):
        students = Student.objects.all().building()
        self.assertEqual(len(students), 2)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.sarah in students)

    def test_qset_students(self):
        students = Student.objects.all().students()
        self.assertEqual(len(students), 3)
        self.assertTrue(self.hillary in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.carly in students)

    def test_qset_building_students(self):
        students = Student.objects.all().building_students()
        self.assertEqual(len(students), 5)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.sarah in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.hillary in students)
        self.assertTrue(self.carly in students)

    def test_qset_floor_building_students(self):
        students = Student.objects.all().floor_building_students()
        self.assertEqual(len(students), 7)
        self.assertTrue(self.george in students)
        self.assertTrue(self.dolley in students)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.sarah in students)
        self.assertTrue(self.hillary in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.carly in students)

    def test_visible_room_same_room(self):
        students = Student.objects.visible(student=self.george, housing=self.wilson_313)
        self.assertEqual(len(students), 3)
        self.assertTrue(self.george in students)  # george's privacy is floor
        self.assertTrue(self.thomas in students)  # thomas's privacy is building
        self.assertTrue(self.john in students)  # john's privacy is students

    def test_visible_room_same_floor(self):
        students = Student.objects.visible(student=self.sarah, housing=self.wilson_313)
        self.assertEqual(len(students), 3)
        self.assertTrue(self.george in students)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.john in students)

    def test_visible_room_different_floor_same_building(self):
        students = Student.objects.visible(student=self.hillary, housing=self.wilson_313)
        self.assertEqual(len(students), 2)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.john in students)

    def test_visible_room_different_building(self):
        students = Student.objects.visible(student=self.dolley, housing=self.wilson_313)
        self.assertEqual(len(students), 1)
        self.assertTrue(self.john in students)

    def test_visible_floor_same_floor(self):
        students = Student.objects.visible(student=self.sarah, housing=self.wilson_third)
        self.assertEqual(len(students), 4)
        self.assertTrue(self.george in students)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.sarah in students)

    def test_visible_floor_different_floor_same_building(self):
        students = Student.objects.visible(student=self.hillary, housing=self.wilson_third)
        self.assertEqual(len(students), 3)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.sarah in students)

    def test_visible_floor_different_building(self):
        students = Student.objects.visible(student=self.dolley, housing=self.wilson_third)
        self.assertEqual(len(students), 1)
        self.assertTrue(self.john in students)

    def test_visible_building_same_building(self):
        students = Student.objects.visible(student=self.hillary, housing=self.wilson)
        self.assertEqual(len(students), 4)
        self.assertTrue(self.thomas in students)
        self.assertTrue(self.john in students)
        self.assertTrue(self.sarah in students)
        self.assertTrue(self.hillary in students)

    def test_visible_building_different_building(self):
        students = Student.objects.visible(student=self.dolley, housing=self.wilson)
        self.assertEqual(len(students), 2)
        self.assertTrue(self.john in students)
        self.assertTrue(self.hillary in students)

    def test_visible_none_room(self):
        students = Student.objects.visible(student=self.carly, housing=self.wilson_313)
        self.assertEqual(len(students), 1)
        self.assertTrue(self.john in students)

    def test_visible_none_floor(self):
        students = Student.objects.visible(student=self.carly, housing=self.wilson_third)
        self.assertEqual(len(students), 1)
        self.assertTrue(self.john in students)

    def test_visible_none_building(self):
        students = Student.objects.visible(student=self.carly, housing=self.wilson)
        self.assertEqual(len(students), 2)
        self.assertTrue(self.john in students)
        self.assertTrue(self.hillary in students)
