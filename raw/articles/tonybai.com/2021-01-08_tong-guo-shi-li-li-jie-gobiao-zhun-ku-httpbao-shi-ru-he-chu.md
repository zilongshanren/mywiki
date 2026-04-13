---
title: 通过实例理解Go标准库http包是如何处理keep-alive连接的
url: https://tonybai.com/2021/01/08/understand-how-http-package-deal-with-keep-alive-connection/
published: '2021-01-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Go标准库http包是如何处理keep-alive连接的

![img{512x368}](../../assets/80955bb8063598b8.png)


HTTP是如今互联网的基础协议，承载了互联网上的绝大部分应用层流量，并且从目前趋势来看，在未来10年，http仍然会是互联网应用的主要协议。[Go语言自带“电池”](https://www.imooc.com/read/87/article/2341)，基于Go标准库我们可以轻松建立起一个http server处理客户端http请求，或创建一个http client向服务端发送http请求。

最初早期的http 1.0协议只支持短连接，即客户端每发送一个请求，就要和服务器端建立一个新TCP连接，请求处理完毕后，该连接将被拆除。显然每次tcp连接握手和拆除都将带来较大损耗，为了能充分利用已建立的连接，后来的http 1.0更新版和http 1.1支持在http请求头中加入**Connection: keep-alive**来告诉对方这个请求响应完成后不要关闭链接，下一次还要复用这个连接以继续传输后续请求和响应。后HTTP协议规范明确规定了HTTP/1.0版本如果想要保持长连接，需要在请求头中加上**Connection: keep-alive**，而HTTP/1.1版本将支持keep-alive长连接作为默认选项，有没有这个请求头都可以。

本文我们就来一起看看Go标准库中net/http包的http.Server和http.Client对keep-alive长连接的处理以及如何在Server和Client侧关闭keep-alive机制。

### 1. http包默认启用keep-alive

按照HTTP/1.1的规范，Go http包的http server和client的实现默认将所有连接视为长连接，无论这些连接上的初始请求是否带有**Connection: keep-alive**。

下面分别是使用go http包的默认机制实现的一个http client和一个http server：

默认开启keep-alive的http client实现：

```
//github.com/bigwhite/experiments/http-keep-alive/client-keepalive-on/client.go
package main
import (
"fmt"
"io/ioutil"
"net/http"
)
func main() {
c := &http.Client{}
req, err := http.NewRequest("Get", "http://localhost:8080", nil)
if err != nil {
panic(err)
}
fmt.Printf("%#v\n", *req)
for i := 0; i < 5; i++ {
resp, err := c.Do(req)
if err != nil {
fmt.Println("http get error:", err)
return
}
defer resp.Body.Close()
b, err := ioutil.ReadAll(resp.Body)
if err != nil {
fmt.Println("read body error:", err)
return
}
fmt.Println("response body:", string(b))
}
}
```


默认开启keep-alive的http server实现：

```
//github.com/bigwhite/experiments/http-keep-alive/server-keepalive-on/server.go
package main
import (
"fmt"
"net/http"
)
func Index(w http.ResponseWriter, r *http.Request) {
fmt.Println("receive a request from:", r.RemoteAddr, r.Header)
w.Write([]byte("ok"))
}
func main() {
var s = http.Server{
Addr: ":8080",
Handler: http.HandlerFunc(Index),
}
s.ListenAndServe()
}
```


现在我们启动上面的http server：

```
// server-keepalive-on目录下
$go run server.go
```


我们使用上面的client向该server发起5次http请求：

```
// client-keepalive-on目录下
$go run client.go
http.Request{Method:"Get", URL:(*url.URL)(0xc00016a000), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{}, Body:io.ReadCloser(nil), GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:0, TransferEncoding:[]string(nil), Close:false, Host:"localhost:8080", Form:url.Values(nil), PostForm:url.Values(nil), MultipartForm:(*multipart.Form)(nil), Trailer:http.Header(nil), RemoteAddr:"", RequestURI:"", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.emptyCtx)(0xc00012c008)}
response body: ok
response body: ok
response body: ok
response body: ok
response body: ok
```


这期间server端输出的日志如下：

```
receive a request from: [::1]:55238 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:55238 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:55238 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:55238 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:55238 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


我们简单分析一下两端的输出结果：

- 从server端打印的请求的头部字段来看，客户端发来的请求header中并没有显式包含
**Connection: keep-alive**，而仅有Accept-Encoding和User-Agent两个header字段； - server端处理的5个请求均来自同一个连接“[::1]:55238”，Server端默认保持了该连接，而不是在处理完一个请求后将连接关闭，说明两端均复用了第一个请求创建的http连接。

即便我们的client端每间隔5秒发送一次请求，server端默认也不会关闭连接(我们将fmt包缓冲log包，输出带有时间戳的日志)：

```
// client-keepalive-on目录下
$go run client-with-delay.go
http.Request{Method:"Get", URL:(*url.URL)(0xc00016a000), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{}, Body:io.ReadCloser(nil), GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:0, TransferEncoding:[]string(nil), Close:false, Host:"localhost:8080", Form:url.Values(nil), PostForm:url.Values(nil), MultipartForm:(*multipart.Form)(nil), Trailer:http.Header(nil), RemoteAddr:"", RequestURI:"", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.emptyCtx)(0xc00012c008)}
2021/01/03 12:25:21 response body: ok
2021/01/03 12:25:26 response body: ok
2021/01/03 12:25:31 response body: ok
2021/01/03 12:25:36 response body: ok
2021/01/03 12:25:41 response body: ok
// server-keepalive-on目录下
$go run server.go
2021/01/03 12:25:21 receive a request from: [::1]:58419 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:25:26 receive a request from: [::1]:58419 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:25:31 receive a request from: [::1]:58419 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:25:36 receive a request from: [::1]:58419 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:25:41 receive a request from: [::1]:58419 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


