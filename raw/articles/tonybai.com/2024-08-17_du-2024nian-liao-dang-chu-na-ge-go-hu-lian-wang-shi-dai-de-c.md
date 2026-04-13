---
title: 都2024年了，当初那个“Go，互联网时代的C语言”的预言成真了吗？
url: https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true/
published: '2024-08-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 都2024年了，当初那个“Go，互联网时代的C语言”的预言成真了吗？

![](../../assets/dc93de95f2b960d2.png)


[本文永久链接](https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true) – https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true

[本文最初发表于我个人的微信公众号(iamtonybai)](https://mp.weixin.qq.com/s/GTXSNoPTmJ-mprMKAY8esw)，但鉴于图片消息的篇幅受限(<=1000字)，一些内容没能如愿展开，这里在博客上重新发布一下，也顺道丰富一下文章的内容。

2012年，[七牛云](https://www.qiniu.com/)创始人、[goplus语言](https://github.com/goplus/gop)之父[许式伟](https://github.com/xushiwei)在一次演讲中给出一个大胆的预言：“**Go，互联网时代的C语言**”。

![](../../assets/833b5ce40ee8597e.png)


十余年过去了，我们不禁要问：当初的那个预言是否已经成真？

在讨论这个预言之前，我们先来看在同一份演讲稿中，老许给出的另外三个预判：

![](../../assets/faf49d44af77c67d.png)


它们是：

- Java语言份额继续下滑，最终被C和Go语言超越；
- C语言将长居编程榜第二的位置，有望在Go取代Java前重获第一的宝座；
- Go语言最终会取代Java位居编程榜榜首。

编程语言排行榜有很多，我们就以名气最大的[TIOBE](https://www.tiobe.com/tiobe-index/)刚刚发布的2024年8月排行榜为例，看看这些预判是否成真。

![](../../assets/7c8045a32742787e.png)


很遗憾，**一个也没命中**。

在这份最新榜单中，C位列第三、Java位列第四，Go位列第九，[相对于前两个月的第七](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247497403&idx=1&sn=03bc972e38163e1539da765249d46586&chksm=e860115adf17984cfe47f9680d8c0fb6370987ad45415ff2d38233d05fe6b315210ce6ada385#rd)还下降了两位。不过不得不说，老许对C语言的预判还是相对准确的。

那这是否意味着老许最初的那个预言也Miss了呢？个人觉得：**并没有**。因为这要看从哪个角度来审视。

传统观点认为，C语言被视为系统编程语言的杰出代表，因其卓越的底层操作能力和极致性能而广受推崇。它允许开发者直接与硬件交互，提供了高效的资源管理和快速的执行速度。如果从这样的视角去看待那则预言，那显然Go与“互联网时代C语言”这个评价和地位是不相称的。虽然[Go最初的定位也是一门系统编程语言](https://go.dev/talks/2012/splash.article)。

但如果我们跳出以“低级操作和性能”为中心的比较框架，而是**从不同时代软件技术栈的层次与构建来看，Go与C语言的地位又极其的相似**。

在互联网时代到来之前，C语言已经是整个软件技术栈的基石：从操作系统内核、设备驱动程序、中间件到应用程序，C语言凭借卓越的性能、无以伦比的生态，在技术栈的各个层次都有着广泛且核心的应用。

当时针指向云原生时代时，**Go语言在云原生技术栈的构建中，发挥了与C语言相似的作用**：

- 云原生“操作系统”：
[Kubernetes](https://mp.weixin.qq.com/s/paOduv0t1CtBCUoUBfJ7rQ)； - 云原生“驱动程序”：容器运行时（
[docker](https://tonybai.com/tag/docker)、[containerd](https://github.com/containerd/containerd)、[podman](https://github.com/containers/podman)）、网络插件([Calico](https://github.com/projectcalico/calico)、[cilium](https://github.com/cilium/cilium)、[CoreDNS](https://github.com/coredns/coredns)等)、存储插件（[Rook](https://github.com/rook/rook)、[longhorn](https://github.com/longhorn/longhorn?tab=readme-ov-file)等）； - 云原生“中间件”：数据库(
[CockroachDB](https://github.com/cockroachdb/cockroach)、[Vitess](https://github.com/vitessio/vitess)、[InfluxDB(2.x)](https://github.com/influxdata/influxdb/tree/main-2.x)、[VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics)、[Dgraph](https://github.com/dgraph-io/dgraph)、[milvus](https://github.com/milvus-io/milvus)等)、消息队列([NATS](https://github.com/nats-io/nats-server)、[nsq](https://github.com/nsqio/nsq)等)、服务网格([Istio](https://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio)、[linkerd2](https://github.com/linkerd/linkerd2))、API网关/代理([Traefik](https://github.com/traefik/traefik)、[emissary](https://github.com/emissary-ingress/emissary)等)、镜像仓库/加速器([harbor](https://tonybai.com/2017/10/23/the-speech-script-practice-on-deploying-a-ha-harbor-cluster-for-osc-shenyang-2017/)、[Dragonfly](https://github.com/dragonflyoss/Dragonfly2))、key-value存储([Etcd](https://github.com/etcd-io/etcd)、[consul](https://github.com/hashicorp/consul)、[junodb](https://github.com/paypal/junodb))、安全相关([falco](https://github.com/falcosecurity/falco)、[OPA](https://github.com/open-policy-agent/opa)、[vault](https://github.com/hashicorp/vault))、可观测组件([OpenTelemetry](https://github.com/open-telemetry/community)、[Prometheus](https://github.com/prometheus/prometheus)、[Thanos](https://github.com/thanos-io/thanos)、[Cortex](https://github.com/cortexproject/cortex)等)、基础设施管理([terraform](https://github.com/hashicorp/terraform)、[dagger](https://github.com/dagger/dagger))、分布式存储([minio](https://github.com/minio/)、[SeaweedFS](https://github.com/seaweedfs/seaweedfs)、[juicefs](https://github.com/juicedata/juicefs))、AI大模型运维([ollama](https://github.com/ollama/ollama))。 - 应用层：
[Caddy](https://github.com/caddyserver/caddy)、[gohugo](https://github.com/gohugoio/hugo)、[mattermost](https://github.com/mattermost/mattermost)等。

我们用一张示意图来横向对比一下：

![](../../assets/03e7c66b59d96cff.png)


听我讲到这里，你是不是觉得老许的那个预言好像命中了呢！

当然，从狭义的角度来看，Go与C还有一些地方是很像的，比如：语法简单、跨平台可移植性好等。并且两者还“沾亲带故”：Unix之父Ken Thompson当年和Dennis Ritchie一起发明了C语言，又和Rob Pike等一起设计了Go语言！

最后，回顾许式伟2012年的预言，我们不得不惊叹于其洞察力。Go语言确实在很大程度上成为了”互联网时代的C语言”，但不是通过传统的性能优势，而是通过**重新构建了云原生技术栈**，从这个角度看，Go语言也不失为云原生时代的”系统语言” —— 它不仅能够优雅地处理分布式系统的复杂性，它还使得构建和维护大规模、高可靠性的分布式系统变得更为简单，是云原生时代的思维方式和解决方案的集大成者，某种程度上还可以说定义了云原生时代的软件开发范式。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

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
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论