# core django imports
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import ListBuildings, DetailBuilding, DetailFloor, DetailRoom


urlpatterns = patterns('',

    url(r'^$',
        ListBuildings.as_view(), name='list_buildings'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/$',
        cache_page(60 * 15)(DetailBuilding.as_view()),
        name='detail_building'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/(?P<floor>[\w-]+)/$',
        cache_page(60 * 2)(DetailFloor.as_view()),
        name='detail_floor'),

    url(r'^(?P<slug>[\w-]+)/(?P<building>[\w-]+)/(?P<floor>[\w-]+)/(?P<room>[\w-]+)/$',
        cache_page(60 * 2)(DetailRoom.as_view()),
        name='detail_room'),

)
