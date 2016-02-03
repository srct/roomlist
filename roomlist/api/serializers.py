# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework import serializers
# imports from your apps
from housing.models import Building, Floor, Room


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('name', 'neighbourhood', 'campus')


class FloorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Floor
        fields = ('number', )


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('number', )
