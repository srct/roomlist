# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import BuildingList, BuildingRetrieve, FloorRetrieve, RoomRetrieve,\
                   MajorList, MajorRetrieve, APIRoot

# custom routing ftw

# API v1
# separate out major and building patterns
building_urls = patterns('',
    url(r'^$', BuildingList.as_view(), cache_page(60*60)(name='api_list_buildings')),
    url(r'^(?P<building_name>[\w-]+)/$', BuildingRetrieve.as_view(), cache_page(60*60)(name='api_detail_building')),
    # the naming here and for floors is a little obnoxious
    url(r'^(?P<building__building_name>[\w-]+)/(?P<floor_num>\d+)/$', FloorRetrieve.as_view(), cache_page(60*60)(name='api_detail_floor')),
    # list all the floors still?
    url(r'^(?P<floor__building__building_name>[\w-]+)/(?P<floor__floor_num>\d+)/(?P<room_num>\d+)/$', RoomRetrieve.as_view(), cache_page(60*60)(name='api_detail_room')),
    # list all the rooms still?
)

major_urls = patterns('',
    url(r'^$', MajorList.as_view(), cache_page(60*60)(name='api_list_majors')),
    url(r'^(?P<slug>[\w-]+)/$', MajorRetrieve.as_view(), cache_page(60*60)(name='api_detail_major')),
)

# Added API Caching
urlpatterns = patterns('',
    url(r'^v1/housing/', include(building_urls)),
    url(r'^v1/majors/', include(major_urls)),
    url(r'^v1/$', APIRoot.as_view(), cache_page(60*60)(name='api_root')),
    url(r'^$',  RedirectView.as_view(pattern_name='api_root')),
)

# Subsequent API versions below