### 2. http client端基于非keep-alive连接发送请求

有时候http client在一条连接上的数据请求密度并不高，因此client端并不想长期保持这条连接(占用端口资源)，那么client端如何协调Server端在处理完请求返回应答后就关闭这条连接呢？我们看看在Go中如何实现这一场景需求：

```
//github.com/bigwhite/experiments/http-keep-alive/client-keepalive-off/client.go
... ...
func main() {
tr := &http.Transport{
DisableKeepAlives: true,
}
c := &http.Client{
Transport: tr,
}
req, err := http.NewRequest("Get", "http://localhost:8080", nil)
if err != nil {
panic(err)
}
for i := 0; i < 5; i++ {
resp, err := c.Do(req)
if err != nil {
fmt.Println("http get error:", err)
return
}
defer resp.Body.Close()
b, err := ioutil.ReadAll(resp.Body)
if err != nil {
fmt.Println("read body error:", err)
return
}
log.Println("response body:", string(b))
time.Sleep(5 * time.Second)
}
}
```


http.Client底层的数据连接建立和维护是由http.Transport实现的，http.Transport结构有一个DisableKeepAlives字段，其默认值为false，即启动keep-alive。这里我们将其置为true，即关闭keep-alive，然后将该Transport实例作为初值，赋值给http Client实例的Transport字段。

接下来，我们使用这个client向上面那个http server发送五个请求，请求间间隔5秒(模拟连接空闲的状态)，我们得到如下结果(从server端打印信息观察)：

```
// 在client-keepalive-off下面
$go run client.go
2021/01/03 12:42:38 response body: ok
2021/01/03 12:42:43 response body: ok
2021/01/03 12:42:48 response body: ok
2021/01/03 12:42:53 response body: ok
2021/01/03 12:42:58 response body: ok
// 在server-keepalive-on下面
$go run server.go
2021/01/03 12:42:38 receive a request from: [::1]:62287 map[Accept-Encoding:[gzip] Connection:[close] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:42:43 receive a request from: [::1]:62301 map[Accept-Encoding:[gzip] Connection:[close] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:42:48 receive a request from: [::1]:62314 map[Accept-Encoding:[gzip] Connection:[close] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:42:53 receive a request from: [::1]:62328 map[Accept-Encoding:[gzip] Connection:[close] User-Agent:[Go-http-client/1.1]]
2021/01/03 12:42:58 receive a request from: [::1]:62342 map[Accept-Encoding:[gzip] Connection:[close] User-Agent:[Go-http-client/1.1]]
```


