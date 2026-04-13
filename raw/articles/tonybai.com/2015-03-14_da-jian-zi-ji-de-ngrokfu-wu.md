---
title: 搭建自己的ngrok服务
url: https://tonybai.com/2015/03/14/selfhost-ngrok-service/
published: '2015-03-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 搭建自己的ngrok服务

在国内开发[微信公众号](https://mp.weixin.qq.com)、[企业号](http://qydev.weixin.qq.com/)以及做前端开发的朋友想必对[ngrok](https://github.com/inconshreveable/ngrok)都不陌生吧，就目前来看，ngrok可是最佳的在内网调试微信服务的tunnel工 具。记得今年春节前，ngrok.com提供的服务还一切正常呢，但春节后似乎就一切不正常了。ngrok.com无法访问，ngrok虽然能连上 ngrok.com提供的服务，但微信端因为无法访问ngrok.com，导致消息一直无法发送到我们的服务地址上，比如xxxx.ngrok.com。 这一切都表明，ngork被墙了。没有了ngrok tunnel，一切开始变得困难且没有效率起来。内网到外部主机部署和调试是一件慢的让人想骂街的事情。

ngrok不能少。ngrok以及其服务端ngrokd都是开源的，之前我也知道通过源码可以自搭建ngrok服务。请求搜索引擎后，发现国内有个朋友已经搭建了一个www.tunnel.mobi的ngrok公共服务，与ngrok.com类似，我也实验了一下。

编写一个ngrok.cfg，内容如下：

server_addr: "tunnel.mobi:44433"

trust_host_root_certs: true

用ngrok最新客户端1.7版本执行如下命令：

$ngrok -subdomain tonybaiexample -config=ngrok.cfg 80

可以顺利建立一个tunnel，用于本机向外部提供"tonybaiexample.tunnel.mobi"服务。

Tunnel Status online

Version 1.7/1.7

Forwarding http://tonybaiexample.tunnel.mobi -> 127.0.0.1:80

Forwarding https://tonybaiexample.tunnel.mobi -> 127.0.0.1:80

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

而且国内的ngrok服务显然要远远快于ngrok.com提供的服务，消息瞬间即达。

但这是在公网上直接访问的结果。放在公司内部，我看到的却是另外一个结果：

Tunnel Status reconnecting

Version 1.7/

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

我们无法从内网建立tunnel，意味着依旧不方便和低效，因为很多基础服务都在内网部署，内外网之间的交互十分不便。但内网连不上tunnel.mobi也是个事实，且无法知道原因，因为看不到server端的连接错误日志。

于是我决定自建一个ngrok服务。

**一、准备工作**

搭建ngrok服务需要在公网有一台vps，去年年末曾经在Amazon申请了一个体验主机[EC2](https://aws.amazon.com/cn)，有公网IP一个，这次就打算用这个主机作为ngrokd服务端。

需要一个自己的域名。已有域名的，可以建立一个子域名，用于关联ngrok服务，这样也不会干扰原先域名提供的服务。(不用域名的方式也许可以，但我没有试验过。）

搭建的参考资料主要来自下面三个：

1) ngrok的官方SELFHOST指南：https://github.com/inconshreveable/ngrok/blob/master/docs/SELFHOSTING.md

2) 国外一哥们的博客：http://www.svenbit.com/2014/09/run-ngrok-on-your-own-server/

3) "海运的博客"中的一篇文章：http://www.haiyun.me/archives/1012.html

**二、实操****步骤**

我的AWS EC2实例安装的是[Ubuntu ](http://tonybai.com/tag/ubuntu)Server 14.04 x86_64，并安装了[golang](http://tonybai.com/tag/golang) 1.4（go version go1.4 linux/amd64）。Golang是编译ngrokd和ngrok所必须的，建议直接从golang官方下载对应平台的二进制安装包（国内可以从 golangtc.com上下载，速度慢些罢了）。

**1、下载ngrok源码**

（GOPATH=~/goproj)

$ mkdir ~/goproj/src/github.com/inconshreveable

$ git clone https://github.com/inconshreveable/ngrok.git

$ export GOPATH=~/goproj/src/github.com/inconshreveable/ngrok

**2、生成自签名证书**

使用ngrok.com官方服务时，我们使用的是官方的SSL证书。自建ngrokd服务，我们需要生成自己的证书，并提供携带该证书的ngrok客户端。

