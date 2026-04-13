---
title: Gopher的Rust第一课：Rust的那些事儿
url: https://tonybai.com/2024/04/22/gopher-rust-first-lesson-all-about-rust/
published: '2024-04-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher的Rust第一课：Rust的那些事儿

![](../../assets/2d577ea1e3a884b8.png)


[本文永久链接](https://tonybai.com/2024/04/22/gopher-rust-first-lesson-all-about-rust) – https://tonybai.com/2024/04/22/gopher-rust-first-lesson-all-about-rust

要说这两年后端编程语言谁最火，[Rust](https://www.rust-lang.org)说自己第二，没人敢说第一。[Rust连续8年霸榜stackoverflow最受推崇的编程语言](https://survey.stackoverflow.co/2023/#section-admired-and-desired-programming-scripting-and-markup-languages)，甚至被推特之父Jack Dorsey称为“完美的编程语言”：

![](../../assets/e13bc87c1ae3f438.png)


注：最火：仅代表人气最旺，最受欢迎，但并不代表使用者最多。


如果你经常读我的博客，你可能会问：“你不是Go语言布道师吗？怎么也要转Rust了？”其实不然，**学习Rust不是要蹭热度，而是实际开发的需要**。这些年在汽车行业这个赛道上，云端和车端都要兼顾。目前车端基础软件的开发语言主要是C/C++，但内存安全、性能不输C且高可靠的Rust日益受到车载软件开发的青睐，AUTOSAR组织在2022年成立了Rust工作组就是一个重要的信号。并且据我所知，一些国内造车新势力已经或正在将一些Rust开发的中间件或应用放到了量产车或即将量产的车上。

注：

[AUTOSAR (Automotive Open System Architecture)]是一个面向汽车电子系统的开放式软件架构标准，由汽车制造商、零部件供应商和电子供应商共同发起并持续维护的一个全球性标准化组织。

不过，Rust语言在某些领域的崛起确实引发了其他编程语言社区的一些不满和争议。特别是Rust社区的一些人提出“Rewrite Everything in Rust”的观点，让很多编程语言社区，尤其是C++社区十分不安。Go社区则相对更加开放和友好的，主流观点是Go与Rust是可以互补的，两种语言在各自的优势领域发挥作用，通过合作而非对抗的方式，能为开发者提供更好的选择。更多细节，可以参考几年前我曾翻译过的前Go团队产品经理、gohugo的作者Steve Francia联合创作的一篇文章《[Rust vs. Go：为什么强强联合会更好](https://tonybai.com/2021/03/15/rust-vs-go-why-they-are-better-together)》。

也就是说Go依然是我的主力语言，但考虑工作上的需要，我要系统学学Rust了。为了避免“从入门到放弃”，我打算采用边学习边输出的方式，一方面可以督促自己学习，另一方面也希望能和读者及时互动，纠正学习中的错误理解。

我的[Go语言第一课专栏](http://gk.link/a/10AVZ)广受欢迎，其知识结构想必也是大家认可的，这里我就仿照其形式，写一下学习Rust的第一课这个入门系列。

正如我在[Go语言第一课专栏](http://gk.link/a/10AVZ)所说的那样：我一直认为，当你开始接触一门新语言的时候，你一定要去了解它的历史和现状。因为这样，你才能建立起对这门语言的整体认知，了解它未来的走向。而且，也能建立起学习的“安全感”，即相信它能够给你带来足够的价值和收益，更加坚定地学习下去。

在这篇文章中，我就先来了解一下Rust的诞生历史和现状发展，以及它独特的设计哲学。并与Go语言做个简单对比，希望能够让自己和读者对Rust有一个初步的认识。

## 1.1 Rust的历史与现状

### 1.1.1 Rust的诞生与演进

Rust诞生于2006年，这比Google三巨头“密谋”创建Go语言还要早上一年。不过和Go的三位创始人：图灵奖获得者、C语法联合发明人、Unix之父肯·汤普森（Ken Thompson），Plan 9操作系统领导者、UTF-8编码的最初设计者罗伯·派克（Rob Pike），以及Java的HotSpot虚拟机和Chrome浏览器的JavaScript V8引擎的设计者之一罗伯特·格瑞史莫（Robert Griesemer）相比，Rust之父[格雷登·霍尔（Graydon Hoare）](https://graydon2.dreamwidth.org)的身份和江湖地位却没有那么“显赫”。彼时的他只是Mozilla Research的一位加拿大籍的、不到30岁的开发人员：

![](../../assets/3b4586048b708b48.png)


注：Graydon Hoare这个人非常低调，极少在公开场合露面，因此在网络上很难找到他的肖像，上面图中的肖像来自https://www.crunchbase.com/person/graydon-hoare，我这里甚至不能保证这个肖像就是Hoare本人的。


新生代编程语言的诞生都伴随着一段轶事，比如Go语言的创始人们在Google内部经常遇到C++项目漫长的编译时间问题，每当他们启动一个C++项目的编译，都要等很长时间，期间都能喝上几杯咖啡。这让他们深有感触并意识到需要设计一门编译速度更快的新语言，于是Go语言就这样诞生了。和Go语言“喝咖啡，等C++项目编译”类似，Rust的诞生也有一段轶事：

2006年，29岁的Hoare有一天回到温哥华的家中，但他发现电梯坏了，电梯软件崩溃了！他不得不爬楼梯回到位于21层的家中。当他爬上楼梯时，他感到很恼火。他想：“我们做计算机编程的人居然无法制造出一部可以正常工作而不崩溃的电梯！” Hoare知道，许多此类崩溃都是由于程序使用内存的问题造成的。电梯等设备内部的软件通常是用C++或C语言编写的，这些语言以允许程序员编写运行速度非常快且相当紧凑的代码而闻名。问题是这些语言也很容易意外引入内存错误，这些错误会导致崩溃。Hoare决定对此做点什么。于是他打开笔记本电脑，开始设计一种新的计算机语言，他希望这种语言能够编写小而快速的代码，而不会出现内存错误，他将其命名为**Rust**。

这段轶事显然不可考证了。但可以确定的是从2006年开始的若干年里，Hoare创建的个人语言项目Rust并没有真正的用于改善电梯系统的程序，而是在得到了Mozilla的赞助下，用在了持续开发Mozilla的浏览器引擎Servo上了，Mozilla在2010年官宣了该项目，[Hoare在2010年的一次演讲](http://venge.net/graydon/talks/intro-talk-2.pdf)中也第一次介绍了Rust语言：

![](../../assets/89e1dd2c678343d9.png)


Rust开源的第一行代码也是在2010年完成的：

![](../../assets/cfbffbbb94aa9086.png)


此外，最初的Rust编译器是由OCaml实现的，2011年Rust团队使用Rust基于LLVM重新实现了编译器并实现了自举。同年，Rust也有了自己的LOGO，其[设计灵感来自于自行车齿盘](https://bugzilla.mozilla.org/show_bug.cgi?id=680521)：

![](../../assets/ff796d060ad13f71.png)


2012年，[Graydon Hoare接受InfoQ专访](https://www.infoq.com/news/2012/08/Interview-Rust/)，谈及他带领Rust team在Mozilla开发的系统编程语言Rust，包括Rust的特性、Rust相对于C/C++/Java/Go的优势与不同以及Rust的1.0版本发布计划。

但是，就在下一年，即2013年，[Graydon Hoare就因为精力耗尽而辞去了Rust team的领导职务](https://wikitia.com/wiki/Graydon_Hoare)，离开了自己的Rust team，并从此远离了Rust开发。Hoare的离开对Rust team和语言本身来说是一次重大的损失，但Rust社区和团队采取了积极的措施来确保Rust的持续发展和演进。

2014年11月，[Rust官宣了cargo和crates.io](https://blog.rust-lang.org/2014/11/20/Cargo.html)，前者是Rust项目构建管理器，后者则是Rust官方维护的Rust代码的中央包存储库，通过cargo可以轻松构建和发布包到crates.io，或从crates.io上拉取Rust代码的依赖。

2015年5月15日，Rust迎来了一个里程碑的时刻：[Rust 1.0正式发布！](https://blog.rust-lang.org/2015/05/15/Rust-1.0.html) ，这要比[Go发布1.0版本](https://go.dev/blog/go1)迟了3年。但正如官博所说：“1.0版本的发布标志着混乱的结束。此版本是我们对稳定性承诺的正式开始，因此它为构建应用程序和库提供了坚实的基础。从现在开始，重大更改基本上超出了范围（一些小的警告适用，例如编译器错误）”。

Rust 1.0发布后，Rust的版本发布周期与节奏也得以确定下来，即[每6周发布一个稳定版本](https://blog.rust-lang.org/2014/10/30/Stability.html)，按照这个节奏，与Rust 1.0同时发布的还有Rust 1.1 Beta版本。经过六周的测试后，Rust 1.1 Beta转为Rust 1.1稳定版本，同时发布Rust 1.2 Beta版本，依次类推。当然，Rust还有一个nightly build版本，这个版本包含了最新但不稳定的特性。和Go社区和开发人员每年只能high两次相比，Rust开发者和社区更加幸运，每六周就能high一次！

Rust的演进是[基于RFC（Request For Comments）驱动的](https://github.com/rust-lang/rfcs)，并且这一措施是[早于Rust 1.0发布前就基于RFC确定下来的](https://github.com/rust-lang/rfcs/blob/master/text/0002-rfc-process.md)。这与[Go的Proposal process](https://github.com/golang/proposal)类似，但感觉比Go的流程更规范和严谨，当然这与两种语言的治理结构的组成和规则有关。

然而，Rust 1.0的发布只是Rust语言发展的一个新起点，这件事并没有像[Go语言在2009年宣布开源](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)那样获得足够的曝光度并赢得TIOBE年度最佳编程语言的称号。

Rust之后的发展依旧是一波三折，这主要也是缘于Rust当时没有一个“[好爹](https://tonybai.com/2012/10/08/the-new-age-of-programming-language/)”：

![](../../assets/3baecf9bb1b9dfa3.png)



2020年，Rust语言迎来了自己诞生以来的至暗时刻。因新冠疫情全球流行导致的业绩下滑，2020年8月，Mozilla解雇了全球1000名员工中的250名，这其中就包含Servo引擎背后的团队。该事件引起了人们对Rust未来的担忧，因为团队的一些成员是Rust的主要贡献者。

但塞翁失马焉知非福，2021年2月8日，由五家创始公司（AWS、华为、谷歌、微软和Mozilla）共同赞助的独立非营利组织[Rust基金会宣布成立](https://foundation.rust-lang.org/news/2021-02-08-hello-world/)！Rust团队终于有了新家，并且这次除了亲爹Mozilla外，还有四个财大气粗、执IT牛耳的干爹，Rust语言的未来一下变得光明了。

实际上Rust的发展也是如此，从2021年基金会成立至今(2024.4)，Rust取得了长足的发展：语言特性不断增强，编译器性能持续优化，生态系统日渐壮大和完善，增加和完善了对WebAssembly、嵌入式、大数据、区块链、人工智能等领域的支持。下面我们就来说说Rust语言的现状。

### 1.1.2 Rust的现状发展

#### 1.1.2.1 语言排名

虽然Rust热度很高，但在语言排名方面与几乎同期的Go还有一定差距，在2024.3月的TIOBE排名中，Go稳居第8位，而Rust虽然刷新了自己的历史最高排名，但也仅仅排在第17位：

![](../../assets/29d6c44b43f04988.png)



在[Redmonk 2024.1月排名](https://redmonk.com/sogrady/2024/03/08/language-rankings-1-24/)中，Rust位列19位，Go位列12位：

![](../../assets/532c2875c5313532.png)



不过，Rust的热度和社区活跃度甚至要高于Go，究其根源，我认为还是与两个开源语言的治理结构有关，下面是Go和Rust在Reddit论坛上的拥趸数量与在线人数对比（2024.4.6 21:39北京时间）：

![](../../assets/3406517ba921ffd9.png)


如果能持续保持住这样的热度和发展势头，Rust可能在未来几年迅速接近Go的位置，甚至超越也是有很大可能的。

和Go开发人员自称Gopher类似，Rust开发人员自称**Rustacean**，这是一个结合了“Rust”和“Crustacean”（甲壳类）两个词语的组合词。此外，Rust社区还设计了Rust的非官方吉祥物(mascot)：[Ferris](https://www.rustacean.net/)，一只可爱的红色螃蟹，它是由设计师Karen Rustad Tölva在2010年创作的。Ferris象征着Rust语言的安全性、并发性和生产力，同时也代表着Rust社区的活跃和友好。

![](../../assets/57014ceb9b8684f8.png)


crates.io上还有一个名为[ferris-says](https://crates.io/crates/ferris-says)的crate，可以用来打印Ferris吉祥物相关的文字，可以输出像下面这样的ASCII字符拼接出的Ferris形象：

![](../../assets/b94bfca7c27faddc.png)


#### 1.1.2.2 语言采纳

从上面TIOBE的Rust排名曲线来看，Rust在2018 edition和2021 edition前后到达过两个“尖峰”。各大公司以及初创也基本都是在2018 edition之后开始逐渐采纳Rust的。

注：

[关于Rust edition，感兴趣的读者可以先参考Rust官方文档]，在后续学习cargo和Rust项目编译构建的时候，我们还会深入学习和理解edition。

接下来，我们列举一下Rust基金会创始公司以及其他一些知名IT公司和组织对Rust的采纳情况。

- AWS

除了成为Rust基金会创始成员，让大家真正知道了AWS对Rust投入的决心外，真正让大家看到AWS内部大量使用Rust的文章是2022年2月AWS在官博发表的一篇名为[Sustainability with Rust](https://aws.amazon.com/cn/blogs/opensource/sustainability-with-rust/)的文章，这篇文章介绍了Rust在AWS内部基础设施构建上发挥的关键作用，包括用Rust进行Firecracker、AWS Lambda、Amazon S3、 Bottlerocket等开发。这篇文章还引用了一篇2017年发表的论文[Energy Efficiency across Programming Languages](https://greenlab.di.uminho.pt/wp-content/uploads/2017/10/sleFinal.pdf)中的结论，认为Rust在能耗方面的优势是其他语言如Go、Java不能匹敌的，这一定程度上引发了争议，记得Russ Cox在Twitter上海批驳了这篇文章中引用的数据不准确。

- 华为

作为国内以一己之力力抗美帝的通信、IT、手机、汽车等多赛道公司，同样也是拥有处理器、OS、编译器等全技术栈的研发型公司，华为对Rust这一的系统级编程语言尤为青睐。但从公开资料上能看到的东西不多，从[华为可信编程实验室](https://trusted-programming.github.io/)的主页上，我们看到了Rust在华为应用的一些情况。

华为的目标是在全球最大的电信行业设计值得信赖的软件系统。华为正在努力将部分代码库迁移到Rust，它比C/C++更安全且性能更高。为了帮助开发人员完成这个过程，华为利用开源[C2Rust翻译器](https://github.com/immunant/c2rust)直接从C生成Rust代码。

huawei还在内部用Rust开发了一组丰富的内部库，这些库围绕基于actor的并发范式而构建，这样利用Rust语言功能（例如async、await等）简化了异步编程。

Google已将Rust应用到Chromium、Android和FuchsiaOS中，其中Chromium对Rust的支持处于实验阶段。开发者可以使用Rust来开发适用于Android和FuchsiaOS的组件，并且Rust在Android和FuchsiaOS的内部代码中使用的比例相当大，特别是FuchsiaOS，Rust代码已经超过50%。由于内部Cpp代码量较大，2022年10月，谷歌推出了基于开源RISC-V芯片的新型安全操作系统KataOS。Sparrow是KataOS的参考实现，运行在seL4上，几乎完全用Rust编写。该操作系统不是为台式电脑或智能手机设计的，而是为物联网设计的，可用于智能家居设备。目标是为嵌入式硬件或边缘设备构建可验证的安全操作系统，例如捕获图像的网络连接摄像头，这些图像在设备上或云中处理以进行机器学习。在2022年发布的Android 13版本中，谷歌还宣布Android版本13中大约21%的新原生代码（C/C++/Rust）是Rust。AOSP拥有约150万行Rust代码，涵盖了新功能和组件。此外，Android的Rust代码中已发现零内存安全漏洞。为了实现提高Android内部安全性、稳定性和质量的目标，Android团队还表示，Rust应该用在代码库中需要原生代码的任何地方。

- 微软

Microsoft拥有世界上最大的用C/C++编写的代码集合之一，其所有核心产品（例如Windows、Office和Azure云）均使用该代码。2019年，微软开始探索内存安全的编程语言，并试用了Rust。随后，[Rust for Windows Library](https://github.com/microsoft/windows-rs/releases)在GitHub上开源，使Rust开发人员能够顺利使用Windows API。

2022年，微软Azure CTO Mark Russinovich表示，新项目不应再使用C和C++。他建议，Rust应该用于需要非GC语言的项目，以提高安全性和可靠性。

2023年7月，微软宣布[在Windows 11 Insider Preview Build 25905版本中发布了Rust参与编写的Windows内核模块](https://blogs.windows.com/windows-insider/2023/07/12/announcing-windows-11-insider-preview-build-25905)。其中包含了一个 GDI 引擎的实现。

- Meta（前身为Facebook)

虽然不是创始成员，但财大气粗的Meta目前已经是唯一非创始成员的铂金赞助商了。Meta历史上以C++为主，但从2021年开始，Rust便开始大量使用Rust了，并成为Meta支持的服务器端语言列表中的最新成员。

Meta在2021和2022年先后发表过[A brief history of Rust at Facebook](https://engineering.fb.com/2021/04/29/developer-tools/rust/)和[Programming languages endorsed for server-side use at Meta](https://engineering.fb.com/2022/07/27/developer-tools/programming-languages-endorsed-for-server-side-use-at-meta/)详细说明了Rust在Meta内部的应用，感兴趣的读者可以去看看。

- Linux基金会

炒得沸沸扬扬的在Linux Kernel中支持Rust语言终于尘埃落定，[Linux Kernel 6.1版本对Rust提供了支持](https://www.infoq.com/news/2022/12/linux-6-1-rust/)。Rust同时进入Windows、Linux内核，这让Rust的江湖地位得到进一步提升。相信未来，Rust在两大操作系统内核中的代码比例会逐步提升的。

- 其他一些公司对Rust的应用

2024年初，cloudflare公司开源了其内部替代nginx的Rust库[pingora](https://github.com/cloudflare/pingora)，作为业界一家提供互联网基础设施和网络服务的公司，其采用Rust的示范效应也是非常明显的。

influxdb的母公司influxdata在2023年发布了influxdb 3.0版本，该版本采用Rust全面重写。不光是influxdb，诸多新兴时序数据库都采用了Rust技术栈(+[Arrow](https://tonybai.com/2023/06/25/a-guide-of-using-apache-arrow-for-gopher-part1)+[Parquet](https://tonybai.com/2023/07/31/a-guide-of-using-apache-arrow-for-gopher-part6/)+DataFusion)，比如greptimedb、cnosdb、CeresDB等。

字节跳动内部服务大量使用Go，但这几年也有一些Rust爱好者在字节内部布道Rust，并开源了诸如Rust RPC框架[volo](https://github.com/cloudwego/volo)、基于io-uring的Rust async runtime [monoio](https://github.com/bytedance/monoio)等。

埃隆马斯克的xAI在2024年发布的[grok-1大模型](https://github.com/xai-org/grok-1)中，Rust开发的[Qdrant向量数据库](https://github.com/xai-org/qdrant)也发挥了重要作用，也是Rust在AI领域应用迈出的重要一步。

#### 1.1.2.3 应用领域

在Rust官网，我们能看到官方列出的Rust应用的四大领域：

![](../../assets/f90c0740c225b39f.png)


在这四个领域中，Rust都有非常活跃的发展和应用，每个领域都有大量的优秀开源项目，这里无法穷尽，大家可以参考与[awesome-go](https://awesome-go.com/)类似的[awesome-rust项目](https://github.com/rust-unofficial/awesome-rust)查看自己关于领域的开源项目。

#### 1.1.2.4 工作机会与薪酬

从[devjobsscanner统计的2023年的各个编程语言的工作需求](https://www.devjobsscanner.com/blog/top-8-most-demanded-programming-languages/)来看，Rust目前依旧比较小众！

![](../../assets/7af5cc24bf4fa01d.png)


从[stackoverflow 2023薪酬统计](https://survey.stackoverflow.co/2023/#technology-top-paying-technologies)来看，Rust薪资位于中游：

![](../../assets/85306666e64e668d.png)


另外[4 day week的工作数量和薪酬分析](https://4dayweek.io/salary/highest-paying-programming-languages)也印证了上面两点：Rust小众(工作数量相对较少)，薪酬位于中游：

![](../../assets/daf7fe464c559d36.png)


国内Rust的工作数量与国际相同，都处于较少的位置，但国内Rust薪酬数据可能并不低，因为这些Rust岗位基本都在一线大厂，或是拿了较多融资的初创，待遇可能都比较不错。

了解了Rust的诞生和演化历史以及Rust的不错的现状后，我们再来看看Rust的设计哲学。

## 1.2 Rust的设计哲学

**设计哲学之于编程语言，就好比一个人的价值观之于这个人的行为**。因为如果你不认同一个人的价值观，那你其实很难与之持续交往下去，即所谓道不同不相为谋。类似的，如果你不认同一门编程语言的设计哲学，那么大概率你在后续的语言学习中，就会遇到上面提到的这些问题，而且可能会让你失去继续学习的精神动力。因此，在真正开始学习Rust语法和编码之前，我们还需要先来了解一下Rust的设计哲学，等了解完这些之后，你就能更深刻地认识到自己学习Rust的原因了。

### 1.2.1 Rust核心价值观

2019年6月，Rust核心组成员Stephen Klabnik在QCon London发表了一次名为[How Rust Views Tradeoffs](https://www.infoq.com/presentations/rust-tradeoffs/)的演讲，在这次演讲中，他阐述了他个人理解的Rust的核心价值观，**这些价值观是Rust team在做设计取舍时拒绝妥协的点**，它们包括内存安全、执行速度和生产力：

![](../../assets/61402a5d7e445909.png)


按照Stephen Klabnik的说法，这三个核心价值观也是有序的，首先是内存安全，这是Rust最为在乎的立身之本，其次是高性能，最后是生产力。当它们之间出现冲突时，按最高价值观决策！

这其实与Rust官方对Rust的介绍也是一样的：

![](../../assets/9ed0c3eed79e2cc2.png)


官方的Reliable对应的就是内存安全（memory safety)，而efficient则有两层含义，一是运行时的高效，另外一个方面则是构建时的生产力也要保持高水准。

这三个价值观是Rust语言的设计目标，也是Rust语言的特色和优势所在。在失去了Graydon Hoare这个语言之父后，这些价值观也成为了Rust核心团队在判定语言演进方向的根本依据。

- 内存安全

内存安全是**Rust最重要的价值观**，它意味着Rust程序在运行时不会出现内存泄漏(不使用unsafe代码的前提下)、缓冲区溢出、野指针等内存相关的错误。这些错误不仅会导致程序崩溃，还可能导致安全漏洞的产生。Rust通过所有权（ownership）、生命周期（lifetime）和借用（borrowing）等特性，在编译时最大程度地检查出这些错误，从而保证程序的内存安全。

Rust的内存安全机制不仅能够提高程序的稳定性和可靠性，还能够降低开发和维护的难度。由于Rust能够在编译时就检查出内存错误，开发者就不必再花费大量时间和精力去寻找和修复这些错误了。

- 高性能

高性能是Rust的仅次于内存安全的一个核心价值观，Rust语言的设计目标之一就是要成为一种高性能的系统编程语言。Rust通过零成本抽象、移动语义、泛型编程等特性，使得程序能够在运行时达到与C、C++等传统系统编程语言相当的性能。

Rust的高性能机制不仅能够提高程序的运行速度，还能够降低硬件成本。由于Rust能够更好地利用硬件资源，因此在相同的硬件条件和资源开销下，Rust程序的性能通常比其他语言的程序更高。

- 生产力

生产力是Rust的第三个核心价值观，Rust语言的设计目标之一就是要成为一种能够提高开发者生产力的语言。Rust通过包管理器Cargo、智能编辑器支持、丰富的库生态、详实系统的文档等特性，使得开发者能够更轻松地编写、调试和维护Rust程序。

### 1.2.2 Rust的次要价值观

Stephen Klabnik还总结了三条Rust的次要价值观(secondary values)：

![](../../assets/6ec9b85f46a6c196.png)


我们看到：Rust的次要价值观包括ergonomics、compile times和correctness，这三个价值观也是Rust语言的设计目标之一，但和上面的第一级核心价值观相比，它们是可以被妥协掉的。

Ergonomics是指Rust语言的易用性，它是Rust语言的一个重要设计目标。Rust希望通过简单易用的语法和丰富的库生态，使得开发者能够更轻松地编写Rust程序。

Compile Times是指Rust编译器的编译时间。Rust编译器很慢，这是一个问题，Rust team也正在努力优化，但Rust team更关心二进制文件的最终执行速度，而不是让编译器变得更快，这就是Compile Time作为次要价值观的原因。

Correctness是指Rust语言的正确性，Rust真的很在乎你的程序是否正确，Rust希望通过强大的类型系统和静态检查，来尽可能地保证Rust程序的正确性。但Rust不愿意使用完全依赖类型以及证明助手来证明你的代码是正确的。

### 1.2.3 与Go的价值观的对比

我们来对比一下Go官方的对Go的介绍，看一下其隐含的Go价值观(设计哲学)：

![](../../assets/380a62f739fdaeec.png)


在官方对Go的介绍中有三个关键词：Simple、Secure和Scalable。

Simple是Go语言的首要设计原则，Go语言的设计者希望Go语言能够简单易用，使得开发者能够更快地学习和使用Go语言，以快速形成生产能力。Go语言的语法简单易懂，并且去掉了许多其他编程语言中复杂的特性，如类型层次与继承等，使得Go语言更加简洁易学、易读、易用和易维护。

至于Secure，Go语言的设计者希望Go语言能够更加安全可靠，避免许多其他编程语言中常见的安全漏洞。Go语言通过垃圾回收机制来自动管理内存，避免了许多其他编程语言中常见的内存泄漏和缓冲区溢出等问题。同时，Go语言提供了轻量级的goroutine和通道机制，使得开发者能够更加方便地实现并发编程，并且通过数据竞争检测工具，避免了并发编程中常见的数据竞争问题。同时Go语言提供了简单易用的显式错误处理机制，让开发者不遗漏任一处错误处理。

Scalable则体现在Go面向工程、原生内置并发以及崇尚组合的设计哲学上了。 Go语言的设计者希望Go语言能够更好地支持可扩展性，使得Go程序能够更好地适应不同的组织规模、不同的工作负载和硬件环境。Go语言通过简单的语法、基于module的可重现的构建管理、极高的编译速度、高质量的标准库、实用的工具链、强大的内置并发机制以及面向接口编程等特性，使得Go程序更加可扩展，生产力更为高效。

总的来说，Rust更注重安全、底层控制和极致性能，而Go则更加关注简单、安全、扩展性与工程效率。两者在定位和设计哲学上存在区别，但也有一些共同特点，比如都拥有现代的工具链、活跃的社区等。

## 1.3 本章小结

在这篇博文中，我们了解了Rust语言的诞生历程、现状发展，以及它独特的设计哲学。通过与Go语言进行对比，我们可以看出两者在出身、目标和设计理念上的一些差异。

随着软件系统的复杂度不断提高，对安全性、性能和并发的需求也越来越高。作为一门专注于底层系统编程、性能极致化的新语言，Rust正在吸引越来越多开发者的关注。相信通过后面对Rust的全方面的系统学习，我和大家都能够更深入地理解和掌握Rust。

如果你认为Rust的价值观与你的十分匹配，你也认同Rust未来的发展。那就期待下一篇吧，在下一篇中，我们将开始动手学习Rust了!

## 1.4 参考资料

[Rust维基百科](https://en.wikipedia.org/wiki/Rust_(programming_language))– https://en.wikipedia.org/wiki/Rust_(programming_language)[How Rust went from a side project to the world’s most-loved programming language](https://www.technologyreview.com/2023/02/14/1067869/rust-worlds-fastest-growing-programming-language/)– https://www.technologyreview.com/2023/02/14/1067869/rust-worlds-fastest-growing-programming-language/[2022 Review | The adoption of Rust in Business](https://rustmagazine.org/issue-1/2022-review-the-adoption-of-rust-in-business/)– https://rustmagazine.org/issue-1/2022-review-the-adoption-of-rust-in-business/[How Rust Views Tradeoffs](https://www.infoq.com/presentations/rust-tradeoffs/)– https://www.infoq.com/presentations/rust-tradeoffs/[非官方Rust吉祥物Ferris](https://rustacean.net)– https://rustacean.net

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论