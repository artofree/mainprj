# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from explore import views

urlpatterns = patterns('',
    url(r'^(?P<rqst>(-)?(\d){1,2}(.)(\d)+(,)(-)?(\d){1,3}(.)(\d)+(,)(\d){1,2})$', views.index, name='index'),
    url(r'^getPhotos$', views.getPhotos, name='getPhotos'),
    url(r'^getPhotoInfo$', views.getPhotoInfo, name='getPhotoInfo'),
    url(r'^.*$', views.rdrct, name='rdrct'),
)
