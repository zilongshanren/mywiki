---
title: 使用functrace辅助进行Go项目源码分析
url: https://tonybai.com/2021/06/04/go-source-analysis-with-functrace/
published: '2021-06-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用functrace辅助进行Go项目源码分析

![](../../assets/2c5421972d3c6fb1.png)


[本文永久链接](https://tonybai.com/2021/06/04/go-source-analysis-with-functrace) – https://tonybai.com/2021/06/04/go-source-analysis-with-functrace

在[《像跟踪分布式服务调用那样跟踪Go函数调用链》](https://mp.weixin.qq.com/s/zrM0I-CsEujAm6ho6AD79g)一文中，我们介绍了一种跟踪函数调用链的思路，并给出了一种实现[functrace](https://github.com/bigwhite/functrace)：https://github.com/bigwhite/functrace。这个小工具不仅仅是分享给大家的，我自己在工作和学习时也在使用。最近发现这个小工具在阅读和分析某个Go项目源码时也能起到关键的辅助作用。这里就和大家简单讲解一下如何用functrace来辅助Go源码阅读和分析。

程序员的日常离不开“源码阅读和分析”，日常阅读代码的姿势无非是这么几种（或几种的组合）：

- 结合源码编辑器或IDE提供的强大的源码交叉索引和跳转功能在一个庞大的源码库中建立起代码间的联系；
- 将代码跑起来，在代码中加上一些print输出，跟踪执行流并画出；
- 也有人喜欢用调试器从一点（通常是main）开始单步跟踪执行流。

无论哪一种方式，最终只要时间够长，态度到位，总是会将代码分析出个七七八八的。

就笔者来看，无论是哪种范式：命令式、面向对象、函数式，最终梳理出来的源码脉络都是建立在执行基本单元(函数或方法)上，代码的执行主线（并发程序会有若干条）本质上就是一条函数/方法调用链。只要把这条链理出来，代码理解起来就不难了。上述的代码阅读方法实质也是参照这个逻辑的。只是对于调用层次较深，还伴随有回调的代码，梳理调用链难度高、效率低。

functrace最初用于跟踪函数调用链（得益于Go核心开发团队公开的[抽象语法树AST API](https://tip.golang.org/pkg/go/ast/)），但如果在阅读代码时直接用functrace输出函数调用链，那将大幅提高我们源码阅读分析的效率。下面我们就用一个样例项目来试试如何用functrace梳理出代码的执行主线。

我们以Go高性能、轻量级、非阻塞的事件驱动网络框架gnet为例，来看看如何阅读分析gnet的源码。首先我们需要安装functrace工具：

```
$go install github.com/bigwhite/functrace/cmd/gen@latest
go: downloading github.com/bigwhite/functrace v0.0.0-20210603024853-ccab68a2604c
go: downloading golang.org/x/tools v0.0.0-20201204062850-545788942d5f
$gen -h
[gen -h]
gen [-w] xxx.go
-w write result to (source) file instead of stdout
```


接下来，我们下载要进行源码分析的gnet源码：

```
$git clone git@github.com:panjf2000/gnet.git
```


我们进入gnet目录，现在我们可以使用gen命令为任意go源文件添加“跟踪设施”了，比如：

```
$gen -w gnet.go
[gen -w gnet.go]
add trace for gnet.go ok
$ git diff gnet.go
diff --git a/gnet.go b/gnet.go
index b4c04a5..a7afe2b 100644
--- a/gnet.go
+++ b/gnet.go
@@ -29,6 +29,7 @@ import (
"sync"
"time"
+ "github.com/bigwhite/functrace"
"github.com/panjf2000/gnet/errors"
"github.com/panjf2000/gnet/internal"
"github.com/panjf2000/gnet/internal/logging"
... ...
```


我们可以这样根据自己的需要在特定的go源文件上添加“跟踪设施”，但是多数情况下，我们也可以通过脚本为项目内所有go源文件批量添加“跟踪设施”，functrace项目提供了一个简单的脚本[batch_add_trace.sh](https://github.com/bigwhite/functrace/blob/main/scripts/batch_add_trace.sh)，下面我们就来通过该脚本将gnet下的go源文件批量加上函数跟踪设施：

下载functrace源码：

```
$git clone https://github.com/bigwhite/functrace.git
```


将functrace/scripts/batch_add_trace.sh 拷贝到上面gnet目录下并执行下面命令：

```
# bash batch_add_trace.sh
... ...
[gen -w ./server_unix.go]
add trace for ./server_unix.go ok
[gen -w ./internal/socket/sockopts_posix.go]
add trace for ./internal/socket/sockopts_posix.go ok
... ...
[gen -w ./ringbuffer/ring_buffer_test.go]
add trace for ./ringbuffer/ring_buffer_test.go ok
[gen -w ./ringbuffer/ring_buffer.go]
add trace for ./ringbuffer/ring_buffer.go ok
[gen -w ./pool/bytebuffer/bytebuffer.go]
no trace added for ./pool/bytebuffer/bytebuffer.go
[gen -w ./pool/goroutine/goroutine.go]
add trace for ./pool/goroutine/goroutine.go ok
[gen -w ./pool/ringbuffer/ringbuffer.go]
add trace for ./pool/ringbuffer/ringbuffer.go ok
[gen -w ./loop_linux.go]
add trace for ./loop_linux.go ok
[gen -w ./server_windows.go]
add trace for ./server_windows.go ok
```


接下来我们编写一个基于gnet的程序，我们就使用gnet参加[TechEmpower](https://github.com/TechEmpower/FrameworkBenchmarks/tree/master/frameworks/Go/gnet)的那份代码：

```
//main.go
package main
import (
"bytes"
"flag"
"fmt"
"log"
"runtime"
"time"
"github.com/panjf2000/gnet"
)
type httpServer struct {
*gnet.EventServer
}
type httpCodec struct {
delimiter []byte
}
func (hc *httpCodec) Encode(c gnet.Conn, buf []byte) (out []byte, err error) {
return buf, nil
}
func (hc *httpCodec) Decode(c gnet.Conn) (out []byte, err error) {
buf := c.Read()
if buf == nil {
return
}
c.ResetBuffer()
// process the pipeline
var i int
pipeline:
if i = bytes.Index(buf, hc.delimiter); i != -1 {
out = append(out, "HTTP/1.1 200 OK\r\nServer: gnet\r\nContent-Type: text/plain\r\nDate: "...)
out = time.Now().AppendFormat(out, "Mon, 02 Jan 2006 15:04:05 GMT")
out = append(out, "\r\nContent-Length: 13\r\n\r\nHello, World!"...)
buf = buf[i+4:]
goto pipeline
}
// request not ready, yet
return
}
func (hs *httpServer) OnInitComplete(srv gnet.Server) (action gnet.Action) {
log.Printf("HTTP server is listening on %s (multi-cores: %t, loops: %d)\n",
srv.Addr.String(), srv.Multicore, srv.NumEventLoop)
return
}
func (hs *httpServer) React(frame []byte, c gnet.Conn) (out []byte, action gnet.Action) {
// handle the request
out = frame
return
}
func init() {
runtime.GOMAXPROCS(runtime.NumCPU() * 2)
}
func main() {
var port int
var multicore bool
// Example command: go run main.go --port 8080 --multicore=true
flag.IntVar(&port, "port", 8080, "server port")
flag.BoolVar(&multicore, "multicore", true, "multicore")
flag.Parse()
http := new(httpServer)
hc := &httpCodec{delimiter: []byte("\r\n\r\n")}
// Start serving!
log.Fatal(gnet.Serve(http, fmt.Sprintf("tcp://:%d", port), gnet.WithMulticore(multicore), gnet.WithCodec(hc)))
}
```


构建这份代码：

```
$go mod init gnet-demo
$go get github.com/panjf2000/gnet
go: downloading github.com/panjf2000/gnet v1.4.5
go get: added github.com/panjf2000/gnet v1.4.5
//修改go.mod，使用replace让gnet-demo使用本地的gnet代码
$cat go.mod
module gnet-demo
go 1.16
replace github.com/panjf2000/gnet => /root/go/src/github.com/panjf2000/gnet
require (
github.com/panjf2000/gnet v1.4.5
)
$go get github.com/bigwhite/functrace
go get: added github.com/bigwhite/functrace v0.0.0-20210603024853-ccab68a2604c
$go build -tags trace //-tags trace务必不能省略，这个是开启functrace的关键
```


构建后，我们来执行构建出的可执行程序：gnet-demo：

```
$ go build -tags trace
root@VM-0-12-ubuntu:~/test/go/gnet-demo# ./gnet-demo
g[01]: ->github.com/panjf2000/gnet/internal/socket.maxListenerBacklog
g[01]: <-github.com/panjf2000/gnet/internal/socket.maxListenerBacklog
g[01]: ->github.com/panjf2000/gnet/ringbuffer.New
g[01]: <-github.com/panjf2000/gnet/ringbuffer.New
g[01]: ->github.com/panjf2000/gnet/internal/logging.init.0
g[01]: <-github.com/panjf2000/gnet/internal/logging.init.0
g[01]: ->github.com/panjf2000/gnet.WithMulticore
g[01]: <-github.com/panjf2000/gnet.WithMulticore
g[01]: ->github.com/panjf2000/gnet.WithCodec
g[01]: <-github.com/panjf2000/gnet.WithCodec
g[01]: ->github.com/panjf2000/gnet.Serve
g[01]: ->github.com/panjf2000/gnet.loadOptions
g[01]: <-github.com/panjf2000/gnet.loadOptions
g[01]: ->github.com/panjf2000/gnet.parseProtoAddr
g[01]: <-github.com/panjf2000/gnet.parseProtoAddr
g[01]: ->github.com/panjf2000/gnet.initListener
g[01]: ->github.com/panjf2000/gnet.(*listener).normalize
g[01]: ->github.com/panjf2000/gnet/internal/socket.TCPSocket
g[01]: ->github.com/panjf2000/gnet/internal/socket.tcpSocket
g[01]: ->github.com/panjf2000/gnet/internal/socket.getTCPSockaddr
g[01]: ->github.com/panjf2000/gnet/internal/socket.determineTCPProto
g[01]: <-github.com/panjf2000/gnet/internal/socket.determineTCPProto
g[01]: <-github.com/panjf2000/gnet/internal/socket.getTCPSockaddr
g[01]: ->github.com/panjf2000/gnet/internal/socket.sysSocket
g[01]: <-github.com/panjf2000/gnet/internal/socket.sysSocket
g[01]: ->github.com/panjf2000/gnet/internal/socket.SetNoDelay
g[01]: <-github.com/panjf2000/gnet/internal/socket.SetNoDelay
g[01]: <-github.com/panjf2000/gnet/internal/socket.tcpSocket
g[01]: <-github.com/panjf2000/gnet/internal/socket.TCPSocket
g[01]: <-github.com/panjf2000/gnet.(*listener).normalize
g[01]: <-github.com/panjf2000/gnet.initListener
g[01]: ->github.com/panjf2000/gnet.serve
2021/06/03 14:53:30 HTTP server is listening on :8080 (multi-cores: true, loops: 1)
g[01]: ->github.com/panjf2000/gnet.(*server).start
g[01]: ->github.com/panjf2000/gnet.(*server).activateReactors
g[01]: ->github.com/panjf2000/gnet/internal/netpoll.OpenPoller
g[01]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: ->github.com/panjf2000/gnet/internal/netpoll/queue.NewLockFreeQueue
g[01]: <-github.com/panjf2000/gnet/internal/netpoll/queue.NewLockFreeQueue
g[01]: <-github.com/panjf2000/gnet/internal/netpoll.OpenPoller
g[01]: ->github.com/panjf2000/gnet.(*roundRobinLoadBalancer).register
g[01]: <-github.com/panjf2000/gnet.(*roundRobinLoadBalancer).register
g[01]: ->github.com/panjf2000/gnet.(*server).startSubReactors
g[01]: ->github.com/panjf2000/gnet.(*roundRobinLoadBalancer).iterate
g[01]: <-github.com/panjf2000/gnet.(*roundRobinLoadBalancer).iterate
g[01]: <-github.com/panjf2000/gnet.(*server).startSubReactors
g[01]: ->github.com/panjf2000/gnet/internal/netpoll.OpenPoller
g[01]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: ->github.com/panjf2000/gnet/internal/netpoll/queue.NewLockFreeQueue
g[01]: <-github.com/panjf2000/gnet/internal/netpoll/queue.NewLockFreeQueue
g[01]: <-github.com/panjf2000/gnet/internal/netpoll.OpenPoller
g[01]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[01]: <-github.com/panjf2000/gnet.(*server).activateReactors
g[01]: <-github.com/panjf2000/gnet.(*server).start
g[01]: ->github.com/panjf2000/gnet.(*server).stop
g[01]: ->github.com/panjf2000/gnet.(*server).waitForShutdown
g[07]: ->github.com/panjf2000/gnet.(*server).activateMainReactor
g[07]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).Polling
g[07]: ->github.com/panjf2000/gnet/internal/netpoll.newEventList
g[07]: <-github.com/panjf2000/gnet/internal/netpoll.newEventList
g[06]: ->github.com/panjf2000/gnet.(*server).activateSubReactor
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).Polling
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.newEventList
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.newEventList
```


我们看到gnet的执行主线被清晰的打印出来，通过输出的函数所在包我们可以轻松找到对应的源文件。g[01]这goroutine显然是main goroutine，整个程序的初始化线索通过跟踪g[01]的函数链便一目了然。

如果我们要看gnet是如何处理一个外部链接的，我们可以向gnet-demo建立一个连接，看看gnet-demo的输出。

我们通过curl命令向gnet-demo发起一个http请求：

```
$curl localhost:8080
Hello, World!
```


gnet-demo输出：

```
g[07]: ->github.com/panjf2000/gnet.(*server).acceptNewConnection
g[07]: ->github.com/panjf2000/gnet/internal/socket.SockaddrToTCPOrUnixAddr
g[07]: ->github.com/panjf2000/gnet/internal/socket.sockaddrInet6ToIPAndZone
g[07]: ->github.com/panjf2000/gnet/internal/socket.ip6ZoneToString
g[07]: <-github.com/panjf2000/gnet/internal/socket.ip6ZoneToString
g[07]: <-github.com/panjf2000/gnet/internal/socket.sockaddrInet6ToIPAndZone
g[07]: <-github.com/panjf2000/gnet/internal/socket.SockaddrToTCPOrUnixAddr
g[07]: ->github.com/panjf2000/gnet.(*roundRobinLoadBalancer).next
g[07]: <-github.com/panjf2000/gnet.(*roundRobinLoadBalancer).next
g[07]: ->github.com/panjf2000/gnet.newTCPConn
g[07]: ->github.com/panjf2000/gnet/pool/ringbuffer.Get
g[07]: ->github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Get
g[07]: ->github.com/panjf2000/gnet/ringbuffer.New
g[07]: <-github.com/panjf2000/gnet/ringbuffer.New
g[07]: <-github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Get
g[07]: <-github.com/panjf2000/gnet/pool/ringbuffer.Get
g[07]: ->github.com/panjf2000/gnet/pool/ringbuffer.Get
g[07]: ->github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Get
g[07]: ->github.com/panjf2000/gnet/ringbuffer.New
g[07]: <-github.com/panjf2000/gnet/ringbuffer.New
g[07]: <-github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Get
g[07]: <-github.com/panjf2000/gnet/pool/ringbuffer.Get
g[07]: <-github.com/panjf2000/gnet.newTCPConn
g[07]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).Trigger
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Enqueue
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[07]: ->github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[07]: <-github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Enqueue
g[07]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).Trigger
g[07]: <-github.com/panjf2000/gnet.(*server).acceptNewConnection
g[07]: ->github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[07]: <-github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Dequeue
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.cas
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Dequeue
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).AddRead
g[06]: ->github.com/panjf2000/gnet.(*eventloop).loopOpen
g[06]: ->github.com/panjf2000/gnet.(*eventloop).addConn
g[06]: <-github.com/panjf2000/gnet.(*eventloop).addConn
g[06]: ->github.com/panjf2000/gnet.(*EventServer).OnOpened
g[06]: <-github.com/panjf2000/gnet.(*EventServer).OnOpened
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: ->github.com/panjf2000/gnet.(*eventloop).handleAction
g[06]: <-github.com/panjf2000/gnet.(*eventloop).handleAction
g[06]: <-github.com/panjf2000/gnet.(*eventloop).loopOpen
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Dequeue
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.load
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Dequeue
g[06]: ->github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Empty
g[06]: <-github.com/panjf2000/gnet/internal/netpoll/queue.(*lockFreeQueue).Empty
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: ->github.com/panjf2000/gnet.(*eventloop).loopRead
g[06]: ->github.com/panjf2000/gnet.(*conn).read
g[06]: ->github.com/panjf2000/gnet.(*conn).Read
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet.(*conn).Read
g[06]: ->github.com/panjf2000/gnet.(*conn).ResetBuffer
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet.(*conn).ResetBuffer
g[06]: <-github.com/panjf2000/gnet.(*conn).read
g[06]: ->github.com/panjf2000/gnet.(*EventServer).PreWrite
g[06]: <-github.com/panjf2000/gnet.(*EventServer).PreWrite
g[06]: ->github.com/panjf2000/gnet.(*conn).write
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet.(*conn).write
g[06]: ->github.com/panjf2000/gnet.(*conn).read
g[06]: ->github.com/panjf2000/gnet.(*conn).Read
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet.(*conn).Read
g[06]: ->github.com/panjf2000/gnet.(*conn).ResetBuffer
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet.(*conn).ResetBuffer
g[06]: <-github.com/panjf2000/gnet.(*conn).read
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Write
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Write
g[06]: <-github.com/panjf2000/gnet.(*eventloop).loopRead
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: ->github.com/panjf2000/gnet.(*eventloop).loopRead
g[06]: ->github.com/panjf2000/gnet.(*eventloop).loopCloseConn
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).IsEmpty
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*Poller).Delete
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.(*Poller).Delete
g[06]: ->github.com/panjf2000/gnet.(*eventloop).addConn
g[06]: <-github.com/panjf2000/gnet.(*eventloop).addConn
g[06]: ->github.com/panjf2000/gnet.(*EventServer).OnClosed
g[06]: <-github.com/panjf2000/gnet.(*EventServer).OnClosed
g[06]: ->github.com/panjf2000/gnet.(*conn).releaseTCP
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.Put
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Put
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Len
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Len
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.index
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.index
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Put
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.Put
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.Put
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Put
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Len
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Len
g[06]: ->github.com/panjf2000/gnet/pool/ringbuffer.index
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.index
g[06]: ->github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/ringbuffer.(*RingBuffer).Reset
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.(*Pool).Put
g[06]: <-github.com/panjf2000/gnet/pool/ringbuffer.Put
g[06]: <-github.com/panjf2000/gnet.(*conn).releaseTCP
g[06]: <-github.com/panjf2000/gnet.(*eventloop).loopCloseConn
g[06]: <-github.com/panjf2000/gnet.(*eventloop).loopRead
g[06]: ->github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
g[06]: <-github.com/panjf2000/gnet/internal/netpoll.(*eventList).shrink
```


通过gnet-demo输出，我们可以清晰看到gnet接收一个连接，在这个连接上读写以及关闭这个连接的函数调用链，有了这个链条，我们再来阅读gnet源码就轻松许多了，即便有回调函数也没有问题。

上面输出的函数调用链的内容已经很多了。但如果你还不满足于这些，比如我还要跟踪到gnet依赖的golang.org/x/sys中，那可以利用相同思路，将golang.org/x/sys下载到本地，并通过functrace添加跟踪设施，并在gnet-demo中用replace换掉golang.org/x/sys，让其指向本地的sys包代码。如果觉得信息太多，可以通过gen命令做单个必要go源文件的跟踪信息添加，而不必要用批量方式。进一步的跟踪sys包的函数调用链的作业就留给大家了，这里就不深入了。

代码阅读完成后，我们只需在gnet目录下执行如下命令便可以恢复gnet原来的面貌：

```
$git checkout .
```


[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

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

感觉这样更方便

“`bash

go install github.com/bigwhite/functrace/cmd/gen@latest

find ./ -name “*.go” | xargs -n1 gnet -w

go get github.com/bigwhite/functrace

go mod vendor

“`

这个感觉如果能静态检测就好了。。。