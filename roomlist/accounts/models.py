from django.db import models
from housing.models import User, Room, Class
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from allauth.socialaccount.models import SocialAccount
import hashlib

# Create your models here.
class Major(TimeStampedModel):
    major_name = models.CharField(max_length = 30)

class Student(TimeStampedModel):
    user = models.OneToOneField(User)
    # Django user includes a username, password, email, first name, and last name
    room = models.OneToOneField(Room)
    clas = models.OneToOneField(Class)
    major = models.OneToOneField(Major)
    # major = models.

    # social media accounts

    slug = AutoSlugField(populate_from='user', unique=True)

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

            return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())


    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
