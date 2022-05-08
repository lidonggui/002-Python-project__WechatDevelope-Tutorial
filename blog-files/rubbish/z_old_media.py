# -*- coding: utf-8 -*-
# filename: media.py

# media.py 编写完成之后，直接运行media.py 即可上传临时素材。

from basic import Basic
import urllib.request
import urllib
import poster3.encode
from urllib import *
from poster3.streaminghttp import register_openers
import requests
import json


class Media(object):
    def __init__(self):
        register_openers()
    
    # 上传图片
    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")  # which is "rb" before
        param = {'media': openFile}

        postData, postHeaders = poster3.encode.multipart_encode(param)
        # to solve "AttributeError: 'bytes' object has no attribute 'encode'. Did you mean: 'decode'?", 
        # I tried to comment line 94 and line 95 in "C:\Python310\lib\site-packages\poster3\encode.py"

        # postHeaders = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"}
        # postData = urllib.parse.urlencode(param).encode('utf-8')

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib.request.Request(postUrl, postData, postHeaders)
        # use "urllib.request.Request" instead "urllib.Request" <- this is in python2
        urlResp = urllib.request.urlopen(request)
        # use "urllib.request.urlopen(request)" instead "urllib.urlopen(request)"
        print (urlResp.read())


if __name__ == '__main__':
    myMedia = Media()
    accessToken = Basic().get_access_token()
    filePath = "D:/Selfdate/Python/project_blog/medias/image/city.jpg"  # 请按实际填写
    mediaType = "image"
    myMedia.upload(accessToken, filePath, mediaType)
