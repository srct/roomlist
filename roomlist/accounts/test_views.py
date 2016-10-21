# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# imports from your apps
from .models import Student, Major, Confirmation
from housing.models import Room, Floor
from housing.test_views import RoomlistViewTest


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


class DeleteStudentTest(RoomlistViewTest):

    def test_delete_student_ok(self):
        client = self.client_login()
        response = client.get(reverse('delete_student',
                                      kwargs={'slug': 'gmason'}))
        self.assertEqual(response.status_code, 200)


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
        thomas = Student.objects.create(user=tjefferson, room=wilson_307)


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


class DeleteConfirmationTest(ConfirmationViewTest):

    def setUp(self):
        setUp = super(DeleteConfirmationTest, self).setUp()

        thomas = Student.objects.get(user__username='tjefferson')
        george = Student.objects.get(user__username='gmason')
        confirmation = Confirmation.objects.create(confirmer=george, student=thomas)
        confirmation.save()

    def test_delete_confirmation_ok(self):
        client = self.client_login()
        response = client.get(reverse('deleteConfirmation',
                                      kwargs={'confirmer_slug': 'gmason',
                                              'student_slug': 'tjefferson'}))
        self.assertEqual(response.status_code, 200)
