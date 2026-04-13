---
title: 使用go-metrics在Go应用中增加度量
url: https://tonybai.com/2021/07/06/add-metrics-for-go-application-using-go-metrics/
published: '2021-07-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用go-metrics在Go应用中增加度量

![](../../assets/a0a7aeb63dbea662.png)


[本文永久链接](https://tonybai.com/2021/07/06/add-metrics-for-go-application-using-go-metrics) – https://tonybai.com/2021/07/06/add-metrics-for-go-application-using-go-metrics

Go语言内置[expvar](https://mp.weixin.qq.com/s/cr2JeUq5HOYQC0qji_Ip5g)，基于expvar提供的对基础度量的支持能力，我们可以自定义各种度量（metrics）。但是expvar仅仅是提供了最底层的度量定义支持，对于一些复杂的度量场景，第三方或自实现的metrics包必不可少。

go-metrics包是Go领域使用较多的是metrics包，该包是对Java社区依旧十分活跃的[Coda Hale’s Metrics library](https://github.com/dropwizard/metrics)的不完全Go移植（不得不感慨一下：Java的生态还真是强大）。因此该包在概念上与Coda Hale’s Metrics library是基本保持一致的。go-metrics包在文档方面做的还不够，要理解很多概念性的东西，我们还得回到[Coda Hale’s Metrics library的项目文档](https://metrics.dropwizard.io/4.2.0/manual/core.html)去挖掘。

go-metrics这样的包是纯工具类的包，没有太多“烧脑”的地方，只需要会用即可，这篇文章我们就来简单地看看如何使用go-metrics在Go应用中增加度量。

### 1. go-metrics的结构

go-metrics在度量指标组织上采用了与Coda Hale’s Metrics library相同的结构，即使用Metrics Registry（Metrics注册表）。Metrics注册表是一个度量指标的集合：

```
┌─────────────┐
│ │
┌──────┤ metric1 │
│ │ │
│ └─────────────┘
│
│
┌─────────────────┐ │ ┌─────────────┐
│ ├───┘ │ │
│ │ │ metric2 │
│ Registry ├──────────┤ │
│ │ └─────────────┘
│ ├───────┐
│ │ │
└──────────────┬──┘ │ ┌─────────────┐
│ │ │ │
│ └──┤ metric3 │
│ │ │
│ └─────────────┘
│ ... ...
│ ┌─────────────┐
│ │ │
└─────────────┤ metricN │
│ │
└─────────────┘
```


go-metrics包将Metrics注册表的行为定义为了一个接口类型：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
type Registry interface {
// Call the given function for each registered metric.
Each(func(string, interface{}))
// Get the metric by the given name or nil if none is registered.
Get(string) interface{}
// GetAll metrics in the Registry.
GetAll() map[string]map[string]interface{}
// Gets an existing metric or registers the given one.
// The interface can be the metric to register if not found in registry,
// or a function returning the metric for lazy instantiation.
GetOrRegister(string, interface{}) interface{}
// Register the given metric under the given name.
Register(string, interface{}) error
// Run all registered healthchecks.
RunHealthchecks()
// Unregister the metric with the given name.
Unregister(string)
// Unregister all metrics. (Mostly for testing.)
UnregisterAll()
}
```


并提供了一个Registry的标准实现类型StandardRegistry：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
type StandardRegistry struct {
metrics map[string]interface{}
mutex sync.RWMutex
}
```


我们看到StandardRegistry使用map结构来组织metrics。我们可以通过NewRegistry函数创建了一个基于StandardRegistry的Registry实例：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
func NewRegistry() Registry {
return &StandardRegistry{metrics: make(map[string]interface{})}
}
```


和标准库的flag或log包的设计方式类似，go-metrics包也在包层面上提供了默认的StandardRegistry实例：**DefaultRegistry**，这样大多数情况直接使用DefaultRegistry实例即可满足你的需求：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
var DefaultRegistry Registry = NewRegistry()
```


一旦有了默认Registry实例，我们通常使用下面goroutine并发安全的包级函数GetOrRegister来注册或获取某个度量指标：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
func GetOrRegister(name string, i interface{}) interface{} {
return DefaultRegistry.GetOrRegister(name, i)
}
```


### 2. go-metrics的度量类型

go-metrics继承了其前身Coda Hale’s Metrics library所支持的几种基本的度量类型，它们是Gauges、Counters、Histograms、Meters和Timers。下面我们就针对这几种基本度量类型逐一说明一下其含义和使用方法。

#### 1) Gauge

Gauge是对一个数值的即时测量值，其反映一个值的瞬时快照，比如我们要度量当前队列中待发送消息数量、当前应用程序启动的goroutine数量，都可以用Gauge这种度量类型实现。

下面的例子使用一个Gauge度量类型度量程序当前启动的goroutine数量：

```
// gauge.go
package main
import (
"fmt"
"net/http"
"runtime"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
g := metrics.NewGauge()
metrics.GetOrRegister("goroutines.now", g)
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
})
go func() {
t := time.NewTicker(time.Second)
for {
select {
case <-t.C:
c := runtime.NumGoroutine()
g.Update(int64(c))
fmt.Println("goroutines now =", g.Value())
}
}
}()
http.ListenAndServe(":8080", nil)
}
```


启动该程序，并用[hey工具](https://github.com/rakyll/hey/)发起http请求，我们看到如下输出：

```
$hey -c 5 -n 1000000 -m GET http://127.0.0.1:8080
$go run gauge.go
goroutines now = 9
goroutines now = 10
goroutines now = 7
goroutines now = 8
goroutines now = 7
goroutines now = 7
... ...
```


go-metrics包提供了将Registry中的度量指标格式化输出的接口，我们可以使用该接口将指标情况输出出来，而无需自行输出log，比如上面例子可以改造为下面这样：

```
// gauge1.go
package main
import (
"log"
"net/http"
"runtime"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
g := metrics.NewGauge()
metrics.GetOrRegister("goroutines.now", g)
go metrics.Log(metrics.DefaultRegistry, time.Second, log.Default())
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
})
go func() {
t := time.NewTicker(time.Second)
for {
select {
case <-t.C:
c := runtime.NumGoroutine()
g.Update(int64(c))
}
}
}()
http.ListenAndServe(":8080", nil)
}
```


同样方式运行上面gauge1.log：

```
$go run gauge1.go
2021/07/04 09:42:58 gauge goroutines.now
2021/07/04 09:42:58 value: 10
2021/07/04 09:42:59 gauge goroutines.now
2021/07/04 09:42:59 value: 9
2021/07/04 09:43:00 gauge goroutines.now
2021/07/04 09:43:00 value: 9
2021/07/04 09:43:01 gauge goroutines.now
2021/07/04 09:43:01 value: 10
... ...
```


go-metrics包的Log函数必须放在一个单独的goroutine中执行，否则它将阻塞调用它的goroutine的继续执行。但Log函数也是goroutine安全的，其每次输出度量值时其实输出的都是Registry中各个度量值的“快照副本”：

```
// https://github.com/rcrowley/go-metrics/blob/master/registry.go
func (r *StandardRegistry) Each(f func(string, interface{})) {
metrics := r.registered()
for i := range metrics {
kv := &metrics[i]
f(kv.name, kv.value)
}
}
func (r *StandardRegistry) registered() []metricKV {
r.mutex.RLock()
defer r.mutex.RUnlock()
metrics := make([]metricKV, 0, len(r.metrics))
for name, i := range r.metrics {
metrics = append(metrics, metricKV{
name: name,
value: i,
})
}
return metrics
}
```


对于Gauge这类的季世志度量，就像上面代码那样，我们都是通过Update直接设置其值的。

#### 2) Counter

Counter顾名思义**计数器**！和Gauge相比，其提供了指标增减方法Inc和Dec，如下面代码：

```
// https://github.com/rcrowley/go-metrics/blob/master/counter.go
type Counter interface {
Clear()
Count() int64
Dec(int64)
Inc(int64)
Snapshot() Counter
}
```


计数是日常使用较多的度量场景，比如一个服务处理的请求次数就十分适合用计数这个度量指标，下面这段代码演示的就是这一场景：

```
// counter.go
package main
import (
"log"
"net/http"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
c := metrics.NewCounter()
metrics.GetOrRegister("total.requests", c)
go metrics.Log(metrics.DefaultRegistry, time.Second, log.Default())
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
c.Inc(1)
})
http.ListenAndServe(":8080", nil)
}
```


在这段代码中，我们每收到一个http request就在其对应的处理函数中利用Counter的Inc方法增加计数，运行上述代码：

```
$go run counter.go
2021/07/04 10:29:03 counter total.requests
... ...
2021/07/04 10:29:06 counter total.requests
2021/07/04 10:29:06 count: 0
2021/07/04 10:29:07 counter total.requests
2021/07/04 10:29:07 count: 33890
2021/07/04 10:29:08 counter total.requests
2021/07/04 10:29:08 count: 80160
2021/07/04 10:29:09 counter total.requests
2021/07/04 10:29:09 count: 124855
2021/07/04 10:29:10 counter total.requests
2021/07/04 10:29:10 count: 172077
2021/07/04 10:29:11 counter total.requests
2021/07/04 10:29:11 count: 218466
2021/07/04 10:29:12 counter total.requests
2021/07/04 10:29:12 count: 265476
2021/07/04 10:29:13 counter total.requests
2021/07/04 10:29:13 count: 309153
... ...
```


#### 3) Meter

Meter这个类型用于测量一组事件发生的速度，比如：web服务的平均处理性能(条/秒)，除了平均值，go-metrics的Meter默认还提供1分钟、5分钟和15分钟时间段的平均速度，和top命令中的load average输出的一分钟、五分钟、以及十五分钟的系统平均负载类似。

下面就是一个用Meter来测量web服务处理性能的例子：

```
// meter.go
package main
import (
"log"
"net/http"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
m := metrics.NewMeter()
metrics.GetOrRegister("rate.requests", m)
go metrics.Log(metrics.DefaultRegistry, time.Second, log.Default())
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
m.Mark(1)
})
http.ListenAndServe(":8080", nil)
}
```


我们用hey给该web server“施压”并查看Meter度量指标的输出结果：

```
$hey -c 5 -n 1000000 -m GET http://127.0.0.1:8080
$go run meter.go
2021/07/04 10:55:59 meter rate.requests
2021/07/04 10:55:59 count: 0
2021/07/04 10:55:59 1-min rate: 0.00
2021/07/04 10:55:59 5-min rate: 0.00
2021/07/04 10:55:59 15-min rate: 0.00
2021/07/04 10:55:59 mean rate: 0.00
2021/07/04 10:56:00 meter rate.requests
2021/07/04 10:56:00 count: 0
2021/07/04 10:56:00 1-min rate: 0.00
2021/07/04 10:56:00 5-min rate: 0.00
2021/07/04 10:56:00 15-min rate: 0.00
2021/07/04 10:56:00 mean rate: 0.00
2021/07/04 10:56:01 meter rate.requests
2021/07/04 10:56:01 count: 8155
2021/07/04 10:56:01 1-min rate: 0.00
2021/07/04 10:56:01 5-min rate: 0.00
2021/07/04 10:56:01 15-min rate: 0.00
2021/07/04 10:56:01 mean rate: 2718.27
2021/07/04 10:56:02 meter rate.requests
2021/07/04 10:56:02 count: 50937
2021/07/04 10:56:02 1-min rate: 0.00
2021/07/04 10:56:02 5-min rate: 0.00
2021/07/04 10:56:02 15-min rate: 0.00
2021/07/04 10:56:02 mean rate: 12734.04
2021/07/04 10:56:03 meter rate.requests
2021/07/04 10:56:03 count: 96129
2021/07/04 10:56:03 1-min rate: 19225.00
2021/07/04 10:56:03 5-min rate: 19225.00
2021/07/04 10:56:03 15-min rate: 19225.00
2021/07/04 10:56:03 mean rate: 19225.54
2021/07/04 10:56:04 meter rate.requests
2021/07/04 10:56:04 count: 141076
2021/07/04 10:56:04 1-min rate: 19225.00
2021/07/04 10:56:04 5-min rate: 19225.00
2021/07/04 10:56:04 15-min rate: 19225.00
2021/07/04 10:56:04 mean rate: 23512.40
2021/07/04 10:56:05 meter rate.requests
2021/07/04 10:56:05 count: 187733
2021/07/04 10:56:05 1-min rate: 19225.00
2021/07/04 10:56:05 5-min rate: 19225.00
2021/07/04 10:56:05 15-min rate: 19225.00
2021/07/04 10:56:05 mean rate: 26818.71
2021/07/04 10:56:06 meter rate.requests
2021/07/04 10:56:06 count: 234874
2021/07/04 10:56:06 1-min rate: 19225.00
2021/07/04 10:56:06 5-min rate: 19225.00
2021/07/04 10:56:06 15-min rate: 19225.00
2021/07/04 10:56:06 mean rate: 29358.98
2021/07/04 10:56:07 meter rate.requests
2021/07/04 10:56:07 count: 279201
2021/07/04 10:56:07 1-min rate: 19225.00
2021/07/04 10:56:07 5-min rate: 19225.00
2021/07/04 10:56:07 15-min rate: 19225.00
2021/07/04 10:56:07 mean rate: 31022.05
2021/07/04 10:56:08 meter rate.requests
2021/07/04 10:56:08 count: 321704
2021/07/04 10:56:08 1-min rate: 21295.03
2021/07/04 10:56:08 5-min rate: 19652.92
2021/07/04 10:56:08 15-min rate: 19368.43
2021/07/04 10:56:08 mean rate: 32170.20
2021/07/04 10:56:09 meter rate.requests
2021/07/04 10:56:09 count: 362403
2021/07/04 10:56:09 1-min rate: 21295.03
2021/07/04 10:56:09 5-min rate: 19652.92
2021/07/04 10:56:09 15-min rate: 19368.43
2021/07/04 10:56:09 mean rate: 32945.48
2021/07/04 10:56:10 meter rate.requests
2021/07/04 10:56:10 count: 401442
2021/07/04 10:56:10 1-min rate: 21295.03
2021/07/04 10:56:10 5-min rate: 19652.92
2021/07/04 10:56:10 15-min rate: 19368.43
2021/07/04 10:56:10 mean rate: 33453.34
2021/07/04 10:56:11 meter rate.requests
2021/07/04 10:56:11 count: 440905
2021/07/04 10:56:11 1-min rate: 21295.03
2021/07/04 10:56:11 5-min rate: 19652.92
2021/07/04 10:56:11 15-min rate: 19368.43
2021/07/04 10:56:11 mean rate: 33915.67
2021/07/04 10:56:12 meter rate.requests
2021/07/04 10:56:12 count: 479301
2021/07/04 10:56:12 1-min rate: 21295.03
2021/07/04 10:56:12 5-min rate: 19652.92
2021/07/04 10:56:12 15-min rate: 19368.43
2021/07/04 10:56:12 mean rate: 34235.60
2021/07/04 10:56:13 meter rate.requests
2021/07/04 10:56:13 count: 518843
2021/07/04 10:56:13 1-min rate: 22744.85
2021/07/04 10:56:13 5-min rate: 19979.77
2021/07/04 10:56:13 15-min rate: 19479.57
2021/07/04 10:56:13 mean rate: 34589.43
2021/07/04 10:56:14 meter rate.requests
2021/07/04 10:56:14 count: 560260
2021/07/04 10:56:14 1-min rate: 22744.85
2021/07/04 10:56:14 5-min rate: 19979.77
2021/07/04 10:56:14 15-min rate: 19479.57
2021/07/04 10:56:14 mean rate: 35016.17
```


如果使用Meter度量服务的最佳性能值，那么需要有持续稳定的“施压”，待1、5、15分钟速率稳定后，这时的值才有意义。Meter的最后一项mean rate是平均值，即服务启动后处理请求的总量与程序运行时间的比值。

#### 4) Histogram

Histogram是直方图，与概率统计学上直方图的概念类似，go-metrics中的Histogram也是用来统计一组数据的统计学分布情况的。除了最小值(min)、最大值(max)、平均值(mean)等，它还测量中位数(median)、第75、90、95、98、99和99.9百分位数。

直方图可以用来度量事件发生的数据分布情况，比如：服务器处理请求时长的数据分布情况，下面就是这样一个例子：

```
// histogram.go
package main
import (
"log"
"math/rand"
"net/http"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
s := metrics.NewExpDecaySample(1028, 0.015)
h := metrics.NewHistogram(s)
metrics.GetOrRegister("latency.response", h)
go metrics.Log(metrics.DefaultRegistry, time.Second, log.Default())
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
i := rand.Intn(10)
h.Update(int64(time.Microsecond * time.Duration(i)))
})
http.ListenAndServe(":8080", nil)
}
```


在上面这个例子中，我们使用一个随机值来模拟服务处理http请求的时间。Histogram需要一个采样算法，go-metrics内置了ExpDecaySample采样。运行上述示例，并使用hey模拟客户端请求，我们得到如下输出：

```
$go run histogram.go
2021/07/04 11:31:54 histogram latency.response
2021/07/04 11:31:54 count: 0
2021/07/04 11:31:54 min: 0
2021/07/04 11:31:54 max: 0
2021/07/04 11:31:54 mean: 0.00
2021/07/04 11:31:54 stddev: 0.00
2021/07/04 11:31:54 median: 0.00
2021/07/04 11:31:54 75%: 0.00
2021/07/04 11:31:54 95%: 0.00
2021/07/04 11:31:54 99%: 0.00
2021/07/04 11:31:54 99.9%: 0.00
2021/07/04 11:31:55 99.9%: 0.00
... ...
2021/07/04 11:31:59 histogram latency.response
2021/07/04 11:31:59 count: 33244
2021/07/04 11:31:59 min: 0
2021/07/04 11:31:59 max: 9000
2021/07/04 11:31:59 mean: 4457.20
2021/07/04 11:31:59 stddev: 2793.67
2021/07/04 11:31:59 median: 4000.00
2021/07/04 11:31:59 75%: 7000.00
2021/07/04 11:31:59 95%: 9000.00
2021/07/04 11:31:59 99%: 9000.00
2021/07/04 11:31:59 99.9%: 9000.00
2021/07/04 11:32:00 histogram latency.response
2021/07/04 11:32:00 count: 78970
2021/07/04 11:32:00 min: 0
2021/07/04 11:32:00 max: 9000
2021/07/04 11:32:00 mean: 4465.95
2021/07/04 11:32:00 stddev: 2842.12
2021/07/04 11:32:00 median: 4000.00
2021/07/04 11:32:00 75%: 7000.00
2021/07/04 11:32:00 95%: 9000.00
2021/07/04 11:32:00 99%: 9000.00
2021/07/04 11:32:00 99.9%: 9000.00
2021/07/04 11:32:01 histogram latency.response
2021/07/04 11:32:01 count: 124573
2021/07/04 11:32:01 min: 0
2021/07/04 11:32:01 max: 9000
2021/07/04 11:32:01 mean: 4459.14
2021/07/04 11:32:01 stddev: 2820.38
2021/07/04 11:32:01 median: 4000.00
2021/07/04 11:32:01 75%: 7000.00
2021/07/04 11:32:01 95%: 9000.00
2021/07/04 11:32:01 99%: 9000.00
2021/07/04 11:32:01 99.9%: 9000.00
... ...
```


Histogram度量输出的值包括min、max、mean(平均数）、median（中位数）、75、95、99、99.9百分位数上的度量结果。

#### 5) Timer

最后我们来介绍Timer这个度量类型。大家千万别被这度量类型的名称所误导，这并不是一个定时器。

Timer是go-metrics定义的一个抽象度量类型，它可以理解为Histogram和Meter的“合体”，即既度量一段代码的执行频率（rate）,又给出这段代码执行时间的数据分布。这一点从Timer的实现亦可以看出来：

```
// https://github.com/rcrowley/go-metrics/blob/master/timer.go
func NewTimer() Timer {
if UseNilMetrics {
return NilTimer{}
}
return &StandardTimer{
histogram: NewHistogram(NewExpDecaySample(1028, 0.015)),
meter: NewMeter(),
}
}
```


我们看到一个StandardTimer是由histogram和meter组成的。 我们还是以上面的http server服务为例，我们这次用Timer来度量：

```
// timer.go
package main
import (
"log"
"math/rand"
"net/http"
"time"
"github.com/rcrowley/go-metrics"
)
func main() {
m := metrics.NewTimer()
metrics.GetOrRegister("timer.requests", m)
go metrics.Log(metrics.DefaultRegistry, time.Second, log.Default())
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
i := rand.Intn(10)
m.Update(time.Microsecond * time.Duration(i))
})
http.ListenAndServe(":8080", nil)
}
```


大家可以看到在这里我们同样用随机数模拟请求的处理时间并传给Timer的Update方法。运行这段代码并用hey压测：

```
$go run timer.go
2021/07/04 17:13:47 timer timer.requests
2021/07/04 17:13:47 count: 13750
2021/07/04 17:13:47 min: 0.00ns
2021/07/04 17:13:47 max: 9000.00ns
2021/07/04 17:13:47 mean: 4406.61ns
2021/07/04 17:13:47 stddev: 2785.11ns
2021/07/04 17:13:47 median: 4000.00ns
2021/07/04 17:13:47 75%: 7000.00ns
2021/07/04 17:13:47 95%: 9000.00ns
2021/07/04 17:13:47 99%: 9000.00ns
2021/07/04 17:13:47 99.9%: 9000.00ns
2021/07/04 17:13:47 1-min rate: 0.00
2021/07/04 17:13:47 5-min rate: 0.00
2021/07/04 17:13:47 15-min rate: 0.00
2021/07/04 17:13:47 mean rate: 13748.57
2021/07/04 17:13:48 timer timer.requests
2021/07/04 17:13:48 count: 56584
2021/07/04 17:13:48 min: 0.00ns
2021/07/04 17:13:48 max: 9000.00ns
2021/07/04 17:13:48 mean: 4442.61ns
2021/07/04 17:13:48 stddev: 2895.66ns
2021/07/04 17:13:48 median: 4000.00ns
2021/07/04 17:13:48 75%: 7000.00ns
2021/07/04 17:13:48 95%: 9000.00ns
2021/07/04 17:13:48 99%: 9000.00ns
2021/07/04 17:13:48 99.9%: 9000.00ns
2021/07/04 17:13:48 1-min rate: 0.00
2021/07/04 17:13:48 5-min rate: 0.00
2021/07/04 17:13:48 15-min rate: 0.00
2021/07/04 17:13:48 mean rate: 28289.23
2021/07/04 17:13:49 timer timer.requests
2021/07/04 17:13:49 count: 102426
2021/07/04 17:13:49 min: 0.00ns
2021/07/04 17:13:49 max: 9000.00ns
2021/07/04 17:13:49 mean: 4436.77ns
2021/07/04 17:13:49 stddev: 2892.85ns
2021/07/04 17:13:49 median: 4000.00ns
2021/07/04 17:13:49 75%: 7000.00ns
2021/07/04 17:13:49 95%: 9000.00ns
2021/07/04 17:13:49 99%: 9000.00ns
2021/07/04 17:13:49 99.9%: 9000.00ns
2021/07/04 17:13:49 1-min rate: 0.00
2021/07/04 17:13:49 5-min rate: 0.00
2021/07/04 17:13:49 15-min rate: 0.00
2021/07/04 17:13:49 mean rate: 34140.68
```


我们看到Timer度量的输出也的确是Histogram和Meter的联合体！

### 3. 小结

通过go-metrics包，我们可以很方便地为一个Go应用添加度量指标，go-metrics提供的meter、histogram可以覆盖Go应用基本性能指标需求（吞吐性能、延迟数据分布等）。go-metrics还支持各种指标值导出的，只是这里没有提及，大家可以到go-metrics官网了解详情。

本文涉及的源码可以在[这里下载](https://github.com/bigwhite/experiments/tree/master/go-metrics) – https://github.com/bigwhite/experiments/tree/master/go-metrics

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

## 评论