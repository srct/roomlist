# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.core.serializers import serialize
# third party imports
from rest_framework import serializers
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Major


class BuildingSerializer(serializers.ModelSerializer):

    floors = serializers.SerializerMethodField('get_building_floors')

    def get_building_floors(self, building):
        floors = serialize('json', Floor.objects.filter(building=building),
                           fields=('number'))
        return floors

    class Meta:
        model = Building
        fields = ('name', 'neighbourhood', 'campus')


class FloorSerializer(serializers.ModelSerializer):

    building = serializers.SerializerMethodField('get_building_name')

    def get_building_name(self, floor):
        return floor.building.name

    def get_floor_rooms(self, floor):
        rooms = serialize('json', Room.objects.filter(floor=floor),
                          fields=('number'))
        return rooms

    class Meta:
        model = Floor
        fields = ('number', 'building')


class RoomSerializer(serializers.ModelSerializer):

    building = serializers.SerializerMethodField('get_building_name')
    floor = serializers.SerializerMethodField('get_floor_number')

    def get_building_name(self, room):
        return room.floor.building.name

    def get_floor_number(self, room):
        return room.floor.number

    class Meta:
        model = Room
        fields = ('number', 'floor', 'building')


class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = ('name', )
