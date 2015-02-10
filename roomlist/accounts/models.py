from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from autoslug import AutoSlugField

from housing.models import Building, Room, Class

from allauth.socialaccount.models import SocialAccount
import hashlib

# Create your models here.
class Major(TimeStampedModel):
    name = models.CharField(max_length = 50)
    # I believe the longest is "Government and International Politics"

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

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user=self.user.id, provider='facebook')
        print("profile_image")

        if len(fb_uid)>0:
            return "http://graph.facebook.com/{}/picture?width=175&height=175".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=175".format(hashlib.md5(self.user.email).hexdigest())


    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
