# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('coursename', models.CharField(max_length=254, blank=True)),
                ('createtime', models.DateTimeField()),
                ('begindate', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(max_length=254, blank=True)),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coursecell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pointid', models.PositiveIntegerField()),
                ('begintime', models.TimeField(blank=True, null=True)),
                ('endtime', models.TimeField(blank=True, null=True)),
                ('comment', models.CharField(max_length=254, blank=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Courseclue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=254, blank=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Daycourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=254, blank=True)),
                ('status', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pointid', models.PositiveIntegerField()),
                ('time', models.DateTimeField()),
                ('pointtype', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pointid', models.PositiveIntegerField()),
                ('time', models.DateTimeField()),
                ('pointtype', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('lt', models.FloatField()),
                ('ln', models.FloatField()),
                ('testid', models.IntegerField()),
                ('file', models.CharField(max_length=254, blank=True)),
                ('title', models.CharField(max_length=127, blank=True)),
                ('takenTime', models.CharField(max_length=64, blank=True)),
                ('place', models.CharField(max_length=254, blank=True)),
                ('lable', models.IntegerField(default=0)),
                ('tlooks', models.IntegerField(default=0)),
                ('tlikes', models.IntegerField(default=0)),
                ('tfavorites', models.IntegerField(default=0)),
                ('tcomments', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nationCode', models.CharField(max_length=60, blank=True)),
                ('phoneNum', models.CharField(max_length=30, blank=True)),
                ('sex', models.IntegerField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('headimg', models.URLField(blank=True)),
                ('lable', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pointid', models.PositiveIntegerField()),
                ('time', models.DateTimeField()),
                ('pointtype', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='courseclue',
            name='daycourse',
            field=models.ForeignKey(to='main.Daycourse'),
        ),
        migrations.AddField(
            model_name='coursecell',
            name='courseclue',
            field=models.ForeignKey(to='main.Courseclue'),
        ),
        migrations.AddField(
            model_name='coursecell',
            name='pointtype',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='daycourse',
            order_with_respect_to='course',
        ),
        migrations.AlterOrderWithRespectTo(
            name='courseclue',
            order_with_respect_to='daycourse',
        ),
        migrations.AlterOrderWithRespectTo(
            name='coursecell',
            order_with_respect_to='courseclue',
        ),
        migrations.AlterOrderWithRespectTo(
            name='course',
            order_with_respect_to='user',
        ),
    ]
