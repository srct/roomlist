# standard library imports
import hashlib
from datetime import date
# core django imports
from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.text import slugify
# third party imports
from autoslug import AutoSlugField
from randomslugfield import RandomSlugField
from multiselectfield import MultiSelectField
from allauth.socialaccount.models import SocialAccount
# imports from your apps
from housing.models import Room


class Major(TimeStampedModel):
    name = models.CharField(max_length=50)
    # I believe the longest is "Government and International Politics"

    slug = AutoSlugField(populate_from='name', unique=True)

    def first_letter(self):
        return self.name and self.name[0] or ''

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return reverse('detail_major', kwargs={
            'slug': self.slug,
            'major': slugify(self.name),
        })

    class Meta:
        ordering = ['name']


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

    FEMALE = 'female'
    MALE = 'male'
    TRANS = 'trans'
    OTHER = 'other'

    GENDER_CHOICES = (
        (FEMALE, 'female'),
        (MALE, 'male'),
        (TRANS, 'trans'),
        (OTHER, 'other'),
    )

    # selectmultiple in forms
    gender = MultiSelectField(max_length=25, choices=GENDER_CHOICES, blank=True)

    privacy = models.CharField(max_length=100, choices=PRIVACY_CHOICES, default=FLOOR)

    room = models.ForeignKey(Room, null=True, blank=True)
    major = models.ForeignKey('Major', null=True, blank=True)

    current_year = date.today().year
    graduating_year = models.IntegerField(default=current_year, blank=True)

    # from when first logged in through peoplefinder, stored for later
    original_major = models.CharField(max_length=50, blank=True)

    # social media accounts

    # welcome walkthrough completion
    completedName = models.BooleanField(default=False)
    completedPrivacy = models.BooleanField(default=False)
    completedMajor = models.BooleanField(default=False)
    completedSocial = models.BooleanField(default=False)

    slug = AutoSlugField(populate_from='user', unique=True)

    objects = StudentManager()

    # this doesn't take into account superseniors or graduate students or negative values
    # hence private method
    def _get_class(self):
        time_to_graduate = self.graduating_year - self.current_year
        if time_to_graduate >= 4:
            return "freshman"
        elif time_to_graduate == 3:
            return "sophomore"
        elif time_to_graduate == 2:
            return "junior"
        elif time_to_graduate == 1:
            return "freshman"
        else:
            return "magic"

    def get_floor(self):
        try:
            floor = self.room.floor
            return floor
        except AttributeError:
            return None

    def get_building(self):
        try:
            building = self.room.floor.building
            return building
        except AttributeError:
            return None

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user=self.user.id, provider='facebook')
        print("profile_image")

        if len(fb_uid) > 0:
            return "http://graph.facebook.com/{}/picture?width=175&height=175".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=175".format(hashlib.md5(self.user.email).hexdigest())

    def get_absolute_url(self):
        return reverse('detail_student', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['user']

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username

    def __unicode__(self):
        return unicode(self.user.username)

class Confirmation(TimeStampedModel):

    confirmer = models.ForeignKey(Student, related_name='confirmer_set')
    student = models.ForeignKey(Student, related_name='student_set')

    lives_there = models.BooleanField(default=False)
    # is RA?

    slug = RandomSlugField(length=6)

    def __unicode__(self):
        return "%s Flagged %s" % (self.confirmer.user.username, self.student.user.username)
