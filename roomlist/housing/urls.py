# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import url
# imports from your apps
from .views import ListBuildings, DetailBuilding, DetailFloor, DetailRoom


urlpatterns = [

    url(r'^$', ListBuildings.as_view(), name='list_buildings'),

    url(r'^(?P<building>[\w-]+)/$',
        DetailBuilding.as_view(), name='detail_building'),

    url(r'^(?P<building>[\w-]+)/(?P<floor>[\w-]+)/$',
        DetailFloor.as_view(), name='detail_floor'),

    url(r'^(?P<building>[\w-]+)/(?P<floor>[\w-]+)/(?P<room>[\w-]+)/$',
        DetailRoom.as_view(), name='detail_room'),

]
