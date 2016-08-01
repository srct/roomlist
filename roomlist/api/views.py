# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Major
from .serializers import (BuildingSerializer, FloorSerializer, RoomSerializer,
                          MajorSerializer)


# pagination class for optional inheritance
class HousingPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


# the actual api views

# housing apis
class BuildingList(ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class BuildingRetrieve(RetrieveAPIView):
    model = Building
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    lookup_field = 'name'


#class FloorList(ListAPIView):
#    queryset = Floor.objects.all()
#    serializer_class = FloorSerializer
#    pagination_class = HousingPagination


class FloorRetrieve(RetrieveAPIView):
    model = Floor
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class RoomRetrieve(RetrieveAPIView):
    model = Room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


#class RoomList(ListAPIView):  # kek
#    queryset = Room.objects.all()
#    serializer_class = RoomSerializer
#    pagination_class = HousingPagination


# major apis
class MajorList(ListAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer


class MajorRetrieve(RetrieveAPIView):
    model = Major
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
