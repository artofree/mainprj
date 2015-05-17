# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testid', models.IntegerField()),
                ('file', models.FileField(upload_to=b'')),
                ('filename', models.CharField(max_length=254)),
                ('title', models.CharField(max_length=127, blank=True)),
                ('takenTime', models.CharField(max_length=64, blank=True)),
                ('place', models.CharField(max_length=254, blank=True)),
                ('lt', models.FloatField()),
                ('ltc', models.CharField(max_length=62)),
                ('ln', models.FloatField()),
                ('lnc', models.CharField(max_length=62)),
                ('lable', models.IntegerField(default=0)),
                ('looks', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('favorites', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='userinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nationCode', models.CharField(max_length=60, blank=True)),
                ('phoneNum', models.CharField(max_length=30, blank=True)),
                ('sex', models.IntegerField(null=True, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('headimg', models.URLField(blank=True)),
                ('lable', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
