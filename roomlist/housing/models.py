# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.core.validators import RegexValidator
# third party imports
from model_utils.models import TimeStampedModel
from randomslugfield import RandomSlugField
from autoslug import AutoSlugField


class Building(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=2, blank=True)
    NONE = 'na'
    AQUIA = 'aq'
    RAPPAHANNOCK = 'ra'
    SHENANDOAH = 'sh'
    NEIGHBOURHOOD_CHOICES = (
        (NONE, '---'),
        (AQUIA, 'Aquia'),
        (RAPPAHANNOCK, 'Rappahannock'),
        (SHENANDOAH, 'Shenandoah'),
    )

    neighbourhood = models.CharField(max_length=100, choices=NEIGHBOURHOOD_CHOICES,
                                     default=NONE)

    # address = models.ForeignKey('Address')

    PRINCE_WILLIAM = 'pw'
    MASONVALE = 'mv'
    FAIRFAX = 'ff'
    CAMPUS_CHOICES = (
        (NONE, '---'),
        (PRINCE_WILLIAM, 'Prince William'),
        (MASONVALE, 'MasonVale'),
        (FAIRFAX, 'Fairfax'),
    )

    campus = models.CharField(max_length=100, choices=CAMPUS_CHOICES, default='ff')

    slug = RandomSlugField(length=6)
    building_name = AutoSlugField(populate_from='name')

    def get_absolute_url(self):
        return reverse('detail_building', kwargs={
            'building': slugify(self.building_name),
        })

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def __unicode__(self):  # __unicode__ on Python 2
        return unicode(self.name)

    def __contains__(self, obj):
        if isinstance(obj, Floor):
            if obj.building == self:  # floor.building == building
                return True
            else:
                return False
        elif isinstance(obj, Room):
            if obj.floor.building == self:  # room.floor.building == building
                return True
            else:
                return False
        else:
            try:
                if obj.room.floor.building == self:  # student.room.floor.building == building
                    return True
                else:
                    return False
            except:
                return False

    class Meta:
        ordering = ['name']


class Floor(TimeStampedModel):
    building = models.ForeignKey('Building')
    number = models.CharField(max_length=1,  # Mason doesn't like tall buildings
                              validators=[RegexValidator(regex='^[0-9]{1}',)])

    slug = RandomSlugField(length=6)

    floor_num = AutoSlugField(populate_from='number',)  # unique_with='building')

    def get_absolute_url(self):
        return reverse('detail_floor', kwargs={
            'building': slugify(self.building.building_name),
            'floor': self.floor_num,
        })

    def __str__(self):  # __unicode__ on Python 2
        return self.building.__str__()+" "+self.number.__str__()

    def __contains__(self, obj):  # circular imports with Student
        if isinstance(obj, Room):
            if obj.floor == self:  # room.floor == room
                return True
            else:
                return False
        else:
            try:
                if obj.room.floor == self:  # student.room.floor == floor
                    return True
                else:
                    return False
            except:
                return False

    class Meta:
        ordering = ['building', 'number']
        unique_together = ('number', 'building')


class Room(TimeStampedModel):
    number = models.CharField(max_length=5,
                              validators=[RegexValidator(regex='^[A-Z]?[0-9]{3,4}',)])

    floor = models.ForeignKey('Floor')

    slug = RandomSlugField(length=6)

    room_num = AutoSlugField(populate_from='number',)  # unique_with='floor')

    def get_wing(self):
        if self.number[0].isalpha():
            return self.number[0]
        else:
            return None

    def get_absolute_url(self):
        return reverse('detail_room', kwargs={
            'floor': self.floor.floor_num,
            'building': slugify(self.floor.building.building_name),
            'room': self.room_num,
        })

    def __str__(self):  # __unicode__ on Python 2
        return self.floor.building.__str__()+" "+self.number.__str__()

    def __contains__(self, obj):  # circular imports with Student
        try:
            if obj.room == self:  # student.room == room
                return True
            else:
                return False
        except:
            return False

    class Meta:
        ordering = ['number']
        unique_together = ('number', 'floor',)