从Server的输出结果来看，来自客户端的请求中增加了**Connection:[close]**的头字段，当收到这样的请求后，Server端便不再保持这一连接了。我们也看到上面日志中，每个请求都是通过不同的客户端端口发送出来的，显然这是五条不同的连接。

### 3. 建立一个不支持keep-alive连接的http server

假设我们有这样的一个需求，server端完全不支持keep-alive的连接，无论client端发送的请求header中是否显式带有**Connection: keep-alive**，server端都会在返回应答后关闭连接。那么在Go中，我们如何来实现这一需求呢？我们来看下面代码：

```
//github.com/bigwhite/experiments/http-keep-alive/server-keepalive-off/server.go
package main
import (
"log"
"net/http"
)
func Index(w http.ResponseWriter, r *http.Request) {
log.Println("receive a request from:", r.RemoteAddr, r.Header)
w.Write([]byte("ok"))
}
func main() {
var s = http.Server{
Addr: ":8080",
Handler: http.HandlerFunc(Index),
}
s.SetKeepAlivesEnabled(false)
s.ListenAndServe()
}
```


我们看到在ListenAndServe前，我们调用了http.Server的SetKeepAlivesEnabled方法，并传入false参数，这样我们就在全局层面关闭了该Server对keep-alive连接的支持，我们用前面client-keepalive-on下面的client向该Server发送五个请求：

