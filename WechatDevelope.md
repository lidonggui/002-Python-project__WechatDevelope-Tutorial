# 微信公众号—实现自动回复：

## 准备：

- apache
- Python
- Mysql（不必要）
- natapp
- 微信公众号调试工具 — [[微信公众平台接口调试工具 (qq.com)](https://mp.weixin.qq.com/debug/)]
- 注册微信公众号

## 操作步骤：

- 查看端口占用情况：`cmd: netstat -ano`

- 端口范围一般在：0 - 65535 

    - 1024 以下的端口号都留给系统。
    - 80 端口一般留给 Web 服务使用
    - 21 端口留给 FTP 使用，远程连接
    - 25 端口留给邮件服务器使用

- <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417140539516.png" alt="image-20220417140539516" style="zoom:50%;" /> 

- DocumentRoot ：文件根目录。（虚拟目录的路径）

- 访问权限

    - ```json
        <Directory D:/Selfdate/Python/project_blog >
             Options FollowSymLinks
             AllowOverride None
             Order deny,allow
             Allow from all  # 允许所有访问
             Require all granted
             </Directory>
        ```

- 站点和虚拟目录的区别：

    - 站点：就是一个文件夹
    - 虚拟目录：文件夹 + 权限

- DirectoryIndex ：首页

- DNS 解析是一个数据库，在数据库里找对应的。DNS 解析 — DNS 数据库

    - 本机的 DNS 解析数据库在：“C:\Windows\System32\drivers\etc\hosts”

- Virtual-host ：虚拟主机，多端口服务



1. 更改Apache端口为 80 端口：

    1. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417143315554.png" alt="image-20220417143315554" style="zoom:50%;" /> 
    2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417143337128.png" alt="image-20220417143337128" style="zoom:67%;" />  
    3. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417143424152.png" alt="image-20220417143424152" style="zoom:50%;" /> 
    4. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417143442024.png" alt="image-20220417143442024" style="zoom:50%;" />  

2. 编写文件：handle.py + receive.py + reply.py

    1. ```python
        # handle.py
        
        # -*- coding: utf-8 -*-
        # filename: handle.py
         
        import hashlib
        import web
         
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
        ```

    2. 消息传送格式：

        1. ```xml
            <xml>
             <ToUserName><![CDATA[公众号]]></ToUserName>
             <FromUserName><![CDATA[粉丝号]]></FromUserName>
             <CreateTime>1460537339</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[欢迎开启公众号开发者模式]]></Content>
             <MsgId>6272960105994287618</MsgId>
            </xml>
            ```

    3. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/0" alt="img" style="zoom:67%;" />大致思路

    4. 修改 blog.py 文件

        1. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417150844517.png" alt="image-20220417150844517" style="zoom: 67%;" />  
        2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417150901636.png" alt="image-20220417150901636" style="zoom:67%;" />  

    5. 增加 handle.py 内容

        1. ```python
            # -*- coding: utf-8 -*-# 
            # filename: handle.py
            import hashlib
            import reply
            import receive
            import web
            class Handle(object):
                def POST(self):
                    try:
                        webData = web.data()
                        print "Handle Post webdata is ", webData
                        #后台打日志
                        recMsg = receive.parse_xml(webData)
                        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                            toUser = recMsg.FromUserName
                            fromUser = recMsg.ToUserName
                            content = "test"
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            return replyMsg.send()
                        else:
                            print "暂且不处理"
                            return "success"
                    except Exception, Argment:
                        return Argment
            ```

        2. ```python
            # 全文预览
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
                        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                            toUser = recMsg.FromUserName
                            fromUser = recMsg.ToUserName
                            content = "text1"
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            return replyMsg.send()
                        else:
                            print ("暂且不处理")
                            return "success"
                    except Exception as Argment:
                        return Argment
            ```

    6. 编辑 receive.py 的内容：

        1. ```python
            import xml.etree.ElementTree as ET
            
            def parse_xml(web_data):
                if len(web_data) == 0:
                    return None
                xmlData = ET.fromstring(web_data)
                msg_type = xmlData.find('MsgType').text
                if msg_type == 'text':
                    #print('text')
                    return TextMsg(xmlData)
                elif msg_type == 'image':
                    return ImageMsg(xmlData)
                elif msg_type == 'location':
                    #print('location')
                    return LocationMsg(xmlData)
                elif msg_type == 'event':
                    #print('event')
                    return EventMsg(xmlData)
            
            class Event(object):
                def __init__(self, xmlData):
                    self.ToUserName = xmlData.find('ToUserName').text
                    self.FromUserName = xmlData.find('FromUserName').text
                    self.CreateTime = xmlData.find('CreateTime').text
                    self.MsgType = xmlData.find('MsgType').text
                    self.Eventkey = xmlData.find('EventKey').text
                    
            class Msg(object):
                def __init__(self, xmlData):
                    self.ToUserName = xmlData.find('ToUserName').text
                    self.FromUserName = xmlData.find('FromUserName').text
                    self.CreateTime = xmlData.find('CreateTime').text
                    self.MsgType = xmlData.find('MsgType').text
                    self.MsgId = xmlData.find('MsgId').text
            
            class TextMsg(Msg):
                def __init__(self, xmlData):
                    Msg.__init__(self, xmlData)
                    self.Content = xmlData.find('Content').text.encode("utf-8")
            
            class ImageMsg(Msg):
                def __init__(self, xmlData):
                    Msg.__init__(self, xmlData)
                    self.PicUrl = xmlData.find('PicUrl').text
                    self.MediaId = xmlData.find('MediaId').text
                
            class LocationMsg(Msg):
                def __init__(self, xmlData):
                    Msg.__init__(self, xmlData)
                    self.Location_X = xmlData.find('Location_X').text
                    self.Location_Y = xmlData.find('Location_Y').text
            
            class EventMsg(Msg):
                def __init__(self, xmlData):
                    Event.__init__(self, xmlData)
                    self.Event = xmlData.find('Event').text
            ```

    7. 编辑 reply.py 的内容：

        1. ```python
            # -*- coding: utf-8 -*-#
            # filename: reply.py
            import time
            
            class Msg(object):
                def __init__(self):
                    pass
            
                def send(self):
                    return "success"
            
            class TextMsg(Msg):
                def __init__(self, toUserName, fromUserName, content):
                    self.__dict = dict()
                    self.__dict['ToUserName'] = toUserName
                    self.__dict['FromUserName'] = fromUserName
                    self.__dict['CreateTime'] = int(time.time())
                    self.__dict['Content'] = content
            
                def send(self):
                    XmlForm = """
                        <xml>
                            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                            <CreateTime>{CreateTime}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{Content}]]></Content>
                        </xml>
                        """
                    return XmlForm.format(**self.__dict)
            
            class ImageMsg(Msg):
                def __init__(self, toUserName, fromUserName, mediaId):
                    self.__dict = dict()
                    self.__dict['ToUserName'] = toUserName
                    self.__dict['FromUserName'] = fromUserName
                    self.__dict['CreateTime'] = int(time.time())
                    self.__dict['MediaId'] = mediaId
            
                def send(self):
                    XmlForm = """
                        <xml>
                            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                            <CreateTime>{CreateTime}</CreateTime>
                            <MsgType><![CDATA[image]]></MsgType>
                            <Image>
                            <MediaId><![CDATA[{MediaId}]]></MediaId>
                            </Image>
                        </xml>
                        """
                    return XmlForm.format(**self.__dict)
            ```

3. 在线测试：

    1. 使用开头提供的网址，配置好信息就可以测试了。
    2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417145145972.png" alt="image-20220417145145972" style="zoom:50%;" />  

    1. 测试成功就是可以了，有问题的话再自己调试。
        1. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417145847408.png" alt="image-20220417145847408" style="zoom: 50%;" />  
        2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417145949683.png" alt="image-20220417145949683" style="zoom:50%;" />  
        3. 一定要注意这个细节，我第一次就是因为这个浪费了好多时间。

4. 进一步完善 handle.py 的内容

    1. ```python
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
        ```

    2. 肯定还有很多优秀的设计办法，目前先到这吧。























































