---
title: “Go语言第一课”结课了
url: https://tonybai.com/2022/02/17/go-first-course-close/
published: '2022-02-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “Go语言第一课”结课了

![](../../assets/cd65088b0ace1d21.png)


[本文永久链接](https://tonybai.com/2022/02/17/go-first-course-close) – https://tonybai.com/2022/02/17/go-first-course-close

就在家家户户刚刚过完虎年元宵佳节之际，我的Go语言专栏：[《Tony Bai·Go语言第一课》](http://gk.link/a/10AVZ)也迎来了它的最后一讲[ 结术语](https://time.geekbang.org/column/article/486536)。

这门专栏的撰写开始于2021年5月中旬，翻看我用于管理专栏原始文稿的github仓库的commit log记录，这一有纪念价值的日子被精确定位在5月16日：

![](../../assets/b0e21082834f1b62.png)


从那时开始，我便进入了专栏的节奏。从2021年5月到2022年2月，9个月的时间洋洋洒洒写下了20多万字(估计值)，写作过程的艰辛只有写过极客时间专栏的作者们才会知道。每天睡眠4-5个小时是我的常态。这也算是对我个人极限的一种挑战了:)。

专栏于2021年10月13日[正式上线](https://mp.weixin.qq.com/s/xg_jnbRPqaolNksNLjStRw)！上线后，当我看到有那么订阅学习专栏、认真完成课后思考题以及在留言区留言的童鞋，**我顿感之前的努力与付出都没有白费**。

写结束语之前，我认真回顾了一下这门课的内容，当初设定的目标，包括覆盖了绝大多数Go语言的语法点等都基本实现。此外，从大家的留言反馈情况来看，彻底抛弃GOPATH，并将对Go module构建模式、Go项目布局的讲解前置到入门篇中是无比正确的决定。另外专栏对一些语法概念，比如切片、字符串、map、接口类型等进行了超出入门范畴的原理性地讲解也得到了来自学员的肯定，这也算是这个入门课的吸睛之处。

不过课程依然存在遗憾，其中最令我感到不安的是对指针这个概念的讲解的缺失。在规划课程之初，我没有意识到很多来自动态语言的童鞋完全没有对指针这个概念的认知，我的这个疏忽导致给一些学员的后续学习带去了困惑。为了弥补这个遗憾，我会在后面以加餐的形式补充对Go指针基础的讲解。

2022年3月份，[Go 1.18版本将携着泛型语法正式发布](https://go.dev/blog/go1.18beta2)。对于定位为“Go语言第一课”的本专栏来说，不能缺少对泛型语法的系统讲解，并且Go泛型很可能是Go语法特性的最后一次较大更新了。虽然通过加餐聊过泛型，但那些还是较为粗线条的，我将在后续**补充泛型篇**，系统全面介绍Go泛型语法的细节，专栏也要做到“与时俱进”！

Go语言第一课专栏上线以来得到了广大童鞋的点赞，这让我尤其开心。有些童鞋在结束语的留言中还期望我能后续能再出进阶或深度Go专栏：

![](../../assets/af59233543c69a24.png)


![](https://tonybai.com/wp-content/uploads/go-first-course-close-4.png)


![](../../assets/f6d4232494c787d6.png)


![](../../assets/90bfd773af4228a6.png)


这真的让我受宠若惊！不过，是否能出其他极客专栏，暂时还无法给大家承诺，还需要给我时间**复复盘、充充电，再策划策划^_^**。

撰写结束语时，恰逢著名编程语言排名指数[TIOBE](https://www.tiobe.com/tiobe-index/)发布2022年2月编程语言排名情况，如下图：

![](../../assets/6249273cbb97550f.png)


在这期排名中，Go上升到第11位，相较于2021年年底各大编程语言的最终排名以及2021年2月份的同比排名都上升了2位。Go语言位次的提升在我的预料之中。TIOBE在1月份发布的[2021年年终编程语言排行榜](https://mp.weixin.qq.com/s/5g7T7VP8Xj-IrJhZKt9Ovw)配文中也认为：除了Swift和Go之外，尚不会有新的编程语言能迅速进入前3名甚至前5名，这也在一定程度上证明了对Go发展趋势的看好。

在本专栏的第一讲[“前世今生：你不得不了解的Go的历史和现状”](https://time.geekbang.org/column/article/426282)一文中，我曾提到过：**绝大多数主流编程语言将在其诞生后的第15至第20年间大步前进**。按照这个编程语言的一般规律，已经迈过开源第12个年头的Go很可能将进入自己的黄金5-10年。而2022年很大可能会成为Go语言黄金5-10年的起点，并且其标志只能是Go泛型语法的落地。

按照Go语言的调性，在语法层面上，Go在加入泛型后很难再有大的改变了，错误处理是最后一个硬骨头，也许在泛型引入后，Go核心团队能有新的解决思路。剩下的就是对Go编译器、运行时层、标准库以及工具链的不断的打磨与优化了。到时候，我们就坐收这些优化所带来的红利即可。

学习Go语言10+年的我，很庆幸也很骄傲当初做出了正确的选择。在Go即将迎来黄金十年的历史时刻，希望各位Gopher都能在Go语言之路上走的更远并兑现个人价值。

**《Go语言第一课》的结束不是Go语言学习的终点，而是深入和实践Go的起点！**

![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/c4a1500def8561d3.png)


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


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论