证书生成过程需要一个**NGROK_BASE_DOMAIN**。 以ngrok官方随机生成的地址693c358d.ngrok.com为例，其NGROK_BASE_DOMAIN就是"ngrok.com"，如果你要 提供服务的地址为"example.tunnel.tonybai.com"，那NGROK_BASE_DOMAIN就应该 是"tunnel.tonybai.com"。

我们这里以NGROK_BASE_DOMAIN="tunnel.tonybai.com"为例，生成证书的命令如下：

$ cd ~/goproj/src/github.com/inconshreveable/ngrok

$ openssl genrsa -out rootCA.key 2048

$ openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=tunnel.tonybai.com" -days 5000 -out rootCA.pem

$ openssl genrsa -out device.key 2048

$ openssl req -new -key device.key -subj "/CN=tunnel.tonybai.com" -out device.csr

$ openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 5000

执行完以上命令，在ngrok目录下就会新生成6个文件：

-rw-rw-r– 1 ubuntu ubuntu 1001 Mar 14 02:22 device.crt

-rw-rw-r– 1 ubuntu ubuntu 903 Mar 14 02:22 device.csr

-rw-rw-r– 1 ubuntu ubuntu 1679 Mar 14 02:22 device.key

-rw-rw-r– 1 ubuntu ubuntu 1679 Mar 14 02:21 rootCA.key

-rw-rw-r– 1 ubuntu ubuntu 1119 Mar 14 02:21 rootCA.pem

-rw-rw-r– 1 ubuntu ubuntu 17 Mar 14 02:22 rootCA.srl

ngrok通过bindata将ngrok源码目录下的assets目录（资源文件）打包到可执行文件(ngrokd和ngrok)中 去，assets/client/tls和assets/server/tls下分别存放着用于ngrok和ngrokd的默认证书文件，我们需要将它们替换成我们自己生成的：(因此这一步务必放在编译可执行文件之前)

cp rootCA.pem assets/client/tls/ngrokroot.crt

cp device.crt assets/server/tls/snakeoil.crt

cp device.key assets/server/tls/snakeoil.key

**3、编译ngrokd和ngrok**

在ngrok目录下执行如下命令，编译ngrokd：

$ make release-server

不过在我的AWS上，出现如下错误：

GOOS="" GOARCH="" go get github.com/jteeuwen/go-bindata/go-bindata

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/client/assets/assets_release.go \

assets/client/…

make: bin/go-bindata: Command not found

make: *** [client-assets] Error 127

go-bindata被安装到了$GOBIN下了，go编译器找不到了。修正方法是将$GOBIN/go-bindata拷贝到当前ngrok/bin下。

$ cp /home/ubuntu/.bin/go14/bin/go-bindata ./bin

再次执行make release-server。

[~/goproj/src/github.com/inconshreveable/ngrok$](mailto:ubuntu@ip-172-31-4-131:%7E/goproj/src/github.com/inconshreveable/ngrok$) make release-server

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/client/assets/assets_release.go \

assets/client/…

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/server/assets/assets_release.go \

assets/server/…

go get -tags 'release' -d -v ngrok/…

code.google.com/p/log4go (download)

