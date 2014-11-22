from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

# custom 404
# custom 500

urlpatterns = patterns('',

    # project-level urls
    url(r'^$', TemplateView.as_view( template_name="index.html" ), name='index'),
    # url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    # url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    # url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    # logins
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'index.html'}, name='logout'),

    # app-level urls
    url(r'^housing/', include('housing.urls')),
    url(r'^accounts/', include('accounts.urls')),

    # alternate interfaces
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
