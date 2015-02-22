from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from django.core.urlresolvers import reverse

from housing.models import Building, Room, Class

from allauth.socialaccount.models import SocialAccount
import hashlib

class Major(TimeStampedModel):
    name = models.CharField(max_length = 50)
    # I believe the longest is "Government and International Politics"

    def __str__(self):
        return self.name

class StudentQuerySet(models.query.QuerySet):
    def floor(self):
        return self.filter(privacy='floor')

    def building(self):
        return self.filter(privacy='building')

    def students(self):
        return self.filter(privacy='students')

    # when a student is not on a floor, but in a building
    def building_students(self):
        building = self.building()
        students = self.students()
        return list(building) + list(set(students) - set(building))

    # when a student is on a floor
    def floor_building_students(self):
        floor = self.floor()
        building = self.building()
        students = self.students()

        # using the function above results in UnboundLocalError excpetion
        #building_students = building_students()
        building_students = list(building) + list(set(students) - set(building))

        return list(floor) + list(set(building_students) - set(floor))

class StudentManager(models.Manager):

    # this 'duplication' allows for queryset chaining

    def get_queryset(self):
        return StudentQuerySet(self.model, using=self._db)

    def floor(self):
        return self.get_queryset().floor()

    def building(self):
        return self.get_queryset().building()

    def students(self):
        return self.get_queryset().students()

    def building_students(self):
        return self.get_queryset().building_students()
 
    def floor_building_students(self):
        return self.get_queryset().floor_building_students()

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

    room = models.ForeignKey(Room)
    clas = models.ForeignKey(Class)
    major = models.ForeignKey('Major')

    # social media accounts

    slug = AutoSlugField(populate_from='user', unique=True)

    objects = StudentManager()

    def get_floor(self):
        floor = self.room.floor
        return floor

    def get_building(self):
        building = self.room.floor.building
        return building

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user=self.user.id, provider='facebook')
        print("profile_image")

        if len(fb_uid)>0:
            return "http://graph.facebook.com/{}/picture?width=175&height=175".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=175".format(hashlib.md5(self.user.email).hexdigest())


    def get_absolute_url(self):
        return reverse('detail_student', kwargs={'slug':self.slug})

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