go: missing Mercurial command. See [http://golang.org/s/gogetcmd](http://golang.org/s/gogetcmd)

**package code.google.com/p/log4go: exec: "hg": executable file not found in $PATH**

github.com/gorilla/websocket (download)

github.com/inconshreveable/go-update (download)

github.com/kardianos/osext (download)

github.com/kr/binarydist (download)

github.com/inconshreveable/go-vhost (download)

github.com/inconshreveable/mousetrap (download)

github.com/nsf/termbox-go (download)

github.com/mattn/go-runewidth (download)

github.com/rcrowley/go-metrics (download)

Fetching [https://gopkg.in/yaml.v1?go-get=1](https://gopkg.in/yaml.v1?go-get=1)

Parsing meta tags from [https://gopkg.in/yaml.v1?go-get=1](https://gopkg.in/yaml.v1?go-get=1) (status code 200)

get "gopkg.in/yaml.v1": found meta tag main.metaImport{Prefix:"gopkg.in/yaml.v1", VCS:"git", RepoRoot:["https://gopkg.in/yaml.v1"](https://gopkg.in/yaml.v1)} at [https://gopkg.in/yaml.v1?go-get=1](https://gopkg.in/yaml.v1?go-get=1)

gopkg.in/yaml.v1 (download)

make: *** [deps] Error 1

又出错！提示找不到hg，原来是aws上没有安装hg。install hg后（sudo apt-get install mercurial），再编译。

$ make release-server

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/client/assets/assets_release.go \

assets/client/…

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/server/assets/assets_release.go \

assets/server/…

go get -tags 'release' -d -v ngrok/…

code.google.com/p/log4go (download)

go install -tags 'release' ngrok/main/ngrokd

同样编译ngrok:

$ make release-client

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/client/assets/assets_release.go \

assets/client/…

bin/go-bindata -nomemcopy -pkg=assets -tags=release \

-debug=false \

-o=src/ngrok/server/assets/assets_release.go \

assets/server/…

go get -tags 'release' -d -v ngrok/…

go install -tags 'release' ngrok/main/ngrok

AWS上ngrokd和ngrok被安装到了$GOBIN下。

**三、调试**

1、**启动ngrokd**

$ ngrokd -domain="tunnel.tonybai.com" -httpAddr=":8080" -httpsAddr=":8081"

[03/14/15 04:47:24] [INFO] [registry] [tun] No affinity cache specified

[03/14/15 04:47:24] [INFO] [metrics] Reporting every 30 seconds

[03/14/15 04:47:24] [INFO] Listening for public http connections on [::]:8080

[03/14/15 04:47:24] [INFO] Listening for public https connections on [::]:8081

[03/14/15 04:47:24] [INFO] Listening for control and proxy connections on [::]:4443

… …

**2、公网连接ngrok****d**

将生成的ngrok下载到自己的电脑上。

创建一个配置文件ngrok.cfg，内容如下：

server_addr: "tunnel.tonybai.com:4443"

trust_host_root_certs: false

执行ngrok：

$ ngrok -subdomain example -config=ngrok.cfg 80

Tunnel Status reconnecting

Version 1.7/

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

连接失败。此刻我的电脑是在公网上。查看ngrokd的日志，没有发现连接到达Server端。试着在本地ping tunnel.tonybai.com这个地址，发现地址不通。难道是DNS设置的问题。之前我只是设置了"*.tunnel.tonybai.com"的A地址，并未设置"tunnel.tonybai.com"。于是到DNS管理页面，添加了"tunnel.tonybai.com"的A记录。

待DNS记录刷新OK后，再次启动ngrok：

Tunnel Status online

Version 1.7/1.7

Forwarding http://epower.tunnel.tonybai.com:8080 -> 127.0.0.1:80

Forwarding https://epower.tunnel.tonybai.com:8080 -> 127.0.0.1:80

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

这回连接成功了！

**3、内网连接ngrokd**

将ngrok拷贝到内网的一台PC上，这台PC设置了公司的代理。

按照同样的步骤启动ngrok：

$ ngrok -subdomain example -config=ngrok.cfg 80

Tunnel Status reconnecting

Version 1.7/

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

不巧，怎么又失败了！从Server端来看，还是没有收到客户端的连接，显然是连接没有打通公司内网。从我自己的squid代理服务器来看，似乎只有443端口的请求被公司代理服务器允许通过，4443则无法出去。

1426301143.558 9294 10.10.126.101 TCP_MISS/000 366772 CONNECT api.equinox.io:443 – DEFAULT_PARENT/proxy.xxx.com - 通过了

1426301144.441 27 10.10.126.101 TCP_MISS/000 1185 CONNECT tunnel.tonybai.com:4443 – DEFAULT_PARENT/proxy.xxx.com - 似乎没有通过

只能修改server监听端口了。将-tunnelAddr由4443改为443(注意AWS上需要修改防火墙的端口规则，这个是实时生效的，无需重启实例)：

$ sudo ngrokd -domain="tunnel.tonybai.com" -httpAddr=":8080" -httpsAddr=":8081" -tunnelAddr=":443"

[03/14/15 04:47:24] [INFO] [registry] [tun] No affinity cache specified

[03/14/15 04:47:24] [INFO] [metrics] Reporting every 30 seconds

[03/14/15 04:47:24] [INFO] Listening for public http connections on [::]:8080

[03/14/15 04:47:24] [INFO] Listening for public https connections on [::]:8081

[03/14/15 04:47:24] [INFO] Listening for control and proxy connections on [::]:443

… …

将ngrok.cfg中的地址改为443：

server_addr: "tunnel.tonybai.com:443"

再次执行ngrok客户端：

Tunnel Status online

Version 1.7/1.7

Forwarding http://epower.tunnel.tonybai.com:8080 -> 127.0.0.1:80

Forwarding https://epower.tunnel.tonybai.com:8080 -> 127.0.0.1:80

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

这回成功连上了。

**4、80端口**

是否大功告成了呢？我们看看ngrok的结果，总感觉哪里不对呢？噢，转发的地址怎么是8080端口呢？为何不是80？微信公众号/企业号可只是支持80端口啊！

我们还需要修改一下Server端的参数，将-httpAddr从8080改为80。

$ sudo ngrokd -domain="tunnel.tonybai.com" -httpAddr=":80" -httpsAddr=":8081" -tunnelAddr=":443"

这回再用ngrok连接一下：

Tunnel Status online

Version 1.7/1.7

Forwarding http://epower.tunnel.tonybai.com -> 127.0.0.1:80

Forwarding https://epower.tunnel.tonybai.com -> 127.0.0.1:80

Web Interface 127.0.0.1:4040

# Conn 0

Avg Conn Time 0.00ms

这回与我们的需求匹配上了。

**5、测试**

在内网的PC上建立一个简单的http server 程序：hello

//hello.go

package main

import "net/http"

func main() {

http.HandleFunc("/", hello)

http.ListenAndServe(":80", nil)

}

func hello(w http.ResponseWriter, r *http.Request) {

w.Write([]byte("hello!"))

}

$ go build -o hello hello.go

$ sudo ./hello

通过公网浏览器访问一下“http://epower.tunnel.tonybai.com”这个地址，如果你看到浏览器返回"hello!"字样，那么你的ngrokd服务就搭建成功了！

**四、注意事项**

客户端ngrok.cfg中server_addr后的值必须严格与-domain以及证书中的NGROK_BASE_DOMAIN相同，否则Server端就会出现如下错误日志：

[03/13/15 09:55:46] [INFO] [tun:15dd7522] New connection from 54.149.100.42:38252

[03/13/15 09:55:46] [DEBG] [tun:15dd7522] Waiting to read message

[03/13/15 09:55:46] [WARN] [tun:15dd7522] Failed to read message: remote error: **bad certificate**

[03/13/15 09:55:46] [DEBG] [tun:15dd7522] Closing

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

沙发。学习中

借个楼，http://ngrok.ciqiuwl.cn 国内的免费ngrok服务 自己搭建的！欢迎大家一起交流

太棒了，有空也搭建一个，我也是从过完年之后回来就用不了了，感觉灰常受伤

只能对特定端口吗？譬如文章所说的80端口、443端口等等？而且只能对但一台电脑访问？那么是不是这个穿透配置太麻烦了？而且外网也不能访问内网内的其他PC和打印机，还是有很大欠缺。倒不如直接上一个n2n就什么端口都OK了，包括提到的80口什么的所有口都可以通过了。

只能对特定端口吗？譬如文章所说的80端口、443端口等等？而且只能对单一台电脑访问？那么是不是这个穿透配置太麻烦了？而且外网也不能访问内网内的其他PC和打印机，还是有很大欠缺。倒不如直接上一个n2n就什么端口都OK了，包括提到的80口什么的所有口都可以通过了。

无论是ngrokd(服务端)还是ngrok(客户端）都支持任意端口的。ngrokd在命令行参数指定；ngrok端口可以在命令行参数指定，也可以在config文件中指定。ngrok原理可以参考本站《ngrok原理浅析》一文。

好用， 真是好用， thanks

博主 这个服务器还能用不？

我目前都是在用自己搭建的服务器，ngrok.com那个官服之前春节后就无法使用了。近期也没试。你可以自己试试看。

<img src="%E8%AF%B7%E8%BE%93%E5%85%A5%E5%9B%BE%5B%E7%94%9F%E7%97%85%5D%E7%89%87%E5%9C%B0%E5%9D%80" alt=" 片地址” />

新服务 natapp.cn 可以用了

赞！

搭好了，免费给大家使用 qydev.com

[嘻嘻]感谢楼主

使用国内的www.ngrok.cc并且有详细的视频使用教程

你好，我参考您的教程，自己搭建了ngrok，但是一直报Failed to read message: remote error: bad certificate，重新生成过很多次证书，检查过生成证书时的域名和客户端是一致的，但还是报证书错误，麻烦您给解答一下吧。万分感谢。

因为你的证书是自己生成的，所以客户端也得自行生成。

没错，需要专门自行生成。

这里汇总了大部分ngrok

http://likejin.cn/2015/12/08/ngrok%E6%9C%8D%E5%8A%A1/

我现在用的是金万维的NAT移动版，使用的还不错，各位可以试试。www.gnway.com可以免费注册。

花生壳不可以么

也许可以，这个我不清楚。目前在我的工作环境下，不具备安装和配置花生壳的网络条件，也就没有去try。

国内开源内网穿透 https://github.com/d1sm/xtunnel

这里有一篇很不错关于的ngrok的文章http://blog.lzp.name/archives/24

你好，

我现在在这一步：“连接失败。此刻我的电脑是在公网上。查看ngrokd的日志，没有发现连接到达Server端。试着在本地ping tunnel.tonybai.com这个地址，发现地址不通。难道是DNS设置的问题。之前我只是设置了”*.tunnel.tonybai.com”的A地址，并未设置”tunnel.tonybai.com”。于是到DNS管理页面，添加了”tunnel.tonybai.com”的A记录。”

请问如何到DNS管理页面来添加记录呢？

谢谢！！

文章里的tonybai.com只是一个示例，你需要使用自己的server和域名来搭建，将tonybai.com换成你自己的域名，并在你自己的域名管理页面添加相应信息。

ngrok 1.x 版本作者也说了有严重的内存、文件描述符泄漏等问题，国内的那些服务用的都是这个版本的客户端，稳定性很差（1.x版本目前作者已经停止了更新，也不再修复bug，2.x版本原作者没有开源，用于他自己的商业服务了）。有兴趣的话可以一起来参与另外一个开源项目 frp，和ngrok类似，目前实现了基本的功能，未来也会加入很多新的特性 https://github.com/fatedier/frp。

非常好

请问在编译时卡在 gopkg.in/inconshreveable/go-update.v0 (download) ，这要怎么处理呢

这个问题我没遇到过，你可以再确认一下你的本地是否安装了mercurial (hg)工具？

已经搞定了，是git版本太低了

go install -tags ‘release’ ngrok/main/ngrok

# github.com/gorilla/websocket

src/github.com/gorilla/websocket/conn.go:647: c.br.Discard undefined (type *bufio.Reader has no field or method Discard)

make: *** [client] 错误 2

应该是github.com/gorilla/websocket更新了版本，但这个版本没有通过编译的原因吧。可以试试自己手动先go get一个能通过编译的websocke版本。这就是为啥golang要加入vendor机制的原因了。这种问题常发生。

frp试了，不能通过内网的代理

自己搭建的ngrok1.7有严重内存泄露问题，直接使用natapp 吧。内存泄露已解决

都是国内顶尖大神啊 还有很多以及搭建好自己服务器开卖的了 很看好你们 支持

/root/ngrok/src/ngrok/server/control.go:229 (0x44b8af)

[10:30:13 CST 2017/04/19] [INFO] (ngrok/log.(*PrefixLogger).Info:83) [ctl:d24c848] [73f3c731ac901466f5ef39e3fe11373e] Shutdown complete

[10:30:13 CST 2017/04/19] [WARN] (ngrok/log.(*PrefixLogger).Warn:87) [ctl:d24c848] [73f3c731ac901466f5ef39e3fe11373e] Control::reader failed with error read tcp 116.7.98.224:6867: use of closed network connection: /root/ngrok/src/ngrok/server/control.go:229 (0x44b8af)

func.004: c.conn.Warn(“Control::reader failed with error %v: %s”, err, debug.Stack())

/usr/local/go/src/runtime/asm_amd64.s:401 (0x43bde5)

call16: CALLFN(·call16, 16)

/usr/local/go/src/runtime/panic.go:387 (0×413538)

gopanic: reflectcall(unsafe.Pointer(d.fn), deferArgs(d), uint32(d.siz), uint32(d.siz))

/root/ngrok/src/ngrok/server/control.go:246 (0x440f17)

(*Control).reader: panic(err)

/usr/local/go/src/runtime/asm_amd64.s:2232 (0x43df01)

goexit:

试了一下成功了，顺带说一下，编译的时候在国外主机上编译，国内网络下载库都下载不了

我搭好服务端OK可以用了，但是编译的Mac版客户软件本地执行报Segmentation fault: 11，请问有什么解决办法没有》

ngrok 1.x已经不再develop了，并且现有代码存在很多bug。我看有人和你遇到同样的问题：https://github.com/inconshreveable/ngrok/issues/458 我怀疑是不是可能与Go compiler的版本有关？你可以试试使用版本老旧一些的go compiler去编译ngrok，比如：go 1.4版本，看看是否还有这个段错误。

学习了，感谢！