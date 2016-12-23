# standard library imports
from __future__ import absolute_import, print_function, unicode_literals
# core django imports
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# imports from your apps
from .models import Student, Major, Confirmation
from housing.models import Room, Floor
from housing.test_views import RoomlistViewTest
from .cas_callbacks import pfinfo


# peoplefinder lookup tests
# these specific examples will eventually have to change
class PeoplefinderTest(TestCase):

    # presently enrolled student who has been added to peoplefinder
    def test_pf_peoplefinder_method(self):
        username = 'dhaynes'
        pf_data = pfinfo(username)
        self.assertEqual(pf_data[0], ['David', 'Haynes'])
        self.assertEqual(pf_data[1], 'CYSE')

    # student no longer in peoplefinder, or who hasn't yet been added
    def test_pf_ldap_method(self):
        username = 'lfaraone'
        pf_data = pfinfo(username)
        self.assertEqual(pf_data[0], ['Luke W', 'Faraone'])
        self.assertEqual(pf_data[1], '')

    # student employees will have their staff info return before their student info
    def test_pf_employee_method(self):
        username = 'nander13'
        pf_data = pfinfo(username)
        self.assertEqual(pf_data[0], ['Nicholas', 'Anderson'])
        self.assertEqual(pf_data[1], 'Undeclared')

    # a name not found for either (should never happen, but gracefully handle anyway)
    def test_pf_dne(self):
        username = 'bobama'
        pf_data = pfinfo(username)
        self.assertEqual(pf_data[0], ['', ''])
        self.assertEqual(pf_data[1], '')


# view tests
class ListMajorsTest(RoomlistViewTest):

    def test_list_majors_ok(self):
        client = Client()
        response = client.get(reverse('list_majors'))
        self.assertEqual(response.status_code, 200)


class DetailMajorTest(RoomlistViewTest):

    def setUp(self):
        major = Major.objects.create(name='Government and International Politics, BA')
        major.save()
        return super(DetailMajorTest, self).setUp()

    def test_list_majors_ok(self):
        client = self.client_login()
        response = client.get(reverse('detail_major',
                                      kwargs={'slug': 'government-and-international-politics-ba'}))
        self.assertEqual(response.status_code, 200)


class DetailStudentTest(RoomlistViewTest):

    def test_detail_student_ok(self):
        client = self.client_login()
        response = client.get(reverse('detail_student',
                                      kwargs={'slug': 'gmason'}))
        self.assertEqual(response.status_code, 200)


class UpdateStudentTest(RoomlistViewTest):

    def test_update_student_ok(self):
        client = self.client_login()
        response = client.get(reverse('update_student',
                                      kwargs={'slug': 'gmason'}))
        self.assertEqual(response.status_code, 200)

    def test_update_student_redirect(self):
        tjefferson = User.objects.create_user(username='tjefferson',
                                              first_name='Thomas',
                                              last_name='Jefferson',
                                              email='tjefferson@masonlive.gmu.edu',
                                              password='louisiana')
        thomas = Student.objects.create(user=tjefferson)

        client = self.client_login()
        response = client.get(reverse('update_student',
                                      kwargs={'slug': 'tjefferson'}))
        # you may not update other people-- we helpfully send you
        # to your own uptate page
        self.assertEqual(response.status_code, 302)

class DeleteStudentTest(RoomlistViewTest):

    def test_delete_student_ok(self):
        client = self.client_login()
        response = client.get(reverse('delete_student',
                                      kwargs={'slug': 'gmason'}))
        # you may delete yourself
        self.assertEqual(response.status_code, 200)

    def test_delete_student_redirect(self):
        tjefferson = User.objects.create_user(username='tjefferson',
                                              first_name='Thomas',
                                              last_name='Jefferson',
                                              email='tjefferson@masonlive.gmu.edu',
                                              password='louisiana')
        thomas = Student.objects.create(user=tjefferson)

        client = self.client_login()
        response = client.get(reverse('delete_student',
                                      kwargs={'slug': 'tjefferson'}))
        # you may not delete other people-- we helpfully send you
        # to your own deletion page
        self.assertEqual(response.status_code, 302)


class RemoveSocialConfirmationTest(RoomlistViewTest):

    def test_remove_social_redirect(self):
        client = self.client_login()
        response = client.get(reverse('remove_social',
                                      kwargs={'slug': 'gmason'}))
        # student does not have any social media acounts set
        self.assertEqual(response.status_code, 302)


class ConfirmationViewTest(RoomlistViewTest):

    def setUp(self):
        # 'extending' the method
        setUp = super(ConfirmationViewTest, self).setUp()

        wilson_third = Floor.objects.get(building__name='Wilson', number='3')
        wilson_307 = Room.objects.create(floor=wilson_third, number='307')
        tjefferson = User.objects.create_user(username='tjefferson',
                                              first_name='Thomas',
                                              last_name='Jefferson',
                                              email='tjefferson@masonlive.gmu.edu',
                                              password='louisiana')
        self.thomas = Student.objects.create(user=tjefferson, room=wilson_307)


class CreateConfirmationTest(ConfirmationViewTest):

    def test_create_confirmation_self(self):
        client = self.client_login()
        response = client.get(reverse('createConfirmation',
                                      kwargs={'confirmer_slug': 'gmason',
                                              'student_slug': 'gmason'}))
        self.assertEqual(response.status_code, 404)

    def test_create_confirmation_same_floor(self):
        client = self.client_login()
        response = client.get(reverse('createConfirmation',
                                      kwargs={'confirmer_slug': 'tjefferson',
                                              'student_slug': 'gmason'}))
        self.assertEqual(response.status_code, 200)

    def test_create_confirmation_already_flagged(self):
        george = Student.objects.get(user__username='gmason')
        confirmation = Confirmation.objects.create(confirmer=george, student=self.thomas)
        confirmation.save()
        # just to verify that, yes, the confirmation was created
        self.assertEqual(self.thomas.get_flag_count(), 1)

        client = self.client_login()
        response = client.get(reverse('createConfirmation',
                                      kwargs={'confirmer_slug': 'gmason',
                                              'student_slug': 'tjefferson'}))
        self.assertEqual(response.status_code, 403)


class DeleteConfirmationTest(ConfirmationViewTest):

    def test_delete_confirmation_ok(self):
        george = Student.objects.get(user__username='gmason')
        confirmation = Confirmation.objects.create(confirmer=george, student=self.thomas)
        confirmation.save()

        client = self.client_login()
        # george accesses his own confirmation
        response = client.get(reverse('deleteConfirmation',
                                      kwargs={'confirmer_slug': 'gmason',
                                              'student_slug': 'tjefferson'}))
        self.assertEqual(response.status_code, 200)

    def test_delete_confirmation_dne(self):
        client = self.client_login()
        response = client.get(reverse('deleteConfirmation',
                                      kwargs={'confirmer_slug': 'gmason',
                                              'student_slug': 'tjefferson'}))
        # try to go to a delete confirmation that does not exist
        self.assertEqual(response.status_code, 404)


    def test_delete_confirmation_other_student(self):
        george = Student.objects.get(user__username='gmason')
        confirmation = Confirmation.objects.create(confirmer=self.thomas, student=george)
        confirmation.save()

        client = self.client_login()
        # george tries to access thomas' confirmation
        response = client.get(reverse('deleteConfirmation',
                                      kwargs={'confirmer_slug': 'tjefferson',
                                              'student_slug': 'gmason'}))
        self.assertEqual(response.status_code, 403)


class SearchViewTest(RoomlistViewTest):

    def test_search_ok(self):
        client = self.client_login()
        response = client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
