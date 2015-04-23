# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
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
def index(request):
    #return render(request, 'explore/index.html')
    return HttpResponse(theStudent.name)