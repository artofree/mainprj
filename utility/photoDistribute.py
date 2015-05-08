# -*- coding: utf-8 -*-

import math
from coordChange import ln2px ,lt2py ,px2ln ,py2lt ,ltperpx ,lnperpx

class ltlnrect(object):
    def __init__(self, nelt, swlt ,neln ,swln ,tag =1):
        if tag:
            self.nelt = nelt
            self.neln = neln
            self.swlt = swlt
            self.swln = swln
            self.ct =py2lt((lt2py(nelt) +lt2py(swlt)) /2)
            self.cn =(neln +swln)/2
        else:
            self.nelt =py2lt(0.0)
            self.neln =px2ln(256.0)
            self.swlt =py2lt(256.0)
            self.swln =px2ln(0.0)
            self.ct =0.0
            self.cn =0.0

    #按相限来
    def pointIndex(self ,lt ,ln):
        if self.nelt >=lt >self.ct:
            if self.neln >=ln >self.cn:
                return 0
            elif self.cn >=ln >self.swln:
                return 1
            else:
                return -1
        elif self.ct >=lt >self.swlt:
            if self.neln >=ln >self.cn:
                return 3
            elif self.cn >=ln >self.swln:
                return 2
            else:
                return -1
        else:
            return -1

    def indexRect(self ,index):
        if index ==0:
            rect =ltlnrect(self.nelt ,self.ct ,self.neln ,self.cn)
            return rect
        elif index ==1:
            rect =ltlnrect(self.nelt ,self.ct ,self.cn ,self.swln)
            return rect
        elif index ==3:
            rect =ltlnrect(self.ct ,self.swlt ,self.neln ,self.cn)
            return rect
        else:
            rect =ltlnrect(self.ct ,self.swlt ,self.cn ,self.swln)
            return rect

    def ptInRect(self ,lt ,ln):
        if self.swlt <=lt <=self.nelt and self.swln <=ln <=self.neln:
            return True
        else:
            return False


#oriscore基准评分：c*10+f*5+l*2
class cellphoto(object):
    def __init__(self ,photo):
        self.photoid =photo.id
        self.oriscore =photo.comments *10 +photo.favorites *5 +photo.likes *2
        self.lt =photo.lt
        self.ln =photo.ln
        self.testid =photo.testid


#deep,count,childs
#初始化时直接把childs创建并置空
#此处photo为cellphoto
class cell(object):
    def __init__(self, tnrect ,cphoto ,parent):
        self.tnrect = tnrect
        self.cphoto = cphoto
        self.parent = parent
        self.childs =[None ,None ,None ,None]
        self.childcount =0
        if parent:
            self.deep =parent.deep +1
        else:
            self.deep =0

    def addphotodown(self ,cphoto):
        index =self.tnrect.pointIndex(cphoto.lt ,cphoto.ln)
        if index <0:
            return
        if self.childs[index]:
            self.childs[index].addphoto(cphoto)
        else:
            self.childs[index] =cell(self.tnrect.indexRect(index) ,cphoto ,self)
        self.childcount +=1

    def addphoto(self ,cphoto):
        #往下走
        if cphoto.oriscore <self.cphoto.oriscore:
            self.addphotodown(cphoto)
        #替换该位置点
        else:
            self.addphotodown(self.cphoto)
            self.cphoto =cphoto

    #寻找指定深度内某点所在cell
    def findPointCell(self ,lt ,ln ,deepStep):
        if deepStep ==0:
            return self
        index =self.tnrect.pointIndex(lt ,ln)
        if  index==-1:
            return None
        else:
            if not self.childs[index]:
                return self
            else:
                return self.childs[index].findPointCell(lt ,ln ,deepStep -1)

    def findCell(self ,tilex ,tiley ,deepStep):
        if deepStep ==0:
            return self
        else:
            bound =int(math.pow(2 ,deepStep -1))
            if tilex <bound and tiley <bound:
                if self.childs[1]:
                    return self.childs[1].findCell(tilex %bound ,tiley %bound ,deepStep -1)
                else:
                    return self
            elif tilex <bound and tiley >=bound:
                if self.childs[2]:
                    return self.childs[2].findCell(tilex %bound ,tiley %bound ,deepStep -1)
                else:
                    return self
            elif tilex >=bound and tiley >=bound:
                if self.childs[3]:
                    return self.childs[3].findCell(tilex %bound ,tiley %bound ,deepStep -1)
                else:
                    return self
            else:
                if self.childs[0]:
                    return self.childs[0].findCell(tilex %bound ,tiley %bound ,deepStep -1)
                else:
                    return self

    #寻找参数点与本点的最近父节点：
    def findRecentParent(self ,desCell):
        desList =[desCell,]
        desParent =desCell.parent
        if not desParent:
            return desCell
        while desParent:
            desList.append(desParent)
            desParent =desParent.parent
        for p in desList:
            if self is p:
                return p
            curParent =self.parent
            while curParent:
                if curParent is p:
                    return p
                else:
                    curParent =curParent.parent

    def rectInCell(self ,desRect):
        if self.tnrect.ptInRect(desRect.nelt ,desRect.neln) and self.tnrect.ptInRect(desRect.swlt ,desRect.swln):
            return True
        else:
            return False

    #找到包含某区域的最小cell，该区域必须在root区域内！！！
    def findFitCell(self ,desRect):
        tagCell =None
        for theCell in self.childs:
            if theCell:
                if theCell.rectInCell(desRect):
                    tagCell =theCell
        if tagCell:
            return tagCell.findFitCell(desRect)
        else:
            return self

    def getDeepAllCell(self ,zoom ,theSet):
        if self.deep <=zoom:
            theSet.add(self)
        else:
            return
        for x in self.childs:
            if x:
                x.getDeepAllCell(zoom ,theSet)

    #广度优先遍历,越往后的级别越低
    def getAllCell(self ,zoom ,theList):
        if self.deep <zoom:
            for x in self.childs:
                if x:
                    theList.append(x)
            for x in self.childs:
                if x:
                    x.getAllCell(zoom ,theList)



