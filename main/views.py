# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse

from django.contrib import auth
from django.contrib.auth.models import User


#smallPhotoCache =pc.photoCache('/Users/guopeng/Documents/panoramio/smalls')
#tinyPhotoCache =pc.photoCache('/Users/guopeng/Documents/panoramio/tinis')

def home(request):
    #if request.session.get('user_id', False):
    if request.user.is_authenticated():
        return render(request, 'main/home.html')
    else:
        return render(request, 'main/login.html')

def login(request):
    username=request.POST['username']
    password =request.POST['password']
    user =auth.authenticate(username=username, password=password)
    if user:
        #request.session['user_id'] =user.id
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse("Your username and password didn't match.")



def getsmallphoto(request ,photofile):
    thePhoto =smallPhotoCache.photoDict.get(photofile)
    smallPhotoCache.photoStream.seek(thePhoto[0])
    rsp =smallPhotoCache.photoStream.read(thePhoto[1])
    return HttpResponse(rsp, 'image/jpeg')

def gettinyphoto(request ,photofile):
    thePhoto =tinyPhotoCache.photoDict.get(photofile)
    tinyPhotoCache.photoStream.seek(thePhoto[0])
    rsp =tinyPhotoCache.photoStream.read(thePhoto[1])
    return HttpResponse(rsp, 'image/jpeg')

