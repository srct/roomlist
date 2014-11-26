from django.db import models
from housing.models import User, Room, Class
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

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

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username
