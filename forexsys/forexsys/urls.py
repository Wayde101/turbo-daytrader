from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forexsys.views.home', name='home'),
    # url(r'^forexsys/', include('forexsys.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    # our modules goes here,
    url(r'^$', redirect_to, {'url': '/accounts/profile'}),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^tradesys/$', 'tradesys.views.create_view'),
    url(r'^tradesys/create/$', 'tradesys.views.create_view')
)
