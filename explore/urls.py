# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from explore import views

urlpatterns = patterns('',
    url(r'^(?P<rqst>(-)?(\d){1,2}(.)(\d)+(,)(-)?(\d){1,3}(.)(\d)+(,)(\d){1,2})$', views.index, name='index'),
    url(r'^getPhotoInfo$', views.getPhotoInfo, name='getPhotoInfo'),
    url(r'^getPhotoList$', views.getPhotoList, name='getPhotoList'),
    url(r'^genRequest$', views.genRequest, name='genRequest'),
    url(r'^.*$', views.rdrct, name='rdrct'),
)
