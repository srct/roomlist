from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

#from localflavor.us.models import USStateField
from django.core.urlresolvers import reverse

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
        (MASONVALE, 'MasonVale'),
        (FAIRFAX, 'Fairfax'),
    )

    campus = models.CharField(max_length=100, choices=CAMPUS_CHOICES, default=NONE)

    slug = AutoSlugField(populate_from='name', unique=True)

    def get_absolute_url(self):
        return reverse('detail_building', kwargs={'slug':self.slug})

    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def __unicode__(self):              # __unicode__ on Python 2
        return unicode(self.name)
    
    class Meta:
        ordering = ['name']

class Floor(TimeStampedModel):
    building = models.ForeignKey('Building')
    number = models.IntegerField()

    slug = AutoSlugField(populate_from='number',# unique_with='building')
        unique=True)

    def get_absolute_url(self):
        return reverse('detail_floor', kwargs={
            'slug':self.slug,
            'building':self.building.slug,
        })

    def __str__(self):              # __unicode__ on Python 2
        return self.building.__str__()+" "+self.number.__str__()

    class Meta:
        ordering = ['building', 'number']

class Room(TimeStampedModel):
    number = models.IntegerField()
    floor = models.ForeignKey('Floor')

    slug = AutoSlugField(populate_from='number',# unique_with='floor')
        unique=True)

    def get_absolute_url(self):
        return reverse('detail_room', kwargs={
            'slug':self.slug,
            'floor':self.floor.slug,
            'building':self.floor.building.slug,
        })

    def __str__(self):              # __unicode__ on Python 2
        return self.floor.building.__str__()+" "+self.number.__str__()

    class Meta:
        ordering = ['number']

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
    OTHER = 'OR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (OTHER, 'Other'),
    )
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)
    class Meta: 
        verbose_name_plural = 'classes'

    def __str__(self):              # __unicode__ on Python 2
        return str(self.year_int)
