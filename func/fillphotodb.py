from main.models import Question, Choice
import datetime
from django.utils import timezone
import os, sys
import random

def createqcs():
    for x in range(1 ,11):
        q =Question()
        q.question_text ="qst_" +str(x)
        q.pub_date =timezone.now()
        q.save()
        for y in range(1 ,6):
            c =Choice()
            c.question =q
            c.choice_text ="chs_" +str(x) +"_" +str(y)
            c.votes =random.randint(0 ,10)
            c.save()

#>>> from thetest.createqc import createqcs
#>>> createqcs()