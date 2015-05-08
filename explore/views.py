# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from main.models import userinfo ,photo
import utility.photoDistribute as pd
from PIL import Image
try:
    import cStringIO as StringIO
except ImportError: # 导入失败会捕获到ImportError
    import StringIO
import json

photoSet =set()
rootCell =pd.cell(pd.ltlnrect(0 ,0 ,0 ,0 ,0) ,pd.cellphoto(photo.objects.get(id=1)) ,None)
photoSet.add(1)
for x in photo.objects.all():
    if x.id not in photoSet:
        photoSet.add(x.id)
        rootCell.addphoto(pd.cellphoto(x))


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
    return HttpResponseRedirect(reverse('explore:index', args=('43.648614,104.68,5',)))

def getPhotos(request):
    nelt =float(request.GET['nelt'])
    neln =float(request.GET['neln'])
    swlt =float(request.GET['swlt'])
    swln =float(request.GET['swln'])
    zoom =int(request.GET['zoom'])
    bigSet =set()
    smallSet =set()
    bigUrl ='/static/smalls/'
    smallUrl ='/static/tinis/'
    #bigUrl ='/photo/small/'
    #smallUrl ='/photo/tiny/'
    fileTail ='.jpg'
    bigPhotos =[]
    smallPhotos =[]

    pd.choosePhotos(rootCell ,nelt ,swlt ,neln ,swln ,zoom ,bigSet ,smallSet)
    for cell in bigSet:
        bigPhotos.append([bigUrl +str(cell.cphoto.testid) +fileTail ,cell.cphoto.lt ,cell.cphoto.ln])
    for cell in smallSet:
        smallPhotos.append([smallUrl +str(cell.cphoto.testid) +fileTail ,cell.cphoto.lt ,cell.cphoto.ln])

    thePhotos =[bigPhotos ,smallPhotos]
    return JsonResponse(thePhotos ,safe=False)


blankTile = Image.new('RGBA', (256 ,256) ,(0 ,0 ,0 ,0))
blankStream =StringIO.StringIO()
blankTile.save(blankStream ,"PNG")
tilesInfo =list()
# def getTilesInfo(request):
#     data = json.dumps(theRsp["elements"])
#     #response =HttpResponse('data: %s\n\n' % data,content_type='text/event-stream')
#     response =HttpResponse('data: 123\n\n',content_type='text/event-stream')
#     response['Cache-Control'] = 'no-cache'
#     return response
def getTilesInfo(request):
    if len(tilesInfo):
        data = json.dumps(tilesInfo)
        del tilesInfo[:]
        return HttpResponse('data:%s\n\nretry:1000\n' % data,content_type='text/event-stream')
    # if len(tilesInfo):
    #     data = json.dumps(tilesInfo)
    #     tilesInfo =[]
    #     #return HttpResponse('data:%s\n\n' % data,content_type='text/event-stream')
    #     return HttpResponse('data:123123123\n\n',content_type='text/event-stream')

def getphotolayer(request ,zoom ,tilex ,tiley):
    photolist =[]
    pd.getTilePhoto(rootCell ,int(zoom) ,int(tilex) ,int(tiley) ,photolist)
    if not photolist:
        return HttpResponse(blankStream.getvalue(),"image/png")

    #推送tile信息：
    theRsp =dict()
    theRect =pd.makeRect(int(zoom) ,int(tilex) ,int(tiley))
    theRsp["zoom"] =zoom
    theRsp["x"] =tilex
    theRsp["y"] =tiley
    theRsp["nelt"] =theRect.nelt
    theRsp["neln"] =theRect.neln
    theRsp["swlt"] =theRect.swlt
    theRsp["swln"] =theRect.swln
    theElements =[]
    for thePhoto in photolist:
        theElements.append([thePhoto[10] ,thePhoto[3] ,thePhoto[4] ,thePhoto[5] ,thePhoto[6] ,thePhoto[1] ,thePhoto[2]])
    theRsp["elements"] =theElements
    tilesInfo.append(theRsp)

    #整合图片并返回
    theTile = Image.new('RGBA', (256 ,256) ,(0 ,0 ,0 ,0))
    for thePhoto in reversed(photolist):
        im = Image.open(thePhoto[0])
        theTile.paste(im ,(thePhoto[7] ,thePhoto[8] ,thePhoto[7] +2*thePhoto[9] ,thePhoto[8] +2*thePhoto[9]))
    photoStream =StringIO.StringIO()
    theTile.save(photoStream ,"PNG")
    return HttpResponse(photoStream.getvalue(),"image/png")













