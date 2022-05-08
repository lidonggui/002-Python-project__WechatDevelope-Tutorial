# -*- coding: utf-8 -*-
# filename: material.py

# import urllib2,we do not need 2 in py3,explorers had already merged them in one package--urllib
import urllib.request
import urllib.request
import json
from basic import Basic

class Material(object):
    # 上传图文
    def add_news(self, accessToken, news):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s" % accessToken
        urlResp = urllib.request.urlopen(postUrl, news)
        print (urlResp.read())


if __name__ == '__main__':
    myMaterial = Material()
    accessToken = Basic().get_access_token()
    news = (
        {
            "articles":
            [
                {
                    "title": "test",
                    "thumb_media_id": "EZ7gWsrgxME62LRm0CibVt9KBAUkY_2zuTKbOOTWlFQoAyiK61DVASryPUhYSWrZ",
                    "author": "DongyangLi",
                    "digest": "",
                    "show_cover_pic": 1,
                    "content": "<p><img src=\"\" alt=\"\" data-width=\"null\" data-ratio=\"NaN\"><br  /><img src=\"\" alt=\"\" data-width=\"null\" data-ratio=\"NaN\"><br  /></p>",
                    "content_source_url": "",
                }
            ]
        })
    # news 是个dict类型，可通过下面方式修改内容
    # news['articles'][0]['title'] = u"测试".encode('utf-8')
    # print news['articles'][0]['title']
    news = json.dumps(news, ensure_ascii=False)
    # data = urllib.parse.urlencode(news).encode("utf-8")
    myMaterial.add_news(accessToken, news.encode("utf-8"))