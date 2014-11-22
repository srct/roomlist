from django.conf.urls import patterns, include, url
from housing import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^building/(?P<buildingName>[a-zA-Z]+)$', views.building, name='building'),
)