#rootCell =cell(pd.ltlnrect(90.0 ,-90.0 ,180.0 ,-180.0) ,pd.cellphoto(photo ,None))
#列行式
def genMatrix(theRect ,deep):
    theCount =int(math.pow(2 ,deep))
    ltLen =(theRect.nelt -theRect.swlt)/theCount
    lnLen =(theRect.neln -theRect.swln)/theCount
    return [[ltlnrect(theRect.nelt -col*ltLen ,theRect.nelt -(col +1)*ltLen ,theRect.swln +(row +1)*lnLen ,theRect.swln +row *lnLen) for col in range(theCount)] for row in range(theCount)]



#给一个区域和zoom
#最终是返回两个列表
#从根向下找到ne和sw两个点所在该zoom下的cell
#从这两个cell向上找到共同的根节点，既为我们的操作重点
#从该根节点向下广度遍历至zoom级别，过滤请求区域之外的cell，即基本上合理的大图
#从过滤后cell向下3个级别，并投射即基本合理的小图，可按子节点数剔除部分合理图
#小图可在生成base矩阵的时候就限定合理区域!!!
def selectPhotos(rootCell ,nelt, swlt ,neln ,swln ,zoom):
    bigList =[]
    smallList =[]
    bigAll =[]
    smallAll =[]

    neCell =rootCell.findPointCell(nelt ,neln ,zoom)
    swCell =rootCell.findPointCell(swlt ,swln ,zoom)
    parentCell =neCell.findRecentParent(swCell)
    deepStep =zoom -parentCell.deep
    #必须重新生成这个基准矩阵，因为实际四叉树中该矩阵层可能元素缺失
    bigBase =genMatrix(parentCell.tnrect ,deepStep)

    #广度优先遍历节点下某深度之前的cell全集
    #定义目标层的大图二维数组，遍历上述cell全集投射到二维数组中
    #再遍历所有小图层上cell全集从该cell全集中剔除已选中返回部分，其余再投射到小图二维数组上
    parentCell.getDeepAllCell(zoom ,bigList)


