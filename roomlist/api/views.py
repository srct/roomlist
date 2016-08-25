# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.shortcuts import get_object_or_404
# third party imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
# imports from your apps
from housing.models import Building, Floor, Room
from accounts.models import Major
from .serializers import (BuildingSerializer, BuildingFloorListSerializer,
                          FloorSerializer, RoomSerializer,
                          MajorSerializer)


# pagination class for optional inheritance
class HousingPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MultipleFieldLookupMixin(object):

    # http://www.django-rest-framework.org/api-guide/generic-views/#get_objectself
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        return obj


# the actual api views

# housing apis
class BuildingList(ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class BuildingRetrieve(RetrieveAPIView):
    model = Building
    queryset = Building.objects.all()
    serializer_class = BuildingFloorListSerializer
    lookup_field = 'building_name'


#class FloorList(ListAPIView):
#    queryset = Floor.objects.all()
#    serializer_class = FloorSerializer
#    pagination_class = HousingPagination


class FloorRetrieve(MultipleFieldLookupMixin, RetrieveAPIView):
    model = Floor
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    multiple_lookup_fields = ('building__building_name', 'floor_num')


class RoomRetrieve(MultipleFieldLookupMixin, RetrieveAPIView):
    model = Room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    multiple_lookup_fields = ('room_num', 'floor__floor_num',
                              'floor__building__building_name')


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
    lookup_field = 'slug'


# root urls
class APIRoot(APIView):
    def get(self, request):
        return Response({
            'housing': reverse('api_list_buildings', request=request),
            'majors': reverse('api_list_majors', request=request),
        })
