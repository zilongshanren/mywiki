---
title: 使用Golang开发微信公众平台-接收文本消息
url: https://tonybai.com/2014/12/20/receive-text-for-wechat-public-platform-dev-in-golang/
published: '2014-12-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Golang开发微信公众平台-接收文本消息

一旦[接入验证](http://tonybai.com/2014/12/18/access-validation-for-wechat-public-platform-dev-in-golang/)成功，成为正式开发者，你可能会迫不及待地想通过手机微信发送一条"Hello, Wechat”到你的公众号服务器。不过上一篇的那个程序还无法处理手机提交的文本消息，本篇将介绍如何用[Golang](http://tonybai.com/tag/golang)编写公众号程序来接收手机端发送的 文本消息以及回复响应消息。

根据[微信公众平台开发文档](http://mp.weixin.qq.com/wiki/home/index.html)中描述：“当普通微信用户向公众账号发消息时，微信服务器将POST消息的XML数据包到开发者填写的URL上”。我们 用一个示意图展示一下这个消息流程：

![](../../assets/08aaf2f39cfddfdd.png)


微信服务器通过一个HTTP Post请求将终端用户发送的消息转发给公众号服务器，消息内容被包装在HTTP Post Request的Body中。数据包以XML格式存储，文本类消息XML格式样例如下（引自微信公众平台开发文档）：

![](../../assets/1231cd3e3f04d7e7.png)


数据包中各个字段的含义都显而易见，我们重点关注的时Content这个字段填写的内容，也就是终端用户发送的消息内容。为了得到这个字段值，我 们需要解析微信服务器发来的HTTP Post包的Body。

在“[接入验证](http://tonybai.com/2014/12/18/access-validation-for-wechat-public-platform-dev-in-golang/)”一文中我们提到过，微信服务器发起的请求都带有验证字段，可被公众号服务用于验证HTTP Request是否来自于微信服务器，避免恶意请求。这些用于验证来源的信息，不仅仅在接入验证阶段会发给公众号服务器，在后续微信服务器与公众号服务器 的消息交互过程中，HTTP Request中也都会携带这些信息(注意：没有echostr参数了)。

下面我们来看接收文本消息的Golang程序。

**一、接收文本消息**

公众号所用的HTTP Server可以沿用“接入验证”一文中的那个main中的Server，我们需要修改的是procRequest函数。

在procRequest函数中，我们保留validateUrl，用于校验请求是否来自于微信服务器。

func procRequest(w http.ResponseWriter, r *http.Request) {

r.ParseForm()

if !validateUrl(w, r) {

log.Println("Wechat Service: this http request is not from Wechat platform!")

return

}

log.Println("Wechat Service: validateUrl Ok!")


… …//在此解析HTTP Request Body

}

通过验证后，我们开始解析HTTP Request的Body，Body中的数据是XML格式的，我们可以通过Golang标准库encoding/xml包中提供的函数对Body进行解 析。encoding/xml根据xml字段名与struct字段名或struct tag(struct中每个字段后面反单引号引用的内容，比如xml: "xml")的对应关系将xml数据中的字段值解析到struct的字段中，因此我们需要根据这个xml包的组成定义出对应该格式的struct，这个 struct定义如下：

type TextRequestBody struct {

XMLName xml.Name `xml:"xml"`

ToUserName string

FromUserName string

CreateTime time.Duration

MsgType string

Content string

MsgId int

}

其中FromUserName是发送方账号，这是一个OpenID，每个微信用户针对某个关注的公众号都有唯一OpenID。举个例 子："tonybai"这个微信用户，关注了"GoNuts"和"GoDev"两个公众号，则"tonybai"发给GoNuts的消息中的 OpenID是“tonybai-gonuts”，而tonybai发给GoDev的消息中的OpenID则是“tonybai-godev”。

MsgId是一个64位整型，可用于消息排重。对于一个HTTP Post，微信服务器在五秒内如果收不到响应会断掉连接，并且针对该消息重新发起请求，总共重试三次。严谨的公众号服务端实现是应该实现消息排重功能的。

通过encoding/xml包中的Unmarshal函数，我们将上面的xml数据转换为一个TextRequestBody实例，具体代码如 下：

//recvtextmsg_unencrypt.go

func parseTextRequestBody(r *http.Request) *TextRequestBody {

body, err := ioutil.ReadAll(r.Body)

if err != nil {

log.Fatal(err)

return nil

}

fmt.Println(string(body))

requestBody := &TextRequestBody{}

xml.Unmarshal(body, requestBody)

return requestBody

}

func procRequest(w http.ResponseWriter, r *http.Request) {

r.ParseForm()

if !validateUrl(w, r) {

log.Println("Wechat Service: this http request is not from Wechat platform!")

return

}

if r.Method == "POST" {

textRequestBody := parseTextRequestBody(r)

if textRequestBody != nil {

fmt.Printf("Wechat Service: Recv text msg [%s] from user [%s]!",

textRequestBody.Content,

textRequestBody.FromUserName)

}

}

}

构建并执行该程序：

$>sudo ./recvtextmsg_unencrypt

2014/12/19 08:03:27 Wechat Service: Start!

通过手机微信或公众开发平台提供的[页面调试工具](https://mp.weixin.qq.com/debug/cgi-bin/apiinfo?t=index&type=%E6%B6%88%E6%81%AF%E6%8E%A5%E5%8F%A3%E8%B0%83%E8%AF%95&form=%E9%93%BE%E6%8E%A5%E6%B6%88%E6%81%AF)发送"Hello, Wechat"，我们可以看到如下输出：

2014/12/19 08:05:51 Wechat Service: validateUrl Ok!

Wechat Service: Recv text msg [Hello, Wechat] from user [oBQcwuAbKpiSAbbvd_DEZg7q27QI]!

上述接收"Hello, Wechat"文本消息的Http抓包分析文本如下(Copy from wireshark output)：

POST /?signature=9b8233c4ef635eaf5b9545dc196da6661ee039b0×tamp=1418976343&nonce=1368270896 HTTP/1.0\r\n

User-Agent: Mozilla/4.0\r\n

Accept: */*\r\n

Host: wechat.tonybai.com\r\n

Pragma: no-cache\r\n

Content-Length: 286\r\n

Content-Type: text/xml\r\n

公众号服务器给微信服务器返回的HTTP Post Response为：

HTTP/1.0 200 OK\r\n

Date: Fri, 19 Dec 2014 08:05:51 GMT\r\n

Content-Length: 0\r\n

Content-Type: text/plain; charset=utf-8\r\n

**二、响应文本消息**

上面的例子中，终端用户发送"Hello, Wechat"，虽然公众号服务器成功接收到了这段内容，但终端用户并没有得到响应，这显然不那么友好！这里我们来给终端用户补发一个文本消息的响 应：Hello，用户OpenID。

这类响应消息可以通过HTTP Post Request的Response包携带，将数据放入Response包的Body中，当然也可以单独向微信公众平台发起请求（后话）。微信公众平台开发 文档中关于被动的文本消息响应的定义如下：

![](../../assets/83f2619db5be366b.png)


这与前面的接收消息结构极其类似，字段含义也不说自明。Golang encoding/xml中的Marshal(和MarshalIndent)函数提供了将struct编码为XML数据流的功能，它是 Unmarshal的逆过程，Golang实现回复 文本响应消息的代码如下：

type TextResponseBody struct {

XMLName xml.Name `xml:"xml"`

ToUserName string

FromUserName string

CreateTime time.Duration

MsgType string

Content string

}

func makeTextResponseBody(fromUserName, toUserName, content string) ([]byte, error) {

textResponseBody := &TextResponseBody{}

textResponseBody.FromUserName = fromUserName

textResponseBody.ToUserName = toUserName

textResponseBody.MsgType = "text"

textResponseBody.Content = content

textResponseBody.CreateTime = time.Duration(time.Now().Unix())

return xml.MarshalIndent(textResponseBody, " ", " ")

}

func procRequest(w http.ResponseWriter, r *http.Request) {

r.ParseForm()

if !validateUrl(w, r) {

log.Println("Wechat Service: this http request is not from Wechat platform!")

return

}

if r.Method == "POST" {

textRequestBody := parseTextRequestBody(r)

if textRequestBody != nil {

fmt.Printf("Wechat Service: Recv text msg [%s] from user [%s]!",

textRequestBody.Content,

textRequestBody.FromUserName)

responseTextBody, err := makeTextResponseBody(textRequestBody.ToUserName,

textRequestBody.FromUserName,

"Hello, "+textRequestBody.FromUserName)

if err != nil {

log.Println("Wechat Service: makeTextResponseBody error: ", err)

return

}

fmt.Fprintf(w, string(responseTextBody))

}

}

}

编译执行上面程序后，通过手机微信或网页调试工具发送一条"Hello, Wechat"到公众号，公众号会响应如下信息：“Hello, oBQcwuAbKpiSAbbvd_DEZg7q27QI"，手机端微信会正确接收该响应。

上述响应的抓包分析如下。公众号服务器给微信服务器返回的HTTP Post Response为：

HTTP/1.0 200 OK\r\n

Date: Fri, 19 Dec 2014 09:03:55 GMT\r\n

Content-Length: 220\r\n

Content-Type: text/plain; charset=utf-8\r\n

\r\n

<xml><ToUserName>oBQcwuAbKpiSAbbvd_DEZg7q27QI</ToUserName><FromUserName>gh_xxxxxxxx</FromUserName><CreateTime>1418979835</CreateTime><MsgType>text</MsgType><Content>Hello, oBQcwuAbKpiSAbbvd_DEZg7q27QI</Content></xml>

**三、关于Content-Type设置**

虽然Content-Type为：text/plain; charset=utf-8的 响应信息可以被微信平台正确解析，但通过抓取微信平台给公众号服务器发送的HTTP Post Request来看，在发送xml数据时微信服务器用的Content-Type为Content-Type: text/xml。我们的响应信息Body也是xml数据包，我们能否为响应信息重新设置Content-Type为 text/xml呢？我们可以通过如下代码设置：

w.Header().Set("Content-Type", "text/xml")

fmt.Fprintf(w, string(responseTextBody))

不过奇怪的是我通过AWS EC2上抓包得到的Content-Type始终是“text/plain; charset=utf-8”。但利用ngrok映射到本地端口后抓包看到的却是正确的"text/xml"，在AWS本地用 curl -d xxx.xxx.xxx.xxx测试公众号服务程序而抓到的包也是正确的。通过代码没看出什么端倪，因为逻辑上显式设置Header的Content- Type后，Go标准库不会在sniff内容的格式了。

通过ngrok映射本地80端口后，得到的HTTP Post Response抓包分析文字：

HTTP/1.1 200 OK\r\n

Content-Type: text/xml\r\n

Date: Sat, 20 Dec 2014 04:29:16 GMT\r\n

Content-Length: 220\r\n

xml数据包这里忽略。

**四、CDATA的使用**

从抓包可以看到，我们回复的响应中的XML数据包是不带CDATA，即便这样微信客户端接收也没有问题。但这并未严遵循协议样例。

XML下CDATA含义是：在标记CDATA下，所有的标记、实体引用都被忽略，而被XML处理程序一视同仁地当做字符数据看待，CDATA的形 式如下：

<![CDATA[文本内容]]>

我们尝试加上为每个文本类型的字段值上直接添加CDATA标记。

func value2CDATA(v string) string {

return "<![CDATA[" + v + "]]>"

}

func makeTextResponseBody(fromUserName, toUserName, content string) ([]byte, error) {

textResponseBody := &TextResponseBody{}

textResponseBody.FromUserName = value2CDATA(fromUserName)

textResponseBody.ToUserName = value2CDATA(toUserName)

textResponseBody.MsgType = value2CDATA("text")

textResponseBody.Content = value2CDATA(content)

textResponseBody.CreateTime = time.Duration(time.Now().Unix())

return xml.MarshalIndent(textResponseBody, " ", " ")

}

这样修改后，我们试着发一条消息给微信公众号平台，不过结果并不正确。手机微信无法收到响应信息，并显示“该公众号暂时无法提供服务，请稍后再 试”。通过Println输出Body可以看到：

<xml><ToUserName><![CDATA[oBQcwuAbKpiSAbbvd_DEZg7q27QI]]>

可以看到左右尖括号分别被转义为<和>了，这显然不是我们想要的结果。那如何加入CDATA标记呢。Golang并 不直接显式支持生成CDATA字段的xml流，我们只能间接实现。前面提到过struct定义时的struct tag，golang xml包规定："a field with tag ",innerxml" is written verbatim, not subject to the usual marshalling procedure"。 大致的意思是如果一个字段的struct tag是",innerxml"，则Marshal时字段值原封不动，不提交给通常的marshalling程序。我们就利用innerxml来实现 CDATA标记。

type TextResponseBody struct {

XMLName xml.Name `xml:"xml"`

ToUserName CDATAText

FromUserName CDATAText

CreateTime time.Duration

MsgType CDATAText

Content CDATAText

}

type CDATAText struct {

Text string `xml:",innerxml"`

}

func value2CDATA(v string) CDATAText {

return CDATAText{"<![CDATA[" + v + "]]>"}

}

编译程序后测试，这回CDATA标记正确了，微信客户端也收到的响应信息。

**五、用ngrok在本地调试微信公众平台接口**

在“接入验证”一文中，我们建议申请诸如AWS EC2来应对微信公众平台接口开发，但其方便程度毕竟不如本地。网上一开源工具ngrok可以帮助我们实现本地调试微信公众平台接口。

使用ngrok的步骤如下：

1、下载ngrok

ngrok也是使用golang实现的，因此主流平台都支持。ngrok下载后就是一个可执行的二进制文件，可直接执行（放在PATH路径 下）。

2、注册ngrok

到ngrok.com上注册一个账号，注册成功后，就能看到ngrok.com为你分配的auth token，把这个auth token放到~/.ngrok中：

auth_token:YOUR_AUTH_TOKEN

3、执行ngrok

$ngrok 80

ngrok (Ctrl+C to quit)

Tunnel Status online

Version 1.7/1.6

Forwarding [http://xxxxxxxx.ngrok.com](http://xxxxxxxx.ngrok.com) -> 127.0.0.1:80

Forwarding [https://xxxxxxxx.ngrok.com](https://xxxxxxxx.ngrok.com) -> 127.0.0.1:80

Web Interface 127.0.0.1:4040

# Conn 1

Avg Conn Time 1.90ms

其中"xxxxxxxx.ngrok.com"就是ngrok为你分配的子域名。

在你的微信开发者中心将这个地址配置到URL字段中，提交验证，验证消息就会顺着ngrok建立的隧道流到你的local机器的80端口上。

另外本地调试抓包，要用loopback网口，比如：

$sudo tcpdump -w http.cap -i lo0 tcp port 80

本篇文章涉及的代码在[这里](https://github.com/bigwhite/experiments/tree/master/wechat_examples/public/2-recvtextmsg)可以找到。

© 2014 – 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

函数 makeTextResponseBody 里面的 return xml.Marshal(textResponseBody, ” “, ” “) 应该改为 xml.MarshalIndent(textResponseBody, ” “, ” “)

笔误，已改。谢谢提醒:)

xie xie

使用ngrok需要翻墙吗？

以前不需要。春节后好像被墙了。现在ngrok.com无法访问，估计需要翻把。现在用自己搭建的ngrok服务了。