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
)
