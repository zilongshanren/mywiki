---
title: 通过实例理解Web应用跨域问题
url: https://tonybai.com/2023/11/19/understand-go-web-cross-origin-problem-by-example/
published: '2023-11-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Web应用跨域问题

![](../../assets/a0aee6681e0d60e6.png)


[本文永久链接](https://tonybai.com/2023/11/19/understand-go-web-cross-origin-problem-by-example) – https://tonybai.com/2023/11/19/understand-go-web-cross-origin-problem-by-example

在开发Web应用的过程中，我们经常会遇到所谓“跨域问题(Cross Origin Problem)”。跨域问题是由于浏览器的[同源策略(Same-origin policy)](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)导致的，它限制了不同源(Origin：域名、协议或端口）之间的资源交互。在这篇文章中，我将通过一些具体的示例来把跨域问题以及主流解决方法说清楚，供大家参考。

## 1. 什么是跨域问题

跨域问题指的是当一个Web应用程序在访问另一个域(Origin)的资源时，浏览器会阻止这个跨域的请求(Cross Origin Request)。这句针对跨域问题的诠释里有一个术语“域(Origin)”，它到底是什么呢？

### 1.1 什么是Origin

在Mozilla官方术语表中，”Origin”指的是一个Web应用/网站的标识，由协议(protocol/scheme)、域名(domain，或主机名host)和端口(port)组成。如果两个应用/网站的协议、域名和端口都相同，它们就被认为是同源的(same origin)；否则，它们被视为不同源。我们看到：**Origin是一个典型的三元组(protocol, domain, port)**，只有三元组相同的两个应用/站点才会被认为是同源的(same origin)。

下面是一些判断两个应用/站点是否同源的例子及判断理由：

![](../../assets/dc1051153704e647.png)


知道了Origin三元组后，我们来揪出跨域问题背后的“罪魁祸首”。

### 1.2 同源策略 – 跨域问题的“罪魁祸首”

浏览器为了增加安全性而采取的一项重要措施，那就是“[同源策略](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)”。同源策略限制了一个网页中的脚本只能与同源（三元组：协议、域名、端口相同）的资源进行交互，而不能直接访问不同源的资源。

浏览器的这种同源策略限制主要包含以下几点:

- Cookie、LocalStorage和IndexDB无法读取非同源的资源。
- DOM和JS对象无法获得非同源资源。例如iframe、img等标签加载的资源，DOM无法访问；JS无法操作非同源页面的DOM。
- AJAX请求不能发送到非同源的域名，浏览器会阻止非同源的AJAX请求。
- 不能读取非同源网页的Cookie、LocalStorage和IndexDB。

下图(图片来自网络)展示了同源策略对恶意脚本代码对非同源数据访问的限制：

![](../../assets/3d35e793c538e2af.png)


上面这张图片清晰地展示了恶意脚本代码试图访问非同源数据进行恶意登录的过程。

首先，用户通过浏览器访问正常网站domain1.com，并用用户名密码正常登录该网站，domain1.com使用[cookie技术](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example)在用户浏览器中保存了与用户登录domain1.com相关的会话信息或token信息。

之后，用户又访问了恶意站点domain2.com，该站点首页的脚本代码在被下载到用户浏览器中后，试图访问浏览器cookie中有关domain1.com的cookie信息，并试图用该信息冒充用户登录domain1.com做恶意操作。

浏览器的同源策略成功禁止了恶意代码的这些恶意操作，浏览器从domain2.com下载的脚本代码只能访问与domain2.com同源的信息。

通过这个过程我们看到：浏览器同源策略的本意是防止恶意网站通过脚本窃取用户的敏感信息，比如登录凭证、个人资料等。如果同源策略不存在，恶意网站就可以自由地读取、修改甚至篡改其他网站的数据，给用户和网站带来巨大的安全风险。

不过，这种策略的存在**给开发人员在开发过程带来诸多烦恼**，比如：跨域数据访问限制、跨域脚本调用限制以及无法在不同域名之间共享会话信息等。为此，开发人员需要使用一些技术手段来解决这些跨域问题，这增加了开发的复杂性，并且需要额外的配置和处理，给开发人员带来了一定的麻烦。此外，不正确地处理跨域请求也可能导致安全漏洞，因此开发人员还需要对跨域请求进行合理的安全控制和验证。

### 1.3 获取请求中的“origin”

为了做同源检测，我们需要获取和确定请求中的origin信息。那么如何读取和确定呢？

在HTTP请求头中，”Origin”字段表示发送请求的页面或资源的源信息。该字段包含了发送请求的页面的完整URL或者仅包含协议、域名和端口的部分URL。

在同源策略下，所有的跨域请求都必须携带”Origin”请求头字段，指示请求的来源。因此，在符合同源策略的情况下，每个请求都应该携带”Origin”字段。

在服务器端，我们可以通过读取请求头中的”Origin”字段来确定请求的origin，具体的方法会根据使用的编程语言和框架而有所不同，例如在Go中可以通过r.Header.Get(“Origin”)来获取”Origin”字段的值。由于”Origin”字段是由客户端提供的，服务器端在处理请求时，需要进行验证和安全性检查，以防止伪造或恶意的请求。

然而，有些情况下，请求可能不会携带”Origin”字段。例如，非浏览器环境下的请求（如服务器间的请求、命令行工具等）可能不会包含”Origin”字段。此外，某些旧版本的浏览器可能也不会发送”Origin”字段。

在这种情况下，我们就需要通过其他方式来确定请求的来源。例如，服务端可以查看请求头中的Referer字段来获取请求的来源。Referer字段指示了请求的来源页面的URL。通过检查Referer字段，服务端可以判断请求是否来自不同的域。此外，服务器端还可以检查请求头中的Host字段，该字段指示了请求的目标主机。如果请求的目标主机与服务端所在的主机不一致，那么可以判断请求是跨域的。

不过，需要注意的是，服务端的这些方法都依赖于请求头中的信息，而请求头可以被客户端伪造或修改。因此，为了更可靠地判断请求是否跨域，服务端应该综合考虑多个因素，并进行适当的验证和安全措施。

下面我们看一个可以复现跨域问题的示例。

### 1.4 复现跨域问题的Go代码示例

出现跨域问题的示例的图示如下：

![](../../assets/012ccf9b2f252004.png)


在这个示例中，我们有两个Web应用：server1.com:8081和server2.com:8082。根据前面对Origin的理解，这两个Web应用显然不是同源的。

server1.com和server2.com对应的Go代码分别如下：

```
// cross-origin-examples/reproduce/server1.com
func main() {
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
w.Header().Set("Content-Type", "text/html; charset=utf-8")
html := `
<!DOCTYPE html>
<html>
<head>
<title>Cross-Origin Example</title>
<script>
function makeCrossOriginRequest() {
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://server2.com:8082/api/data", true);
xhr.onreadystatechange = function() {
if (xhr.readyState === 4 && xhr.status === 200) {
console.log(xhr.responseText);
}
};
xhr.send();
}
</script>
</head>
<body>
<h1>Cross-Origin Example</h1>
<button onclick="makeCrossOriginRequest()">Make Cross-Origin Request</button>
</body>
</html>
`
fmt.Fprintf(w, html)
})
err := http.ListenAndServe("server1.com:8081", nil)
if err != nil {
panic(err)
}
}
// cross-origin-examples/reproduce/server2.com
package main
import (
"fmt"
"net/http"
)
func main() {
http.HandleFunc("/api/data", func(w http.ResponseWriter, r *http.Request) {
fmt.Printf("recv request: %#v\n", *r)
w.Write([]byte("Welcome to api/data"))
})
http.ListenAndServe("server2.com:8082", nil)
}
```


注：在编译启动上面两个程序之前，需要在/etc/hosts中将server1.com和server2.com的地址指为127.0.0.1。


从示意图来看，用户使用浏览器与两个Web应用的交互过程是这样的：

首先，用户通过浏览器访问了server1.com:8081的主页，并收到server1.com:8081返回的应答包体。该应答包体是一个html页面，如下图：

![](../../assets/73fa453670cb7538.png)


接下来，用户点击“Make Cross-Origin Request”按钮，页面内通过ajax向server2.com:8082/api/data发起GET请求。

最后，我们在(Edge/Chrome)浏览器的控制台上将看到下面错误：

![](../../assets/43aeecfe90c137ba.png)


通过下面server2.com的日志，我们看到ajax请求已经发到server2.com并被正确处理：

```
recv request: http.Request{Method:"GET", URL:(*url.URL)(0xc00010a480), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{"Accept":[]string{"*/*"}, "Accept-Encoding":[]string{"gzip, deflate"}, "Accept-Language":[]string{"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}, "Connection":[]string{"keep-alive"}, "Origin":[]string{"http://server1.com:8081"}, "Referer":[]string{"http://server1.com:8081/"}, "User-Agent":[]string{"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"}}, Body:http.noBody{}, GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:0, TransferEncoding:[]string(nil), Close:false, Host:"server2.com:8082", Form:url.Values(nil), PostForm:url.Values(nil), MultipartForm:(*multipart.Form)(nil), Trailer:http.Header(nil), RemoteAddr:"127.0.0.1:49773", RequestURI:"/api/data", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.cancelCtx)(0xc000106320)}
```


server2.com在服务端并没有主动判断是否是同源请求，但即使服务器没有进行跨域校验并返回成功的响应和数据，浏览器也会拦截脚本读取跨域响应数据的尝试，这是由浏览器的同源策略所决定的。这也是我们看到上面截图中报错的原因。

那么解决跨域问题有哪些主流的解决方法呢？我们继续看一下。

## 2. 跨域问题的主流解决方法

为了解决跨域问题，有下面几种常见的解决方法：

- JSONP（JSON with Padding）

通过动态创建\<script>标签来加载跨域的JavaScript脚本，进而实现跨域数据获取。

[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)（跨域资源共享, CORS是Cross-Origin Resource Sharing）

通过在服务器响应头中设置CORS访问策略以允许指定的Origin访问资源。

- 代理服务器

在同域下创建一个代理服务器，将跨域请求转发到目标服务器并返回结果。代理服务器对响应头统一增加Access-Control-Allow-Origin等CORS相关字段，表示允许跨域访问。

其中CORS是解决跨域问题时应用最为广泛的方法。CORS(跨域资源共享)主要是通过设置HTTP头来解决跨域问题的。

服务器端通过在响应(Response)的HTTP头中设置Access-Control-Allow-Origin头来设置允许的请求来源域(Origin: 三元组)。

如果设置为“*”，则表示允许任意域发起跨域请求：

```
Access-Control-Allow-Origin: *
```


也可以在响应中将Access-Control-Allow-Origin设置为只允许指定的Origin访问资源，比如：

```
Access-Control-Allow-Origin: http://server1.com:8081
```


Access-Control-Allow-Origin头的值还支持设置多个origin，多个origin用逗号分隔：

```
Access-Control-Allow-Origin: http://server1.com:8081,https://server2.com:8082
```


注：关于Access-Control-Allow-Origin的值是否要带上protocol和port的问题，我实测的情况是必须带。前面说过：Origin是三元组，只有完全相同才算是同源。


此外，域名必须具体到二级域名才能匹配成功。顶级域名如“.com”、“.org”是不允许的。

服务端响应的跨域设置还不仅Access-Control-Allow-Origin一个，我们还可以设置Access-Control-Allow-Methods、Access-Control-Allow-Headers、Access-Control-Max-Age等字段来更细粒度的进行跨域访问控制。

注：有些值Access-Control-XXX-xxx字段仅用于

[Preflight Request(预检请求)]，比如：Access-Control-Allow-Methods。CORS Preflight Request是一种CORS请求，它使用特定的方法和Header检查CORS协议是否被理解和服务器是否被感知。它是一个OPTIONS请求，使用两个或三个HTTP请求头： Access-Control-Request-Method（访问控制请求方法）、Origin（起源）和可选的 Access-Control-Request-Headers（访问控制请求头）。

## 3. 使用CORS解决跨域问题的示例

下面我们修改一下server2.com的代码来解决前面遇到的跨域问题：

```
// cross-origin-examples/solve/server2.com/main.go
func main() {
http.HandleFunc("/api/data", func(w http.ResponseWriter, r *http.Request) {
fmt.Printf("recv request: %#v\n", *r)
w.Header().Set("Access-Control-Allow-Origin", "http://server1.com:8081")
w.Write([]byte("Welcome to api/data"))
})
http.ListenAndServe("server2.com:8082", nil)
}
```


我们仅在server2.com/main.go中增加了一行代码，旨在允许来自http://server1.com:8081的跨域请求访问server2.com的资源：

```
w.Header().Set("Access-Control-Allow-Origin", "http://server1.com:8081")
```


启动新版server2.com后，再点击页面上的“Make Cross-Origin Request”按钮，我们在浏览器的控制台上就能看到应答成功被接受并显示。

## 4. 小结

本文介绍了日常Web应用开发过程中经常遇到的跨域问题，探讨了“域(Origin)”概念以及跨域问题的真实原因：即浏览器的同源策略限制了不同源请求资源的访问。

接下来通过Go代码示例演示了跨域问题的表现形式，并介绍了几种主要的跨域解决方案，最后对最常见的CORS解决方案做了细致说明，并用实例展示了服务端设置CORS头后跨域问题的解决。

希望本文可以帮助大家更深入的理解和掌握Web应用跨域问题以及解决方法。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/cross-origin-examples)下载。

## 5. 参考资料

[The ultimate guide to enabling Cross-Origin Resource Sharing (CORS)](https://blog.logrocket.com/the-ultimate-guide-to-enabling-cross-origin-resource-sharing-cors/)– https://blog.logrocket.com/the-ultimate-guide-to-enabling-cross-origin-resource-sharing-cors/[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)– https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS[Glossary: Origin](https://developer.mozilla.org/en-US/docs/Glossary/Origin)– https://developer.mozilla.org/en-US/docs/Glossary/Origin[Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)– https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论