```
// 在client-keepalive-on下面
$go run client.go
http.Request{Method:"Get", URL:(*url.URL)(0xc000174000), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{}, Body:io.ReadCloser(nil), GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:0, TransferEncoding:[]string(nil), Close:false, Host:"localhost:8080", Form:url.Values(nil), PostForm:url.Values(nil), MultipartForm:(*multipart.Form)(nil), Trailer:http.Header(nil), RemoteAddr:"", RequestURI:"", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.emptyCtx)(0xc00013a008)}
2021/01/03 13:30:08 response body: ok
2021/01/03 13:30:08 response body: ok
2021/01/03 13:30:08 response body: ok
2021/01/03 13:30:08 response body: ok
2021/01/03 13:30:08 response body: ok
// 在server-keepalive-off下面
$go run server.go
2021/01/03 13:30:08 receive a request from: [::1]:53005 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 13:30:08 receive a request from: [::1]:53006 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 13:30:08 receive a request from: [::1]:53007 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 13:30:08 receive a request from: [::1]:53008 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 13:30:08 receive a request from: [::1]:53009 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


我们看到该Server在处理完每个请求后就关闭了传输该请求的连接，这导致client测不得不为每个请求建立一个新连接(从server输出的客户端地址和端口看出)。

### 4. 支持长连接闲置超时关闭的http server

显然上面的server处理方式“太过霸道”，对于想要复用连接，提高请求和应答传输效率的client而言，上面的“一刀切”机制并不合理。那么是否有一种机制可以让http server即可以对高密度传输数据的连接保持keep-alive，又可以及时清理掉那些长时间没有数据传输的idle连接，释放占用的系统资源呢？我们来看下面这个go实现的server：

```
//github.com/bigwhite/experiments/http-keep-alive/server-keepalive-with-idletimeout/server.go
package main
import (
"log"
"net/http"
"time"
)
func Index(w http.ResponseWriter, r *http.Request) {
log.Println("receive a request from:", r.RemoteAddr, r.Header)
w.Write([]byte("ok"))
}
func main() {
var s = http.Server{
Addr: ":8080",
Handler: http.HandlerFunc(Index),
IdleTimeout: 5 * time.Second,
}
s.ListenAndServe()
}
```


从代码中我们看到，我们仅在创建http.Server实例时显式为其字段IdleTimeout做了一次显式赋值，设置idle连接的超时时间为5s。下面是Go标准库中关于http.Server的字段IdleTimeout的注释：

```
// $GOROOT/src/net/server.go
// IdleTimeout是当启用keep-alive时等待下一个请求的最大时间。
// 如果IdleTimeout为零，则使用ReadTimeout的值。如果两者都是
// 零，则没有超时。
IdleTimeout time.Duration
```


我们来看看效果如何，是否是我们期望那样的。为了测试效果，我们改造了client端，放在client-keepalive-on-with-idle下面：

```
//github.com/bigwhite/experiments/http-keep-alive/client-keepalive-on-with-idle/client.go
... ...
func main() {
c := &http.Client{}
req, err := http.NewRequest("Get", "http://localhost:8080", nil)
if err != nil {
panic(err)
}
for i := 0; i < 5; i++ {
log.Printf("round %d begin:\n", i+1)
for j := 0; j < i+1; j++ {
resp, err := c.Do(req)
if err != nil {
fmt.Println("http get error:", err)
return
}
defer resp.Body.Close()
b, err := ioutil.ReadAll(resp.Body)
if err != nil {
fmt.Println("read body error:", err)
return
}
log.Println("response body:", string(b))
}
log.Printf("round %d end\n", i+1)
time.Sleep(7 * time.Second)
}
}
```


client端请求分为5轮，轮与轮之间间隔7秒，下面是通信过程与结果：

```
// 在client-keepalive-on-with-idle下
$go run client.go
2021/01/03 14:17:05 round 1 begin:
2021/01/03 14:17:05 response body: ok
2021/01/03 14:17:05 round 1 end
2021/01/03 14:17:12 round 2 begin:
2021/01/03 14:17:12 response body: ok
2021/01/03 14:17:12 response body: ok
2021/01/03 14:17:12 round 2 end
2021/01/03 14:17:19 round 3 begin:
2021/01/03 14:17:19 response body: ok
2021/01/03 14:17:19 response body: ok
2021/01/03 14:17:19 response body: ok
2021/01/03 14:17:19 round 3 end
2021/01/03 14:17:26 round 4 begin:
2021/01/03 14:17:26 response body: ok
2021/01/03 14:17:26 response body: ok
2021/01/03 14:17:26 response body: ok
2021/01/03 14:17:26 response body: ok
2021/01/03 14:17:26 round 4 end
2021/01/03 14:17:33 round 5 begin:
2021/01/03 14:17:33 response body: ok
2021/01/03 14:17:33 response body: ok
2021/01/03 14:17:33 response body: ok
2021/01/03 14:17:33 response body: ok
2021/01/03 14:17:33 response body: ok
2021/01/03 14:17:33 round 5 end
// 在server-keepalive-with-idletimeout下
$go run server.go
2021/01/03 14:17:05 receive a request from: [::1]:64071 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:12 receive a request from: [::1]:64145 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:12 receive a request from: [::1]:64145 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:19 receive a request from: [::1]:64189 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:19 receive a request from: [::1]:64189 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:19 receive a request from: [::1]:64189 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:26 receive a request from: [::1]:64250 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:26 receive a request from: [::1]:64250 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:26 receive a request from: [::1]:64250 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:26 receive a request from: [::1]:64250 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:33 receive a request from: [::1]:64304 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:33 receive a request from: [::1]:64304 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:33 receive a request from: [::1]:64304 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:33 receive a request from: [::1]:64304 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:17:33 receive a request from: [::1]:64304 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


我们看到：

- 在每轮内，client端的所有请求都是复用已建立的连接；

- 但每轮之间，由于Sleep了7秒，超出了server端idletimeout的时长，上一轮的连接被拆除，新一轮只能重建连接。

我们期望的效果实现了！

### 5. 一个http client可管理到多个server的连接

Go标准库的http.Client与一个server可不是一对一的关系，它可以实现一对多的http通信，也就是说一个http client可管理到多个server的连接，并优先复用到同一server的连接(keep-alive)，而不是建立新连接，就像我们上面看到的那样。我们来创建一个向多个server发送请求的client：

