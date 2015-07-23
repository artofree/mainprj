# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.

class Userinfo(models.Model):
    user =models.OneToOneField(settings.AUTH_USER_MODEL)
    nationCode =models.CharField(max_length=60 ,blank=True)
    phoneNum =models.CharField(max_length=30 ,blank=True)
    sex =models.IntegerField(blank=True ,null=True)#1女2男
    birthday =models.DateField(blank=True ,null=True)
    headimg =models.URLField(blank=True)
    lable =models.IntegerField(default=0)#1测试数据
    def __str__(self):              # __unicode__ on Python 2
        return self.user

class Point(models.Model):
    lt =models.FloatField()
    ln =models.FloatField()
    class Meta:
        abstract =True

    views = GenericRelation('Views',content_type_field = 'pointtype',object_id_field = 'pointid')
    likes = GenericRelation('Likes',content_type_field = 'pointtype',object_id_field = 'pointid')
    favorites = GenericRelation('Favorites',content_type_field = 'pointtype',object_id_field = 'pointid')
    coursecells = GenericRelation('Coursecell',content_type_field = 'pointtype',object_id_field = 'pointid')



class Photo(Point):
    testid =models.IntegerField()#测试数据id
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    file =models.CharField(max_length=254 ,blank=True)
    title =models.CharField(max_length=127 ,blank=True)
    takenTime =models.CharField(max_length=64 ,blank=True)
    place =models.CharField(max_length=254 ,blank=True)
    lable =models.IntegerField(default=0)#1测试数据
    tlooks =models.IntegerField(default=0)#测试数据
    tlikes =models.IntegerField(default=0)#测试数据
    tfavorites =models.IntegerField(default=0)#测试数据
    tcomments =models.IntegerField(default=0)#测试数据
    def __str__(self):              # __unicode__ on Python 2
        return str(self.testid)

#
class Views(models.Model):
    pointtype =models.ForeignKey(ContentType)
    pointid =models.PositiveIntegerField()
    point =GenericForeignKey('pointtype','pointid')

    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

class Likes(models.Model):
    pointtype =models.ForeignKey(ContentType)
    pointid =models.PositiveIntegerField()
    point =GenericForeignKey('pointtype','pointid')

    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

class Favorites(models.Model):
    pointtype =models.ForeignKey(ContentType)
    pointid =models.PositiveIntegerField()
    point =GenericForeignKey('pointtype','pointid')

    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    time =models.DateTimeField()

#行程,最近编辑的在前
class Course(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL)
    coursename =models.CharField(max_length=254 ,blank=True)
    createtime =models.DateTimeField()
    begindate =models.DateField(blank=True ,null=True)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成
    class Meta:
        order_with_respect_to = 'user'

class Daycourse(models.Model):
    course =models.ForeignKey(Course)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成
    class Meta:
        order_with_respect_to = 'course'


class Courseclue(models.Model):
    daycourse =models.ForeignKey(Daycourse)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成
    class Meta:
        order_with_respect_to = 'daycourse'

class Coursecell(models.Model):
    pointtype =models.ForeignKey(ContentType)
    pointid =models.PositiveIntegerField()
    point =GenericForeignKey('pointtype','pointid')

    courseclue =models.ForeignKey(Courseclue)
    begintime =models.TimeField(blank=True ,null=True)
    endtime =models.TimeField(blank=True ,null=True)
    comment =models.CharField(max_length=254 ,blank=True)
    status =models.IntegerField(default=0)#0：未开始，1：正进行，2：已完成
    class Meta:
        order_with_respect_to = 'courseclue'












