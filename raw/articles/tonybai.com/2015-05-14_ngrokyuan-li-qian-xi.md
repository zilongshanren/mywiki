---
title: ngrok原理浅析
url: https://tonybai.com/2015/05/14/ngrok-source-intro/
published: '2015-05-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# ngrok原理浅析

之前在进行[微信Demo开发](http://tonybai.com/2014/12/18/access-validation-for-wechat-public-platform-dev-in-golang/)时曾用到过[ngrok](https://github.com/inconshreveable/ngrok)这个强大的tunnel(隧道)工具，ngrok在其github官方页面上的自我诠释是 “introspected tunnels to localhost"，这个诠释有两层含义：

1、可以用来建立public到localhost的tunnel，让居于内网主机上的服务可以暴露给public，俗称内网穿透。

2、支持对隧道中数据的introspection（内省），支持可视化的观察隧道内数据，并replay（重放）相关请求（诸如http请 求）。

因此[ngrok](http://tonybai.com/2015/03/14/selfhost-ngrok-service/)可以很便捷的协助进行服务端程序调试，尤其在进行一些Web server开发中。ngrok更强大的一点是它支持tcp层之上的所有应用协议或者说与应用层协议无关。比如：你可以通过ngrok实现ssh登录到内 网主 机，也可以通过ngrok实现远程桌面(VNC)方式访问内网主机。

今天我们就来简单分析一下这款强大工具的实现原理。ngrok本身是用[go语言](http://tonybai.com/tag/go)实现的，需要go 1.1以上版本编译。ngrok官方代码最新版为1.7，作者似乎已经完成了ngrok 2.0版本，但不知为何迟迟不放出最新代码。因此这里我们就以ngrok 1.7版本源码作为原理分析的基础。

**一、ngrok tunnel与ngrok部署**

网络tunnel（隧道）对多数人都是很”神秘“的概念，tunnel种类很多，没有标准定义，我了解的也不多（日常工作较少涉及），这里也就不 深入了。在《[HTTP权威指南](http://book.douban.com/subject/10746113/)》中有关于HTTP tunnel（http上承载非web流量）和SSL tunnel的说明，但ngrok中的tunnel又与这些有所不同。

ngrok实现了一个tcp之上的端到端的tunnel，两端的程序在ngrok实现的Tunnel内透明的进行数据交互。

![](../../assets/d57dde46d32b4f17.png)


ngrok分为client端(ngrok)和服务端(ngrokd)，实际使用中的部署如下：

![](../../assets/484f1d994d1e2013.png)


内网服务程序可以与ngrok client部署在同一主机，也可以部署在内网可达的其他主机上。ngrok和ngrokd会为建立与public client间的专用通道（tunnel）。

**二、****ngrok开发调试环境搭建**

在学习ngrok代码或试验ngrok功能的时候，我们可能需要搭建一个ngrok的开发调试环境。ngrok作者在[ngrok developer guide](https://github.com/inconshreveable/ngrok/blob/master/docs/DEVELOPMENT.md)中给出了步骤：

$> git clone [https://github.com/inconshreveable/ngrok](https://github.com/inconshreveable/ngrok)

$> cd ngrok

$> make client

$> make server

make client和make server执行后，会建构出ngrok和ngrokd的debug版本。如果要得到release版本，请使用make release-client和make release-server。debug版本与release版本的区别在于debug版本不打包 assets下的资源文件，执行时通过文件系统访问。

修改/etc/hosts文件，添加两行：

127.0.0.1 ngrok.me

127.0.0.1 test.ngrok.me

创建客户端配置文件debug.yml：

server_addr: ngrok.me:4443

trust_host_root_certs: false

tunnels:

test:

proto:

http: 8080

不过要想让ngrok与ngrokd顺利建立通信，我们还得制作数字证书(自签发)，源码中自带的证书是无法使用的，证书制作方法可参见《[搭建自 己的ngrok服务](http://tonybai.com/2015/03/14/selfhost-ngrok-service/)》一文，相关原理可参考《[Go和HTTPS](http://tonybai.com/2015/04/30/go-and-https/)》一文，这里就不赘述了。

我直接使用的是release版本(放在bin/release下)，这样在执行命令时可以少传入几个参数：

启动服务端：

$> sudo ./bin/release/ngrokd -domain ngrok.me

[05/13/15 17:15:37] [INFO] Listening for public http connections on [::]:80

[05/13/15 17:15:37] [INFO] Listening for public https connections on [::]:443

[05/13/15 17:15:37] [INFO] Listening for control and proxy connections on [::]:4443

启动客户端：

$> ./bin/release/ngrok -config=debug.yml -log=ngrok.log -subdomain=test 8080

有了调试环境，我们就可以通过debug日志验证我们的分析了。

ngrok的源码结构如下：

drwxr-xr-x 3 tony staff 102 3 31 16:09 cache/

drwxr-xr-x 16 tony staff 544 5 13 17:21 client/

drwxr-xr-x 4 tony staff 136 5 13 15:02 conn/

drwxr-xr-x 3 tony staff 102 3 31 16:09 log/

drwxr-xr-x 4 tony staff 136 3 31 16:09 main/

drwxr-xr-x 5 tony staff 170 5 12 16:17 msg/

drwxr-xr-x 5 tony staff 170 3 31 16:09 proto/

drwxr-xr-x 11 tony staff 374 5 13 17:21 server/

drwxr-xr-x 7 tony staff 238 3 31 16:09 util/

drwxr-xr-x 3 tony staff 102 3 31 16:09 version/

main目录下的ngrok/和ngrokd/分别是ngrok和ngrokd main包，main函数存放的位置，但这里仅仅是一个stub。以ngrok为例：

// ngrok/src/ngrok/main/ngrok/ngrok.go

package main

import (

"ngrok/client"

)

func main() {

client.Main()

}

真正的“main”被client包的Main函数实现。

client/和server/目录分别对应ngrok和ngrokd的主要逻辑，其他目录（或包）都是一些工具类的实现。

**三、第一阶段：Control Connection建立**

在ngrokd的启动日志中我们可以看到这样一行：

[INFO] Listening for control and proxy connections on [::]:4443

ngrokd在4443端口（默认）监听control和proxy connection。Control Connection，顾名思义“控制连接”，有些类似于FTP协议的控制连接（不知道ngrok作者在设计协议时是否参考了FTP协议^_^）。该连接 只用于收发控制类消息。作为客户端的ngrok启动后的第一件事就是与ngrokd建立Control Connection，建立过程序列图如下：

![](../../assets/61e4d659ec484da4.png)


前面提到过，ngrok客户端的实际entrypoint在ngrok/src/ngrok/client目录下，包名client，实际入口是 client.Main函数。

//ngrok/src/ngrok/client/main.go

func Main() {

// parse options

// set up logging

// read configuration file

…. …

**NewController().****Run****(config)**

}

ngrok采用了MVC模式构架代码，这既包括ngrok与ngrokd之间的逻辑处理，也包括ngrok本地web页面（用于隧道数据的 introspection）的处理。

//ngrok/src/ngrok/client/controller.go

func (ctl *Controller) Run(config *Configuration) {

var model *ClientModel

if ctl.model == nil {

model = ctl.SetupModel(config)

} else {

model = ctl.model.(*ClientModel)

}

// init the model

// init web ui

// init term ui

… …

**ctl.Go(ctl.model.Run)**

… …


}

我们来继续看看model.Run都做了些什么。

//ngrok/src/ngrok/client/model.go

func (c *ClientModel) Run() {

… …

for {

// run the control channel

**c.control()**

… …

if c.connStatus == mvc.ConnOnline {

wait = 1 * time.Second

}

… …

c.connStatus = mvc.ConnReconnecting

c.update()

}

}

Run函数调用c.control来运行Control Connection的主逻辑，并在control connection断开后，尝试重连。

c.control是ClientModel的一个method，用来真正建立ngrok到ngrokd的control connection，并完成基于ngrok的鉴权（用户名、密码配置在配置文件中）。

//ngrok/src/ngrok/client/model.go

func (c *ClientModel) control() {

… …

var (

ctlConn conn.Conn

err error

)

if c.proxyUrl == "" {

// simple non-proxied case, just connect to the server

ctlConn, err = conn.**Dial**(c.serverAddr, "ctl", c.tlsConfig)

} else {……}

… …

// authenticate with the server

auth := &msg.Auth{

ClientId: c.id,

OS: runtime.GOOS,

Arch: runtime.GOARCH,

Version: version.Proto,

MmVersion: version.MajorMinor(),

User: c.authToken,

}

if err = msg.WriteMsg(ctlConn, **auth**); err != nil {

panic(err)

}

// wait for the server to authenticate us

var authResp msg.AuthResp

if err = msg.ReadMsgInto(ctlConn, &**authResp**); err != nil {

panic(err)

}

… …

c.id = authResp.ClientId

… ..

}

ngrok封装了connection相关操作，代码在ngrok/src/ngrok/conn下面，包名conn。

//ngrok/src/ngrok/conn/conn.go

func Dial(addr, typ string, tlsCfg *tls.Config) (conn *loggedConn, err error) {

var rawConn net.Conn

if rawConn, err = net.Dial("tcp", addr); err != nil {

return

}

conn = wrapConn(rawConn, typ)

conn.Debug("New connection to: %v", rawConn.RemoteAddr())

if tlsCfg != nil {

**conn.StartTLS(tlsCfg)**

}

return

}

ngrok首先创建一条TCP连接，并基于该连接创建了TLS client：

func (c *loggedConn) StartTLS(tlsCfg *tls.Config) {

c.Conn = tls.Client(c.Conn, tlsCfg)

}

不过此时并未进行TLS的初始化，即handshake。handshake发生在ngrok首次向ngrokd发送auth消息（msg.WriteMsg, ngrok/src/ngrok/msg/msg.go）时，go标准库的TLS相关函数默默的完成这一handshake过程。我们经常遇到的ngrok证书验证失败等问题，就发生在该过程中。

在AuthResp中，ngrokd为该Control Connection分配一个ClientID，该ClientID在后续Proxy Connection建立时使用，用于关联和校验之用。

前面的逻辑和代码都是ngrok客户端的，现在我们再从ngrokd server端代码review一遍Control Connection的建立过程。

ngrokd的代码放在ngrok/src/ngrok/server下面，entrypoint如下：

//ngrok/src/ngrok/server/main.go

func Main() {

// parse options

opts = parseArgs()

// init logging

// init tunnel/control registry

… …

// start listeners

listeners = make(map[string]*conn.Listener)

// load tls configuration

tlsConfig, err := LoadTLSConfig(opts.tlsCrt, opts.tlsKey)

if err != nil {

panic(err)

}

// listen for http

// listen for https

… …

// ngrok clients

**tunnelListener**(opts.tunnelAddr, tlsConfig)

}

ngrokd启动了三个监听，其中最后一个tunnelListenner用于监听ngrok发起的Control Connection或者后续的proxy connection，作者意图通过一个端口，监听两种类型连接，旨在于方便部署。

//ngrok/src/ngrok/server/main.go

func tunnelListener(addr string, tlsConfig *tls.Config) {

// listen for incoming connections

listener, err := conn.Listen(addr, "tun", tlsConfig)

… …

for c := range listener.Conns {

go func(tunnelConn conn.Conn) {

… …

var rawMsg msg.Message

if rawMsg, err = msg.ReadMsg(tunnelConn); err != nil {

tunnelConn.Warn("Failed to read message: %v", err)

tunnelConn.Close()

return

}

… …

switch m := rawMsg.(type) {

case *msg.Auth:

**NewControl**(tunnelConn, m)

… …

}

}(c)

}

}

从tunnelListener可以看到，当ngrokd在新建立的Control Connection上收到Auth消息后，ngrokd执行NewControl来处理该Control Connection上的后续事情。

//ngrok/src/ngrok/server/control.go

func NewControl(ctlConn conn.Conn, authMsg *msg.Auth) {

var err error

// create the object

c := &Control{

… …

}

// register the clientid

… …

// register the control

… …

// start the writer first so that

// the following messages get sent

go c.writer()

// Respond to authentication

c.out <- &**msg.AuthResp**{

Version: version.Proto,

MmVersion: version.MajorMinor(),

ClientId: c.id,

}

// As a performance optimization,

// ask for a proxy connection up front

c.out <- &msg.ReqProxy{}

// manage the connection

go c.manager()

go c.reader()

go c.stopper()

}

在NewControl中，ngrokd返回了AuthResp。到这里，一条新的Control Connection建立完毕。

我们最后再来看一下Control Connection建立过程时ngrok和ngrokd的输出日志，增强一下感性认知：

ngrok Server:

[INFO] [tun:d866234] **New connection** from 127.0.0.1:59949

[DEBG] [tun:d866234] Waiting to read message

[DEBG] [tun:d866234] Reading message with length: 126

[DEBG] [tun:d866234] Read message {"Type":"**Auth**",

"Payload":{"Version":"2","MmVersion":"1.7","User":"","Password":"","OS":"darwin","Arch":"amd64","ClientId":""}}

[INFO] [ctl:d866234] Renamed connection tun:d866234

[INFO] [registry] [ctl] Registered control with id ac1d14e0634f243f8a0cc2306bb466af

[DEBG] [ctl:d866234] [ac1d14e0634f243f8a0cc2306bb466af] Writing message: {"Type":"**AuthResp**","Payload":{"Version":"2","MmVersion":"1.7","ClientId":"**ac1d14e0634f243f8a0cc2306bb466af**","Error":""}}

Client:

[INFO] (ngrok/log.Info:112) Reading configuration file debug.yml

[INFO] (ngrok/log.(*PrefixLogger).Info:83) [client] Trusting root CAs: [assets/client/tls/ngrokroot.crt]

[INFO] (ngrok/log.(*PrefixLogger).Info:83) [view] [web] Serving web interface on 127.0.0.1:4040

[INFO] (ngrok/log.Info:112) Checking for update

[DEBG] (ngrok/log.(*PrefixLogger).Debug:79) [view] [term] Waiting for update

[DEBG] (ngrok/log.(*PrefixLogger).Debug:79) [ctl:31deb681] **New connection** to: 127.0.0.1:4443

[DEBG] (ngrok/log.(*PrefixLogger).Debug:79) [ctl:31deb681] Writing message: {"Type":"**Auth**","Payload":{"Version":"2","MmVersion":"1.7","User":"","Password":"","OS":"darwin","Arch":"amd64","ClientId":""}}

[DEBG] (ngrok/log.(*PrefixLogger).Debug:79) [ctl:31deb681] Waiting to read message

(ngrok/log.(*PrefixLogger).Debug:79) [ctl:31deb681] Reading message with length: 120

(ngrok/log.(*PrefixLogger).Debug:79) [ctl:31deb681] Read message {"Type":"**AuthResp**","Payload":{"Version":"2","MmVersion":"1.7","ClientId":"ac1d14e0634f243f8a0cc2306bb466af","Error":""}}

[INFO] (ngrok/log.(*PrefixLogger).Info:83) [client] Authenticated with server, client id: ac1d14e0634f243f8a0cc2306bb466af

**四、Tunnel Creation**

![](../../assets/f5d1d65a35a0585b.png)


Tunnel Creation是ngrok将配置文件中的tunnel信息通过刚刚建立的Control Connection传输给 ngrokd，ngrokd登记、启动相应端口监听（如果配置了remote_port或多路复用ngrokd默认监听的http和https端口）并返回相应应答。ngrok和ngrokd之间并未真正建立新连接。

我们回到ngrok的model.go，继续看ClientModel的control方法。在收到AuthResp后，ngrok还做了如下事情：

//ngrok/src/ngrok/client/model.go


// request tunnels

reqIdToTunnelConfig := make(map[string]*TunnelConfiguration)

for _, config := range c.tunnelConfig {

// create the protocol list to ask for

var protocols []string

for proto, _ := range config.Protocols {

protocols = append(protocols, proto)

}

reqTunnel := &msg.**ReqTunnel**{

… …

}

// send the tunnel request

if err = msg.WriteMsg(ctlConn, reqTunnel); err != nil {

panic(err)

}

// save request id association so we know which local address

// to proxy to later

reqIdToTunnelConfig[reqTunnel.ReqId] = config

}

// main control loop

for {

var rawMsg msg.Message


switch m := rawMsg.(type) {

… …

case *msg.**NewTunnel**:

… …

tunnel := mvc.Tunnel{

… …

}

c.tunnels[tunnel.PublicUrl] = tunnel

c.connStatus = mvc.ConnOnline


c.update()

… …

}

}

ngrok将配置的Tunnel信息逐一以ReqTunnel消息发送给ngrokd以注册登记Tunnel，并在随后的main control loop中处理ngrokd回送的NewTunnel消息，完成一些登记索引工作。

ngrokd Server端对tunnel creation的处理是在NewControl的结尾处：

//ngrok/src/ngrok/server/control.go

func NewControl(ctlConn conn.Conn, authMsg *msg.Auth) {

… …

// manage the connection

go c.manager()

… …

}

func (c *Control) manager() {

//… …

for {

select {

case <-reap.C:

… …

case mRaw, ok := <-c.in:

// c.in closes to indicate shutdown

if !ok {

return

}

switch m := mRaw.(type) {

case ***msg.ReqTunnel**:

**c.registerTunnel**(m)

.. …

}

}

}

}

Control的manager在收到ngrok发来的ReqTunnel消息后，调用registerTunnel进行处理。

// ngrok/src/ngrok/server/control.go

// Register a new tunnel on this control connection

func (c *Control) registerTunnel(rawTunnelReq *msg.ReqTunnel) {

for _, proto := range strings.Split(rawTunnelReq.Protocol, "+") {

tunnelReq := *rawTunnelReq

tunnelReq.Protocol = proto

c.conn.Debug("Registering new tunnel")

t, err := **NewTunnel**(&tunnelReq, c)

if err != nil {

c.out <- &**msg.NewTunnel**{Error: err.Error()}

if len(c.tunnels) == 0 {

c.shutdown.Begin()

}

// we're done

return

}

// add it to the list of tunnels

c.tunnels = append(c.tunnels, t)

// acknowledge success

** c.out <- &msg.NewTunnel {**

Url: t.url,

Protocol: proto,

ReqId: rawTunnelReq.ReqId,

}

rawTunnelReq.Hostname = strings.Replace(t.url, proto+"://", "", 1)

}

}

Server端创建tunnel的实际工作由NewTunnel完成：

// ngrok/src/ngrok/server/tunnel.go

func NewTunnel(m *msg.ReqTunnel, ctl *Control) (t *Tunnel, err error) {

t = &Tunnel{

… …

}

proto := t.req.Protocol

switch proto {

case "**tcp**":

bindTcp := func(port int) error {

if t.listener, err = **net.ListenTCP**("tcp",

&net.TCPAddr{IP: net.ParseIP("0.0.0.0"),

Port: port}); err != nil {

… …

return err

}

// create the url

addr := t.listener.Addr().(*net.TCPAddr)

t.url = fmt.Sprintf("tcp://%s:%d", opts.domain, addr.Port)

// register it

if err = tunnelRegistry.RegisterAndCache(t.url, t);

err != nil {

… …

return err

}

**go t.listenTcp(t.listener)**

return nil

}

// use the custom remote port you asked for

if t.req.**RemotePort** != 0 {

bindTcp(int(t.req.RemotePort))

return

}

// try to return to you the same port you had before

cachedUrl := tunnelRegistry.GetCachedRegistration(t)

if cachedUrl != "" {

… …

}

// Bind for TCP connections

**bindTcp(0)**

return

case "http", "https":

l, ok := listeners[proto]

if !ok {

… …

return

}

if err = **registerVhost(**t, proto, l.Addr.(*net.TCPAddr).Port);

err != nil {

return

}

default:

err = fmt.Errorf("Protocol %s is not supported", proto)

return

}

… …

metrics.OpenTunnel(t)

return

}

可以看出，NewTunnel区别对待tcp和http/https隧道：

- 对于Tcp隧道，NewTunnel先要看是否配置了remote_port，如果remote_port不为空，则启动监听这个 remote_port。否则尝试从cache里找出你之前创建tunnel时使用的端口号，如果可用，则监听这个端口号，否则bindTcp(0)，即 随机选择一个端口作为该tcp tunnel的remote_port。

- 对于http/https隧道，ngrokd启动时就默认监听了80和443，如果ngrok请求建立http/https隧道(目前不支持设置remote_port)，则ngrokd通过一种自实现的vhost的机制实现所有http/https请求多路复用到80和443端口上。ngrokd不会新增监听端口。

从下面例子，我们也可以看出一些端倪。我们将debug.yml改为：

server_addr: ngrok.me:4443

trust_host_root_certs: false

tunnels:

test:

proto:

http: 8080

test1:

proto:

http: 8081

ssh1:

remote_port: 50000

proto:

tcp: 22

ssh2:

proto:

tcp: 22

启动ngrok：

$./bin/release/ngrok -config=debug.yml -log=ngrok.log start test test1 ssh1 ssh2

Tunnel Status online

Version 1.7/1.7

Forwarding tcp://ngrok.me:50000 -> 127.0.0.1:22

Forwarding tcp://ngrok.me:56297 -> 127.0.0.1:22

Forwarding http://test.ngrok.me -> 127.0.0.1:8080

Forwarding http://test1.ngrok.me -> 127.0.0.1:8081

Web Interface 127.0.0.1:4040

可以看出ngrokd为ssh2随机挑选了一个端口56297进行了监听，而两个http隧道，则都默认使用了80端口。

如果像下面这样配置会发生什么呢？

ssh1:

remote_port: 50000

proto:

tcp: 22

ssh2:

remote_port: 50000

proto:

tcp: 22

ngrok启动会得到错误信息：

Server failed to allocate tunnel: [ctl:5332a293] [a87bd111bcc804508c835714c18a5664] Error binding TCP listener: listen tcp 0.0.0.0:50000: bind: address already in use

客户端ngrok在ClientModel control方法的main control loop中收到NewTunnel并处理该消息：

case *msg.NewTunnel:

if m.Error != "" {

… …

}

tunnel := mvc.Tunnel{

PublicUrl: m.Url,

LocalAddr: reqIdToTunnelConfig[m.ReqId].Protocols[m.Protocol],

Protocol: c.protoMap[m.Protocol],

}

c.tunnels[tunnel.PublicUrl] = tunnel

c.connStatus = mvc.ConnOnline

c.Info("Tunnel established at %v", tunnel.PublicUrl)

c.update()

**五、Proxy Connection****和Private Connection**

到目前为止，我们知道了Control Connection：用于ngrok和ngrokd之间传输命令；Public Connection：外部发起的，尝试向内网服务建立的链接。

这节当中，我们要接触到Proxy Connection和Private Connection。

Proxy Connection以及Private Connection的建立过程如下：

![](../../assets/8bf24f95386624c4.png)


前面ngrok和ngrokd的交互进行到了NewTunnel，这些数据都是通过之前已经建立的Control Connection上传输的。

ngrokd侧，NewControl方法的结尾有这样一行代码：

// As a performance optimization, ask for a proxy connection up front

c.out <- &msg.ReqProxy{}

服务端ngrokd在Control Connection上向ngrok发送了"ReqProxy"的消息，意为请求ngrok向ngrokd建立一条Proxy Connection，该链接将作为隧道数据流的承载者。

客户端ngrok在ClientModel control方法的main control loop中收到ReqProxy并处理该消息：

case *msg.ReqProxy:

c.ctl.Go(c.proxy)

// Establishes and manages a tunnel proxy connection with the server

func (c *ClientModel) proxy() {

if c.proxyUrl == "" {

remoteConn, err = conn.Dial(c.serverAddr, "pxy", c.tlsConfig)

}……

err = msg.WriteMsg(remoteConn, &msg.RegProxy{ClientId: c.id})

if err != nil {

remoteConn.Error("Failed to write RegProxy: %v", err)

return

}

… …

}

ngrok客户端收到ReqProxy后，创建一条新连接到ngrokd，该连接即为Proxy Connection。并且ngrok将RegProxy消息通过该新建立的Proxy Connection发到ngrokd，以便ngrokd将该Proxy Connection与对应的Control Connection以及tunnel关联在一起。

// ngrok服务端

func tunnelListener(addr string, tlsConfig *tls.Config) {

…. …

case *msg.RegProxy:

NewProxy(tunnelConn, m)

… …

}

到目前为止, tunnel、Proxy Connection都已经建立了，万事俱备，就等待Public发起Public connection到ngrokd了。

下面我们以Public发起一个http连接到ngrokd为例，比如我们通过curl 命令，向test.ngrok.me发起一次http请求。

前面说过，ngrokd在启动时默认启动了80和443端口的监听，并且与其他http/https隧道共同多路复用该端口（通过vhost机制)。ngrokd server对80端口的处理代码如下：

// ngrok/src/ngrok/server/main.go

func Main() {

… …

// listen for http

if opts.httpAddr != "" {

listeners["http"] =

**startHttpListener**(opts.httpAddr, nil)

}

… …

}

startHttpListener针对每个连接，启动一个goroutine专门处理：

//ngrok/src/ngrok/server/http.go

func startHttpListener(addr string,

tlsCfg *tls.Config) (listener *conn.Listener) {

// bind/listen for incoming connections

var err error

if listener, err = conn.Listen(addr, "pub", tlsCfg);

err != nil {

panic(err)

}

proto := "http"

if tlsCfg != nil {

proto = "https"

}

… …

go func() {

for conn := range listener.Conns {

go** httpHandler**(conn, proto)

}

}()

return

}

// Handles a new http connection from the public internet

func httpHandler(c conn.Conn, proto string) {

… …

// let the tunnel handle the connection now

tunnel.HandlePublicConnection(c)

}

我们终于看到server端处理public connection的真正方法了:

//ngrok/src/ngrok/server/tunnel.go

func (t *Tunnel) HandlePublicConnection(publicConn conn.Conn) {

… …

var proxyConn conn.Conn

var err error

for i := 0; i < (2 * proxyMaxPoolSize); i++ {

// get a proxy connection

if proxyConn, err = t.ctl.**GetProxy**();

err != nil {

… …

}

defer proxyConn.Close()

… …

// tell the client we're going to

// start using this proxy connection

startPxyMsg := &msg.**StartProxy**{

Url: t.url,

ClientAddr: publicConn.RemoteAddr().String(),

}

if err = msg.WriteMsg(proxyConn, startPxyMsg);

err != nil {

… …

}

}

… …

// join the public and proxy connections

bytesIn, bytesOut := **conn.Join(**publicConn, proxyConn)

…. …

}

HandlePublicConnection通过选出的Proxy connection向ngrok client发送StartProxy信息，告知ngrok proxy启动。然后通过conn.Join方法将publicConn和proxyConn关联到一起。

// ngrok/src/ngrok/conn/conn.go

func Join(c Conn, c2 Conn) (int64, int64) {

var wait sync.WaitGroup

pipe := func(to Conn, from Conn, bytesCopied *int64) {

defer to.Close()

defer from.Close()

defer wait.Done()

var err error

*bytesCopied, err = io.Copy(to, from)

if err != nil {

from.Warn("Copied %d bytes to %s before failing with error %v", *bytesCopied, to.Id(), err)

} else {

from.Debug("Copied %d bytes to %s", *bytesCopied, to.Id())

}

}

wait.Add(2)

var fromBytes, toBytes int64

go pipe(c, c2, &fromBytes)

go pipe(c2, c, &toBytes)

c.Info("Joined with connection %s", c2.Id())

wait.Wait()

return fromBytes, toBytes

}

Join通过io.Copy实现public conn和proxy conn数据流的转发，单向被称作一个pipe，Join建立了两个Pipe，实现了双向转发，每个Pipe直到一方返回EOF或异常失败才会退出。后续在ngrok端，proxy conn和private conn也是通过conn.Join关联到一起的。

我们现在就来看看ngrok在收到StartProxy消息后是如何处理的。我们回到ClientModel的proxy方法中。在向ngrokd成功建立proxy connection后，ngrok等待ngrokd的StartProxy指令。

// wait for the server to ack our register

var startPxy msg.StartProxy

if err = msg.ReadMsgInto(remoteConn, &startPxy);

err != nil {

remoteConn.Error("Server failed to write StartProxy: %v",

err)

return

}

一旦收到StartProxy，ngrok将建立一条private connection：

// start up the private connection

start := time.Now()

localConn, err := conn.Dial(tunnel.LocalAddr, "prv", nil)

if err != nil {

… …

return

}

并将private connection和proxy connection通过conn.Join关联在一起，实现数据透明转发。

m.connTimer.Time(func() {

localConn := tunnel.Protocol.WrapConn(localConn,

mvc.ConnectionContext{Tunnel: tunnel,

ClientAddr: startPxy.ClientAddr})

bytesIn, bytesOut := **conn.Join**(localConn, remoteConn)

m.bytesIn.Update(bytesIn)

m.bytesOut.Update(bytesOut)

m.bytesInCount.Inc(bytesIn)

m.bytesOutCount.Inc(bytesOut)

})

这样一来，public connection上的数据通过proxy connection到达ngrok，ngrok再通过private connection将数据转发给本地启动的服务程序，从而实现所谓的内网穿透。从public视角来看，就像是与内网中的那个服务直接交互一样。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

沙发

借个楼，免费的国内Ngrok服务器 支持https http://ngrok.ciqiuwl.cn 欢迎大家使用交流

学习学习，默默的关注博主了，嘿嘿

使用国内的www.ngrok.cc

牛啊,想不到的强文

xtunnel开源内网穿透,图形界面,功能更强大

https://github.com/d1sm/xtunnel

你好，元宵节快乐

博主能不能再详细写写ngrok的鉴权分析

不错的文章

国内免费ngrok服务器-小米球ngrok

http://ngrok.ciqiuwl.cn

受益匪浅，已订阅博文

免费ngrok服务器铂金ngrok

https://ngrok.bob.kim