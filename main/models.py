# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

# Create your models here.

class userinfo(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    nationCode =models.CharField(max_length=60 ,blank=True)
    phoneNum =models.CharField(max_length=30 ,blank=True)
    sex =models.IntegerField(blank=True ,null=True)#1女2男
    birthday =models.DateField(blank=True ,null=True)
    headimg =models.URLField(blank=True)
    lable =models.IntegerField(default=0)#1测试数据
    def __unicode__(self):              # __unicode__ on Python 2
        return self.user

class photo(models.Model):
    testid =models.IntegerField()#测试数据id
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    file =models.FileField()
    filename =models.CharField(max_length=254)
    title =models.CharField(max_length=127 ,blank=True)
    takenTime =models.CharField(max_length=64 ,blank=True)
    place =models.CharField(max_length=254 ,blank=True)
    lt =models.FloatField()
    ltc =models.CharField(max_length=62)
    ln =models.FloatField()
    lnc =models.CharField(max_length=62)
    lable =models.IntegerField(default=0)#1测试数据
    looks =models.IntegerField(default=0)#测试数据
    likes =models.IntegerField(default=0)#测试数据
    favorites =models.IntegerField(default=0)#测试数据
    comments =models.IntegerField(default=0)#测试数据
    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.testid)

#
class photoview(models.Model):
    photoid =models.ForeignKey(photo)
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

class photolike(models.Model):
    photoid =models.ForeignKey(photo)
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

class photofavorite(models.Model):
    photoid =models.ForeignKey(photo)
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

#行程
class course(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    coursename =models.CharField(max_length=254 ,blank=True)
    createtime =models.DateTimeField()
    begindate =models.DateField(blank=True ,null=True)
    begindaycourse =models.ForeignKey(daycourse)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成

class daycourse(models.Model):
    thecourse =models.ForeignKey(course)
    lastday =models.ForeignKey('self' ,null=True)
    nextday =models.ForeignKey('self' ,null=True)
    beginclue =models.ForeignKey(courseclue)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成


class courseclue(models.Model):
    theday =models.ForeignKey(daycourse)
    lastclue =models.ForeignKey('self' ,null=True)
    nextclue =models.ForeignKey('self' ,null=True)
    begincell =models.ForeignKey(coursecell)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成

class coursecell(models.Model):
    begintime =models.TimeField()












