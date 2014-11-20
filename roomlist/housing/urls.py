from django.conf.urls import patterns, include, url
from roomlist import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^buildings/$', views.buildings, name='buildings'),
    url(r'^building/(?P<buildingName>[a-zA-Z]+)$', views.building, name='building'),
)
