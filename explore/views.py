# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse

class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        return self.name +str(self.score)

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'


theStudent =Student('Bart Simpson', 59)

# Create your views here.
def index(request ,rqst):
    #return  HttpResponse(rqst)
    rqstList =rqst.split(',')
    rqstList[0] =float(rqstList[0])
    rqstList[1] =float(rqstList[1])
    rqstList[2] =int(rqstList[2])
    if -90 < rqstList[0] < 90 and rqstList[2] <15 :
        return render(request, 'explore/index.html' ,{
            'lt' :rqstList[0],
            'ln' :rqstList[1],
            'zoom' :rqstList[2],
        })

def rdrct(request):
    #return  HttpResponse(rqst)
    #return render(request, 'explore/index.html')
    return HttpResponseRedirect(reverse('explore:index', args=('20.967361,-33.000000,3',)))

def getPhotos(request):
    nelt =request.GET['nelt']
    neln =request.GET['neln']
    swlt =request.GET['swlt']
    swln =request.GET['swln']
    thePhoto =[['/static/smalls/35284692.jpg' ,(float(nelt) +float(swlt))/2 ,(float(neln) +float(swln))/2]]
    return JsonResponse(thePhoto ,safe=False)