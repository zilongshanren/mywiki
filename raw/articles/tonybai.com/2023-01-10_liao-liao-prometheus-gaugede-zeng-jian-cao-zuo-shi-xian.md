---
title: 聊聊Prometheus Gauge的增减操作实现
url: https://tonybai.com/2023/01/10/how-prometheus-gauge-add-and-sub/
published: '2023-01-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Prometheus Gauge的增减操作实现

![](../../assets/661fad4bdd1a4cb6.png)


[本文永久链接](https://tonybai.com/2023/01/10/how-prometheus-gauge-add-and-sub) – https://tonybai.com/2023/01/10/how-prometheus-gauge-add-and-sub

### 1. Gauge是啥？

熟悉Prometheus的小伙伴们都知道[Prometheus提供了四大指标类型](https://prometheus.io/docs/concepts/metric_types/)：

- Counter
- Gauge
- Histogram
- Summary

Histogram和Summary是一类，但理解起来稍复杂一些，这里我们暂且不提。Counter顾名思义“计数器”，仅提供了Add方法，是一个一直递增的数值；而Gauge直译为“仪表盘”，它也是一个数值，但和Counter不同，它不仅提供Add方法，还提供了Sub方法。如果你的指标可增可减或是需要支持负数，那么Gauge显然是一个比Counter更适合的指标类型。

近期我们在测试时发现一个Gauge值为负的问题，Gauge本身是支持负值的，但我们系统中的这个指标值从业务含义上来说是不应该为负值的，为了fix掉这个问题，我深入看了一下[Prometheus Go client包](https://github.com/prometheus/client_golang)中Gauge的实现方式，Gauge的实现方式代表了一类问题的典型解决方法，这里简单聊聊。

### 2. Gauge增减操作的原理

在Prometheus Go client包中，我们看到Gauge是一个接口类型：

```
// github.com/prometheus/client_golang/prometheus/gauge.go
type Gauge interface {
Metric
Collector
// Set sets the Gauge to an arbitrary value.
Set(float64)
// Inc increments the Gauge by 1. Use Add to increment it by arbitrary
// values.
Inc()
// Dec decrements the Gauge by 1. Use Sub to decrement it by arbitrary
// values.
Dec()
// Add adds the given value to the Gauge. (The value can be negative,
// resulting in a decrease of the Gauge.)
Add(float64)
// Sub subtracts the given value from the Gauge. (The value can be
// negative, resulting in an increase of the Gauge.)
Sub(float64)
// SetToCurrentTime sets the Gauge to the current Unix time in seconds.
SetToCurrentTime()
}
```


client包还提供了该接口的默认实现类型gauge：

```
// github.com/prometheus/client_golang/prometheus/gauge.go
type gauge struct {
// valBits contains the bits of the represented float64 value. It has
// to go first in the struct to guarantee alignment for atomic
// operations. http://golang.org/pkg/sync/atomic/#pkg-note-BUG
valBits uint64
selfCollector
desc *Desc
labelPairs []*dto.LabelPair
}
```


从gauge类型定义来看，作为仪表盘即时数值的gauge，其核心字段是uint64类型的valBits，该字段存储了gauge指标所代表的**即时值**。

不过我们看到Gauge接口类型中的Add和Sub方法的参数都是float64类型。Gauge接口类型中的方法**使用float64类型作为参数是无可厚非的**，这是因为Gauge要支持浮点数，要支持小数，浮点数可以转化为整型，但整型却无法支持转换为带有小数部分的浮点数。

那么为什么gauge类型中使用了uint64类型而不是float64类型的字段来存储gauge代表的即时值呢？这就要从Prometheus go client的一个特性说起，那就是**对Gauge即时值的修改要保证goroutine-safe**。具体来说，gauge使用的是atomic包提供的原子操作来保证这种并发访问安全。但标准库的atomic包支持uint64类型的原子操作，而不支持float64类型的原子操作，恰float64和uint64的size又都是8字节，于是Prometheus go client利用了uint64支持原子操作以及uint64和float64类型都是64bits长度这两点实现了gauge类型的Add和Sub方法：

```
// github.com/prometheus/client_golang/prometheus/gauge.go
func (g *gauge) Add(val float64) {
for {
oldBits := atomic.LoadUint64(&g.valBits)
newBits := math.Float64bits(math.Float64frombits(oldBits) + val)
if atomic.CompareAndSwapUint64(&g.valBits, oldBits, newBits) {
return
}
}
}
func (g *gauge) Sub(val float64) {
g.Add(val * -1)
}
```


我们看到Sub方法实际调用的也是Add方法，只是将val值乘了个-1后作为Add方法的参数。我们接下来重点来看看gauge的Add方法。

gauge Add方法的实现是一个**典型的CAS(CompareAndSwap)原子操作的使用模式**，即在一个无限循环中，先原子读取当前即时值，然后将其与传入的增量值进行加和得到新值，最后通过CAS操作将新值设置为当前即时值。如果CAS操作失败，则重新走一遍循环。

不过值得我们关注的是Add方法中的**float64与uint64类型各自的功用与相互的转换**。Add方法先是利用atomic.LoadUint64原子读取valBits的值，然后通过math.Float64frombits将其转换为float64类型，之后用得到的float64类型即时值与val进行加法运算，得到我们想要的新值。接下来就是将其重新存储到valBits中。float64不支持原子操作，因此再调用CAS之前，Add方法还需将新值转换回uint64，这就是上面代码调用math.Float64bits的原因，之后通过atomic.CompareAndSwapUint64将保存了float64位模式的uint64类型的新值newBits写入valBits中。

大家一定很好奇，math.Float64frombits和math.Float64bits是如何做的uint64和float64间的转换，我们来看一下他们的实现：

```
// $GOROOT/src/math/unsafe.go
// Float64bits returns the IEEE 754 binary representation of f,
// with the sign bit of f and the result in the same bit position,
// and Float64bits(Float64frombits(x)) == x.
func Float64bits(f float64) uint64 { return *(*uint64)(unsafe.Pointer(&f)) }
// Float64frombits returns the floating-point number corresponding
// to the IEEE 754 binary representation b, with the sign bit of b
// and the result in the same bit position.
// Float64frombits(Float64bits(x)) == x.
func Float64frombits(b uint64) float64 { return *(*float64)(unsafe.Pointer(&b)) }
```


我们看到，这两个函数只是利用unsafe包进行了类型转换，而并没有做任何算术运算。

关于如何使用unsafe包进行安全的类型转换，可以参见我的

[《Go语言精进之路》]一书的第58条“掌握unsafe包的安全使用模式”。

综上：

- gauge结构体中uint64类型的valBits实质上只是用来做float64数值的“承载体”，并借助原子操作对其类型的支持实现即时值的更新，它本身并不参与任何整型或浮点型计算；
- Add方法中的运算都是在浮点型之间进行的，Add方法通过math.Float64frombits将uint64中承载的符合IEEE 754的浮点数表示还原为一个浮点数类型，然后与同样是float64类型的输入参数进行加和计算，计算的结果再通过math.Float64bits函数转换为uint64类型，这个过程8字节字段的位模式没有发生任何变化，最后通过CAS操作将结果值(新的位模式)写入valBits。

valBits中存储的是满足

[IEEE 754]的浮点数的位模式。IEEE 754规范中，一个浮点数是由“符号位+阶码+尾数”构成的。详情可参考我的[《Go语言第一课》专栏]的第12讲[基本数据类型：Go原生支持的数值类型有哪些]。

### 3. 小结

gauge结构体以及其Add方法所使用的这种通过位模式转换实现float64原子操作的模式值得借鉴。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论