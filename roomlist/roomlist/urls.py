from django.conf.urls import patterns, include, url
from roomlist import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^buildings/$', views.buildings, name='buildings'),
)
