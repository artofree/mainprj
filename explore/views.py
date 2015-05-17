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
import thread
streamLock = thread.allocate_lock()

#初始化全球图片树
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

tilesContentInfo =dict()
blankStream =StringIO.StringIO()
blankTile = Image.new('RGBA', (256 ,256) ,(0 ,0 ,0 ,0))
blankTile.save(blankStream ,"PNG")
allTileImages =[blankStream]

#获得tile里的cell图片信息
def getPhotoInfo(request):
    zoom =request.GET['zoom']
    tilex =request.GET['x']
    tiley =request.GET['y']
    strKey =zoom +',' +tilex  +',' +tiley
    if not tilesContentInfo.has_key(strKey):
        makeContent(zoom ,tilex ,tiley)
    theTileInfo =tilesContentInfo[strKey]
    if theTileInfo[0] ==0:
        theRsp =dict()
        theRsp["zoom"] =zoom
        theRsp["x"] =tilex
        theRsp["y"] =tiley
        theRsp["nelt"] =0.0
        theRsp["neln"] =0.0
        theRsp["swlt"] =0.0
        theRsp["swln"] =0.0
        theRsp["elements"] =[]
        return JsonResponse(theRsp)
    else:
        return JsonResponse(theTileInfo[1])

#获得tile整合图片本身
def getphotolayer(request ,zoom ,tilex ,tiley):
    strKey =zoom +',' +tilex  +',' +tiley
    if not tilesContentInfo.has_key(strKey):
        makeContent(zoom ,tilex ,tiley)
    theTileInfo =tilesContentInfo[strKey]
    theIo =allTileImages[theTileInfo[0]]
    return HttpResponse(theIo.getvalue(),"image/png")

def makeContent(zoom ,tilex ,tiley):
    strKey =zoom +',' +tilex  +',' +tiley
    photolist =[]
    pd.getTilePhoto(rootCell ,int(zoom) ,int(tilex) ,int(tiley) ,photolist)

    #将空图片加入该tile信息
    if not photolist:
        tilesContentInfo[strKey] =[0]
        return

    #整合图片并置入流
    theTile = Image.new('RGBA', (256 ,256) ,(0 ,0 ,0 ,0))
    for thePhoto in reversed(photolist):
        im = Image.open(thePhoto[0])
        theTile.paste(im ,(thePhoto[7] ,thePhoto[8] ,thePhoto[7] +2*thePhoto[9] ,thePhoto[8] +2*thePhoto[9]))

    theStream =StringIO.StringIO()
    theTile.save(theStream ,"PNG")
    allTileImages.append(theStream)
    theLen =len(allTileImages)

    #tile信息置入
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
        theElements.append([thePhoto[10] ,thePhoto[3] ,thePhoto[4] ,thePhoto[5] ,thePhoto[6] ,thePhoto[1] ,thePhoto[2] ,thePhoto[12]])
    theRsp["elements"] =theElements
    tilesContentInfo[strKey] =[theLen -1 ,theRsp]

#获得右栏区域照片列表，既当前bound下广度优先遍历的所有照片
def getPhotoList(request):
    nelt =float(request.GET['nelt'])
    neln =float(request.GET['neln'])
    swlt =float(request.GET['swlt'])
    swln =float(request.GET['swln'])
    zoom =int(request.GET['zoom'])

    photoList =[]
    if swln >neln:
        pd.choosePhotos(rootCell ,nelt ,swlt ,180.0 ,swln ,zoom ,photoList)
        pd.choosePhotos(rootCell ,nelt ,swlt ,neln ,-180.0 ,zoom ,photoList)
    else:
        pd.choosePhotos(rootCell ,nelt ,swlt ,neln ,swln ,zoom ,photoList)

    photoList.sort(key=lambda col:(col[2]))
    return JsonResponse(photoList ,safe=False)

#通用请求
def genRequest(request):
    return HttpResponse('0')




































