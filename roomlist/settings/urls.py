from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # project-level urls
    # url(r'^$', index.html
    # url(r'^$', about.html

    # login and logout
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'index.html'}, name='logout'),

    # app-level urls
    url(r'^housing/', include('housing.urls')),

    # alternate interfaces
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
