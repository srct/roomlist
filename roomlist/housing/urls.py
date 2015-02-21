from django.conf.urls import patterns, include, url

from housing.views import ListBuildings, DetailBuilding, DetailFloor, DetailRoom
from housing.models import Building, Floor, Room

urlpatterns = patterns('',

    url(r'^buildings/$',
        ListBuildings.as_view(
            model=Building,
            #paginate_by='10',
            queryset=Building.objects.all(),
            context_object_name='buildings',
            template_name='list_buildings.html'),
        name='list_buildings'),

    url(r'^buildings/(?P<slug>[\w-]+)/$',
        DetailBuilding.as_view(
            model=Building,
            slug_field='slug__iexact',
            context_object_name='building',
            template_name='detail_building.html'),
        name='detail_building'),

    url(r'^buildings/(?P<building>[\w-]+)/(?P<slug>[\w-]+)/$',
        DetailFloor.as_view(
            model=Floor,
            context_object_name='floor',
            template_name='detail_floor.html'),
        name='detail_floor'),

    url(r'^buildings/(?P<building>[\w-]+)/(?P<floor>[\w-]+)/(?P<slug>[\w-]+)/$',
        DetailRoom.as_view(
            model=Room,
            context_object_name='room',
            template_name='detail_room.html'),
        name='detail_room'),
)
