---
title: GopherChina2017以讲师身份参会感悟
url: https://tonybai.com/2017/04/18/my-experience-of-gopherchina-2017-as-a-speaker/
published: '2017-04-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# GopherChina2017以讲师身份参会感悟

时光荏苒。2016年[北京GopherChina大会的情形](http://tonybai.com/2016/04/18/my-experience-of-gopherchina2016/)还历历在目，[2017年上海GopherChina大会](https://github.com/gopherchina/conference/tree/master/2017)又如约而至。

![img{512x368}](../../assets/a8fff44d90537e0a.jpg)


### 一、印象

这是我连续第二年参加[AstaXie](http://github.com/astaxie/)组织举办的[GopherChina大会](http://www.gopherchina.org/)。而且不同于去年的是，这次我是以讲师身份参与的。虽然大会地点不同，我的角色不同，但不变的是和广大Gophers一样的对[Go语言](http://tonybai.com/tag/go)的极大热情。

这也是第三届GopherChina大会。随着[Go语言自身的快速演进](http://tonybai.com/2017/02/03/some-changes-in-go-1-8/)以及Go在国内各个行业应用的快速增长，GopherChina大会在大中华区的影响力与日俱增：既得到了更多圈内赞助商的赞助，也得到了Gophers们的极大关注。有好多Gophers都是GopherChina大会的连续参加者，有些Gopher甚至连续参加了三届，我个人就看到了好多去年在北京大会上遇到的Gophers。这让能容纳近1500名观众的主会场又近乎爆满。举办和参加这样级别的技术大会，无论是对于主办方还是观众都是一种考验。索性的是，在谢大和相关工作人员的不懈努力之下，两天的大会举办的是很是成功，大会紧凑而有序。并且在第一天晚上举办的技术Party上，大胡子[Dave Cheney](https://dave.cheney.net/)还为我们带来了[“Gopher puzzlers”](http://talks.godoc.org/github.com/davecheney/presentations/gopher-puzzlers.slide#1)。这让技术party的气氛一下达到了高潮。

### 二、选题考量

由于本次是以讲师身份参加的大会，因此这里就不打算像去年那样对其他讲师以及其presentation进行点评了（若要看点评，可以移步到知乎上小伙伴开的[贴子](https://www.zhihu.com/question/58539818)）。这里我主要来说说我这次参会的选题以及个人对于类似GopherChina这样的技术大会应该讲些什么的理解。

年初，谢大在征集GopherChina的topic的时候问我是否愿意在今年的GopherChina大会上做分享？说实话我非常想去分享，自己也是一个爱分享之人。但是分享什么topic的确是一个问题。自己[研究Go较早](http://tonybai.com/2012/08/08/why-not-go/)，但一直没有全职Go，直到去年才开始成为full-time Go。而自己对GopherChina这类技术大会分享的主题也是有自己的想法的，那就是希望大会能像美国丹佛举办的[gophercon](https://www.gophercon.com/)大会一样，多一些关于Go语言本身的Topic。于是我就有了自己来分享一个关于Go语言自身的topic的想法，和谢大做了沟通后得到了谢大的支持。下面的topic初步描述反映了我当时关于slide的思路规划：

*“2016年Go语言问鼎TIOBE编程语言排行榜的年度语言，证明了Go语言在全世界范围内的蓬勃发展之势，将来会有越来越多的开发人员加入到Gophers行列。Go以语法简单、门槛低、上手快著称。但入门后很多人发现要写出地道的、遵循Go思维的代码却是不易。为此，在本次分享中，作者将结合Go team的talk资料、参考和提炼Go标准库以及主流Go开源项目的精华源码风格和惯用法，和大家一起探讨《go coding in go way》之道。” *

关于这样的一个主题，我的心理也是忐忑的，内心中有种赶脚：这个topic有些大啊！在阅读代码、收集和整理资料方面的工作肯定也不少，于是我早早开始了一些资料收集工作。

最初我的topic是偏向于go idiomatic tricks或best practice这个方向的，但随着准备工作的进行，我的头脑中出现了几个疑问：Go诞生这么多年，go idiomatic tricks或best practice已经为人知晓，但很多问题并无定论，我是否可以探讨一下呢？比如：Go的编程思维到底是如何形成的？为什么Go上手易，写出idiomatic的code难呢？我是否能再上一个层次，将go idiomatic tricks或best practice这些冰山上面的具现事物的底层根源找出来呢？这时恰逢国内上映《[降临](https://movie.douban.com/subject/21324900/)》这部美国大片，在电影院看完片后，我思考着影片中的理论核心：“萨丕尔-沃夫假说”并陷入沉思。

于是乎那天晚上我就有了一个关于topic的新的想法，那就是探究Go编程思维背后的东西。但考虑到如何应用编程思维去写go代码，我又阅读了大量go stdlib、kubernetes的代码，试图在这些代码中找到”Go语言编程思维”的应用实例并补充的slide中。这样slide的大体结构就出来了：

```
铺垫
- “萨丕尔-沃夫假说” 作为引子，说明语言与思维的联系
- 针对一个问题的三个语言版本实现，说明编程语言对编程思维的影响
- 提出：语言价值观是语言影响思维的根本(一个示意图阐述模型)
价值观
- Go语言的价值观的形成和价值观内容
- 每种价值观下的语言设计
- 每种价值观主导下的Go编程思维
- 这写Go编程思维的具体运用实例
```


而随着资料准备的深入，逐渐完成了价值观（“全面简单”、“正交组合”和“偏好并发”）与编程思维的内容体系构架（大纲）：

```
Overall Simplicity
- short naming thought
- minimal thought
Orthogonal Composition
- vertical composition thought
- small interface thought
- horizontal composition thought
Preference in Concurrency
- concurrency thought
```


其实在这个资料准备过程，我个人对于Go语言的理解也得到了一定的升华，也更加理解Go的设计者在当初设计语言时做出的一些选择了，并且感觉在面对实际业务问题时、在代码设计时，更加有道可循了。

临近大会，开始写slide。本着present in go way的思路^_^，我首选[go present tool](https://github.com/golang/tools/tree/master/present)支持[.slide格式文档](https://godoc.org/golang.org/x/tools/present)，最后形成了近70 pages的文档。我也感觉页数有些多，并且每次自己彩排一遍都超时。但页面之间逻辑紧扣，武断地删除一页又担心思维跳跃，不便于整体理解，于是硬着头皮将所有内容都保留到了最后。

### 三、Presentation分析

不过实际presenting过程，我依然超时了:(了，整个presentation过程并不顺利。

- 首先是大会的屏幕分辨率似乎有些问题，slide的标题部分根本没有显示出来，这直接导致在座的gopher们看不清我的思路体系，内容让人感觉突兀。就像知乎上ezbuy 翁总的“批评”：“不知为何说变量统计”。
- 其次，不得不承认自己在千人面前speaking，的确紧张紧张紧张啊，尤其是初期，节奏变慢，有些东西没有讲出来，可能会让在座观众感觉思路有跳跃；
- 再次，也许gopher们更关心编程思维下的具体展现，也就是后面的代码部分，但由于前面节奏控制不好，铺垫部分有些多了，占用了大量时间，而导致后面代码部分讲解非常快。
- 再再次，每个会场的gopher的关注点不同，一些gopher可能更喜欢像“微服务实战”这样的一些关于他们目前所遇到问题的解决方案的topic。
- 最后，话题大，不够聚焦。自己准备这类规模大会topic时的经验还是不足。即便讲语言本身，也应该聚焦，就像
[Dave Cheney](https://dave.cheney.net/)或[Francesc Campoy](https://github.com/campoy/)的topic那样，只把一个事情的来龙去脉讲透。

纵观前两届gopherchina大会，国人讲关于Go语言自身层面topic的比例较低，甚至可以用凤毛麟角来形容。更多topic集中在某一业务领域的产品、架构、原理和工程上的实践等。我并不是说这些topic不好，毕竟像GopherChina这样规模的大会需要topic的多样性。只是这一届我要挑战一下自己，虽然结果不是那么理想。

不过，即便被吐槽，其实也没什么，说明和优秀的Go讲师相比，自己的确是有差距的。有差距就努力去弥补呗。如果下一届还有机会分享，我还会分享与Go语言相关的topic，只是要吸取经验，更加聚焦。

### 四、回复吐槽

在这里也回复一下几个gopher的吐槽：

1、”过度吹捧Go”

我真想不出为何这位Gopher能有这种想法。

首先在Gopher大会上，说Go肯定是没问题的。我从来都说Go是一门牛逼的语言，但从来没说Go是最好的语言。

至于所谓的上升到“价值观”的层面，那是对一门编程语言本质上的探讨，是对Go代码设计思维本源的思考，无关吹捧或不吹捧。

任何一门编程语言都有设计者自己背后的理解和选择，都可以上升到价值观。

不过我不能否认的是上升到编程语言价值观这个层次，是需要一定编程语言积累的。所以初学者体会不到也是正常的。慢慢来:)

2、“一些模凝两可的结论”

我不知道这个“吐槽”的原因是否是因为我在talk开始时说了几句谦虚的话。但谦虚并不代表模棱两可。slide中的所有结论都是我思考后的结果，这种东西本身就是主观的，这又不是数学，需要有精密的证明过程。但我在表达这些观点时一直都是坚定的。不知道在这位gopher心中，萨丕尔-沃夫假说是否也算是模棱两可的结论呢？

我的确希望这个topic能作为一次“抛砖引玉”，让广大gopher一起深层次理解语言设计者的初衷以及go设计过程中的一些考虑和认知，能让我们更好的使用Go语言。你可以补充，可以针对某个观点反驳，但你要拿出你的思考过程。如果能说服我，说服大家，那我就认同。这次的分享就是我的思考过程，绝不是模棱两可。

### 小结

最后，十分感谢AstaXie，没有他就没有GopherChina！希望今后的GopherChina大会越办越好，希望Go基金会越做越大！

gopherchina 2017所有讲师的slide已经放出，可以在[这里](https://github.com/gopherchina/conference/tree/master/2017)下载。

## 我个人的talk slide在[这里](https://github.com/bigwhite/talks/blob/master/gopherchina/2017/go-coding-in-go-way-cn.slide)可以下载。

![img{512x368}](../../assets/4b33708d556d6651.jpg)


GopherChina会场周围的美丽景色

![img{512x368}](../../assets/bc0f2fe6ee6aa208.jpg)


与GopherChina mascot合影

![img{512x368}](../../assets/dda16cf5d6552a9f.jpg)


演讲中

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论