# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework.viewsets import ReadOnlyModelViewSet
# imports from your apps
from housing.models import Building, Floor, Room
from .serializers import BuildingSerializer, FloorSerializer, RoomSerializer


class BuildingAPI(ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class FloorAPI(ReadOnlyModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class RoomAPI(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
