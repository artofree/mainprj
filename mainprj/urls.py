# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mainprj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^explore/', include('explore.urls', namespace="explore")),
    url(r'^main/', include('main.urls', namespace="main")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('main.urls', namespace="main")),
    #url(r'^photo/small/(?P<photofile>\d+).jpg$', 'main.views.getsmallphoto', name='getsmallphoto'),
    url(r'^photolayer/(?P<zoom>(\d){1,2}),(?P<tilex>(\d)+),(?P<tiley>(\d)+).jpg$', 'explore.views.getphotolayer', name='getphotolayer'),
    #url(r'^accounts/', include('registration_email.backends.default.urls')),
)