```
//github.com/bigwhite/experiments/http-keep-alive/client-keepalive-on-to-multiple-servers/client.go
... ...
func main() {
c := &http.Client{}
req1, err := http.NewRequest("Get", "http://localhost:8080", nil)
if err != nil {
panic(err)
}
req2, err := http.NewRequest("Get", "http://localhost:8081", nil)
if err != nil {
panic(err)
}
for i := 0; i < 5; i++ {
resp1, err := c.Do(req1)
if err != nil {
fmt.Println("http get error:", err)
return
}
defer resp1.Body.Close()
b1, err := ioutil.ReadAll(resp1.Body)
if err != nil {
fmt.Println("read body error:", err)
return
}
log.Println("response1 body:", string(b1))
resp2, err := c.Do(req2)
if err != nil {
fmt.Println("http get error:", err)
return
}
defer resp2.Body.Close()
b2, err := ioutil.ReadAll(resp2.Body)
if err != nil {
fmt.Println("read body error:", err)
return
}
log.Println("response2 body:", string(b2))
time.Sleep(5 * time.Second)
}
}
```


我们建立两个默认的http server，分别监听8080和8081，运行上面client：

```
$go run client.go
2021/01/03 14:52:20 response1 body: ok
2021/01/03 14:52:20 response2 body: ok
2021/01/03 14:52:25 response1 body: ok
2021/01/03 14:52:25 response2 body: ok
2021/01/03 14:52:30 response1 body: ok
2021/01/03 14:52:30 response2 body: ok
2021/01/03 14:52:35 response1 body: ok
2021/01/03 14:52:35 response2 body: ok
2021/01/03 14:52:40 response1 body: ok
2021/01/03 14:52:40 response2 body: ok
```


server端的输出结果如下：

```
// server1(8080):
2021/01/03 14:52:20 receive a request from: [::1]:63871 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:25 receive a request from: [::1]:63871 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:30 receive a request from: [::1]:63871 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:35 receive a request from: [::1]:63871 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:40 receive a request from: [::1]:63871 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
// server2(8081):
2021/01/03 14:52:20 receive a request from: [::1]:63872 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:25 receive a request from: [::1]:63872 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:30 receive a request from: [::1]:63872 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:35 receive a request from: [::1]:63872 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
2021/01/03 14:52:40 receive a request from: [::1]:63872 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


我们看到client同时支持与多个server进行通信，并针对每个server可以使用keep-alive的连接进行高效率通信。

本文涉及源代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/http-keep-alive)(https://github.com/bigwhite/experiments/tree/master/http-keep-alive)下载。

“Gopher部落”知识星球开球了！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021 – 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

1. 第一段代码里会 defer resp.Body.Close() 会导致循环结束后才真正关闭连接

2. 第二段代码里s设置了Handler之后，http.HandleFunc(“/”, Index) 就没有必要写了

问题1： 有意而为之，毕竟是demo。可能不是好的示范；

问题2：改成自建server后，忘记删除第一行了。:)

感谢提醒。

目前来看在http server层，我们可以通过 SetKeepAlivesEnabled() 方法控制是否开启KeepAlive；另外可以通过配置 IdleTimeout参数来设置超时时间，但目前并不能控制KeepAlive的心跳间隔时间。 tcp层有个SetKeepAlivePeriod()方法，但是貌似tcp和http的KeepAlive概念并不完全一致。

我理解心跳检测由client负责维持，在http client层，可以通过 Transport 下 KeepAlive参数来控制心跳检测间隔。

文章里：

http.Client底层的数据连接建立和维护是由http.Transport实现的，http.Transport结构有一个DisableKeepAlives字段，其默认值为false，即启动keep-alive。这里我们将其置为false，即关闭keep-alive，然后将该Transport实例作为初值，赋值给http Client实例的Transport字段。

—-

应该是将其设为true，关闭keep-alive吧。

笔误，感谢指出！已经修改了。