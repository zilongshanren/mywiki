---
title: http.Client的连接行为控制详解
url: https://tonybai.com/2021/04/02/go-http-client-connection-control/
published: '2021-04-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# http.Client的连接行为控制详解

![](../../assets/7fc5ced520a6e91a.png)


### 1. http包默认客户端

[Go语言以“自带电池”闻名](https://www.imooc.com/read/87/article/2341)，很多开发者对Go自带的功能丰富的标准库喜爱有加。而在Go标准库中，net/http包又是最受欢迎和最常用的包之一，我们用几行代码就能生成一个支持大并发、性能中上的http server。而http.Client也是用途最为广泛的http客户端，其性能也可以满足多数情况下的需求。知名女gopher[Jaana Dogan](https://github.com/rakyll)开源的类[apache ab](https://httpd.apache.org/docs/2.4/programs/ab.html)的[http性能测试工具hey](https://github.com/rakyll/hey)也是直接使用的http.Client，而没有用一些性能更好的第三方库（比如：[fasthttp](https://github.com/valyala/fasthttp))。

使用http包实现http客户端的最简单方法如下(来自[http包的官方文档](https://tip.golang.org/pkg/net/http/))：

```
resp, err := http.Get("http://example.com/")
...
resp, err := http.Post("http://example.com/upload", "image/jpeg", &buf)
...
```


注：别忘了在Get或Post成功后，调用defer resp.Body.Close()。


在http包的Get和Post函数背后，真正完成http客户端操作的是http包原生内置的DefaultClient：

```
// $GOROOT/src/net/http/client.go
// DefaultClient is the default Client and is used by Get, Head, and Post.
var DefaultClient = &Client{}
```


下面是一个使用DefaultClient的例子，我们先来创建一个特殊的http server：

```
// github.com/bigwhite/experiments/blob/master/http-client/default-client/server.go
package main
import (
"log"
"net/http"
"time"
)
func Index(w http.ResponseWriter, r *http.Request) {
log.Println("receive a request from:", r.RemoteAddr, r.Header)
time.Sleep(10 * time.Second)
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


我们看到这个http server的“不同之处”在于它不急于回复http应答，而是在接收请求10秒后再回复应答。下面是我们的http client端的代码：

```
// github.com/bigwhite/experiments/blob/master/http-client/default-client/client.go
package main
import (
"fmt"
"io"
"net/http"
"sync"
)
func main() {
var wg sync.WaitGroup
wg.Add(256)
for i := 0; i < 256; i++ {
go func() {
defer wg.Done()
resp, err := http.Get("http://localhost:8080")
if err != nil {
panic(err)
}
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body)
fmt.Println(string(body))
}()
}
wg.Wait()
}
```


上面的客户端创建了256个goroutine，每个goroutine向server建立一条连接，我们先启动server，然后再运行一下上面的这个客户端程序：

```
$go run server.go
$$go run client.go
panic: Get "http://localhost:8080": dial tcp [::1]:8080: socket: too many open files
goroutine 25 [running]:
main.main.func1(0xc000128280)
/Users/tonybai/Go/src/github.com/bigwhite/experiments/http-client/default-client/client.go:18 +0x1c7
created by main.main
/Users/tonybai/Go/src/github.com/bigwhite/experiments/http-client/default-client/client.go:14 +0x78
exit status 2
```


我们看到上面的客户端抛出了一个panic，提示：打开文件描述符过多。

上面演示环境的ulimit -n的值为256


我们用一幅示意图来描述上面例子中的情况：

![](../../assets/ca25b2239a7f2487.png)


尽管根据[《通过实例理解Go标准库http包是如何处理keep-alive连接的》](https://mp.weixin.qq.com/s/uH4lmsMs-hq5B3Ivq2jR5w)一文我们知道，默认情况下，http客户端是会保持连接并复用到同一主机的服务的连接的。但由于上述示例中server的延迟10s回应答的上下文，客户端在默认情况下不会等待应答回来，而是尝试建立新的连接去发送新的http请求。由于示例运行环境最大允许每个进程打开256个文件描述符，因此在客户端后期向服务端建立连接时，就会出现“socket: too many open files”的错误。

### 2. 定义在小范围应用的http客户端实例

那么我们该如何控制客户端的行为以避免在资源受限的上下文情况下完成客户端的发送任务呢？我们通过设置http.DefaultClient的相关属性来实现这一点，但DefaultClient是包级变量，在整个程序中是共享的，一旦修改其属性，其他使用http默认客户端的包也会受到影响。因此更好的方案是定义一个在小范围应用的http客户端实例。

代码：

```
resp, err := http.Get("http://example.com/")
...
resp, err := http.Post("http://example.com/upload", "image/jpeg", &buf)
...
```


等价于如下代码：

```
client := &http.Client{} // 自定义一个http客户端实例
resp, err := client.Get("http://example.com/")
...
resp, err := client.Post("http://example.com/upload", "image/jpeg", &buf)
...
```


不同的是我们自定义的http.Client实例的应用范围仅限于上述特定范围，不会对其他使用http默认客户端的包产生任何影响。不过此时我们自定义的http.Client实例client的行为与DefaultClient的无异，要想解决上面示例panic的问题，我们还需对自定义的新客户端实例做一进步行为定制。

### 3. 定制到某一host的最大连接数

上述示例的最大问题在于向server端建立的连接数不受控制，即便将每个进程可以打开的最大文件描述符个数调大，客户端还可能会遇到最大向外建立的65535个连接的极限瓶颈(客户端socket端口用尽)，因此一个严谨的客户端需要设置到某个host的最大连接数限制。

那么，http.Client是如何控制到某个host的最大连接数的呢？http包的Client结构如下：

```
//$GOROOT/src/net/http/client.go
type Client struct {
// Transport specifies the mechanism by which individual
// HTTP requests are made.
// If nil, DefaultTransport is used.
Transport RoundTripper
CheckRedirect func(req *Request, via []*Request) error
Jar CookieJar
Timeout time.Duration
```


Client结构体一共四个字段，能控制Client连接行为的是Transport字段。如果Transport的值为nil，那么Client的连接行为遵守DefaultTransport的设置：

```
// $GOROOT/src/net/http/transport.go
var DefaultTransport RoundTripper = &Transport{
Proxy: ProxyFromEnvironment,
DialContext: (&net.Dialer{
Timeout: 30 * time.Second,
KeepAlive: 30 * time.Second,
}).DialContext,
ForceAttemptHTTP2: true,
MaxIdleConns: 100,
IdleConnTimeout: 90 * time.Second,
TLSHandshakeTimeout: 10 * time.Second,
ExpectContinueTimeout: 1 * time.Second,
}
```


不过在这份DefaultTransport的“配置”中，并没有有关向某个host建立最大连接数的设置，因为在Transport结构体中，起到这个作用的字段是MaxConnsPerHost：

```
// $GOROOT/src/net/http/transport.go
type Transport struct {
... ...
// MaxConnsPerHost optionally limits the total number of
// connections per host, including connections in the dialing,
// active, and idle states. On limit violation, dials will block.
//
// Zero means no limit.
MaxConnsPerHost int
... ...
}
```


我们来改造一下上面的示例：

```
// github.com/bigwhite/experiments/blob/master/http-client/client-with-maxconnsperhost/client.go
package main
import (
"fmt"
"io"
"net/http"
"sync"
)
func main() {
var wg sync.WaitGroup
wg.Add(256)
tr := &http.Transport{
MaxConnsPerHost: 5,
}
client := http.Client{
Transport: tr,
}
for i := 0; i < 256; i++ {
go func(i int) {
defer wg.Done()
resp, err := client.Get("http://localhost:8080")
if err != nil {
panic(err)
}
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body)
fmt.Printf("g-%d: %s\n", i, string(body))
}(i)
}
wg.Wait()
}
```


上面的代码不再使用DefaultClient，而是自定义了一个新Client实例，并设置该实例的Transport字段为我们新建的设置了MaxConsPerHost字段的Transport实例。将server启动，并执行上面client.go，我们从server端看到如下结果：

```
$go run server.go
receive a request from: [::1]:63677 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63675 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63676 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63673 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63674 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63673 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63675 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63674 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63676 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63677 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63677 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63674 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63676 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63675 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:63673 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
```


我们看到：客户端一共向server端建立了5条连接(客户端端口号从63673到63677)，并且每隔10s，客户端复用这5条连接发送下一批请求。

http.Transport维护了到每个server host的计数器connsPerHost和请求等待队列：

```
// $GOROOT/src/net/http/transport.go
type Transport struct {
... ...
connsPerHostMu sync.Mutex
connsPerHost map[connectMethodKey]int
connsPerHostWait map[connectMethodKey]wantConnQueue // waiting getConns
... ...
}
```


Transport结构体使用了一个connectMethodKey结构作为key：

```
// $GOROOT/src/net/http/transport.go
type connectMethodKey struct {
proxy, scheme, addr string
onlyH1 bool
}
```


我们看到connectMethodKey使用一个四元组(proxy,scheme,addr, onlyH1)来唯一标识一个“host”。通常对一个Client实例而言，proxy，scheme和onlyH1都是相同的，不同的是addr(ip+port)，因此实际上也就是按addr区分host。我们同样用一幅示意图描示意一下这种情况：

![](../../assets/0e5caa3eb95746c0.png)


### 4. 设定idle池的大小

不知道大家是否想到这点：当上面示例中的到某一个host的五个链接没那么繁忙时，依旧保持这个五个链接是不是有些浪费资源呢？至少占用着客户端端口以及服务端的文件描述符资源。我们是否能让客户端在闲时减少保持的到服务端的链接数量呢？我们可以通过Transport结构体类型中的MaxIdleConnsPerHost字段实现这一点。

其实如果你不显式设置MaxIdleConnsPerHost，http包也会使用其默认值(2)：

```
// $GOROOT/src/net/http/transport.go
// DefaultMaxIdleConnsPerHost is the default value of Transport's
// MaxIdleConnsPerHost.
const DefaultMaxIdleConnsPerHost = 2
```


我们用一个例子来验证http.Client的这一行为！

首先我们改变一下server端的行为，将原先的“等待10s”改为立即返回应答：

```
// github.com/bigwhite/experiments/blob/master/http-client/client-with-maxidleconnsperhost/server.go
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


而对于client，我们需要精心设计一下：

```
// github.com/bigwhite/experiments/blob/master/http-client/client-with-maxidleconnsperhost/client.go
1 package main
2
3 import (
4 "fmt"
5 "io"
6 "net/http"
7 "sync"
8 "time"
9 )
10
11 func main() {
12 var wg sync.WaitGroup
13 wg.Add(5)
14 tr := &http.Transport{
15 MaxConnsPerHost: 5,
16 MaxIdleConnsPerHost: 3,
17 }
18 client := http.Client{
19 Transport: tr,
20 }
21 for i := 0; i < 5; i++ {
22 go func(i int) {
23 defer wg.Done()
24 resp, err := client.Get("http://localhost:8080")
25 if err != nil {
26 panic(err)
27 }
28 defer resp.Body.Close()
29 body, err := io.ReadAll(resp.Body)
30 fmt.Printf("g-%d: %s\n", i, string(body))
31 }(i)
32 }
33 wg.Wait()
34
35 time.Sleep(10 * time.Second)
36
37 wg.Add(5)
38 for i := 0; i < 5; i++ {
39 go func(i int) {
40 defer wg.Done()
41
42 for i := 0; i < 100; i++ {
43 resp, err := client.Get("http://localhost:8080")
44 if err != nil {
45 panic(err)
46 }
47 defer resp.Body.Close()
48 body, err := io.ReadAll(resp.Body)
49 fmt.Printf("g-%d: %s\n", i+10, string(body))
50 time.Sleep(time.Second)
51 }
52 }(i)
53 }
54 wg.Wait()
55 }
```


我们首先制造一次忙碌的发送行为(21~32行)，使得client端建满5个连接；然后等待10s，即让client闲下来；之后再建立5个groutine，以每秒一条的速度向server端发送请求(不忙的节奏)，我们来看看程序运行后服务端的输出：

```
$go run server.go
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56246 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56245 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56242 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56244 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:56243 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
... ...
```


我们来分析一下：

- 第一部分的五行输出是“忙时”client端建立的5条不同的连接，客户端端口号从56242到56246；

- 第二部分的五行输出是“非忙时”client利用idle池中的连接发送的请求，关键点就在于这5个请求的源端口号：56242、56243和56244，五个请求使用了三个早已建立好的alive的连接；

- 后面的几部分使用的也是这三个早已建立好的alive的连接。

这就是MaxIdleConnsPerHost的作用：最初“忙时”建立的5条连接，在client进入闲时时要进入idle状态。但MaxIdleConnsPerHost的值为3，也就是说只有3条连接可以进入idle池，而另外两个会被close掉。于是源端口号为56242、56243和56244的三条连接被保留了下来。

下面是这节例子的示意图：

![](../../assets/730ebeee75321510.png)


Transport结构体还有一个字段与idle池有关，那就是MaxIdleConns，不同于MaxIdleConnsPerHost只针对某个host，MaxIdleConns是针对整个Client的所有idle池中的连接数的和，这个和不能超过MaxIdleConns。

### 5. 清理idle池中的连接

如果没有其他设定，那么一个Client到一个host在闲时至少会保持DefaultMaxIdleConnsPerHost个idle连接(前提是之前已经建立了2条或2条以上的连接)，但如果Client针对这个host一直就保持无流量的状态，那么idle池中的连接也是一种资源浪费。于是Transport又提供了IdleConnTimeout字段用于超时清理idle池中的长连接。下面的示例复用上面的server，但client.go改为如下形式：

```
// github.com/bigwhite/experiments/blob/master/http-client/client-with-idleconntimeout/client.go
1 package main
2
3 import (
4 "fmt"
5 "io"
6 "net/http"
7 "sync"
8 "time"
9 )
10
11 func main() {
12 var wg sync.WaitGroup
13 wg.Add(5)
14 tr := &http.Transport{
15 MaxConnsPerHost: 5,
16 MaxIdleConnsPerHost: 3,
17 IdleConnTimeout: 10 * time.Second,
18 }
19 client := http.Client{
20 Transport: tr,
21 }
22 for i := 0; i < 5; i++ {
23 go func(i int) {
24 defer wg.Done()
25 resp, err := client.Get("http://localhost:8080")
26 if err != nil {
27 panic(err)
28 }
29 defer resp.Body.Close()
30 body, err := io.ReadAll(resp.Body)
31 fmt.Printf("g-%d: %s\n", i, string(body))
32 }(i)
33 }
34 wg.Wait()
35
36 time.Sleep(5 * time.Second)
37
38 wg.Add(5)
39 for i := 0; i < 5; i++ {
40 go func(i int) {
41 defer wg.Done()
42 for i := 0; i < 2; i++ {
43 resp, err := client.Get("http://localhost:8080")
44 if err != nil {
45 panic(err)
46 }
47 defer resp.Body.Close()
48 body, err := io.ReadAll(resp.Body)
49 fmt.Printf("g-%d: %s\n", i+10, string(body))
50 time.Sleep(time.Second)
51 }
52 }(i)
53 }
54
55 time.Sleep(15 * time.Second)
56 wg.Add(5)
57
58 for i := 0; i < 5; i++ {
59 go func(i int) {
60 defer wg.Done()
61 for i := 0; i < 100; i++ {
62 resp, err := client.Get("http://localhost:8080")
63 if err != nil {
64 panic(err)
65 }
66 defer resp.Body.Close()
67 body, err := io.ReadAll(resp.Body)
68 fmt.Printf("g-%d: %s\n", i+20, string(body))
69 time.Sleep(time.Second)
70 }
71 }(i)
72 }
73 wg.Wait()
74 }
```


这个client.go代码分为三部分：首先和上个示例一样，我们首先制造一次忙碌的发送行为(22~33行)，使得client端建满5个连接；然后等待5s，即让client闲下来；之后再建立5个groutine，以每秒一条的速度向server端发送请求(不忙的节奏)；第三部分同样是先等待15s，然后创建5个goroutine分别以不忙的节奏向server端发送请求。我们来看看程序运行后服务端的输出：

```
$go run server.go
receive a request from: [::1]:52484 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52488 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52486 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52485 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52487 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52487 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52488 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52484 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52484 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52487 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52487 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52488 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52484 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52487 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52484 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52542 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52544 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52545 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52543 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52546 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52542 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52544 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52545 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52542 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
receive a request from: [::1]:52544 map[Accept-Encoding:[gzip] User-Agent:[Go-http-client/1.1]]
... ...
```


这里摘录5段输出。和预想的一样，第一段client向server建立了5条连接(客户端的端口号从52484~52487)；暂停5s后，新创建的5个goroutine通过idle池中的三条保持的连接向server发送请求(第二段和第三段，端口号:52484、52487、52488)；之后暂停15s，由于设置了IdleConnTimeout，idle池中的三条连接也被close掉了。这时再发送请求，client会重新建立连接（第四段，端口号52542~52546），最后一段则又开始通过idle池中的三条保持的连接向server发送请求了(端口号：52542、52544和52545)。

### 6. 其他控制项

如果觉得idle池超时清理依旧会占用“资源”一小会儿，那么可以利用Transport的DisableKeepAlives使得每个请求都创建一个新连接，即不复用keep-alive连接。当然这种控制设定在忙时导致的频繁建立新连接的损耗可是要比占用一些“资源”来的更大。示例可参考 github.com/bigwhite/experiments/blob/master/http-client/client-with-disablekeepalives，这里就不贴出来了。

另外像本文开始示例中server那样等待10s才回应答的行为可不是所有client端都能接受的，为了限定应答及时返回，client端可以设定等待应答的超时时间，如果超时，client将返回失败。http.Client结构中的Timeout可以实现这一特性。示例可参考 github.com/bigwhite/experiments/blob/master/http-client/client-with-timeout，这里同样不贴出来了。

本文涉及的代码可以在[这里](https://github.com/bigwhite/experiments/blob/master/http-client)下载：https://github.com/bigwhite/experiments/blob/master/http-client。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，>每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需>求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足>广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖>中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


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

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论