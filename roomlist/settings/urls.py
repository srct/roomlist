# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
# imports from your apps
from .views import HomePageView
from haystack.views import SearchView

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = patterns('',

    # project-level urls
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    # app-level urls
    url(r'^housing/', include('housing.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^welcome/', include('welcome.urls')),

    # search
    url(r'^search/', login_required(SearchView(), login_url='login'), name='search'),

    # login and logout
    url(r'^login/', 'accounts.views.custom_cas_login', name='login'),
    url(r'^logout/', 'cas.views.logout', name='logout'),

    # url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # alternate interfaces
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
