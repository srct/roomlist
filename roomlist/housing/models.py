from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from localflavor.us.models import USStateField

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
    #address = models.ForeignKey('Address')

    PRINCE_WILLIAM = 'pw'
    MASONVALE = 'mv'
    FAIRFAX = 'ff'
    CAMPUS_CHOICES = (
        (NONE, 'None'),
        (PRINCE_WILLIAM, 'Prince William'),
        (MASONVALE, 'mv'),
        (FAIRFAX, 'Fairfax'),
    )

    campus = models.CharField(max_length=100, choices=CAMPUS_CHOICES, default=NONE)

    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.name)

class Room(TimeStampedModel):
    number = models.IntegerField()
    floor = models.IntegerField()
    building = models.ForeignKey('Building')

    slug = AutoSlugField(populate_from='number', unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.building.__str__()+" "+self.number.__str__()

# buildings on campus don't have separate addresses yet
#class Address(TimeStampedModel):
    
#    street = models.CharField(max_length=120)
#    city = models.CharField(max_length=120)
#    state = USStateField()
#    zip_code = models.IntegerField(max_length=5)

#    class Meta: 
#        verbose_name_plural = 'addresses'

#    def __str__(self):              # __unicode__ on Python 2
#        return self.street

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
