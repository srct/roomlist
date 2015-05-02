# core django imports
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()
admin.site.login = login_required(admin.site.login)

handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = patterns('',

    # project-level urls
    url(r'^$', TemplateView.as_view( template_name="index.html" ), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    # app-level urls
    url(r'^housing/', include('housing.urls')),
    url(r'^accounts/', include('accounts.urls')),

    # search
    url(r'^search/', include('haystack.urls'), name='search'),

    # login and logout
    #url(r'^login/', 'cas.views.login', name='login'),
    #url(r'^logout/', 'cas.views.logout', name='logout'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # alternate interfaces
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
