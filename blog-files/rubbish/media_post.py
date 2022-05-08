# -*- coding: utf-8 -*-
# filename: media.py

import requests
import json
from basic import Basic
from poster3.streaminghttp import register_openers


class Media(object):
    def __init__(self):
        register_openers()
    #上传素材库的拖
    def Upload_Media_Img(self, access_token, filepath, mediaType):
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=" + access_token +"&type=image"  # 上传文件
        params = {"access_token": access_token,
                "type": mediaType }
        with open(filepath, 'rb') as fp:
            files = {'media': fp}
            res = requests.post(url, files=files)
            res = json.loads(str(res.content, 'utf8'))
            print(res)
            media_id = res["media_id"]
        
        #返回素材ID
        return media_id


if __name__ == '__main__':
    myMedia = Media()
    accessToken = Basic().get_access_token()
    filePath = "D:/Selfdate/Python/project_blog/medias/image/chuyingirl.jpg"  # 请按实际填写
    mediaType = "image"
    myMedia.Upload_Media_Img(accessToken, filePath, mediaType)