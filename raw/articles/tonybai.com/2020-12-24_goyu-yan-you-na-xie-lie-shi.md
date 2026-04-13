---
title: Go语言有哪些“劣势”
url: https://tonybai.com/2020/12/24/the-disadvantages-of-go/
published: '2020-12-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言有哪些“劣势”

![img{512x368}](../../assets/e66d398e0724ec7b.png)


本文源于笔者对知乎上的一个问题[“Go有哪些劣势？”](https://www.zhihu.com/question/300163211)(https://www.zhihu.com/question/300163211)的一次[回答](https://www.zhihu.com/question/300163211/answer/1632229924)(https://www.zhihu.com/question/300163211/answer/1632229924)。当时随手花几分钟在手机上写了一些点。但事后我觉得应该再做一些系统地思考。在这里我就将更系统地思考后的答案整理并分享给大家。

关于Go语言，我是喜欢的，甚至可以算作“鼓吹者”阵营的一份子。但我一贯秉承“Go并非完美语言”这个观点来尽可能客观地看待Go。每种编程语言都有自己的劣势，Go也不例外，下面我们就来列举一下Go的那些“劣势”：

## 1. 技术路线选择导致的“性能劣势”

众所周知，Go是带垃圾回收的编程语言，因此不管Go的STW(Stop The World)的时间有多么短，GC的延迟有多么的小，它依然属于GC类编程语言，和Java、C#属于一个阵营，同时天然与C、C++、Rust这样的手动管理内存、没有运行时GC负担的编程语言之间划清了界线。虽然[Go语言的初衷是成为系统级编程语言](https://www.imooc.com/read/87/article/2320)(关于Go语言的诞生语言演化历史，可以参考我的技术专栏文章[“Go语言的前生今世”](https://www.imooc.com/read/87/article/2320) https://www.imooc.com/read/87/article/2320 )，虽然Go的运行时性能可以满足99.99%的场合的需要，虽然百度的万亿流量[转发引擎BFE](https://github.com/bfenetworks/bfe)、时序数据库[influxdb](https://github.com/influxdata/influxdb)、分布式关系数据库[TiDB](https://github.com/pingcap/tidb)等性能敏感的项目都选择了用Go实现，但不能否认的是在一些性能超级敏感的场合，选择Go依然要慎重。

## 2 坚持自己的设计哲学所带来的“表达劣势”

### 1) “单一”的表达方法

很多从其他语言转到Go阵营的开发人员抱怨**Go能玩的花样太少，套路不多**，Go之所以表现出“表达劣势”，源于其设计哲学中的一个原则：“崇尚一个事情只有一个或少数几种写法”。这个原则不符合某些开发人员炫技的心理需求，于是Go就被诟病为是**资质平平的程序员才会去用的语言**。

[Go 1.18将加入泛型（类型参数）](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)，这算是对此类“劣势”的一个“弥补”。不过对于我们这些对Go价值观和设计哲学认同已久的Gopher而言，我们十分担心**大幅提高Go表达能力的 泛型将成为奇技淫巧的“滋生地”**。

### 2) “过时”的显式的错误处理

Go语言从诞生那天起就没有像C++、Java、Python等主流编程语言那样提供基于异常（exception）的结构化try-catch-finally错误处理机制，Go的设计者们认为[将异常耦合到程序控制结构中会导致代码混乱](https://tip.golang.org/doc/faq#exceptions)。Go提供了一种简单的基于错误值比较的错误处理机制，这“强迫”每个Go开发人员都必须显式地去关注和处理每个错误，经过显式错误处理的代码会更为健壮，也会让Go开发人员对这些代码更有信心。但这一设计哲学的坚持却被很多来自其他语言的开发者嘲笑为“过时”，被称为“半个世纪前的古老机制”。(笔者注：二十世纪70年代C语言诞生时采用的错误处理机制)

Go开发团队也曾“动摇过”，Go开发团队在发布Go2计划后曾发布过多版[Go错误处理的新机制草案](https://github.com/golang/proposal/blob/master/design/32437-try-builtin.md)。Go社区也针对此问题做过长时间的讨论甚至是“争吵”，知名Gopher Dave Cheney发声、Rob Pike发声，著名Go培训师、《Go语言实战》联合作者之一的威廉·肯尼迪（William Kennedy）更是在Go团队try 提案公示之后，发表了对Go社区的公开信反对try方案(更多内容可参考笔者的专栏文章[“if err != nil 重复太多可以这么办”](https://www.imooc.com/read/87/article/2434)(https://www.imooc.com/read/87/article/2434)，最终坚持Go设计哲学的一派占据了上风，try提案被否决，没有加入到[Go 1.13版本](https://mp.weixin.qq.com/s/Txqvanb17LYQYgohNiUHig)中！

## 3. 背离主流的“小众劣势”

Go早期设计的包依赖管理机制的确存在不小的“瑕疵”，这源于Google内部大单一代码仓库与基于主干的开发模型的影响。走出Google的Go语言听到了不同方面的声音，Go包管理机制长期无法满足社区的需求。于是先后出现了[vendor机制](https://tonybai.com/2015/07/31/understand-go15-vendor/)、[dep](https://tonybai.com/2017/06/08/first-glimpse-of-dep/)等对包依赖管理的改进尝试。

2018 年初，正当广大gopher们认为dep将“顺理成章”地升级为go官方工具链的一部分的时候，Go核心团队的技术负责人，也是Go 核心团队早期成员之一的Russ Cox在个人博客上连续发表了[七篇文章](https://research.swtch.com/vgo)，系统阐述了Go团队解决“包依赖管理” 的技术方案: [vgo](https://tonybai.com/2018/07/15/hello-go-module/)，即go module的前身。

vgo的主要思路包括：语义导入版本 (Semantic Import Versioning)、 最小版本选择 (Minimal Version Selection) ，这些都与当前主流编程语言的包依赖管理的规则相悖，尤其是[最小版本选择(MVS)](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)，算是另辟蹊径，背离主流！(更多关于go module最佳实践的内容可以参考我的专栏文章[“与时俱进！使用module管理依赖包”](https://www.imooc.com/read/87/article/2476)(https://www.imooc.com/read/87/article/2476))。

## 4. Go核心团队的“民主集中制”导致的“社区劣势”

和Rust团队广泛采纳社区建议“猛加语言特性”不同，Go像是另外一个极端：Go核心团队对语言演化的把控力十足，不是社区多数人赞同的就一定会被采纳而加入Go语言，我这里将其戏称为“民主集中制”吧，即真正的投票权其实在Go核心团队的代表社区的少数人手中。

2018年初的dep与vgo之争就是这一“劣势”的典型表现。社区费劲一年多努力精心打造的dep项目被Russ Cox等少数人集中花掉一些时间设计出的vgo给“挤出”了Go包依赖管理工具标准的位置，成为了Go module成功的“垫脚石”。即便最终证明Go团队使用go module的决策的结果是正确的，但 这导致的Go社区与Go核心团队的“裂痕”是确确实实存在的，以致于这两年Go核心团队极力改善与Go社区的关系，规范化和透明化Go proposal的提出、review和接纳流程。

## 5. 全面出击失败后，期望的落空导致的“功能孱弱劣势”

Go 1.5发布之后，由于实现了自举和GC延迟的大幅下降，Go受关注程度逐渐升高，直至2017年初第二次拿到TIOBE年度最佳编程语言，让Go语言有些“膨胀”，甚至狂热的Go鼓吹者曾一度希望Go一统江湖：不仅牢牢把持住自己的云原生市场，占领Java的企业级市场，还要在终端(android. ios)、前端(js)上击败现有对手。

有人可能觉得我的上述说法可笑，但这些说法并非空穴来风。Go语言在终端、前端方面还真的曾经发过力，了解Go历史的都知道，Go团队曾经有全职开发人员参与[gomobile项目](http://golang.org/x/mobile)(http://golang.org/x/mobile)，该项目旨在构建在Android和iOS上的Go技术栈，实现用Go语言编写终端应用的目的。

在前端方面，[gopherjs项目](https://github.com/gopherjs/gopherjs)(https://github.com/gopherjs/gopherjs)可以将go代码编译为js代码并运行于各大浏览器中。后来gopherjs的作者又帮助go项目原生支持webassembly，支持将go编译为webassembly运行在浏览器中。

但上面的尝试最终没能“得偿如愿”，现状是在终端、前端应用领域，使用Go编码的人少之又少。于是Go又逐渐冷静下来，回到自己擅长的主力战场，回归到了企业级应用、基础设施、中间件、微服务、命令行应用等领域，并且在这些领域取得了越来越多开发者的青睐。

但曾经的全面出击失败给很多开发者留下了“Go功能孱弱”的口实，甚至有人说[亲爹Google](https://mp.weixin.qq.com/s/itMeNYq3qBn6tJTz3H89RA)也没能让亲兄弟Android给Go走个后门。

## 小结

记得有人问过Go核心开发团队这样一个问题：**未来Go语言演化之路上最困难的事情是什么**？Go团队的回答是：**使Go语言一直保持简单**。

在本文列出的几点“劣势”中，除了第一点的性能劣势和最后两点有待商榷外，其他几点对于不爱Go的开发人员来说，这些的确都是“劣势”。但对于真正认同Go价值观和设计哲学的开发者而言，这些难道不正是Go语言的“优势”吗！

**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足>广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！78元简直就

是白菜价，简直就是白piao! 欢迎大家订阅！

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

- Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily
- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感觉和 Rust 相比，功能的迭代速度没有那没快，长远看可能也会成为一个劣势

Go核心团队对每一个功能特性提案都是慎之又慎，就像在本站《Go核心开发团队成员谈诞生13年的Go语言：生态系统、演化与未来》一文中qcon记者总结的那样：“编程语言的历史只朝着一个方向发展，每一种新的语言的出现都让事情都变得越来越复杂，越来越抽象。然而，就在十几年前，Go在Google诞生了。这种编程语言走的是另外一条路，它把赌注押在了简单和精心的设计和实现上。这个配方一直保留到今天”。Go走的是与众不同的道路，堆砌功能特性不是go的哲学。