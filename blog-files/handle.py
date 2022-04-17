# -*- coding: utf-8 -*-
# filename: handle.py
 
import hashlib
import web
import reply
import receive

 
class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "token123456" #请按照公众平台官网\基本配置中信息填写
            
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode("utf-8"))
            sha1.update(list[1].encode("utf-8"))
            sha1.update(list[2].encode("utf-8"))
            map(sha1.update, list)
            hashcode = sha1.hexdigest() #获取加密串
 
            print ("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument



    def POST(self):
        try:
            webData = web.data()
            print ("Handle Post webdata is ", webData)
            #后台打日志
            recMsg = receive.parse_xml(webData)
            """Version--1
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "text1"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print ("暂且不处理")
                return "success"
            """
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    if recMsg.Content.decode("utf-8") == "test":
                        content = "test Successed"
                    elif recMsg.Content.decode("utf-8") == "testagain":
                        content = "boring"
                    else:
                        content = "test Failed"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':   # return the same image
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                if recMsg.MsgType == 'location':
                    location_x = recMsg.Location_X
                    location_y = recMsg.Location_Y
                    content = "您所在的位置是在：经度为"+location_x+"；纬度为："+location_y
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'event':
                    #print('yes')
                    event = recMsg.Event
                    if event == 'subscribe':
                        content = "欢迎关注"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print ("暂且不处理")
                return reply.Msg().send()
        except Exception as Argment:
            return Argment
