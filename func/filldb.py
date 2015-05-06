# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from main.models import userinfo ,photo
import datetime
from django.utils import timezone
import os, sys
import random ,codecs

photoPath =r"/Users/guopeng/Documents/panoramio/photos"
resultpath =r"/Users/guopeng/Documents/panoramio/1"

def createphoto():
    dList =[]
    theDict =dict()
    with codecs.open(resultpath, 'r', 'utf-8') as f:
        tList =[line.strip('\n') for line in f.readlines()]
    resultList =[x.split('||') for x in tList]
    for x in resultList:
        if len(x) <16:
            dList.append(x)
    for x in dList:
        resultList.remove(x)
    for x in resultList:
        for idx in range(-4,0):
            if '|' in x[idx]:
                x[idx] =x[idx].strip('|')
            if x[idx] =='':
                x[idx] ='0'
            x[idx] =int(x[idx])

    for x in resultList:
        theDict[x[0]] =x
    photoList =[os.path.splitext(x)[0] for x in os.listdir(photoPath)]
    for x in photoList:
        if theDict.has_key(x):
            #写数据库:
            photoInfo =theDict[x]
            theUser = User.objects.get(pk=1)
            thePhoto =photo()
            thePhoto.testid =photoInfo[0]
            thePhoto.user =theUser
            thePhoto.file =" "
            thePhoto.filename =" "
            thePhoto.lt =float(photoInfo[4])
            thePhoto.ltc =photoInfo[5]
            thePhoto.ln =float(photoInfo[6])
            thePhoto.lnc =photoInfo[7]
            thePhoto.lable =1
            thePhoto.looks =photoInfo[12]
            thePhoto.likes =photoInfo[13]
            thePhoto.favorites =photoInfo[14]
            thePhoto.comments =photoInfo[15]
            thePhoto.save()

















#>>> from func.filldb import createphoto
#>>> createphoto()