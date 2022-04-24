注：本文均由作者本人根据个人操作中遇到的问题进行编写，并非专业教程，如有问题，欢迎指正

# 用 apache 配置网页文件显示在 8080 端口

- ==（我的是 blog.py，就以此为例进行讲解）==

## 操作步骤

1. *第一步*：下载并安装 Apache

    1. Apache下载网址（国内可能需要梯子）：[click here][https://www.apachehaus.com/cgi-bin/download.plx]
    2. 选择合适的版本下载即可，其中 vc、vs 是 Visual Studio 的版本，下载高版本即可，因为 Visual Studio 是向后兼容的，即，高版本可以正常使用低版本的环境，而低版本不可以在高版本的环境下运行。

2. *第二步*：简单配置 Apache

    1. 在 `Apache24\conf` 目录下找到 `httpd.conf` 配置文件，打开后可直接搜索 `SRVROOT` ，修改为自己 apache 的路径即可。如图

    2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220419214025062.png" alt="image-20220419214025062" style="zoom:67%;" />   

    3. 注意，此处的 SRVROOT 路径指的是 Apache24 的根目录，即图示：

    4. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220419214211514.png" alt="image-20220419214211514" style="zoom:67%;" />   

    5. 接下来需要安装 apache 服务：cmd 管理员模式进入到 apache 的 bin 目录，执行 `httpd -k install -n apache2.4` 安装 apache 的服务。如图即为安装成功：

        <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220420102922347.png" alt="image-20220420102922347" style="zoom:67%;" />    

        <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220420103107858.png" alt="image-20220420103107858" style="zoom:67%;" />    

    6. 如果需要卸载 apache2.4 服务， `sc delete apache2.4` 。

3. *启动 Apache* ：`httpd -k start`。（需要在 bin 目录下用 cmd 管理员模式执行；也可以直接将 httpd.exe 文件的目录添加到系统环境中，就可以直接在任何地方的 cmd 使用 httpd ）

    1. 常用的几个指令：
    2. `httpd -k start`：开启服务
    3. `httpd -k stop`：停止服务
    4. `httpd -k restart`：重启服务

4. *第三步*：初步测试，测试 apache 基本配置是否成功。

    1. 打开网页在网址栏输入 `http://localhost` 回车即可。出现下面的页面就说明成功了：
    2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220419214922199.png" alt="image-20220419214922199" style="zoom: 33%;" />    

5. *第四步*：安装 `mod_wsgi` 

    1. 什么是 `mod_wsgi` ：

        > ##### 什么是mod_wsgi ？
        >
        > mod_wsgi的目标是实现一个简单的[Apache](https://so.csdn.net/so/search?q=Apache&spm=1001.2101.3001.7020)模块，支持任何Python WSGI的接口的Python应用程序的托管。该模块适用于高性能生产的WEB站点，同时也适用于自己维护站点的WEB 服务托管（虚拟主机环境–译者注）。
        >
        > ##### 运行模式
        >
        > 用mod_wsgi来托管应用，有两个主要的模式可以使用，一种是“嵌入式”模式，Mod_wsgi与Mod_python运行方式相同，所有的 python代码都将在apache 子进程中执行。因此当[WSGI](https://so.csdn.net/so/search?q=WSGI&spm=1001.2101.3001.7020)应用在此模式下运行可以与其他的Apache托管的模块PHP和Perl共享形同进程。
        >
        > 另一个在UNIX Apache 2.*环境下可选替代的daemon模式,这种模式运作的方式在类似的FastCGI / SCGI解决方案，即在不同的进程运行WSGI应用。与FastCGI / SCGI解决方案不同的是，当执行WSGI程序时不需要单独的基础结构（infrastructure），一切都是自动处理的mod_wsgi。
        >
        > 一切都是自动处理的mod_wsgi，影响正常使用的Apache模块的PHP ， Perl或其他语言的Apache子进程服务的静态文件和主机应用程序使用大大减少。守护（daemon）进程可能需要时也可以作为一个独特的用户运行以确保WSGI应用程序之间不能互相干扰或获取信息。
        >
        > ##### 服务性能
        >
        > 该mod_wsgi模块是用C代码直接对内部的Apache和Python应用程序接口编程。因此，服务WSGI应用与Apache它具有较低的内存开销和性能优于现有的WSGI适配器mod_python或替代的FastCGI / SCGI / CGI或代理的解决方案。
        >
        > 虽然嵌入式技术模式能够表现得更好， daemon模式通常是最安全的选择使用。这是因为要嵌入模式高性能需要调整apache MPM设置，默认设置偏向于服务静态媒体和PHP应用。如果Apache 的MPM设置未与服务的应用相对应，将会表现出糟糕的性能而不是更好的性能。
        >
        > 因此，除非你非常熟悉Aapache的配置，否则推荐使用daemon模式，总体而言，大型Python Web程序，通常你不能看出嵌入式（embedded mode）和守护模式（daemon mode）明显的差异，因为瓶颈在Python Web和数据库访问上。
        >
        > ##### 支持的应用
        >
        > mod_wsgi遵循WSGI接口规范，任何符合WSGI接口规范的Python Web框架或者应用都可以被支持。
        >
        > 我们所熟悉的主要的Python web框架或工具，包括CherryPy, Django, Karrigell, Pylons, TurboGears, web.py, Werkzeug 和Zope 运行良好，我们所熟知的主要的Python web应用包括MoinMoin, PyBlosxom 和 Trac 能够很好的运行。

        > WSGI的全称是*Web Server Gateway Interface*，翻译过来就是*Web服务器网关接口*。具体的来说，**WSGI是一个规范，定义了Web服务器如何与Python应用程序进行交互，使得使用Python写的Web应用程序可以和Web服务器对接起来**。WSGI一开始是在[PEP-0333](https://www.python.org/dev/peps/pep-0333/)中定义的，最新版本是在Python的[PEP-3333](https://www.python.org/dev/peps/pep-3333/)定义的。
        >
        > ### WSGI是什么
        >
        > WSGI的全称是*Web Server Gateway Interface*，翻译过来就是*Web服务器网关接口*。具体的来说，**WSGI是一个规范，定义了Web服务器如何与Python应用程序进行交互，使得使用Python写的Web应用程序可以和Web服务器对接起来**。WSGI一开始是在[PEP-0333](https://www.python.org/dev/peps/pep-0333/)中定义的，最新版本是在Python的[PEP-3333](https://www.python.org/dev/peps/pep-3333/)定义的。
        >
        > 对于初学者来说，上面那段就是废话，说了跟没说一样。本文的主要内容就是说清楚，WSGI到底是如何工作的。
        >
        > #### 为什么需要WSGI这个规范
        >
        > 在Web部署的方案上，有一个方案是目前应用最广泛的：
        >
        > - 首先，部署一个Web服务器专门用来处理HTTP协议层面相关的事情，比如如何在一个物理机上提供多个不同的Web服务（单IP多域名，单IP多端口等）这种事情。
        > - 然后，部署一个用各种语言编写（Java, PHP, Python, Ruby等）的应用程序，这个应用程序会从Web服务器上接收客户端的请求，处理完成后，再返回响应给Web服务器，最后由Web服务器返回给客户端。
        >
        > 那么，要采用这种方案，Web服务器和应用程序之间就要知道如何进行交互。为了定义Web服务器和应用程序之间的交互过程，就形成了很多不同的规范。这种规范里最早的一个是CGI][3，1993年开发的。后来又出现了很多这样的规范。比如改进CGI性能的FasgCGI，Java专用的Servlet规范，还有Python专用的WSGI规范等。提出这些规范的目的就是为了定义统一的标准，提升程序的可移植性。在WSGI规范的最开始的PEP-333中一开始就描述了为什么需要WSGI规范。
        >
        > ### WSGI如何工作
        >
        > 从上文可以知道，WSGI相当于是Web服务器和Python应用程序之间的桥梁。那么这个桥梁是如何工作的呢？首先，我们明确桥梁的作用，WSGI存在的目的有两个：
        >
        > 1. 让Web服务器知道如何调用Python应用程序，并且把用户的请求告诉应用程序。
        > 2. 让Python应用程序知道用户的具体请求是什么，以及如何返回结果给Web服务器。
        >
        > #### WSGI中的角色
        >
        > 在WSGI中定义了两个角色，Web服务器端称为**server**或者**gateway**，应用程序端称为**application**或者**framework**（因为WSGI的应用程序端的规范一般都是由具体的框架来实现的）。我们下面统一使用server和application这两个术语。
        >
        > server端会先收到用户的请求，然后会根据规范的要求调用application端，如下图所示：
        >
        > [图片上传失败...(image-1bd5a9-1541121120404)]
        >
        > 调用的结果会被封装成HTTP响应后再发送给客户端。
        >
        > #### server如何调用application
        >
        > 首先，每个application的入口只有一个，也就是所有的客户端请求都同一个入口进入到应用程序。
        >
        > 接下来，server端需要知道去哪里找application的入口。这个需要在server端指定一个Python模块，也就是Python应用中的一个文件，并且这个模块中需要包含一个名称为**application**的可调用对象（函数和类都可以），这个**application**对象就是这个应用程序的唯一入口了。WSGI还定义了**application**对象的形式：
        >
        > 
        >
        > ```python
        > def simple_app(environ, start_response):
        >       pass
        > ```
        >
        > 上面代码中的`environ`和`start_response`就是server端调用**application**对象时传递的两个参数。
        >
        > 我们来看具体的例子。假设我们的应用程序的入口文件是`/var/www/index.py`，那么我们就需要在server端配置好这个路径（如何配置取决于server端的实现），然后在`index.py`中的代码如下所示：
        >
        > 使用标准库（这个只是demo）
        >
        > 
        >
        > ```swift
        > import wsgiref
        > 
        > application = wsgiref.simple_server.demo_app
        > ```
        >
        > 使用web.py框架
        >
        > 
        >
        > ```python
        > import web
        > 
        > urls = (
        >     '/.*', 'hello',
        > )
        > 
        > class hello(object):
        >     def GET(self):
        >         return "Hello, world."
        > 
        > application = web.application(urls, globals()).wsgifunc()
        > ```
        >
        > 你可以看到，文件中都需要有一个**application**对象，server端会找到这个文件，然后调用这个对象。所以支持WSGI的Python框架最终都会有这么一个application对象，不过框架的使用者不需要关心这个application对象内部是如何工作的，只需要关心路由定义、请求处理等具体的业务逻辑。
        >
        > 因为application对象是唯一的入口，所以不管客户端请求的路径和数据是什么，server都是调用这个application对象，具体的客户端请求的处理有application对象完成。
        >
        > #### application对象需要做什么
        >
        > 上面已经提到了，application对象需要是一个可调用对象，而且其定义需要满足如下形式：
        >
        > 
        >
        > ```python
        > def simple_app(environ, start_response):
        >       pass
        > ```
        >
        > 当server按照WSGI的规范调用了application之后，application就可以开始处理客户端的请求了，处理请求之后，application对象需要返回处理结果给server端。处理请求和返回结果这两个事情，都和server调用application对象时传递的两个参数有关。
        >
        > ##### environ参数
        >
        > environ参数是一个Python的字典，里面存放了所有和客户端相关的信息，这样application对象就能知道客户端请求的资源是什么，请求中带了什么数据等。environ字典包含了一些CGI规范要求的数据，以及WSGI规范新增的数据，还可能包含一些操作系统的环境变量以及Web服务器相关的环境变量。我们来看一些environ中常用的成员：
        >
        > 首先是CGI规范中要求的变量：
        >
        > - **REQUEST_METHOD**： 请求方法，是个字符串，'GET', 'POST'等
        > - **SCRIPT_NAME**： HTTP请求的path中的用于查找到application对象的部分，比如Web服务器可以根据path的一部分来决定请求由哪个virtual host处理
        > - **PATH_INFO**： HTTP请求的path中剩余的部分，也就是application要处理的部分
        > - **QUERY_STRING**： HTTP请求中的查询字符串，URL中**?**后面的内容
        > - **CONTENT_TYPE**： HTTP headers中的content-type内容
        > - **CONTENT_LENGTH**： HTTP headers中的content-length内容
        > - **SERVER_NAME**和**SERVER_PORT**： 服务器名和端口，这两个值和前面的SCRIPT_NAME, PATH_INFO拼起来可以得到完整的URL路径
        > - **SERVER_PROTOCOL**： HTTP协议版本，HTTP/1.0或者HTTP/1.1
        > - **HTTP_**： 和HTTP请求中的headers对应。
        >
        > WSGI规范中还要求environ包含下列成员：
        >
        > - **wsgi.version**：表示WSGI版本，一个元组(1, 0)，表示版本1.0
        > - **wsgi.url_scheme**：http或者https
        > - **wsgi.input**：一个类文件的输入流，application可以通过这个获取HTTP request body
        > - **wsgi.errors**：一个输出流，当应用程序出错时，可以将错误信息写入这里
        > - **wsgi.multithread**：当application对象可能被多个线程同时调用时，这个值需要为True
        > - **wsgi.multiprocess**：当application对象可能被多个进程同时调用时，这个值需要为True
        > - **wsgi.run_once**：当server期望application对象在进程的生命周期内只被调用一次时，该值为True
        >
        > 上面列出的这些内容已经包括了客户端请求的所有数据，足够application对象处理客户端请求了。
        >
        > ##### start_resposne参数
        >
        > start_response是一个可调用对象，接收两个必选参数和一个可选参数：
        >
        > - **status**: 一个字符串，表示HTTP响应状态字符串
        > - **response_headers**: 一个列表，包含有如下形式的元组：(header_name, header_value)，用来表示HTTP响应的headers
        > - **exc_info**（可选）: 用于出错时，server需要返回给浏览器的信息
        >
        > 当application对象根据environ参数的内容执行完业务逻辑后，就需要返回结果给server端。我们知道HTTP的响应需要包含status，headers和body，所以在application对象将body作为返回值return之前，需要先调用`start_response()`，将status和headers的内容返回给server，这同时也是告诉server，application对象要开始返回body了。
        >
        > ##### application对象的返回值
        >
        > application对象的返回值用于为HTTP响应提供body，如果没有body，那么可以返回None。如果有body的化，那么需要返回一个可迭代的对象。server端通过遍历这个可迭代对象可以获得body的全部内容。
        >
        > ##### application demo
        >
        > PEP-3333中有一个application的实现demo，我把它再简化之后如下：
        >
        > 
        >
        > ```python
        > def simple_app(environ, start_response):
        >       status = '200 OK'
        >       response_headers = [('Content-type', 'text/plain')]
        >       start_response(status, response_headers)
        >       return ['hello, world']
        > ```
        >
        > 可以将这段代码和前面的说明对照起来理解。
        >
        > #### 再谈server如何调用application
        >
        > 前面已经知道server如何定位到application的入口了，也知道了application的入口的形式以及application对象内部需要完成的工作。那么，我们还需要再说一下，`environ`和`start_response()`是需要在server端的生成和定义的，其中关于`start_response()`的部分在规范中也有明确的要求。这部分内容太长了，不适合放在本文中，有兴趣的读者可以去看下PEP-3333，里面有一段server端的demo实现。
        >
        > ### WSGI中间件
        >
        > **WSGI Middleware**（中间件）也是WSGI规范的一部分。上一章我们已经说明了WSGI的两个角色：server和application。那么middleware是一种运行在server和application中间的应用（一般都是Python应用）。middleware同时具备server和application角色，对于server来说，它是一个application；对于application来说，它是一个server。middleware并不修改server端和application端的规范，只是同时实现了这两个角色的功能而已。
        >
        > 我们可以通过下图来说明middleware是如何工作的：
        >
        > <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/12899159-c08bb71a5e61b087.png" alt="img" style="zoom: 80%;" />
        >
        > 上图中最上面的三个彩色框表示角色，中间的白色框表示操作，操作的发生顺序按照1 ~ 5进行了排序，我们直接对着上图来说明middleware是如何工作的：
        >
        > 1. Server收到客户端的HTTP请求后，生成了`environ_s`，并且已经定义了`start_response_s`。
        > 2. Server调用Middleware的application对象，传递的参数是`environ_s`和`start_response_s`。
        > 3. Middleware会根据`environ`执行业务逻辑，生成`environ_m`，并且已经定义了`start_response_m`。
        > 4. Middleware决定调用Application的application对象，传递参数是`environ_m`和`start_response_m`。Application的application对象处理完成后，会调用`start_response_m`并且返回结果给Middleware，存放在`result_m`中。
        > 5. Middleware处理`result_m`，然后生成`result_s`，接着调用`start_response_s`，并返回结果`result_s`给Server端。Server端获取到result_s后就可以发送结果给客户端了。
        >
        > 从上面的流程可以看出middleware应用的几个特点：
        >
        > 1. Server认为middleware是一个application。
        > 2. Application认为middleware是一个server。
        > 3. Middleware可以有多层。
        >
        > 因为Middleware能过处理所有经过的request和response，所以要做什么都可以，没有限制。比如可以检查request是否有非法内容，检查response是否有非法内容，为request加上特定的HTTP header等，这些都是可以的。
        >
        > ### WSGI的实现和部署
        >
        > 要使用WSGI，需要分别实现server角色和application角色。
        >
        > Application端的实现一般是由Python的各种框架来实现的，比如Django, web.py等，一般开发者不需要关心WSGI的实现，框架会会提供接口让开发者获取HTTP请求的内容以及发送HTTP响应。
        >
        > Server端的实现会比较复杂一点，这个主要是因为软件架构的原因。一般常用的Web服务器，如Apache和nginx，都不会内置WSGI的支持，而是通过扩展来完成。比如Apache服务器，会通过扩展模块mod_wsgi来支持WSGI。Apache和mod_wsgi之间通过程序内部接口传递信息，mod_wsgi会实现WSGI的server端、进程管理以及对application的调用。Nginx上一般是用proxy的方式，用nginx的协议将请求封装好，发送给应用服务器，比如uWSGI，应用服务器会实现WSGI的服务端、进程管理以及对application的调用。
        >
        > 
        >
        > 作者：iqunqunqun
        > 链接：https://www.jianshu.com/p/c66d3adeaaed
        > 来源：简书
        > 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

    2. 我也不知道为什么，这个包不可以直接用 pip 安装。解决方法如下

    3. 下载mod_wsgi Python的插件 http://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi

    4. 如 mod_wsgi‑4.5.15+ap24vc14‑cp36‑cp36m‑win_amd64.whl

        1. 这个插件对应的Apache版本是24 VC是14
        2. Python版本是3.6
        3. 64位系统
        4. 在下载时要选择相应的版本，否则Apache启动时会有问题  ！！！！

    5. 这里可以直接改扩展名为`zip`解压（但是这样好像不好用，因为接下来不好操作，如果需要  .so 文件的话可以尝试一下）。

    6. 我的方法是，在  .whl 文件所在的文件夹（不行的话可以，把下载的.whl文件复制到python\Scripts下使用 ）打开 cmd ，执行

        ```python
        pip3 install "mod_wsgi-4.5.15+ap24vc14-cp36-cp36m-win_amd64.whl"
        ```

    7. 进行安装在安装成功后在python的安装目录的\scripts文件夹下运行

        ```python
        mod_wsgi-express module-config
        ```

    8. 得到如下结果：

    9. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220419215956187.png" alt="image-20220419215956187" style="zoom:80%;" />   

    10. 将这三行配置复制到 httpd.conf 文件中去，具体位置如图（在那一堆 load 之后即可）：

    11. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220419220137962.png" alt="image-20220419220137962" style="zoom: 50%;" />      

6. *第五步*：补充配置 httpd.conf 文件

    1. 在 httpd.conf 文件中找到 Include conf/extra/httpd-vhosts.conf 将它前边的 `#` 删掉，即取消注释，使用 vhost （virtual host，虚拟主机）

        <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220420111409841.png" alt="image-20220420111409841" style="zoom:67%;" />   

    2. 然后在 conf/extra 目录下找到 “httpd-vhost.conf”文件，打开进行配置

        <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220420111608902.png" alt="image-20220420111608902" style="zoom:67%;" />    

    3. 在文件末尾添加如下配置：

        ```apl
        Listen 8080
        # 监听8080端口
        
        <VirtualHost *:8080>
             DocumentRoot "D:/Selfdate/Python/project_blog"		# 配置到自己的项目目录
             WSGIScriptAlias / D:/Selfdate/Python/project_blog/blog.py		#替换成自己的项目主文件
             Alias /static/ D:/Selfdate/Python/project_blog/static		# 有static的话就如实填写，没有的话创建一个空的写在这里即可
             Alias /templates/ D:/Selfdate/Python/project_blog/templates		# 有templates的话就如实填写
             AddType text/html .py
             ServerName localhost		# 服务名称
             ErrorLog "D:/Selfdate/Python/project_blog/blog_error.log"		# 错误日志，不需要创建，只需要指定位置即可，会自动创建的
             <Directory D:/Selfdate/Python/project_blog>		# 设置权限，需要替换为自己的项目根目录
             Options FollowSymLinks
             AllowOverride None
             Order deny,allow
             Allow from all
             Require all granted
             </Directory>
        </VirtualHost>
        ```

        <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220420111803270.png" alt="image-20220420111803270" style="zoom:67%;" />

7. *第六步*：添加代码

    1. 在自己的项目主文件的开头添加如下配置

        ```python
        import os,sys
        abspath = os.path.dirname(__file__)
        sys.path.append(abspath)
        os.chdir(abspath)
        ```

    2. 然后重启 apache 服务，`httpd -k restart`。

    3. 在网站上打开 `http://localhost:8080` ，即可看到相应的网页页面。

    4. 如果找不到网页，查看错误日志发现 

        > mod_wsgi (pid=21452): Target WSGI script 'D:/Apache22/htdocs/webapp/webapp.py' does not contain WSGI application 'application'

        1. 需要将项目主文件（py文件）中的 `app=web.application(urls,globals())` 改为：

            ```python
            app=web.application(urls,globals())
            application = app.wsgifunc()		# 这句话不加会报错
            ```

        2. py文件中的一下代码,可有可无了.

            ```python
            if __name__ == '__main__':
            	application.run()
            ```

8. 到此，配置完毕，重启 apache 服务即可。如有不懂，欢迎留言。

## 出现过的问题与解决办法

1. Apache 无法启动

    1. ![image-20220421102225625](https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421102225625.png)    
    2. 问题就出在 `PYTHONHOME` 和 `PYTHONPATH` 。这两个说的是系统 寻找 python 的路径，如果在安装 python 时向系统变量中添加过 pythonprth 和 pythonhome 应该就不会出现这样的问题。
    3. 解决办法：自己手动向系统环境变量中添加 python 的路径（==注意：不要向用户变量中添加==），添加 （1）python 的根目录“\python”（2）python 目录下的 Scripts 目录。:happy:
    4. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421103155094.png" alt="image-20220421103155094" style="zoom: 50%;" />  点击徽标键，直接（不需要光标）输入“环境”即可。  
    5. 按如顺序操作即可，如有不懂，可自行查阅相关资料。（这种的网上教程很多的）
    6. 注意一点：多个路径之间要用英文的分号 `;` 间隔开。
    7. 用户变量和下边的系统变量操作同理，这里不再赘述。
    9. 这么设置之后 apache 应该就可以用了。

2. Apache 可以启动，但是启动后相应的页面无法访问，显示 404 `The requested URL was not found on this server`。

    1. 原因一：`httpd.conf` 文件中的 `Include conf/extra/httpd-vhosts.conf` 未添加注释。

        1. 在文件中找到，然后添加修改即可。
        2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421104420727.png" alt="image-20220421104420727" style="zoom:67%;" />  对应如图位置。

    2. 原因二：文件权限设置有问题：

        1. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421104738028.png" alt="image-20220421104738028" style="zoom:67%;" />   

    3. 原因三：这个是我的问题，问题出在我的 `.py` 文件中：

        1. ```python
            # -*- coding: utf-8 -*-
            # filename: main.py
            
            import os,sys
            abspath = os.path.dirname(__file__)
            sys.path.append(abspath)
            os.chdir(abspath)
            
            import web
            from handle import Handle
            
            urls = (
                
                '/wx', 'Handle',
            )
            
            class Handle(object):
                def GET(self):
                    return "hello, this is handle view"
            
            if __name__ == '__main__':
                app = web.application(urls, globals())	# 这个放错位置了，应该往前放，或者说是在这个 if 语句之外
                application = app.wsgifunc()	# 同上，放错位置了，这两句话都要有，否则也会出问题 problems 
                app.run()
            ```

        2. 正确写法：（仅供参考）

        3. ```python
            # -*- coding: utf-8 -*-
            # filename: main.py
            
            import os,sys
            abspath = os.path.dirname(__file__)
            sys.path.append(abspath)
            os.chdir(abspath)
            
            import web
            from handle import Handle
            
            urls = (
                
                '/wx', 'Handle',
            )
            
            app = web.application(urls, globals())
            application = app.wsgifunc()
            
            class Handle(object):
                def GET(self):
                    return "hello, this is handle view"
            
            if __name__ == '__main__':
                app.run()
            ```

3. 这就是我所遇到的问题，如果你还遇到了问题可以上网查找，或者给我留言。Leave me a message ！



# 微信公众号—实现自动回复：

## 准备：

- apache
- Python
- Mysql（不必要）
- natapp
- 微信公众号调试工具 — [[微信公众平台接口调试工具 (qq.com)](https://mp.weixin.qq.com/debug/)]
- 注册微信公众号
- 注意：首先检查自己电脑里有没有reply和receive两个python的包，如果有的话就卸载掉（也可以将接下来的所有reply和receive替换成其他名词），没有的话就算了
    - 检查：在cmd中输入 `pip show reply` 或者 `pip list`，查看结果即可。
    - 卸载：在cmd中输入 `pip uninstall reply` 即可。
    - 以“reply”为例，receive同理。


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

    1. 到这里的时候，可以先去连接公众号的接口
       
        1. 网址：[公众号 (qq.com)](https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&token=1256988445&lang=zh_CN)
        2. 登陆自己的公众号之后，找到基本配置并打开
        3. ![image-20220421105804719](https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421105804719.png)      
        4. ![image-20220421110116055](https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220421110116055.png)    
        5. 如果填写完毕后点击 `提交` 后显示 token 验证失败：常见的问题及解决办法如下：
            1. python 版本问题：参考链接：[(8条消息) 微信公众平台 token 验证失败 python3_Jason_WangYing的博客-CSDN博客](https://blog.csdn.net/Jason_WangYing/article/details/106268219)
            2. 国外的服务器（natapp是国内，挺好用的），速度慢，多试几次就好了。
            3. 还有，但是，我就先不写了，可以上网上自己先查阅一下。
        
    3. 消息传送格式：

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

    4. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/0" alt="img" style="zoom:67%;" />大致思路

    5. 修改 blog.py 文件

        1. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417150844517.png" alt="image-20220417150844517" style="zoom: 67%;" />  
        2. <img src="https://gitee.com/lidonggui/typoranotes_or_pictures/raw/master/pictures/image-20220417150901636.png" alt="image-20220417150901636" style="zoom:67%;" />  

    6. 增加 handle.py 内容

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

    7. 编辑 receive.py 的内容：

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

    8. 编辑 reply.py 的内容：

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























































