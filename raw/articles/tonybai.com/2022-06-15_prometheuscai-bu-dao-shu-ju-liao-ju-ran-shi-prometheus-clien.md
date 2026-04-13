---
title: Prometheus采不到数据了！居然是Prometheus client包的锅
url: https://tonybai.com/2022/06/15/prometheus-can-not-pick-up-data-because-of-the-prometheus-client-package/
published: '2022-06-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Prometheus采不到数据了！居然是Prometheus client包的锅

![](../../assets/bff4ceaba0f0f3fb.png)


[本文永久链接](https://tonybai.com/2022/06/15/prometheus-can-not-pick-up-data-because-of-the-prometheus-client-package) – https://tonybai.com/2022/06/15/prometheus-can-not-pick-up-data-because-of-the-prometheus-client-package

在基于eBPF的新一代观测设施尚未成熟之前，我们采用了业界成熟的[Prometheus](https://prometheus.io/)+[Grafana](https://grafana.com)方案采集节点与应用[度量指标(metrics)信息](https://tonybai.com/2021/07/06/add-metrics-for-go-application-using-go-metrics)。众所周知，这样的方案是一种**对应用有侵入的方案**，即需要在应用内部嵌入采集度量信息及与Prometheus通信的client包。

Prometheus官方提供并维护了主流语言的client包，包括Go、Java、Python、Ruby、[Rust](https://tonybai.com/2021/03/15/rust-vs-go-why-they-are-better-together)等，如下图：

![](../../assets/faa2b3a96fffc1ed.png)


Prometheus的go client端使用起来也不算复杂，总共分两步：

- 把你要获取的度量指标注册(Register)到Prometheus的Registry中；
- 建立起一个HTTP Server，暴露度量指标采集端口即可。

Prometheus采用拉模型(pull)收集时序度量数据，数据拉取行为是由Prometheus服务端来决定的，比如可以设定Prometheus拉取各个采集点的时间周期。 一般来说，这个技术栈已经很成熟，配置完启动后，马上就能看到效果。这个技术栈也很稳定，我们使用后一直运行良好，直到本周压测时遇到一个问题：**Prometheus采不到数据了**！

从最初的数据由连续的线变成“断断续续”的点，见下图：

![](../../assets/04bb5d58dba17ddb.png)


到后来干脆就无法采到任何数据了：

![](../../assets/a314764fc5a7940c.png)


之前Prometheus跑的好好的，为什么现在却采不到数据了呢？这次与之前的不同之处在于我们的压测用例情景下，每个服务节点都要建立百万以上的连接，而之前仅仅是10w左右的量级。

好在我们部署了[在线Continuous Profiling工具](https://github.com/pyroscope-io/pyroscope)，可以查看一下压测那段时间的资源占用，如下图：

![](../../assets/e437cd2be69e7e97.png)


上面是一个alloc object的火焰图，我们看到Prometheus client的Registry.Gather方法占了50%的内存分配开销，这是很不正常的。继续沿着Gather函数的火焰图看，我们看到底端居然是**readdir**。我们应用注册的度量指标也没有哪个采集时需要readdir啊！

要想解决这个问题只有**翻Prometheus client源码**了！

我们使用的是prometheus client端的默认defaultRegistry。 从源码中可以看到：这个defaultRegistry在初始化时，默认注册了两个collector:

```
// registry.go
func init() {
MustRegister(NewProcessCollector(ProcessCollectorOpts{}))
MustRegister(NewGoCollector())
}
```


我们发现：第一个processCollector会采集如下度量指标数据：

```
// process_collector.go
func (c *processCollector) Describe(ch chan<- *Desc) {
ch <- c.cpuTotal
ch <- c.openFDs
ch <- c.maxFDs
ch <- c.vsize
ch <- c.maxVsize
ch <- c.rss
ch <- c.startTime
}
```


在采集openFDs时，processCollector遍历了/proc/{pid}下面的fd目录：

```
// process_collector_other.go
func (c *processCollector) processCollect(ch chan<- Metric) {
pid, err := c.pidFn()
if err != nil {
c.reportError(ch, nil, err)
return
}
p, err := procfs.NewProc(pid)
if err != nil {
c.reportError(ch, nil, err)
return
}
if stat, err := p.Stat(); err == nil {
ch <- MustNewConstMetric(c.cpuTotal, CounterValue, stat.CPUTime())
ch <- MustNewConstMetric(c.vsize, GaugeValue, float64(stat.VirtualMemory()))
ch <- MustNewConstMetric(c.rss, GaugeValue, float64(stat.ResidentMemory()))
if startTime, err := stat.StartTime(); err == nil {
ch <- MustNewConstMetric(c.startTime, GaugeValue, startTime)
} else {
c.reportError(ch, c.startTime, err)
}
} else {
c.reportError(ch, nil, err)
}
if fds, err := p.FileDescriptorsLen(); err == nil { // 这里获取openFDs
ch <- MustNewConstMetric(c.openFDs, GaugeValue, float64(fds))
} else {
c.reportError(ch, c.openFDs, err)
}
if limits, err := p.Limits(); err == nil {
ch <- MustNewConstMetric(c.maxFDs, GaugeValue, float64(limits.OpenFiles))
ch <- MustNewConstMetric(c.maxVsize, GaugeValue, float64(limits.AddressSpace))
} else {
c.reportError(ch, nil, err)
}
}
```


采集openFDS时，processCollector调用了FileDescriptorsLen方法，在FileDescriptorsLen方法调用的fileDescriptors方法中，我们找到了对Readdirnames的调用，见下面源码片段：

```
// github.com/prometheus/procfs/proc.go
// FileDescriptorsLen returns the number of currently open file descriptors of
// a process.
func (p Proc) FileDescriptorsLen() (int, error) {
fds, err := p.fileDescriptors()
if err != nil {
return 0, err
}
return len(fds), nil
}
func (p Proc) fileDescriptors() ([]string, error) {
d, err := os.Open(p.path("fd"))
if err != nil {
return nil, err
}
defer d.Close()
names, err := d.Readdirnames(-1) // 在这里遍历目录中的文件
if err != nil {
return nil, fmt.Errorf("could not read %q: %w", d.Name(), err)
}
return names, nil
}
```


通常情况下，读取/proc/{pid}/fd目录是没有问题的，但当我们的程序上连接着100w+的连接时，意味着fd目录下有100w+的文件，逐一遍历这些文件将带来很大的开销。这就是导致Prometheus在超时时间(通常是10几秒)内无法及时采集到数据的原因。

那么如何解决这个问题呢？

临时解决方法是将registry.go文件的init函数中的MustRegister(NewProcessCollector(ProcessCollectorOpts{}))这一行注释掉！这个进程度量指标信息对我们用处不大。不过这样做的不足是我们自己需要维护一份prometheus golang client包，需要用到go mod replace，十分不便，并且不便于prometheus golang client包的版本升级。

一劳永逸的解决方法是：**不使用默认Registry，而是使用NewRegistry函数新建一个Registry**。这样我们抛开默认注册的那些度量指标，并可以自行定义我们要注册的度量指标。需要时，我们也可以将ProcessCollector加进来，这个根据不同Go程序的需要而定。

按这个方案修改后，那些熟悉的连续曲线就又重现在眼前了！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论