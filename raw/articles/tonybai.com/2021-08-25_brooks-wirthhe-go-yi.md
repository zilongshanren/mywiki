---
title: Brooks、Wirth和Go[译]
url: https://tonybai.com/2021/08/25/brooks-wirth-and-go/
published: '2021-08-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Brooks、Wirth和Go[译]

![](../../assets/5ac3ec8d08575fd7.png)


[本文永久链接](https://tonybai.com/2021/08/25/brooks-wirth-and-go) – https://tonybai.com/2021/08/25/brooks-wirth-and-go

本文翻译自瑞典程序员Fredrik Holmqvist的博客文章[《Brooks, Wirth and Go》](https://www.fredrikholmqvist.com/posts/brooks-wirth-go/)。

现在是1975年。

程序员们带着[FORTRAN代码](https://fortran-lang.org/)回来了，不过使用的是穿孔卡片的形式。

![](../../assets/0a0074d8a3c2bdb2.jpeg)



这些穿孔卡片被小心翼翼的送进大型机，它们被输入、读取、编译、链接并由计算机执行。当得到“文件名称规格错误”这个结果时，时间已经过去了两个多星期了。在这个阶段，很多人参与了代码的编写与制作并消耗了几周的工作时间。

与此同时，另一个用[Smalltalk](https://en.wikipedia.org/wiki/Smalltalk)和[Interlisp](https://en.wikipedia.org/wiki/Interlisp)编程的工程师正直接在一个控制台中编写并运行他的实现。几秒钟后，他得到了程序的运行结果。接下来，他就在那里修复了错误并完成了这个任务。

上述这两种方法在周转时间上的差异是**四个数量级**。

忘了“10倍程序员(10X programmer)”吧，“10000倍程序员(10000X programmer)”怎么样？

由于现代计算机的硬件已经发展到比将人类送上月球的计算机[快几千亿倍](https://en.wikipedia.org/wiki/Moore%27s_law#/media/File:Moore's_Law_Transistor_Count_1970-2020.png)，这些类型的差异已经急剧缩小了。那些即使是简单计算也要等待几个小时出结果的分时的日子已经一去不复返了。即使是手机也足够强大，可以完成人类在20世纪的所有计算结果。

![](../../assets/9b0b98428a7c303b.png)



**但软件却可能没有这么大的进步**。可以说，自[ALGOL 68](https://en.wikipedia.org/wiki/ALGOL_68)以来，在[解决软件危机](https://en.wikipedia.org/wiki/Software_crisis)方面没有发生什么。也许更糟糕的是，我们（集体）从那个时代的巨头那里学到的东西太少。我想举例说明这些巨头中的两位，以及他们可以教给我们的经验。

### 弗雷德里克·布鲁克斯

![](../../assets/509a288ae70a1690.png)


1964年，IBM宣布了其迄今为止最雄心勃勃的项目：[IBM 360](https://en.wikipedia.org/wiki/IBM_System/360)。该项目由[Gene Amdahl](https://en.wikipedia.org/wiki/Gene_Amdahl)负责设计，[弗雷德里克·布鲁克斯(Frederick Brooks)](https://en.wikipedia.org/wiki/Fred_Brooks)负责管理。

这是世界上第一台真正的可编程大型计算机，开启了计算机可以被重新编程以适应新问题的概念，而不是被更新的模型所取代。该系统结构引入了许多我们今天仍在使用的标准，如[8位字节、32位字(word)等](https://en.wikipedia.org/wiki/IBM_System/360#Technical_description)。

也许更有趣的是这个项目本身。该项目……比最初想象的要昂贵得多。它将预算提高了200倍：从2500万美元提高到50亿美元。要知道，当时作为美国国家核武器研究的[曼哈顿项目](https://en.wikipedia.org/wiki/Manhattan_Project)的预算才仅为20亿美元。

![](../../assets/c7392ab25ded253b.png)


该项目遇到了你能想到的所有开发和管理问题。

多年以后，布鲁克斯决定，回答”为什么软件项目经常出错”这个问题的最好方法是把他的经验和IBM的教训写成一本书。那本书就是现在传说中的[《人月神话》](https://book.douban.com/subject/1102259/)。

![](../../assets/2dadc81667d0f615.jpg)



这也许是关于软件管理的最佳读物之一。其中有一篇文章是“没有银弹(No Silver Bullet)”，它指出：

无论是技术还是管理技术，都没有任何一种可以在十年内保证在生产力、可靠性和简单性方面有哪怕一个数量级的改进。


鉴于与穿孔卡的前辈相比，现代程序员可以很快纠正他们的错误，布鲁克斯认为，剩下的大部分复杂性是问题本身，而意外的复杂性大部分已经解决了。

这并不是说自60年代以来生产力没有提高，实际上恰恰相反。来看看下面的例子：

- 自由/开放源码软件
- 高速硬件
- 通用计算机
- 高性能编译器
- 全球互联网(Internet)

它们一起将我们的整体生产力推到了一个很高的水平。它们也重新引入了许多意外的复杂性，而这些复杂性是我们的前辈们在最初就很努力地消除的。(稍后会有更多关于这方面的内容)

这种将偶然的复杂性降低到最低限度的概念是我们很多问题的关键，没有比[尼克劳斯·沃思(Niklaus Wirth)](https://en.wikipedia.org/wiki/Niklaus_Wirth)更能体现这一原则的了。

### 尼克劳斯·沃思

![](../../assets/f3390980ef67ef38.png)


在创造了[PASCAL](https://en.wikipedia.org/wiki/Pascal_(programming_language))、[MODULA](https://en.wikipedia.org/wiki/Modula)和[MODULA-2](https://en.wikipedia.org/wiki/Modula-2)之后，沃思开始着手开发[OBERON系列语言](https://en.wikipedia.org/wiki/Oberon_(programming_language))，以便在他的Ceres[工作站](https://en.wikipedia.org/wiki/Ceres_(workstation))上建立他自己的Oberon[操作系统](https://en.wikipedia.org/wiki/Oberon_(operating_system))。

如果说沃思在他的职业生涯中完成了很多伟大的事情，那就太轻描淡写了，而[上面给出的例子只是他成就的一小部分](https://en.wikipedia.org/wiki/Niklaus_Wirth#Biography)。

他设法通过遵循一套原则来执行所有这些想法，这些原则可以总结如下：

你必须完全理解你的想法，才能完全实现它。

Oberon语言的出现是出于降低编程语言，特别是针对Modula的复杂性的考虑。这一努力产生了一种非常简洁的语言。Oberon的范围，它的功能和结构的数量，甚至比Pascal小。然而，它的功能却大大增强了。


这个人的结论是：**Pascal太复杂了**。

利用他发现的新力量，他在自己的硬件上从头开始建立了他的操作系统，[这个操作系统仅有12K行源码，占用200K字节的空间资源](http://www.edm2.com/0608/oberon.html)。我们可以对比一下，Mac OSX拥有86M行源码，占用3GB的空间，并且是由世界上最富有的公司之一建立的。现在，也许OSX比Oberon的功能更完整，但肯定不是40000倍的关系。一路走来，有些东西已经失去了。

布鲁克斯的“没有银弹”的概念和沃思的哲学在这里有交集：

你不能通过增加你的语言的复杂性来减少你的问题的复杂性。


你的语言的表面积越大(译：我理解指语言的设计目标越多)，就会有越多的[风沙](http://www.open-std.org/jtc1/sc22/wg21/docs/standards)（译注：风沙指语言的特性）来掩盖其本质。在某些时候，指针已经向前移动到循环开始的地方，因为旧的子集变成了新的，循环再次开始。

这种“少即是多”的概念让我想起了另一位巨人的一句同样性质的话：

有两种构建软件设计的方法：一种是使其简单到明显没有缺陷，另一种是使其复杂到没有明显缺陷 –

[Tony Hoare]

在理论上拒绝沃思的前提，必然会导致走向Hoare观点中的第二个方法。

‘在Objective-C和Swift之间的某个地方，你最终得到了一个来自过去的框架，一个来自未来的框架，以及现在的一个纠结的混乱。


走这条路的代价是什么？

### 束缚我们的石头

#### 培训

- 学习一个新的操作系统，与你的技术绑定。
- 学习一个新的IDE，与你的技术绑定。
- 学习一个新的框架来取代已经工作的框架。
- 学习使用你的旧语言的新版本。

你所有的旧技能都得益于你多年的经验，就像[特修斯之船](https://en.wikipedia.org/wiki/Ship_of_Theseus)一样(译注：特修斯之船是一个思想实验，它提出了一个问题：一个已经更换了所有组件的物体从根本上是否与原物体是相同的)，到了一个时刻，这些技能所占的比重越来越小。经验应该增加价值，而不是减少它。

#### 仓鼠轮(译注：循环往复的重复工作)

- 以前工作的项目在更新后被破坏。
- 你所依赖的其他人以前工作的项目在更新后也会被破坏。
- 筛选几页的文档和StackOverflow的帖子，这些都不再有意义了。
- 不得不跟上新闻，以便预测你的下一个待命的头痛问题。

被迫修复由你的项目、公司、客户或大陆以外的外部力量产生的问题，对任何人都没有帮助，尤其是对你。

- 这个行业是非常难学的。
- 除了厨房里的水槽，什么都有，这不是一个介绍新人的好方法。
- 花在学习工具上的时间本可以用来了解这个项目或学习一般的技能以延续到下一个项目。

你所碰到的大多数后辈都被压倒了，感到困惑，并有压力要跟上不断变化的皇帝的衣服层。

裁缝被封为所有顾问的守护神，因为尽管他榨取了大量的费用，但他始终无法说服他的客户，让他们恍然大悟，他们的衣服没有皇帝。- Tony Hoare


除了老人和可能的内核开发者之外，整个行业往往没有意识到，忽视或拒绝这一前提。相反，轮子的每一次旋转都会到达它开始的地方，并承诺会有新的开始。

幸运的是，也有例外的情况。这里就是其中之一。

### Go

这种奇妙的、著名的”停留在70年代”的语言，满足了所有必要的条件，避免了大部分（如果不是全部）的问题，并从古老的语言中获得了灵感，但又颇具现代感。

-
一蹴而就

- 单一安装，没有许可证/注册/祭祀仪式。
- 可以在任何东西上运行，即使那东西是一台布满灰尘的旧笔记本电脑。
- 语言（相对而言）容易掌握。
- 直接的过程化编程(procedural programming)，不给自己贴上FP(函数式)和OOP(面向对象)标签。

-
没有IDE的耦合。

- 不需要购买许可证，工程师不会被过期的许可证困扰。
- 不需要重新培训工程师将文本输入文本文件。如果他们有几十年使用一个编辑器的经验，他们就可以使用它。
- 没有解决方案文件或复杂的需要IDE才能工作的构建系统。

-
即时编译为静态二进制文件。

- 不需要在项目编译时坐着什么都不做(译注：编译速度快，几乎无需等待)。
- 不需要为了把一种文本编译成另一种文本而把自己的所有内核旋转到100%。
- 通过运行一个单一的可执行文件进行部署。

-
如果十年前能用，现在也能用。

- 停留在70年代意味着自喇叭裤以来就没有突破性的变化。
- 阳光下的一切都包含在自带电池的标准库中。
- 每一行代码都是可检查的，没有闭源库。


它是由[Ken Thompson、Rob Pike和Robert Griesemer](https://www.imooc.com/read/87/article/2320)（沃思的一个学生）设计的。该语言的[入门书籍](http://www.gopl.io)是由[Brian Kernighan撰写](https://en.wikipedia.org/wiki/Brian_Kernighan)的。很明显，这种语言是C语言的精神继承者。

![](../../assets/38bc53df3f7714f6.png)



距离我第一次使用Go已经两年了，我想不出有什么比它更适合通用的软件开发了，尤其是在尊重自己和他人的时间方面。它是为数不多的可以让我自由编程的语言之一，而不需要向互联网咨询，也不需要向在这方面有更多经验的人催促那些应该是不言自明的事情。它没有那么多的魔力，没有那么多的隐藏，这就产生了更多更大的清晰性。没有惊喜，”**它只是能工作**“。

这并不是说每个人都有这种感觉，恰恰相反。[批评是很多的](https://github.com/ksimka/go-is-not-good)。关于Go缺失功能的讨论（比如，[缺乏泛型](https://blog.golang.org/generics-proposal)）已经持续了很多年（到现在已经超过十年了），我只能假设在不可预见的未来还会继续下去。

在这期间，我敦促你去试试这门语言。也许你会喜欢上它。

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