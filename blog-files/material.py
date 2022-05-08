# -*- coding: utf-8 -*-
# filename: material.py
import urllib
import urllib.request
import json
import poster3.encode
import requests
from poster3.streaminghttp import register_openers
from basic import Basic

class Material(object):
    def __init__(self):
        register_openers()
    
    #上传
    def Upload_Media(self, access_token, filepath, mediaType):
        # mediaType : image \ voice \ vedio \ thumb
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=" + access_token +"&type=" + mediaType  # 上传文件
        params = {"access_token": access_token, "type": mediaType }
        with open(filepath, 'rb') as fp:
            files = {'media': fp}
            res = requests.post(url, files=files)
            res = json.loads(str(res.content, 'utf8'))
            print(res)
            media_id = res["media_id"]
        #返回素材ID
        return media_id

    #下载
    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib.request.urlopen(postUrl, postData.encode("utf-8"))
        headers = urlResp.headers
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print(jsonDict)
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = open("get_media.jpg", "wb")
            mediaFile.write(buffer)
            print("get successful")

    #删除
    def delete(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib.request.urlopen(postUrl, postData.encode("utf-8"))
        print(urlResp.read())
    
    #获取素材列表--it works !
    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/material"
               "/batchget_material?access_token=%s" % accessToken)
        postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }" % (mediaType, offset, count))
        urlResp = urllib.request.urlopen(postUrl, postData.encode("utf-8"))
        print(urlResp.read())

if __name__ == '__main__':
    myMaterial = Material()
    accessToken = Basic().get_access_token()
    # 上传
    
    mediaType = "image"
    filepath = "D:/Selfdate/Python/project_blog/medias/image/cute.jpeg"
    myMaterial.Upload_Media(accessToken, filepath, mediaType)
    
    # 下载
    """
    mediaId = "EZ7gWsrgxME62LRm0CibVv8a-JzhI2r9RpjgjiB_hB-T3GTRfIi4j8fiY3Tf5KXj"
    myMaterial.get(accessToken, mediaId)
    """
    # 删除
    """
    mediaId = "EZ7gWsrgxME62LRm0CibVv8a-JzhI2r9RpjgjiB_hB-T3GTRfIi4j8fiY3Tf5KXj"
    myMaterial.delete(accessToken, mediaId)
    """