# -*- coding: utf-8 -*-

from PIL import Image
import os
try:
    import cStringIO as StringIO
except ImportError: # 导入失败会捕获到ImportError
    import StringIO

class photoCache(object):
    def __init__(self ,path):
        self.photoDict =dict()
        self.photoStream =StringIO.StringIO()
        photoList =os.listdir(path)
        for thePhoto in photoList:
            if thePhoto.find('.jpg') >0:
                im =Image.open(os.path.join(path ,thePhoto))
                begin =self.photoStream.tell()
                im.save(self.photoStream ,'JPEG')
                self.photoDict[os.path.splitext(thePhoto)[0]] =[begin ,self.photoStream.tell() -begin]

