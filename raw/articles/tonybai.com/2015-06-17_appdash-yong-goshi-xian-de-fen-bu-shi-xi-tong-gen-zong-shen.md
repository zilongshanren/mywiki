---
title: Appdash，用Go实现的分布式系统跟踪神器
url: https://tonybai.com/2015/06/17/appdash-distributed-systems-tracing-in-go/
published: '2015-06-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Appdash，用Go实现的分布式系统跟踪神器

在“云”盛行的今天，[分布式系统](https://en.wikipedia.org/wiki/Distributed_computing)已不是什么新鲜的玩意儿。用脚也能想得出来：Google、baidu、淘宝、亚马逊、twitter等IT巨头 背后的巨型计算平台都是分布式系统了，甚至就连一个简单的微信公众号应用的后端也都分布式了，即便仅有几台机器而已。分布式让系统富有弹性，面 对纷繁变化的需求，可以伸缩自如。但分布式系统也给开发以及运维人员带来了难题：如何监控和优化分布式系统的行为。

以google为例，想象一下，用户通过浏览器发起一个搜索请求，Google后端可能会有成百上千台机器、多种编程语言实现的几十个、上百个应 用服务开始忙碌起来，一起计算请求的返回结果。一旦这个过程中某一个环节出现问题/bug，那么查找和定位起来是相当困难的，于是乎分布式系统跟 踪系统出炉了。Google在2010年发表了著名论文《[Dapper, a Large-Scale Distributed Systems Tracing Infrastructure](http://research.google.com /pubs/pub36356.html)》(中文版在[这里](http://bigbully.github.io/Dapper-translation/))。Dapper是google内部使用的一个分布式系统跟踪基础设施，与之前的一些跟踪系统相比，Dapper以低消耗、对应用透明以及良好的扩展性著称。并且 Google Dapper更倾向于性能数据方面的收集和调查，可以辅助开发人员和运维人员发现分布式系统的性能瓶颈并着手优化。Dapper出现后，各大巨头开始跟 风，比如twitter的[Zipkin](https://github.com/twitter/zipkin)（开源）、淘宝的“鹰眼”、eBay的Centralized Activity Logging (CAL)等，它们基本上都是参考google的dapper论文设计和实现的。

而本文将要介绍的[Appdash](https://sourcegraph.com/sourcegraph/appdash)则是[sourcegraph](https://sourcegraph.com/)开源的一款用[Go](http://golang.org)实现的分布式系统跟踪工具套件，它同样是以google的 dapper为原型设计和实现的，目前用于sourcegraph平台的性能跟踪和监控。

**一、原理**

![](../../assets/7e738d77e2c1a098.png)


Appdash实现了Google dapper中的四个主要概念：

【Span】

Span指的是一个服务调用的跨度，在实现中用SpanId标识。根服务调用者的Span为根span（root span)，在根级别进行的下一级服务调用Span的Parent Span为root span。以此类推，服务调用链构成了一棵tree，整个tree构成了一个Trace。

Appdash中SpanId由三部分组成：TraceID/SpanID/parentSpanID，例如： 34c31a18026f61df/aab2a63e86ac0166/592043d0a5871aaf。TraceID用于唯一标识一次Trace。traceid在申请RootSpanID时自动分配。

在上面原理图中，我们也可以看到一次Trace过程中SpanID的情况。图中调用链大致是：

frontservice:

call serviceA

call serviceB

call serviceB1

… …

call serviceN

对应服务调用的Span的树形结构如下：

frontservice: SpanId = xxxxx/nnnn1，该span为root span：traceid=xxxxx, spanid=nnnn1，parent span id为空。

serviceA: SpanId = xxxxx/nnnn2/nnnn1，该span为child span：traceid=xxxxx, spanid=nnnn2，parent span id为root span id:nnnn1。

serviceB: SpanId = xxxxx/nnnn3/nnnn1，该span为child span：traceid=xxxxx, spanid=nnnn3，parent span id为root span id:nnnn1。

… …

serviceN: SpanId = xxxxx/nnnnm/nnnn1，该span为child span：traceid=xxxxx, spanid=nnnnm，parent span id为root span id:nnnn1。

serviceB1: SpanId = xxxxx/nnnn3-1/nnnn3，该span为serviceB的child span，traceid=xxxxx, spanid=nnnn3-1，parent span id为serviceB的spanid：nnnn3

【Event】

个人理解在Appdash中Event是服务调用跟踪信息的wrapper。最终我们在Appdash UI上看到的信息，都是由event承载的并且发给Appdash Server的信息。在Appdash中，你可以显式使用event埋点，吐出跟踪信息，也可以使用Appdash封装好的包接口，比如 httptrace.Transport等发送调用跟踪信息，这些包的底层实现也是基于event的。event在传输前会被encoding为 Annotation的形式。

【Recorder】

在Appdash中，Recorder是用来发送event给Appdash的Collector的，每个Recorder会与一个特定的span相关联。

【Collector】

从Recorder那接收Annotation（即encoded event）。通常一个appdash server会运行一个Collector，监听某个跟踪信息收集端口，将收到的信息存储在Store中。

**二、安装**

appdash是开源的，通过go get即可得到源码并安装example：


appdash自带一个example，在examples/cmd/webapp下面。执行webapp，你会看到如下结果：

$webapp

2015/06/17 13:14:55 Appdash web UI running on HTTP :8700

[negroni] listening on :8699

这是一个集appdash server, frontservice, fakebackendservice于一身的example，其大致结构如下图：

![](../../assets/1eb64014ca8bb42e.png)


通过浏览器打开:localhost:8700页面，你会看到appdash server的UI，通过该UI你可以看到所有Trace的全貌。

访问http://localhost:8699/，你就触发了一次Trace。在appdash server ui下可以看到如下画面：

![](../../assets/4e4f6011e0b33ac5.png)


从页面上展示的信息可以看出，该webapp在处理用户request时共进行了三次服务调用，三次调用的耗时分别为：201ms，202ms， 218ms，共耗时632ms。

一个更复杂的例子在cmd/appdash下面，后面的应用实例也是根据这个改造出来的，这里就不细说了。

**三、应用实例**

这里根据cmd/appdash改造出一个应用appdash的例子，例子的结构如下图：

![](../../assets/cb13178f262e9152.png)


例子大致分为三部分：

appdash — 实现了一个appdash server， 该server带有一个collector，用于收集跟踪信息，收集后的信息存储在一个memstore中；appdash server提供ui，ui从memstore提取信息并展示在ui上供operator查看。

backendservices — 实现两个模拟的后端服务，供frontservice调用。

frontservice — 服务调用的起始端，当用户访问系统时触发一次跟踪。

先从backendservice这个简单的demo service说起，backendservice下有两个service: ServiceA和ServiceB，两个service几乎一模一样，我们看一个就ok了：

//appdash_examples/backendservices/serviceA.go

package main

import (

"fmt"

"net/http"

"time"

)

func handleRequest(w http.ResponseWriter, r *http.Request) {

var err error

if err = r.ParseForm(); err != nil {

fmt.Println("Http parse form err:", err)

return

}

fmt.Println("SpanId =", r.Header.Get("Span-Id"))

time.Sleep(time.Millisecond * 101)

w.Write([]byte("service1 ok"))

}

func main() {

http.HandleFunc("/", handleRequest)

http.ListenAndServe(":6601", nil)

}

这是一个"hello world"级别的web server。值得注意的只有两点：

1、在handleRequest中我们故意Sleep 101ms，用来模拟服务的耗时。

2、打印出request头中的"Span-Id"选项值，用于跟踪Span-Id的分配情况。

接下来我们来看appdash server。appdash server = collector +store +ui。

//appdash.go

var c Server

func init() {

c = Server{

CollectorAddr: ":3001",

HTTPAddr: ":3000",

}

}

type Server struct {

CollectorAddr string

HTTPAddr string

}

func main() {

var (

memStore = appdash.NewMemoryStore()

Store = appdash.Store(memStore)

Queryer = memStore

)

app := traceapp.New(nil)

app.Store = Store

app.Queryer = Queryer

var h http.Handler = app

var l net.Listener

var proto string

var err error

l, err = net.Listen("tcp", c.CollectorAddr)

if err != nil {

log.Fatal(err)

}

proto = "plaintext TCP (no security)"

log.Printf("appdash collector listening on %s (%s)",

c.CollectorAddr, proto)

cs := appdash.NewServer(l, appdash.NewLocalCollector(Store))

go cs.Start()

log.Printf("appdash HTTP server listening on %s", c.HTTPAddr)

err = http.ListenAndServe(c.HTTPAddr, h)

if err != nil {

fmt.Println("listenandserver listen err:", err)

}

}

appdash中的Store是用来存储收集到的跟踪结果的，Store是Collector接口的超集，这个例子中，直接利用memstore(实现了 Collector接口)作为local collector，利用store的Collect方法收集trace数据。UI侧则从store中读取结果展示给用户。

最后我们说说：frontservice。frontservice是Trace的触发起点。当用户访问8080端口时，frontservice调用两个backend service：

//frontservice.go

func handleRequest(w http.ResponseWriter, r *http.Request) {

var result string

span := appdash.**NewRootSpanID**()

fmt.Println("span is ", span)

collector := appdash.NewRemoteCollector(":3001")

httpClient := &http.Client{

Transport: &httptrace.Transport{

Recorder: appdash.NewRecorder(span, collector),

SetName: true,

},

}

//Service A

resp, err := httpClient.Get("http://localhost:6601")

if err != nil {

log.Println("access serviceA err:", err)

} else {

log.Println("access serviceA ok")

resp.Body.Close()

result += "access serviceA ok\n"

}

//Service B

resp, err = httpClient.Get("http://localhost:6602")

if err != nil {

log.Println("access serviceB err:", err)

return

} else {

log.Println("access serviceB ok")

resp.Body.Close()

result += "access serviceB ok\n"

}

w.Write([]byte(result))

}

func main() {

http.HandleFunc("/", handleRequest)

http.ListenAndServe(":8080", nil)

}

从代码看，处理每个请求时都会分配一个root span，同时traceid也随之分配出来。例子中没有直接使用Recorder埋点发送event，而是利用了appdash封装好的 httptrace.Transport，在初始化httpClient时，将transport实例与span和一个remoteCollector想 关联。后续每次调用httpClient进行Get/Post操作时，底层代码会自动调用httptrace.Transport的RoundTrip方 法，后者在Request header上添加"Span-Id"参数，并调用Recorder的Event方法将跟踪信息发给RemoteCollector：

//appdash/httptrace/client.go

func (t *Transport) RoundTrip(req *http.Request) (*http.Response, error) {

var transport http.RoundTripper

if t.Transport != nil {

transport = t.Transport

} else {

transport = http.DefaultTransport

}

… …

req = cloneRequest(req)

child := t.Recorder.Child()

if t.SetName {

child.Name(req.URL.Host)

}

** SetSpanIDHeader(req.Header, child.SpanID)**

e := NewClientEvent(req)

e.ClientSend = time.Now()

// Make the HTTP request.

resp, err := transport.RoundTrip(req)

e.ClientRecv = time.Now()

if err == nil {

e.Response = responseInfo(resp)

} else {

e.Response.StatusCode = -1

}

** child.Event(e)**

return resp, err

}

这种方法在一定程度上实现了trace对应用的透明性。

你也可以显式的在代码中调用Recorder的Event的方法将trace信息发送给Collector，下面是一个fake SQLEvent的跟踪发送：

// SQL event

traceRec := appdash.NewRecorder(span, collector)

traceRec.Name("sqlevent example")

// A random length for the trace.

length := time.Duration(rand.Intn(1000)) * time.Millisecond

startTime := time.Now().Add(-time.Duration(rand.Intn(100)) * time.Minute)

traceRec.Event(&sqltrace.SQLEvent{

ClientSend: startTime,

ClientRecv: startTime.Add(length),

SQL: "SELECT * FROM table_name;",

Tag: fmt.Sprintf("fakeTag%d", rand.Intn(10)),

})

不过这种显式埋点需要程序配合做一些改造。

**四、小结**

目前Appdash的资料甚少，似乎只是其东家sourcegraph在production环境有应用。在github.com上受到的关注度也不算高。

appdash是参考google dapper实现的，但目前来看appdash只是实现了“形”，也许称为神器有些言过其实^_^。

首先，dapper强调对应用透明，并使用了Thread LocalStorage。appdash实现了底层的recorder+event机制，上层通过httptrace、sqltrace做了封装，以降 低对应用代码的侵入性。但从上面的应用来看，透明性还有很大提高空间。

其次，appdash的性能数据、扩展方案sourcegraph并没有给出明确说明。

不过作为用go实现的第一个分布式系统跟踪工具，appdash还是值得肯定的。在小规模分布式系统中应用对于系统行为的优化还是会有很大帮助的。

BTW，上述例子的完整源码在[这里](https://github.com/bigwhite/experiments/tree/master/appdash_examples)可以下载到。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

来学习一下 哈哈