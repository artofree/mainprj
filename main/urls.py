# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from main import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
)
