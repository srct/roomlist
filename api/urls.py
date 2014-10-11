from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^building/(?P<building>.+)/(?P<room_number>\d+)', views.room, name='room'),
    url(r'^building/(?P<building>[a-zA-Z]+)', views.building, name='building'),
    url(r'^buildings/', views.buildings_list, name='buildings_list'),
)
