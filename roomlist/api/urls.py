# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
# third party imports
from rest_framework.routers import DefaultRouter
# imports from your apps
from .views import BuildingAPI, FloorAPI, RoomAPI


router = DefaultRouter()
router.register(r'buildings', BuildingAPI)
router.register(r'floors', FloorAPI)
router.register(r'rooms', RoomAPI)

urlpatterns = router.urls
