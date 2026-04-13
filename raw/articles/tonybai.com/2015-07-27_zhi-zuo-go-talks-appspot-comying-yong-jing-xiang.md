---
title: 制作go-talks.appspot.com应用镜像
url: https://tonybai.com/2015/07/27/make-a-mirror-of-gotalks-appsport-app/
published: '2015-07-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 制作go-talks.appspot.com应用镜像

[Go语言](http://tonybai.com/tag/go)号称面向工程：对工程目录组织、代码风格（gofmt）、文档（生成）都制定的相应的“**标准**”，并提供了相应的工具帮助开发者满足这些工程specs。

gofmt用于格式化代码，形成统一代码风格。

godoc.org用于查看标准库或repo的doc。

go-talks.appspot.com则是用来查看go slide。

像[godoc](http://godoc.org)和[go-talks](http://go-talks.appspot.com)这种以服务形式提供文档查看的形式不得不说是[golang](http://golang.org)的又一创新。

这几年Golang的开发者们是非常勤奋的，为了推广Golang，他们撰写博客，编写文档，并四处布道，积累下许多有价值的文档，这些文档多以 Gopher所特有的[present格式](http://godoc.org/golang.org/x/tools/present)存在着，这些 present格式的文档以.slide、.article或.ext为后缀，通过go-talks.appspot.com提供的present渲染服 务浏览，并且支持github.com repo中的slide文件。Go开发者们只需要将自己写好的slide文件存放在自己github.com上的repo中，就可以随时随地在世界各地打 开这类present文件为大家布道了。

不过来到中国大陆后，事情就没那么顺利了，因为appspot.com在大陆是无法直接访问的，你懂得哦。为了观看这些大牛的slide，内地的Go程序员只能四处寻找出(fan)国(qiang)工具，但这毕竟不是十分方便。

上周末[@开发者头条](http://weibo.com/kaifazhetoutiao)分享了“[why Go is fast? [Slide] High performance servers without the event loop (Golang)](http://go-talks.tonybai.com/github.com/davecheney/presentations/performance-without-the-event-loop.slide)”这个[Dave Cheney](http://dave.cheney.net)在O'Reilly [OSCON](http://www.oscon.com)上分享的Go slide，但因为链接被qiang，无法直接观看。于是就想到能不能制作一个go-talks.appspot.com的镜像站点，让国内Go程序员也 能享受些福利呢？于是乎我就开始了镜像制作的探索过程。

**一、在本地搭建go-talks.appspot.com镜像**

present格式类似于[markup](http://en.wikipedia.org/wiki/Markup_language)，是一种标记语言，只是present格式更多用来制作slide。

golang.org/x/tools/present提供了present文件格式的解析库，最初本以为需要从头开始写server，并利用 present库解析，写模板和javascript实现类似翻页等功能呢。但后来居然在[gddo repo](https://github.com/golang/gddo/)，也就是godoc.org的源码工程中找到了go-talks.appsport.com站点的源码: talksapp。

不过talksapp是运行在[google app engine](http://appengine.google.com)上的应用，要将其直接运行在standalone server上是否可行呢？是否需要改造？这些都是未知数，不过有了源码自然是很好的。我们先来试试这个程序是否能在本地运行起来。

首先下载gddo repo：

$go get github.com/golang/gddo/

$cd $GOPATH/src/github.com/golang/gddo/talksapp

talksapp的主页文档似乎有些out-dated，我并没有找到config.go.template。

但按照文档要求，需要下载Go App Engine SDK，这个需要搭梯子。在https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Go页面根据您的平台版本下载最新Go SDK版本。解压后，先放在那里不动。

根据talksapp文档，第三步就应该是sh setup.sh。setup.sh中get两个repo均在qiang外，需要梯子才能下载。

setup.sh正确执行之后，我们用go_appengine下dev_appserver.py来运行talksapp：

$dev_appserver.py ~/Test/GoToolsProjects/src/github.com/golang/gddo/talksapp

INFO 2015-07-27 08:25:09,076 api_server.py:205] Starting API server at: http://localhost:51801

INFO 2015-07-27 08:25:09,080 dispatcher.py:197] Starting module "default" running at: http://localhost:8080

INFO 2015-07-27 08:25:09,083 admin_server.py:118] Starting admin server at: http://localhost:8000

/Users/tony/Test/GoToolsProjects/src/appengine/google/appengine/tools/devappserver2/mtime_file_watcher.py:115: UserWarning: There are too many files in your application for changes in all of them to be monitored. You may have to restart the development server to see some changes to your files.

'There are too many files in your application for '

ERROR 2015-07-27 08:25:11,941 http_runtime.py:380] bad runtime process port ['']

**2015/07/27 08:25:11 secret.json needs to define ClientID and ClientSecret**

使用浏览器访问localhost:8080，得到的页面中也只是有些错误日志，日志与上面最后两行相同。从错误日志来看，似乎需要配置一下secret.json这个文件，至少ClientID和ClientSecret不能为空。

我就随意配置两个值(这两个值似乎应该是github.com的账号和密码，用于OAuth2，如果随意配置无法成功，那建议配置上真实的账号和密码)，看看是否可以访问：

{

"ClientID": "xx",

"ClientSecret": "yy"

}

这回再执行talksapp就不再报错了。用浏览器访问localhost:8080, go-talks的页面顺利正常显示出来！看来在本地是可以运行的哦！

我们再来测试一下访问github.com上的一个slide,地址如下：

http://localhost:8080/github.com/gophercon/2015-talks/Dmitry_Vyukov_-_Go_Dynamic_Tools/tools.slide

加载有些慢，有些时候提示：


canceled: Deadline exceeded (timeout)

试了几次后，居然加载成功了！又试了几个slide，除了有些慢，都是成功的。看来talksapp是可以在standalone主机上运行的。

**二、在vps上部署go-talks镜像**

虽然在本机上可以正常浏览Golang大牛们的slide的了，但毕竟放在local上不是很方便，离开这台机器又无法访问了。广大内地go程序员们依旧 生活在“水深火热”中，在“分享经济”兴起的今天，我想也力所能及的做些贡献吧。于是想到了将这个镜像部署到我的[blog vps](https://www.digitalocean.com/?refcode=bff6eed92687)上，这样大家就可以自由浏览golang slide了。

我的vps放在了[DigitalOcean](https://www.digitalocean.com/?refcode=bff6eed92687)上(Ubuntu 14.04 server amd64)，配置较低，平时仅仅作为blog托管主机。不过放一个go-talks镜像应该还是可以满足的，也可以更充分“压榨”一下DO的资源。

于是乎，我就按照上面的步骤将talksapp安装在了vps上。考虑到talksapp作为一个守护进程，又安装了supervisor对其进行管理：

/etc/supervisor/conf.d/go-talks.conf

[program:go-talks]

environment=GOROOT=/root/.bin/go142

environment=GOPATH=/root/go-talks

directory=/root/go-talks/src/github.com/golang/gddo/talksapp

command=/root/go-talks/go_appengine/goapp serve

autostart=true

autorestart=true

startsecs=3

这里没有使用dev_appserver.py，而是用了两位一个程序goapp，通过在talksapp目录下执行goapp serve来启动这个"GAE"服务。现在vps上启动了localhost:8080服务，但外面的人还是无法访问到这个服务。

如果要对外发布这个服务，我需要一个域名，考虑到自己已有的blog域名，为了快速开通服务，我添加了一个二级域名：go-talks.tonybai.com，模仿go-talks.appspot.com。

我们还需要调整一下apache2 server。原先的apache2 server只是为blog(wordpress)提供服务，现在我们需要将go-talks.tonybai.com映射到主机内部的8080端口服务 上，这就需要开启apache2的反向代理功能，对apache2也不是很熟悉，于是在网上找到了一段配置，补充到/etc/apache2 /apache2.conf中：

<VirtualHost *:80>

ServerName go-talks.tonybai.com

ProxyPreserveHost On

ProxyRequests Off

ProxyPass / http://localhost:8080/

ProxyPassReverse / http://localhost:8080/

</VirtualHost>

Include /etc/phpmyadmin/apache.conf

重启apache2，出现下面错误：

root@tonybai:/etc/apache2# sudo service apache2 restart

* Restarting web server apache2 [fail]

* The apache2 configtest failed.

Output of config test was:

AH00526: Syntax error on line 85 of /etc/apache2/apache2.conf:

Invalid command 'ProxyPreserveHost', perhaps misspelled or defined by a module not included in the server configuration

Action 'configtest' failed.

The Apache error log may have more information.

似乎是反向代理需要更多apache2 module才能运行，于是：

sudo a2enmod proxy

sudo a2enmod proxy_http

再重启apache2，这回ok了。

在DNS服务商内已经添加了go-talks.tonybai.com这个域名，但由于国内DNS生效时间较慢，为了测试服务是否ok，我修改了 hosts文件，手动将go-talks.tonybai.com指向vps的公网地址。接下来访问go-talks.tonybai.com这个地址， 镜像制作成功了！ 又测试了几个slide，均正确生成！速度稍慢，那是因为vps的一般延迟都在2600ms左右。

我的VPS性能不高，大家访问时也许会感觉较慢，但有胜于无！

最后再重申一下go-talks.tonybai.com的使用方法：

**如果某个分享链接为：go-talks.appspot.com/xxx/yy/zz/foo.slide，那么将该地址替换为:go- talks.tonybai.com/xxx/yy/zz/foo.slide即可。也就是将appspot换成tonybai，其他不变。**

该服务已经利用[监控宝](http://jiankongbao.com)监控起来了，如果出现问题（比如网络或资源不足的问题），我会及时处理。但这里不保证100%可用哦！希望大家友好使用，不要拍砖！

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论