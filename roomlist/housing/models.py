from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from django.contrib.auth.models import User

class Building(TimeStampedModel):
    name = models.CharField(max_length=100)

    NONE = 'na'
    AQUIA = 'aq'
    RAPPAHANNOCK = 'ra'
    SHENANDOAH = 'sh'
    NEIGHBOURHOOD_CHOICES = (
        (NONE, 'None'),
        (AQUIA, 'Aquia'),
        (RAPPAHANNOCK, 'Rappahannock'),
        (SHENANDOAH, 'Shenandoah'),
    )

    neighbourhood = models.CharField(max_length=100, choices=NEIGHBOURHOOD_CHOICES,
    default=NONE)
    address = models.ForeignKey('Address')

    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.name)

class Room(TimeStampedModel):
    number = models.IntegerField()
    floor = models.IntegerField()
    bedA = models.CharField(max_length=80)
    bedB = models.CharField(max_length=80, blank=True)
    bedC = models.CharField(max_length=80, blank=True)
    bedD = models.CharField(max_length=80, blank=True)
    building = models.ForeignKey('Building')

    slug = AutoSlugField(populate_from='number', unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.building.__str__()+" "+self.number.__str__()


class Address(TimeStampedModel):
    street = models.CharField(max_length=100)
    zip_code = models.IntegerField(max_length=5)
    state = models.CharField(max_length=2)

    class Meta: 
        verbose_name_plural = 'addresses'

    def __str__(self):              # __unicode__ on Python 2
        return self.street


class Class(TimeStampedModel):
    year_int = models.IntegerField()
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)
    class Meta: 
        verbose_name_plural = 'classes'


    def __str__(self):              # __unicode__ on Python 2
        return str(self.year_int)
