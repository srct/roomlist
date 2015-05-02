# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import ListBuildings, DetailBuilding, DetailFloor, DetailRoom
from .models import Building, Floor, Room


urlpatterns = patterns('',

    url(r'^$',
        ListBuildings.as_view(), name='list_buildings'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/$',
        DetailBuilding.as_view(), name='detail_building'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/(?P<floor>[\w-]+)/$',
        DetailFloor.as_view(), name='detail_floor'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/(?P<floor>[\w-]+)/(?P<room>[\w-]+)/$',
        DetailRoom.as_view(), name='detail_room'),

)
