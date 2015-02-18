from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from autoslug import AutoSlugField

from housing.models import Building, Room, Class

from allauth.socialaccount.models import SocialAccount
import hashlib

class Major(TimeStampedModel):
    name = models.CharField(max_length = 50)
    # I believe the longest is "Government and International Politics"

class StudentQuerySet(models.query.QuerySet):
    def floor(self):
        return self.filter(privacy=FLOOR)

    def building(self):
        return self.filter(privacy=BUILDING)

    def students(self):
        return self.filter(privacy=STUDENTS)

class StudentManager(models.Manager):
    def get_query_set(self):
        return StudentQuerySet(self.model, using=self._db)

    def floor(self):
        return self.get_query_set().floor()

    def building(self):
        return self.get_query_set().building()

    def students(self):
        return self.get_query_set().students()

    def floor_building(self):
        floor = self.get_query_set().floor()
        building = self.get_query_set().building()
        return floor + list(set(building) - set(floor))

    # when a student is not on a floor, but in a building
    def building_students(self):
        building = self.get_query_set().building()
        students = self.get_query_set().students()
        return building + list(set(students) - set(building))
 
    # when a student is on a floor
    def floor_building_students(self):
        floor = self.get_query_set().floor()
        building = self.get_query_set().building()
        students = self.get_query_set().students()

        building_students = building_students()

        return floor + list(set(building_students) - set(floor))

class Student(TimeStampedModel):
    user = models.OneToOneField(User)
    # Django user includes a username, password, email, first name, and last name

    FLOOR = 'floor'
    BUILDING = 'building'
    STUDENTS = 'students'

    PRIVACY_CHOICES = (
        (FLOOR, 'My Floor'),
        (BUILDING, 'My Building'),
        (STUDENTS, 'All Students'),
    )

    privacy = models.CharField(max_length=100, choices=PRIVACY_CHOICES, default=FLOOR)

    room = models.OneToOneField(Room)
    clas = models.OneToOneField(Class)
    major = models.OneToOneField(Major)

    # social media accounts

    slug = AutoSlugField(populate_from='user', unique=True)

    objects = StudentManager()

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user=self.user.id, provider='facebook')
        print("profile_image")

        if len(fb_uid)>0:
            return "http://graph.facebook.com/{}/picture?width=175&height=175".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=175".format(hashlib.md5(self.user.email).hexdigest())


    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
