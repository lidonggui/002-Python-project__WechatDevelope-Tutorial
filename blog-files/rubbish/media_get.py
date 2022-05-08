# -*- coding: utf-8 -*-
# filename: media.py
import urllib.request
import json
from basic import Basic


# get temporary-media , but there is some trouble with it , invalid media_id !!!

class Media(object):
    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (accessToken, mediaId)
        urlResp = urllib.request.urlopen(postUrl)
        # get the http.headers
        headers = urlResp.headers

        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print(jsonDict)
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = open("get_media.jpg", "wb")
            # get_media.jpg is the name for the new downloaded image
            mediaFile.write(buffer)
            print("get successful")


if __name__ == '__main__':
    myMedia = Media()
    accessToken = Basic().get_access_token()
    mediaId = "EZ7gWsrgxME62LRm0CibVt9KBAUkY_2zuTKbOOTWlFQoAyiK61DVASryPUhYSWrZ"
    # here , use your own mediaID
    myMedia.get(accessToken, mediaId)

