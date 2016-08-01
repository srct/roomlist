# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
# imports from your apps
from .views import BuildingList, BuildingRetrieve, FloorRetrieve, RoomRetrieve,\
                   MajorList, MajorRetrieve

# custom routing ftw
# separate out major and building patterns
building_urls = patterns('',
    url(r'^$', BuildingList.as_view(), name='api_list_buildings'),
    url(r'^(?P<name>[\w-]+)/$', BuildingRetrieve.as_view(), name='api_detail_building'),
    url(r'^building/(?P<pk>\d+)/$', FloorRetrieve.as_view(), name='api_detail_floor'),
    # list all the floors still?
    url(r'^building/floor/(?P<pk>\d+)/$', RoomRetrieve.as_view(), name='api_deatil_room'),
    # list all the rooms still?
)

major_urls = patterns('',
    url(r'^$', MajorList.as_view(), name='api_list_majors'),
    url(r'^(?P<pk>\d+)/$', MajorRetrieve.as_view(), name='api_detail_building'),
)

urlpatterns = patterns('',
    url(r'^housing/', include(building_urls)),
    url(r'^majors/', include(major_urls)),
)
