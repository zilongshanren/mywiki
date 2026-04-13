---
title: 2021年Go语言盘点：厉兵秣马强技能，蓄势待发新征程
url: https://tonybai.com/2022/01/16/the-2021-review-of-go-programming-language/
published: '2022-01-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 2021年Go语言盘点：厉兵秣马强技能，蓄势待发新征程

![](../../assets/e88f9e53d3997e8b.png)


[本文永久链接](https://tonybai.com/2022/01/16/the-2021-review-of-go-programming-language) – https://tonybai.com/2022/01/16/the-2021-review-of-go-programming-language

由于日常忙工作，闲时忙[专栏](http://gk.link/a/10AVZ)，我早已策划的**2021年Go语言盘点**这篇文章一直拖到了2022年元旦之后才开始落笔。

2021年，[Go迈过了其开源的第12个年头](https://mp.weixin.qq.com/s/ycmFabQVfFeiCiJdcjvOTA)。虽然已经演进了10余年，但在编程语言这个领域中，Go依旧属于“小字辈”，仍处于快速的成长演化期。

纵观整个2021年，如果要用一句话来形容Go语言的发展，那就是**厉兵秣马，蓄势待发**。“厉兵秣马”这个成语的意思是把兵器磨快，把战马喂饱，形容做好战备，也比喻事前做好准备工作。那么2021年的Go究竟在为什么做准备呢？毫无疑问，它就是**2022年泛型语法特性的落地**。泛型既是Go社区最关注的语法特性，也是Go在语言特性方面的又一个“杀手锏”。

在[“Go语言第一课”](http://gk.link/a/10AVZ)专栏的第一讲[“前世今生：你不得不了解的Go的历史和现状”](https://time.geekbang.org/column/article/426282)一文中，我曾提到过：**绝大多数主流编程语言将在其诞生后的第15至第20年间大步前进**。按照这个编程语言的一般规律，已经迈过[开源第12个年头的Go](https://mp.weixin.qq.com/s/ycmFabQVfFeiCiJdcjvOTA)很可能将进入自己的黄金5-10年。而2022年很大可能会成为Go语言黄金5-10年的起点，并且其标志只能是Go泛型语法的落地。

当然，Go核心团队以及Go社区所做的工作远不止打磨、优化和实现Go泛型语法这么简单，2021也是Go在其他方面成果丰硕的一年。下面我们就来盘点一下整个2021年Go语言的演化情况和当前状态，最后再对Go的2022年做个简单的展望。

我们先来看看2021年围绕Go语言项目以及Go社区都发生了哪些大事件(按时间先后顺序)！

### 一. 2021年Go大事件回顾

#### Go 1.16版本发布

按照一年发布两次大版本的节奏，Go核心团队于2021年2月18日发布了[Go 1.16版本](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)。该版本拥有一个重要的意义，那就是**Go module构建模式成为了默认构建模式**，这也意味着Go module构建模式的引入成功。与此同时，这一版本还支持了苹果的M1芯片（通过darwin/arm64环境变量组合）；[新增io/fs包](https://mp.weixin.qq.com/s/_pUtGQSl_oSRnmmfROJ6ZQ)，建立Go原生文件系统抽象；**新增embed包**，作为在二进制文件中嵌入静态资源文件的官方方案；进一步对Go链接器进行现代化改造，新版链接器的性能相比于[Go 1.15版本](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)有20%-25%的提升，资源占用则下降5%-15%。编译出的二进制文件大小下降10%以上。

#### 2020年Go用户调查结果发布

2021年3月初，[Go官网发布了2020年Go用户调查结果](https://go.dev/blog/survey2020-results)。此次调查共收到近1w份有效调查反馈，报告的亮点如下：

- Go在工作场所和企业中的使用范围不断扩大，76%的受访者在工作中使用Go，66%的人说Go对他们公司的成功至关重要。
- 总体满意度很高，92%的受访者对使用Go感到满意。
- 大多数受访者在不到3个月的时间里感觉到了Go的生产力，81%的受访者感觉Go的生产力非常高。
- 受访者表示会及时升级到最新的Go版本，76%的受访者在头5个月就升级了。
- Go module得到了普遍的接纳与采用，满意度达到77%，但受访者也强调了对文档改进的需求。
- Go继续被大量用于API、CLI、Web、DevOps和数据处理。

#### Go 1.17版本发布

2021年8月16日，[Go 1.17版本在经过两个RC版本之后正式发布](https://blog.golang.org/go1.17)！[Go 1.17版本](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)并没有过多受到Go 1.18版本这个“网红”的影响，Go 1.17默默地加入和优化了着实不少的特性。其中最主要的三个变化是：

[支持从切片到数组指针转换的语法特性](https://mp.weixin.qq.com/s/Afj9pV79AParMkMvcNlCTw)- Go module
[使用pruned module graph](https://mp.weixin.qq.com/s/Fer90nattWxXDWDC1VV55w)

Go 1.17不再使用“完整module依赖图”，而是引入了pruned module graph（修剪的module依赖图）。修剪的module依赖图就是在完整module依赖图的基础上将那些“占着茅坑不拉屎”、对构建完全没有“贡献”的间接依赖module修剪后的依赖图。使用修剪后的module依赖图进行构建将有助于避免下载或阅读那些不必要的go.mod文件，这样Go命令可以不去获取那些不相关的依赖关系，从而在日常开发中节省时间。

- 在amd64架构实现了
[从基于堆栈的调用惯例到基于寄存器的调用惯例切换](https://mp.weixin.qq.com/s/AkJoXLlpSmw5vMZDpXoq5w)

切换到[基于寄存器的调用惯例](https://go.googlesource.com/go/+/refs/heads/dev.regabi/src/cmd/compile/internal-abi.md)后，一组有代表性的Go包和程序的基准测试显示，Go程序的运行性能提高了约5%，二进制文件大小典型减少约2%。也就是说你的Go源码使用Go 1.17版本重新编译一下就能获得大约5%的性能提升。

#### Go开源12岁生日

2009年11月10日，Go语言正式对外发布并开源。2021年11月，距那一历史时刻已经过去12年了。Go核心团队技术负责人[Russ Cox在Go官博撰文庆祝Go开源12周年](https://go.dev/blog/12years)。他简单回顾了这一年来Go核心团队与Go社区为Go的发展做出的卓越贡献，展望了在接下来的Go开源的第13个年头中，Go核心团队的工作重点，包括Go module的持续演进、Go泛型的落地、软件材料清单、Go漏洞数据库等。

#### Go官网切换

在2021年11月末，Go核心团队正式将Go语言官网从golang.org切换到go.dev。Go团队对官网体验的改善工作已经进行了很长时间了，从[2019年go.dev被启用](https://go.dev/blog/go.dev)，到[将godoc.org切换到pkg.go.dev](https://go.dev/blog/godoc.org-redirect)，再到[其他原官网功能逐一切换到go.dev](https://go.dev/blog/tidy-web)上，Go核心团队在一点点的引导Gopher去使用和适应go.dev这个站点。

![](../../assets/47b846db1be54a26.png)


为了Go社区建设与Go官网改进，Go团队雇佣专人进行对应。Go核心开发团队专职人员的数量逐年增多。根据[Go核心团队工程总监SAMEER AJMANI在之前Go Time的AMA环节中透露的信息](https://changelog.com/gotime/210)，当前Go核心团队的规模已经达到了50余人：

![](../../assets/41fb0085ce3fb25e.jpg)


不得不感慨一下：[有一个有钱的爹是真好啊](https://tonybai.com/2012/10/08/the-new-age-of-programming-language/)!

#### GopherCon 2021和Go 1.18Beta1发布

由于新冠疫情的影响，这两年的GopherCon大会都以网络直播的形式进行。今年的大会改在了12月初。GopherCon大会向来是既是Go社区的风向标，也是Go核心团队与Go社区互动的一个重要平台。在这次大会上，Go核心团队的两位重量级人物Robert Griesemer和Ian Lance Taylor亲自站台为大家讲解即将到来的Go泛型的相关内容与使用建议。

在GopherCon 2021大会余温未尽的时候，Go核心团队在美国时间12月14日宣布[Go 1.18 Beta1发布](https://mp.weixin.qq.com/s/Zthy6IAxGC10Q7q2N3gqMQ)。Go 1.18 Beta 1是第一个公测版，其主要功能变动包括Go泛型(类型参数)、[Go工作区模式](https://mp.weixin.qq.com/s/AGAz8dti8IwfVntOvBTUTg)、[支持Fuzzing test](https://mp.weixin.qq.com/s/5qnIUz3plQG65FVnbPZVLw)等。

Go团队这次少见的通过官博来发布一个beta版本，足以证明Go团队对Go 1.18版本的重视，毕竟Go 1.18是[Go自诞生以来](https://time.geekbang.org/column/article/426265)最大的一次语法变动，Go团队希望Go社区的gopher们广泛参与公测，在Go 1.18版本发布之前尽可能多地找出版本中存在的bug。

### 二. Go当前状态

经过一年多的发展与演化，Go语言当前的状态究竟如何呢？我们通过几个角度来看一下。

#### TIOBE排名上升一位

著名编程语言排名指数[TIOBE](https://www.tiobe.com/tiobe-index/)近期发布了2021年各大主流编程语言最终排名：

![](../../assets/5cb44d043e68a33c.png)


从上图可以看到，在2021年，Go从2020年终的第14名上升到第13名，继续保持稳健的发展节奏。并且TIOBE配文中认为，除了Swift和Go之外，尚不会有新的编程语言能迅速进入前3名甚至前5名。这样说明了对Go趋势的看好。

在另外一份基于stackoverflow数据的编程语言排行榜[redmonk](https://redmonk.com/sogrady/2021/08/05/language-rankings-6-21/)上(仅2021上半年数据，下半年数据尚未发布)，Go保持稳定：

![](../../assets/473d07ba59e42282.png)


#### 职业教育市场对Go的“追捧”可见一斑，Go“钱途”看好

职业教育市场直接反映了就业市场的需求。今年，国内头部的职业教育，比如：极客时间、慕课网都在Go语言这块发力。慕课网有谢大(astaxie)策划，曹春晖(xargin)主讲的[Go高级工程师实战营](https://class.imooc.com/sale/golive)。

极客时间更是上新多门Go语言相关专栏与课程，当然也包含笔者的[“Go语言第一课”](http://gk.link/a/10AVZ)。在笔者与极客时间郭蕾总编的沟通中，郭总透露了极客时间对Go语言的几个判断：

- 就目前我们的观察来看，Go语言正在加速向企业渗透，越来越多的企业开始用Go。
- 就目前我们的观察来看，越来越多的开发者考虑将Go语言作为第二门编程语言。
- 云原生已经成为趋势，而Go语言是其主要采用的语言。
- 腾讯、字节跳动、美团、阿里、快手等头部公司正在大力推广Go。

Go在国内的就业市场的情况也是越来越好，在年底的一份[程序员薪资报告](https://mp.weixin.qq.com/s/r8mRLESsfgI0i8qGZAht0g)中，我们看到国内Go程序员的平均薪资排在榜首：

![](../../assets/29f5c6e01fa1c216.png)


这总体上也能反映出Go在国内就业市场的“钱途”还是不错的。

#### 大厂Go新闻/输出盘点

Gopher们或想学习Go的童鞋都十分关注大厂中Go语言的应用情况。不过大厂中编程语言的应用范围只能通过官方或其雇员在一些渠道发布的消息来确认。下面是2021年大厂Go新闻/输出开源产品的盘点，通过这些内容我们可以大致勾勒出Go在大厂的应用情况。

##### 腾讯

2021年初，[腾讯官方发布《腾讯研发大数据报告》](https://www.sohu.com/a/456701865_100093134)，在这份报告中，Go语言成为腾讯公司内部增速最快的语言：

![](../../assets/fefd0ca09d1b1b59.jpeg)


2021年腾讯对外输出的公共资料以及开源的Go项目也充分印证了这一点：

[《揭秘腾讯内部Go Modules Proxy服务》](https://mp.weixin.qq.com/s/GuUHq3uyPiMCQg_G1odAWA)[《腾讯发布的Go语言代码安全指南》](https://github.com/Tencent/secguide/blob/main/Go%E5%AE%89%E5%85%A8%E6%8C%87%E5%8D%97.md)[《腾讯开源Go语言实现的百万级服务发现和治理中心北极星》](https://mp.weixin.qq.com/s/YP8aXGwd_vyYSgL8QyomvQ)[《腾讯开源的Kubernetes多集群管理和跨集群编排工具Clusternet》](https://mp.weixin.qq.com/s/t9e0UpInm7S_ojMsX5qJDg)[《腾讯首个CNCF沙箱项目分布式边缘容器系统SuperEdge开源》](https://mp.weixin.qq.com/s/xbkJmY60gyuggJ5GYI4KQQ)[《腾讯开源的etcd一站式治理平台Kstone》](https://github.com/tkestack/kstone)

可以说腾讯近些年在Go上面的投入很大，产出也颇丰。

##### 字节跳动

字节跳动是国内大厂中拥抱Go的最积极的公司之一。从[字节跳动的公开资料](https://zhuanlan.zhihu.com/p/382833278)来看：

字节跳动的技术体系以Go语言为主。根据最新的调查统计，公司里有超过55％的服务是采用Go的，排名第二的语言是前端的NodeJS，之后是Python、JAVA、C++，Rust也有一些使用。


长期的Go实践让字节跳动内部积累的丰富的Go产品和经验，2021年字节也开启了对外开源之路，并且一次性放出若干基于Go的微服务框架与中间件产品，包括kitex、netpoll、thriftgo等。这些开源项目统一放在https://github.com/cloudwego下面了。

腾讯和字节是拥抱Go的急先锋，其他大厂、独角兽也有一些Go应用的动作，比如：微软发布了[Go语言简明教程](https://docs.microsoft.com/en-us/learn/paths/go-first-steps/)、其开源的[dapr](https://dapr.io)也有持续的演化，并[招聘高级工程师参与Go官方编译器、工具生态开发](https://careers.microsoft.com/us/en/job/1038385/Senior-Software-Engineer)；阿里的[sealer](https://github.com/alibaba/sealer)；七牛云发布的[Go+](https://goplus.org/)等。

国外的uber也是公开数据中使用Go打造服务最多的巨头公司，2021年uber也在其[工程博客网站](https://eng.uber.com)发布了一系列Go实践经验的深度文章，值得大家认真拜读和揣摩。

除了上面大厂积极拥抱Go之外，小公司与初创公司也在积极探索Go的落地。只不过小公司数据不好采集，从圈子里、周边朋友、面试时了解的情况，用Go的小公司/初创公司越来越多了。究其原因还是那句话：**Go语言是生产力与性能的最佳结合**。这对小公司/初创公司而言就是真(省)金(人)白(省)银(机器)啊。 甚至Go已经渗透到新冠防疫领域，昨天得知河北移动支撑的流调系统的后端服务就是Go实现的。

接下来，我们再来展望一下2022年Go的发展情况会怎样。

### 三. Go语言2022展望

2022年，Go语言的最大事件就是2月份**Go 1.18的发布以及Go泛型的伴随落地**。泛型的加入势必会给Go社区带来巨大影响。随之而来的将是位于各个层次的Go包的重写或重构：底层库、中间件、数据结构/算法库、乃至业务层面。这一轮之后，Go社区将诞生有关于Go泛型编码的最佳实践，这些实践也会反过来为Go核心团队提供Go泛型演化与在标准库中应用的素材。

但泛型在提升语言表现力的同时，也会带来Gopher们最不想看到的复杂性，也正因为如此，Go核心团队也一直在努力向社区传达[“Go泛型使用的一般准则”](https://mp.weixin.qq.com/s/ur1eiZl4PKbF1PqELAdfKg)，以告知大家哪种场景适合使用泛型来加强代码，哪些场合泛型是不合适的。尽力防止泛型语法被滥用。

当然前面也说过，Go 1.18不仅仅是加入泛型，还有[Go工作区模式](https://mp.weixin.qq.com/s/AGAz8dti8IwfVntOvBTUTg)以及[原生支持fuzzing](https://mp.weixin.qq.com/s/5qnIUz3plQG65FVnbPZVLw)，前者是解决本地module开发与引用的方案，后者则为编写漏洞更少的代码提供了帮助。

有泛型加持的Go语言，“吸粉能力”得到了加强，将进一步得到来自其他语言阵营程序员的青睐。相信在2022年后半段，Gopher数量以及Go语言的受关注度都会有一定的增长。

Go泛型即将上路，也刚刚上路，离“完善”这个目标还有一定距离，就像go module一样，预计经过3-5个版本的打磨与优化，Go泛型才会真正成熟起来，并成为Go语言的又一柄利器。

综上，2021年，Go厉兵秣马，强化自身；2022，伴随着泛型的东风，Go语言将开启自己的新征程。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

偶然间找到了您写的for循环的那片文章，写的真好，后来就坚持看您的博客了。自学GO也有一年多了，书已到货，2022年的计划就是工作之余，消化吸收这两本书。加油

嗯嗯。有问题随时交流:)