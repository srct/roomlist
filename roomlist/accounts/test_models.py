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
        global wilson
        global wilson_third
        global wilson_313

        wilson = Building.objects.create(name='Wilson', neighbourhood='sh', campus='ff')
        wilson_third = Floor.objects.create(building=wilson, number=3)
        wilson_313 = Room.objects.create(floor=wilson_third, number=313)
        wilson_307 = Room.objects.create(floor=wilson_third, number=307)
        wilson_first = Floor.objects.create(building=wilson, number=1)
        wilson_102 = Room.objects.create(floor=wilson_first, number=102)

        wilson.save()
        wilson_third.save()
        wilson_313.save()
        wilson_307.save()
        wilson_first.save()
        wilson_102.save()

        harrison = Building.objects.create(name='Harrison', neighbourhood='sh', campus='ff')
        harrison_second = Floor.objects.create(building=harrison, number=2)
        harrison_207 = Room.objects.create(floor=harrison_second, number=207)

        harrison.save()
        harrison_second.save()
        harrison_207.save()

        gmason = User.objects.create_user(username='gmason',
                                          first_name='George',
                                          last_name='Mason',
                                          email='gmason@masonlive.gmu.edu',
                                          password='eagle_bank')
        tjefferson = User.objects.create_user(username='tjefferson',
                                              first_name='Thomas',
                                              last_name='Jefferson',
                                              email='tjefferson@masonlive.gmu.edu',
                                              password='louisiana')
        dmadison = User.objects.create_user(username='dmadison',
                                            # note lack of first or last name!
                                            email='dmadison@masonlive.gmu.edu',
                                            password='white_house')
        jtyler = User.objects.create_user(username='jtyler',
                                          first_name='John',
                                          last_name='Tyler',
                                          email='jtyler@masonlive.gmu.edu',
                                          password='canhaztexas')
        hclinton = User.objects.create_user(username='hclinton',
                                            first_name='Hillary',
                                            last_name='Clinton',
                                            email='hildawg@mytotallynotsketchysite.biz',
                                            password='')
        spalin = User.objects.create_user(username='spalin',
                                          first_name='Sarah',
                                          last_name='Palin',
                                          email='grizzlymama@mccain08.com',
                                          password='youbetcha')
        cfiorina = User.objects.create_user(username='cfiorina',
                                            first_name='Carly',
                                            last_name='Fiorina',
                                            email='carly@hp.com',
                                            password='lookatthisface')

        # create_user includes .save()

        global george
        global dolley
        global thomas
        global sarah
        global hillary
        global john
        global carly

        george = Student.objects.create(user=gmason, room=wilson_313, privacy=u'floor')
        thomas = Student.objects.create(user=tjefferson, room=wilson_313, privacy=u'building')
        dolley = Student.objects.create(user=dmadison, room=harrison_207, privacy=u'floor')
        sarah = Student.objects.create(user=spalin, room=wilson_307, privacy=u'building')
        hillary = Student.objects.create(user=hclinton, room=wilson_102, privacy=u'students')
        john = Student.objects.create(user=jtyler, room=wilson_313, privacy=u'students')
        carly = Student.objects.create(user=cfiorina, privacy=u'students')  # note lack of room!

        george.save()
        thomas.save()
        dolley.save()
        sarah.save()
        hillary.save()
        john.save()
        carly.save()

    def test_recent_changes(self):
        self.assertEqual(george.recent_changes(), 0)

    def test_totally_done(self):
        # one assert per test?
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
        self.assertEqual(george.get_flag_count(), 0)

    def test_get_first_name_or_uname(self):
        self.assertEqual(george.get_first_name_or_uname(), 'George')
        self.assertEqual(dolley.get_first_name_or_uname(), 'dmadison')

    def test_get_last_name_or_uname(self):
        self.assertEqual(george.get_last_name_or_uname(), 'Mason')
        self.assertEqual(dolley.get_last_name_or_uname(), 'dmadison')

    def test_get_full_name_or_uname(self):
        self.assertEqual(george.get_full_name_or_uname(), 'George Mason')
        self.assertEqual(dolley.get_full_name_or_uname(), 'dmadison')

    def test_qset_floor(self):
        students = Student.objects.all().floor()
        self.assertEqual(len(students), 2)
        self.assertTrue(george in students)
        self.assertTrue(dolley in students)

    def test_qset_building(self):
        students = Student.objects.all().building()
        self.assertEqual(len(students), 2)
        self.assertTrue(thomas in students)
        self.assertTrue(sarah in students)

    def test_qset_students(self):
        students = Student.objects.all().students()
        self.assertEqual(len(students), 3)
        self.assertTrue(hillary in students)
        self.assertTrue(john in students)
        self.assertTrue(carly in students)

    def test_qset_building_students(self):
        students = Student.objects.all().building_students()
        self.assertEqual(len(students), 5)
        self.assertTrue(thomas in students)
        self.assertTrue(sarah in students)
        self.assertTrue(john in students)
        self.assertTrue(hillary in students)
        self.assertTrue(carly in students)

    def test_qset_floor_building_students(self):
        students = Student.objects.all().floor_building_students()
        self.assertEqual(len(students), 7)
        self.assertTrue(george in students)
        self.assertTrue(dolley in students)
        self.assertTrue(thomas in students)
        self.assertTrue(sarah in students)
        self.assertTrue(hillary in students)
        self.assertTrue(john in students)
        self.assertTrue(carly in students)

    def test_visible_room_same_room(self):
        students = Student.objects.visible(student=george, housing=wilson_313)
        self.assertEqual(len(students), 3)
        self.assertTrue(george in students)  # george's privacy is floor
        self.assertTrue(thomas in students)  # thomas's privacy is building
        self.assertTrue(john in students)  # john's privacy is students

    def test_visible_room_same_floor(self):
        students = Student.objects.visible(student=sarah, housing=wilson_313)
        self.assertEqual(len(students), 3)
        self.assertTrue(george in students)
        self.assertTrue(thomas in students)
        self.assertTrue(john in students)

    def test_visible_room_different_floor_same_building(self):
        students = Student.objects.visible(student=hillary, housing=wilson_313)
        self.assertEqual(len(students), 2)
        self.assertTrue(thomas in students)
        self.assertTrue(john in students)

    def test_visible_room_different_building(self):
        students = Student.objects.visible(student=dolley, housing=wilson_313)
        self.assertEqual(len(students), 1)
        self.assertTrue(john in students)

    def test_visible_floor_same_floor(self):
        students = Student.objects.visible(student=sarah, housing=wilson_third)
        self.assertEqual(len(students), 4)
        self.assertTrue(george in students)
        self.assertTrue(thomas in students)
        self.assertTrue(john in students)
        self.assertTrue(sarah in students)

    def test_visible_floor_different_floor_same_building(self):
        students = Student.objects.visible(student=hillary, housing=wilson_third)
        self.assertEqual(len(students), 3)
        self.assertTrue(thomas in students)
        self.assertTrue(john in students)
        self.assertTrue(sarah in students)

    def test_visible_floor_different_building(self):
        students = Student.objects.visible(student=dolley, housing=wilson_third)
        self.assertEqual(len(students), 1)
        self.assertTrue(john in students)

    def test_visible_building_same_building(self):
        students = Student.objects.visible(student=hillary, housing=wilson)
        self.assertEqual(len(students), 4)
        self.assertTrue(thomas in students)
        self.assertTrue(john in students)
        self.assertTrue(sarah in students)
        self.assertTrue(hillary in students)

    def test_visible_building_different_building(self):
        students = Student.objects.visible(student=dolley, housing=wilson)
        self.assertEqual(len(students), 2)
        self.assertTrue(john in students)
        self.assertTrue(hillary in students)

    def test_visible_none_room(self):
        students = Student.objects.visible(student=carly, housing=wilson_313)
        self.assertEqual(len(students), 1)
        self.assertTrue(john in students)

    def test_visible_none_floor(self):
        students = Student.objects.visible(student=carly, housing=wilson_third)
        self.assertEqual(len(students), 1)
        self.assertTrue(john in students)

    def test_visible_none_building(self):
        students = Student.objects.visible(student=carly, housing=wilson)
        self.assertEqual(len(students), 2)
        self.assertTrue(john in students)
        self.assertTrue(hillary in students)
