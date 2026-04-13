---
title: Golang技术幻灯片的查看方法
url: https://tonybai.com/2015/08/22/how-to-view-golang-tech-slide/
published: '2015-08-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Golang技术幻灯片的查看方法

随着[go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)的发布，[golang](http://tonybai.com/tag/golang)在世界各地日益受到欢迎，[golang](http://golang.org)技术鼓吹者在世界各地举办各种级别的技术会议(从[GopherCon](http://www.gophercon.com/)大会到小小的meetup)，并在会议上分享自己的技术心得和技术想法。

Golang相关的技术幻灯片有多种格式，以.ppt, .pdf和.slide为主。ppt、pdf自然不必多说，需要直接下载查看。

.slide是随着golang诞生而出现的一种[present](http://golang.org/x/tools/cmd/present)格式，Go核心开发成员似乎十分喜欢以这种格式分享Go语言。在Golang官方，几乎所有技术会议的talk幻灯片均是以.slide形式提供的。

.slide文件通过web服务查看，目前似乎尚无本地工具可以render slide文件。

目前已知的render .slide文件的服务包括：

- talks.golang.org

- go-talks.appspot.com

talks.golang.org是golang官方的服务，用于查看Go core team发表的各次技术演讲的幻灯片资料，按年份归档。

其他Go开发者用.slide形式编写的文件可以放在自己的github.com repo中，并使用go-talks.appspot.com这个第三方服务render。

比如：[Dave Cheney](http://dave.cheney.net)将自己的performance-without-the-event-loop.slide存放在 github.com/davecheney/presentations下，那我们就可以通过如下url查看该slide render后的形式：

http://go-talks.appspot.com/github.com/davecheney/presentations/performance-without-the-event-loop.slide

不过由于appspot.com是Go appengine托管服务，国内无法访问，因此前期搭建了一个[go-talks的镜像](http://tonybai.com/2015/07/27/make-a-mirror-of-gotalks-appsport-app/)go-talks.tonybai.com，国内程序员可以无需fanqiang就可以访问(由于go-talks.tonybai.com托管主机内存不大，常常出现超时甚至crash现象，望谅解)。

因此要想看到上述slide，可以访问：

http://go-talks.tonybai.com/github.com/davecheney/presentations/performance-without-the-event-loop.slide

对于talks.golang.org上的slide，比如：

http://talks.golang.org/2015/gogo.slide

如果无法fanqiang又如何访问呢？这样行么？

http://go-talks.tonybai.com/talks.golang.org/2015/gogo.slide

结果告诉我们这样是不行的。那如何访问呢？

好在talks.golang.org上的slide都放在了github.com上，repo为https://github.com/golang/talks，上述那个gogo.slide，我们可以通过：

http://go-talks.tonybai.com/github.com/github.com/golang/talks/2015/gogo.slide访问。

**补充**：

“相濡以沫”网友在评论中给出了一种在本地查看.slide的方法：

1、go get -u golang.org/x/tools/cmd/present //需翻墙

2、go install golang.org/x/tools/cmd/present，将present可执行程序放入$GOBIN或$GOPATH/bin中

3、下载你要查看的.slide，比如go get github.com/golang/talks，cd到talks所在目录，执行./present，你会看到如下结果：

$present

2015/08/23 19:34:51 Open your web browser and visit http://127.0.0.1:3999

打开浏览器，如果要查看当前目录下的2015/tricks.slide，则在浏览器里输入：http://127.0.0.1:3999/2015/tricks.slide即可查看该.slide文件。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

clone到本地，用present命令就可以开个本地的web服务了啊

不错，学习了。3ks

本地架的时候，用https

发现有2个写死的地方

src/golang.org/x/tools/cmd/present/local.go

line 62

origin := &url.URL{Scheme: “http”}

写死的 http

src/golang.org/x/tools/godoc/static/static.go

2347行

var websocket = new WebSocket(‘ws://’ + window.location.host + ‘/socket’);

写死的ws

是否可以考虑前端加一个nginx代理，将https转成upstream(present服务)的http协议。如果不行，只能看看是否可以通过改代码来实现你自己的需求了。

bigwhite, 是go里没适配好这个，已经提issue了， 我自己改代码是能支持了

前端是通过代理的，但go里写死的连ws://，不适配wss://