from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # project-level urls
    url(r'^$', TemplateView.as_view( template_name="index.html" ), name='index'),
    # url(r'^$', about.html

    # app-level urls
    url(r'^housing/', include('housing.urls')),
    url(r'^accounts/', include('accounts.urls')),

    # alternate interfaces
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
