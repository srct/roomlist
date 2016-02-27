# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Major
from .serializers import (BuildingSerializer, FloorSerializer, RoomSerializer,
                          MajorSerializer)


class HousingPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BuildingAPI(ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    pagination_class = HousingPagination


class FloorAPI(ReadOnlyModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    pagination_class = HousingPagination


class RoomAPI(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = HousingPagination


class MajorAPI(ReadOnlyModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
