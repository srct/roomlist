# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework import serializers
from rest_framework.reverse import reverse
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Major


# we're not using DRF's default hyperlinks because we need to look up multiple fields
class FloorURLSerializer(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url = reverse(view_name,
                      kwargs={'building__building_name': obj.building.building_name,
                              'floor_num': obj.number},
                      request=request,
                      format=format)
        return url


class RoomURLSerializer(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url = reverse(view_name,
                      kwargs={'floor__building__building_name': obj.floor.building.building_name,
                              'floor__floor_num': obj.floor.number,
                              'room_num': obj.number},
                      request=request,
                      format=format)
        return url


# these serializers are both used as fields for other serialzers
class FloorNumSerializer(serializers.ModelSerializer):

    url = FloorURLSerializer(view_name='api_detail_floor')

    class Meta:
        model = Floor
        fields = ('url', 'number')


class RoomNumSerializer(serializers.ModelSerializer):

    url = RoomURLSerializer(view_name='api_detail_room')

    class Meta:
        model = Room
        fields = ('url', 'number')


# the main serializers
class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('url', 'name', 'neighbourhood', 'campus',)
        extra_kwargs = {
            'url': {'view_name': 'api_detail_building', 'lookup_field': 'building_name'}
        }


class BuildingFloorListSerializer(serializers.ModelSerializer):
    floors = FloorNumSerializer(source='floor_set', many=True)

    class Meta:
        model = Building
        fields = ('name', 'neighbourhood', 'campus', 'floors')


class FloorSerializer(serializers.ModelSerializer):

    building = serializers.SerializerMethodField('get_building_name')

    rooms = RoomNumSerializer(source='room_set', many=True)

    def get_building_name(self, floor):
        return floor.building.name

    class Meta:
        model = Floor
        fields = ('number', 'building', 'rooms')


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