#简化：主节点到基本层以上所有节点全部返回
def choosePhotos(rootCell ,nelt, swlt ,neln ,swln ,zoom ,bigSet ,smallSet):
    desRect =ltlnrect(nelt, swlt ,neln ,swln)
    parentCell =rootCell.findFitCell(desRect)
    parentCell.getDeepAllCell(zoom -1 ,bigSet)
    listOut =[theCell for theCell in bigSet if not desRect.ptInRect(theCell.cphoto.lt ,theCell.cphoto.ln)]
    bigSet -=set(listOut)
    parentCell.getDeepAllCell(zoom +2 ,smallSet)
    listOut =[theCell for theCell in smallSet if not desRect.ptInRect(theCell.cphoto.lt ,theCell.cphoto.ln)]
    smallSet -=set(listOut)
    smallSet -=bigSet

#tiles的方法
smallPath ='/Users/guopeng/Documents/panoramio/smalls/'
tinyPath ='/Users/guopeng/Documents/panoramio/tinis/'
smallhalfsize =32
tinyhalfsize =8

def getPhotoInfo(desCell ,tnrect ,path ,halfsize ,zoom):
    url =path +str(desCell.cphoto.testid) +'.jpg'

    nelt =py2lt(lt2py(desCell.cphoto.lt) -halfsize/math.pow(2 ,zoom))
    neln =desCell.cphoto.ln +halfsize *lnperpx(zoom)
    swlt =py2lt(lt2py(desCell.cphoto.lt) +halfsize/math.pow(2 ,zoom))
    swln =desCell.cphoto.ln -halfsize *lnperpx(zoom)
    if nelt >tnrect.nelt:
        movestep =lt2py(tnrect.nelt) -lt2py(nelt)
        nelt =tnrect.nelt
        swlt =py2lt(lt2py(swlt) +movestep)
    if neln >tnrect.neln:
        swln -=(neln -tnrect.neln)
        neln =tnrect.neln
    if swlt <tnrect.swlt:
        movestep =lt2py(swlt) -lt2py(tnrect.swlt)
        swlt =tnrect.swlt
        nelt =py2lt(lt2py(nelt) -movestep)
    if swln <tnrect.swln:
        neln +=(tnrect.swln -swln)
        swln =tnrect.swln
    left =int((swln -tnrect.swln)/360 *256 *math.pow(2 ,zoom))
    top =int((lt2py(nelt) -lt2py(tnrect.nelt))*math.pow(2 ,zoom))
    # if left +halfsize *2 >256:
    #     left =256 -halfsize *2 -1
    # if top +halfsize *2 >256:
    #     top =256 -halfsize *2 -1
    return [url ,desCell.cphoto.lt ,desCell.cphoto.ln ,nelt ,neln ,swlt ,swln ,left ,top ,halfsize ,desCell.cphoto.testid]

def makeRect(zoom ,tilex ,tiley):
    bound =math.pow(2 ,zoom)
    left =tilex *256 /bound
    top =tiley *256 /bound
    right =(tilex +1)*256/bound
    bottom =(tiley +1)*256/bound
    return ltlnrect(py2lt(top) ,py2lt(bottom) ,px2ln(right) ,px2ln(left))

def getTilePhoto(rootCell ,zoom ,tilex ,tiley ,photoList):
    #找到该tile对应的cell
    theCell =rootCell.findCell(tilex ,tiley ,zoom)
    theRect =theCell.tnrect
    if theCell.deep !=zoom:
        theRect =makeRect(zoom ,tilex ,tiley)
    #向上找有木有落在该cell的父节点
    #每个tile只有一个大图，其将占据zoom+2层的某整个cell，并遮挡其后一切元素，即其后的一切小图皆不再计算
    theList =[]
    if theRect.ptInRect(theCell.cphoto.lt ,theCell.cphoto.ln):
        theList.append(theCell)
    theParent =theCell.parent
    while(theParent):
        if theRect.ptInRect(theParent.cphoto.lt ,theParent.cphoto.ln):
            theList.append(theParent)
        theParent =theParent.parent
    theList.reverse()
    #小图针对zoom +4级别，既zoom+3以上所有
    if theCell.deep ==zoom:
        theCell.getAllCell(zoom +3 ,theList)
    if theList:
        photoList.append(getPhotoInfo(theList[0] ,theRect ,smallPath ,smallhalfsize ,zoom))
    if len(theList) >1:
        for x in theList[1:]:
            photoList.append(getPhotoInfo(x ,theRect ,tinyPath ,tinyhalfsize ,zoom))













