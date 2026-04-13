---
title: Go语言第一课FAQ
url: https://tonybai.com/go-course-faq/
published: '2021-10-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言第一课FAQ

![](../../assets/cb810a9e4f350d20.png)


[本文永久链接](https://tonybai.com/go-course-faq) – https://tonybai.com/go-course-faq

[《Go语言第一课》](http://gk.link/a/10AVZ)专栏正式上线后收到了很多读者的留言反馈，很多留言中的问题显然都是大家认真思考过提出的，在专栏后台我也尽可能地做出认真细致的回答。这些问题以及我的回答也算是我和专栏学习者基于专栏的二次创作，于是我有了将这些问题作为FAQ集中记录起来的想法，这就是这篇文章的由来。

**本页面内容将持续更新**！请持续关注[本FAQ永久链接](https://tonybai.com/go-course-faq) – https://tonybai.com/go-course-faq。

## 一. 本人相关

- 关于音频中带有地方特色的口音^_^

这也是我第一次录带有音频的专栏，虽然音频老师给与了多次耐心的讲解，但毕竟不是专业的，在音频技巧方面还有提高空间。

有些童鞋听出了我的地方特色的口音，这个我得承认，而且这个不是短期能修正的^_^。我是辽宁人，辽宁一些地区的地方特色口音就是平翘舌界限不清晰，这里还希望大家海涵。

## 二. Go专栏

- 为什么要出这个Go专栏？

为此，我特意写了一篇简短的文章，叙述了[这门Go专栏诞生幕后的那些事](https://tonybai.com/2021/10/25/the-things-behind-the-first-lesson-of-go-language)，感兴趣的朋友可以去看看。

- 专栏的更新节奏

根据极客时间要求，专栏每周更新三篇。希望我能保持生产力，争取不断更，压力山大啊！

- 是否有针对该专栏的交流群

目前暂没有。作者精力有限，能力有限，不适合维护这样的一个群，希望大家体谅。欢迎大家在专栏积极留言，我会认真解答大家问题的。

- 阅读完该专栏，我是否可以得到地道的Go代码编写风格、优雅的Go编程姿势呢？

虽然这门课的定位是入门课，而并非进阶课，但我在课程讲解以及Go示例代码中都会尽力以native的Go代码去呈现。并且课程讲解穿插着一些关于Go编码的最佳实践建议，希望大家在阅读后能有收获。

btw，要写出native 的Go代码，一定要多读高质量Go代码，Go标准库是一个最好的选择。俗话说：”熟读唐诗三百首，不会作诗也会吟”，多读高质量代码，与此有异曲同工之妙。

- 专栏讲解使用的是Go最新稳定版本吗？

[专栏写作开始于Go 1.17正式发布之前](https://tonybai.com/2021/10/25/the-things-behind-the-first-lesson-of-go-language)，因此早期的一些篇章使用的可能是[Go 1.16.x版本](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)，后期使用的几乎都是最新的[Go 1.17.x](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)。即便有一些引用的标准库或运行时的代码是Go 1.17之前的某个版本的，我这里也可以保证这些代码的引用仅是为了说明某个具体知识点，不会影响到大家的理解。

一个可能影响大家实践的问题就是从Go 1.17版本开始，go get不再用于安装某个Go版本或工具，我们要用Go install。Go install命令在之前的版本中几乎被弱化到“基本不用”的尴尬境地，其角色都被go get的光环所掩盖。

但从Go 1.17开始，Go install又恢复了其本职工作。

- 老师你好，我想咨询个问题，在听您课的过程中还可以和哪些资料一起参考学习，学习进度可能快些的。

如果富有余力，可以采用“同主题阅读”方法，即确定一个主题，可以以专栏某一讲为主题，然后找几本相关内容的书籍同时阅读，这样可以对这个主题有更深入的了解和认识。建议看一下Go语言的规范、《Go程序设计语言》这样的权威资料。

如果想加快学习和理解的节奏，建议通过预习方式来进行。本专栏的大纲已经公开，可根据大量中的题目，预习一下后续几节课的

内容，带着问题去阅读专栏，可能学习效果更好。

- 专栏课程相关源码从哪里可以下载到？

下面为专栏源码专用仓库地址：

[github仓库](https://github.com/bigwhite/publication/tree/master/column/timegeek/go-first-course) – https://github.com/bigwhite/publication/tree/master/column/timegeek/go-first-course

[码云仓库](https://gitee.com/bigwhite/publication/tree/master/column/timegeek/go-first-course) -https://gitee.com/bigwhite/publication/tree/master/column/timegeek/go-first-course

## 三. 入坑Go与Go前景

- 什么样的人适合学Go语言？

Go设计之初，其目标是成为一门通用的系统编程语言。这一目标基本上就将Go划分到后端编程语言行列。虽然Go社区在前端、移动端编程的支持上面都做了很多尝试，比如：Gopherjs项目以及Go支持编译为webassembly来应对前端开发，再比如Gomobile项目（https://pkg.go.dev/Golang.org/x/mobile）让Go也可以在移动端编程占有一席之地，但这么多年下来，Go的主力战场还是云原生基础设施、中间件、web/api服务、微服务、命令行应用等等。因此如果你的目标与这些领域重合，那么Go是一个很有竞争力的选择。

- 请问中小公司中的Go语言技术栈的岗位多吗？

Go是生产力与执行效率两方面都有突出表现的语言。这两方面都能给中小公司省下不少money。一线城市接纳新语言的开发者较多，招聘也不再是问题了。因此我觉得一线城市应该不少，这方面具体数据还得看招聘网站。二三线城市这些年Go也在拓展地盘。在我地处的东北地区，越来越多小公司选用了Go，趋势是好的。

- 希望老师能说一下Java和Go的区别？

这是很大的话题，也是一个极容易“引战”的话题。

看待这个问题有多种维度，比如从语言语法、生产力、性能、社区活跃度，生态成熟度、发展前景等等。

语言语法见仁见智，java是不折不扣的面向对象编程语言，就像“java编程思想”一书中说：“一切都是对象”。而Go是传统的命令式编程语言，按照Go语言family图谱，它的先祖来自C、Pascal、Newsqueak等。语法简单，但谈不上“领先”，就像很多人说的在最近10年出品的编程语言中，Go的语法显得有些“土气”，我更喜欢称之为朴实无华。很多人就像我，就是喜欢这种朴实。虽然朴实，但Go的表达力并不差哦。

在生产力方面，目前来看Go是要高于java的。

性能方面，同资源消耗下，Go也是要高于java的。另外一点就是即便是新手写Go，性能也不会很差。

社区活跃度方面，两者都是主流语言，java诞生年头多，且是目前企业应用领域的第一语言，其社区自然更好一些。生态成熟度也是如此，现在很难找到一个领域没有java的开源实现。实话说，Go在这方面规模还不及java，但是增长速度要更快。

至于，发展前景，两者都是自己擅长领域的佼佼者，都有不错的前景。Go由于处于成长期，蓝海属性更强一些。

- Go在机器学习算法包括工程这一块前景如何？

这个要实话实说。在机器学习领域，python是当之无愧的老大。但python也有自己的瓶颈，主要是性能相较于静态语言有数量级差距。各个编程语言也都试图争抢python在机器学习领域的份额，包括julia、c++、rust，Go也不例外。但与在云原生领域的投入相比，Go社区在机器学习算法库方向上的投入还不够，但也有一些成果，比较知名的项目包括[Gonum](https://github.com/Gonum/Gonum)、[GorGonia](https://github.com/GorGonia/GorGonia)、[onnx-Go](https://github.com/owulveryck/onnx-Go)等。在帮助构建机器学习/深度学习平台层面上，Go也发挥了很大的作用，比如：kubeflow的部分实现。

机器学习算法上，python已经形成一家独大之势，其他语言，包括Go都会在自己擅长的领域一起助力机器学习的发展了。

- Go在区块链方向应用广吗？

Go在区块链领域应用应该很多啊，至少区块链刚刚起步时，很多都是用Go开发的。比如联盟链fabric。以太坊已经足够Gopher学习好长时间了。另外像ipfs、filecoin等项目虽然不是典型区块链项目，但很多技术点都很相似，也可以了解一下。

- 为什么那些跟云相关的项目，比如docker k8s等项目都选择用Go来开发？

Docker开发团队是最早接纳Go语言的一批创业团队，2013年docker团队的工程师在一次Go分享中提到过选择Go的5个理由：静态编译、语言中立(neutral)、有docker团队所需的所有feature、完整的开发环境、对多cpu架构的原生支持。具体可以看一下[“Docker and Go: why did we decide to write Docker in Go?”](https://www.slideshare.net/jpetazzo/docker-and-go-why-did-we-decide-to-write-docker-in-go)。

至于k8s，k8s原本就是google borg的开源实现，go是google当时的新兴语言。而k8s最初的开发主力都是google的，于是选择go也就不奇怪了。

此外，CNCF聚集了以k8s为首的一大批Go语言实现的云基础设施相关项目，这种示范作用也鼓舞了更多云相关项目使用Go开发。

## 四. Go的历史与哲学

- 有人吐槽 Go 核心人员不想做的东西，就是 Less is more，自己想做就是各种哲学，这个问题，老师怎么看？

Go语言的简单或者说功能特性少，的确来自于less is more的理念。保持一门小语言，让语言更容易学习与理解。同时每个特性都是经过精心打磨与实现，不能再少了。上周我看了[Rob Pike最新一期的talk](https://tonybai.com/2021/10/06/the-go-programming-language-and-environment)，他还在说 “Go语言中变量声明的方式有些多了”，这也是我在实际编码过程中的体会。如果重新来过，我想Rob Pike会更彻底的执行less is more，将变量声明方式再减少一种。所以说，特性少不是不想做，而是经过深思熟虑，那个特性的确没必要加入到语言中。

- Go的异常处理，使用起来简单，但是不方便，请问老师这是在践行Go的简单设计哲学吗？

从Go设计者的初衷来看(https://golang.google.cn/doc/faq#exceptions)，Go没有采用像java那样的结构化异常处理的确是出于对“简单”原则的考虑。

在java中错误处理与真正的“异常”是混杂在Try-catch机制中的，并没有明显的界限，无论是错误还是异常，一旦throw，方法的调用者就得负责处理它。

但在Go中，错误处理与真正的异常处理是严格分开的，也就是说**不要将panic掺和到错误处理中**。

错误处理是常态，Go中只有错误是返回给上层的。一旦出现panic，这意味着整个程序处于即将崩溃的状态，返回给上层几乎也是“无济于事”，所以在Go中，一个常见的api设计思路是：**不要向外部抛出panic（don’t panic!）**。如果api中存在panic的可能性，那么api自己要负责处理panic，并通过error将状态返回给上层。如果api无法处理panic，那程序就很大可能是要崩溃了，这种panic多是因为程序bug导致的。

- Go的统一代码有利的地方是：保证了开发者的编码风格是一致的，增加了代码的可读性。但这会不会对一些高手来说是一个限制呢？

Go面向工程的设计哲学鼓励复杂软件开发的大协作，Go不鼓励“奇技淫巧”，在Go中做一件事一般只有一种方法。所以我们看到的高手编写的开源项目或是标准库，代码绝大多数都是很容易读懂的。

- 什么是Go的自举？

和很多主流语言一样，Go语言编译器最初都是由C语言和汇编语言实现的。C语言和汇编实现的Go编译器(记作A)用来编译Go源文件。那么问题来了？是否可以用Go语言自身实现一个Go编译器B，用编译器A来编译Go编译器B工程的源码并链接成最终的Go编译器B呢？这就是Go核心团队在Go 1.5版本时做的事情。

他们将绝大多数原来用C和汇编编写的Go编译器以及运行时实现改为使用Go语言编写，并用Go 1.4.x编译器(C与汇编实现的，相当于A)编译出Go 1.5编译器。这样自[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)开始，Go编译器就是用Go语言实现的了，这就是所谓的自举。即用要编译的目标编程语言(Go语言)编写其（Go）编译器。

这之后，Go核心团队基本就告别C代码了，可以专心写Go代码了。这可以让Go核心团队积累更为丰富的Go语言编码经验，也算是一种“吃狗粮”。同时Go语言自身就是站在C语言等的肩膀上，修正了C语言等的缺陷并加入创新机制而形成的，用Go编码效率高，还可避面C语言的很多坑。

在这个基础上，使用Go语言实现编译器和runtime还利于Go编译器以及运行时的优化，Go 1.5及后续版本GC延迟大幅降低以及性能的大幅提升都说明了这一点。这就是自举的重要之处。

- 文中提到的正交独立是什么意思？不是很理解？

正交(orthogonality)是从几何学中引入的术语，如果两条线以直角相交，如图形上的轴线，就是正交的。如果说两个事物是正交的，那么我们说

这两个事物是独立且解耦的，一个事物的变化不影响另外一个事物。

我们经常用“正交”来评价一个系统的设计，比如在一个设计良好的系统中，数据库代码将与用户界面正交：你可以在不影响数据库的情况下，独立进行界面的演进。

编程语言的语法元素间也存在着正交的情况，比如文中提到的类型定义与方法是正交的。这意味着一个类型可以有方法，也可以没有方法。而方法本质上接收类型作为其第一个参数的函数而已(具体参考第24讲)。

在Go语言中，正交的语法还有一些，比如接口就与Go语言其他部分是正交的。

但正交的两个语法特性组合起来可以实现其它特性，这也是我们在一个系统中经常做的事情。

[《程序员修炼之道 – 从小工到专家》](https://book.douban.com/subject/5387402/)一书中对正交的概念有详细的讲解，可以阅读一下。

## 五. Go开发环境安装

- 关于gotip版本和beta版本

很多初学者不知道gotip版本的存在，gotip指代就是目前Go核心团队正在积极开发的项目最新提交版本，因此gotip时刻在变化。当我们通过go get/Go install(Go 1.17及以后版本)方式安装go-tip版本时，go get其实也是下载Go项目最新源码，然后编译这份源码。如果某个Go核心开发者提交一次代码恰好导致Go tip源码编译不过去，而你下载的恰恰是这个时刻的Go tip源码，那你的Go tip安装自然就会因build失败而失败。这也是我提到的gotip版本不是每次都能安装成功的原因。

beta版本是大版本发布之前的公测版。比如发布go 1.17正式版之前，go团队会发布几个beta版本供大家体验并提bug。注意：beta版也是不稳定版本，不要用来编译上生产的应用

- Go env里面的配置项究竟是存储在哪儿的？网上有说是生成Go 命令（Go语言的的编译工具）时，直接包含在其中了，也有说是在一个和用户相关的配置文件夹里面，还有的说是来自系统环境变量，那这三种来源的优先级是怎么样的？

Go env的确会综合多个数据源。优先级最高的是用户级环境变量。以linux为例，你的用户下的.profile文件中的环境变量优先级最高。然后是系统级环境变量（但我们很少在linux下用系统级环境变量），最后是Go自带的默认值。

## 六. Go程序构建

- 如何import自己在本地创建的module，在这个module还没有发布到GitHub的情况下？

go module机制在您提到的工作场景下目前的体验做的还不够好。在Go 1.17版本及之前版本的解决方法是使用go mod的replace指示符(directive)。假如你的module a要import的module b将发布到github.com/user/b中，那么你可以手动在module的go.mod中的require块中手工加上一条：

```
require github.com/user/b v1.0.0
```


注意v1.0.0这个版本号是一个临时的版本号。

然后在module a的go.mod中使用replace将上面对module b的require替换为本地的module b:

```
replace github.com/user/b v1.0.0 => module b本地路径
```


这样Go命令就会使用你本地正在开发、尚未提交github的module b了。

- Go应用项目源码还需要放在gopath的src下么？

go module与gopath的一个重要区别就是可以将项目放在任意路径下，而无需局限在$GOPATH/src下面。我之所以将一个module放在一个任意路径下，就是故意要与GOPATH模式区分开的。

- go.mod中的module path必须是github.com/user/repo这样的形式么？

专栏例子中使用github.com/user/repo这个样式作为module path是因为多数实用级module多是要上传到github上的。用这种示例便于后续与真实生产接驳。但对于本地开发使用的简单示例程序而言，module path可以任意选用，比如：

```
// go.mod
module demo1
Go 1.17
```


也是ok的。

module path有三个作用，大家可根据需要作出module path的选择：

a) 定位代码仓库位置。如果你的代码要开源到一些公共代码托管站点，或者在组织内部的代码仓库时，module path中要带上仓库的地址，比如github.com/repo/module，这样依赖你的module的其他代码可以找到你的module代码；

b) 如果你的module不在repo的根路径下，那么在module path中还要包含子目录路径。以github.com/etcd-io/etcd这个仓库为例。这个仓库下管理着多个go module。以其子目录raft下面的module为例，这个module的path为：module go.etcd.io/etcd/raft/v3。其中的raft就是子路径。

c) major版本号。如果major>=2，需要在module path中加上major号后缀，就像上面的module go.etcd.io/etcd/raft/v3。

- go get或go mod tidy下载的go module缓存在哪里了？

go mod tidy下载的第三方module一般在$GOPATH[0]/pkg/mod下面。这里的GOPATH[0]指的是GOPATH环境变量设置的多个路径中的第一个路径，比如说：如果GOPATH的设置如下：

```
export GOPATH=path1:path2:path3
```


那么下载的第三方module就会被缓存在path1/pkg/mod下面。

如果你没有设置GOPATH环境变量也没关系，而且这不是必须的步骤。gopath的默认值为你的home路径下的Go文件夹。这样第三方包就在$HOME/Go文件夹的pkg/mod下面。

[Go 1.15版本](https://tonybai.com/2020/10/11/some-changes-in-go-1-15/)开始，Go提供了GOMODCACHE环境变量用于自定义module cache的存放位置。如果没有显式设置GOMODCACHE，那么module cache的默认存储路径依然是$GOPATH[0]/pkg/mod。

- 是否需要深入了解gopath

Go官方有移除gopath的打算。目前这个时间点，学习Go基本不需要了解太多gopath了。

- 有没有推荐的免费好用的国内module proxy服务？

我个人最常用的是下面这个proxy服务：

```
export GOPROXY=https://goproxy.cn,direct
```


其他的几个proxy服务也应该都很好用：

```
export GOPROXY=https://goproxy.io,direct
export GOPROXY=https://mirrors.aliyun.com/goproxy,direct
export GOPROXY=https://goproxy.baidu.com,direct
```


以上代理除了通过环境变量配置外，还可以用go env命令写入，以阿里的module proxy为例：

```
$Go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/
```


- 如何拉取私有go module？

这个属于稍高级一些话题，这门课尚不会涉及。之前写过一篇有关[拉取私有module](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)的文章可以参考。

- 什么是可重现构建(Reproducible Build)？

可重现构建，顾名思义，就是针对同一份go module的源码进行构建，不同人，在不同机器(同一架构，比如都是x86-64)，相同os上，在不同时间点都能得到相同的二进制文件。

- go.mod文件中能表述依赖的module信息吗？go.mod文件中的内容一般不都是依赖的第三方包和版本吗？

在go module机制进入Go之前，也就是gopath构建模式时代，我们谈到的所有依赖都是包与包的版本；但go module引入后，所有的版本信息都绑定在module上，所以你在go.mod中看到的require块中的依赖都是module与module的版本，不再是包。

- Go团队认为“最小版本选择”为Go程序实现持久的和可重现的构建提供了最佳的方案” 这句话能展开讲讲吗？

对开发者而言，更易于理解和预测，就像课程中例子那样，我们根据依赖图可以很容易确定程序构建最终使用的依赖版本。

对Go核心团队来说，更容易实现，据说实现最小选择的代码也就几十行。

更重要的是最小版本选择更容易实现可重现构建。试想一下，如果选择的是最大最新版本，那么针对同一份代码，其依赖包的最新最大版本在不同时刻可能是不同的，那么在不同时刻的构建，产生的最终文件就是不同的。

当然这一切的前提都是基于语义版本规范，对于不符合规范的module，相当于没有遵守契约，这套规则也就失效。这对任何语言来说都是一样的。

- 在包依赖引用那一节，您说的是A和B依赖C的v1.1.0和v1.3.0版本，这种版本依赖很好理解。但是按照上述的V1和V2不同的原则，如果现在B依赖的不是v1.3.0而是v2.3.0，那我现在项目里引用的C到底是哪个版本？

如果B依赖的是C v2.3.0，那么B导入C的语句就是 import c/v2，而A依赖的是v1.1.0，那么A导入c的语句就是import c，这两个是可以共存的啊。于是你会在go.mod中既看到c v1.1.0，也有c/v2 v2.3.0，它们可以理解为两个不同的module。

- 我用ldd看了几个go编译出来的二进制程序都是没有动态链接库的使用。但是，在看其他几个go编译出来的二进制程序时（比如 containerd、ctr)，它们都是用go编写的，但又有引用动态链接库，这是为什么呢？

Go默认是开启CGO_ENABLED的，即CGO_ENABLED=1(可通过go env命令查看)。但编译出来的二进制程序究竟有无动态链接，取决于你的程序使用了什么包。

如果就是一个打印“hello，world”的Go程序，那么你编译出来的将是一个纯静态链接程序，启动时无需动态链接。

如果你依赖了网络包或一些系统包，比如用http包编写了一个web server(见第9讲示例），那么你编译出来的二进制程序将会是一个包含动态>链接的程序。

原因就在于目前的Go标准库中，某些功能具有两份实现，一份是C语言实现的，一份是Go语言实现的。在CGO_ENABLED=1的情况下，Go链接器会链接C语言的版本，于是就有了依赖动态链接库的情况。如果你将CGO_ENABLED置为0，你再重新编译链接，那么Go链接器会使用Go版本的实现，

这样你将得到一个没有动态链接的纯静态二进制程序。

更多关于Go静态编译还是动态编译的内容，可以参考我的[Go进阶专栏](https://www.imooc.com/read/87)中的文章[《与C互操作不是免费的！一文了解cgo的使用成本》](https://www.imooc.com/read/87/article/2475)。

- java有maven，rust有cargo，js有npm并且它们都有集中可访问的repository，为何Go语言没有这样的一个集中包仓库？

Go的确没有，且也是故意这么设计的。很多人提到Go团队故意忽视了软件工业过去20年的积累，但从Go团队角度来看，这却是他们的一种解决安全风险的方案。可以看看Go官博上的这篇文章：[《Go是如何缓解供应链攻击的》](https://tonybai.com/2022/04/02/how-go-mitigates-supply-chain-attacks)。

从2021-2022年来，npm暴露出的一系列安全问题来看，集中库的确也存在各种各样的问题。

- 文中提到“这是因为下划线这种分隔符，在 Go 源文件命名中有特殊作用，这个我们会在以后的讲解中详细说明” 请问老师下划线的特殊作用是用于测试文件(xxx_test.go)吗？我在后续的章节没看到这个特殊作用的讲解(可能是我没有注意到这个细节)？

这位读者真是非常细心！真不好意思，这个他并没有看错。最初考虑将单元测试相关内容放在后面讲解中，后来取消了，于是这块”特殊作用”的讲解就“没能成行”。

这里简单补充一下：在Go中我们针对包（package）编写测试代码。测试代码与包代码放在同一个包目录下，并且Go要求所有测试代码都存放在以*_test.go结尾的文件中。这使Go开发人员一眼就能分辨出哪些文件存放的是包代码，哪些文件存放的是针对该包的测试代码。

执行单元测试时，go test命令会将所有包目录下的*_test.go文件编译成一个临时二进制文件（我们可以通过go test -c显式编译出该文件），并执行该文件，后者将执行各个测试源文件中的名字格式为TestXxx函数所代表的测试用例并输出测试执行结果。

当然go不仅有_test这样的后缀，还有以os、cpu架构名为特殊中缀和后缀的文件，比如：signal_linux_amd64.go(Go runtime包下的文件)。文件名中的linux、amd64用于限制该文件参与编译的os和平台。以signal_linux_amd64.go为例，该文件仅在linux x86-64平台上才会参与编译。

## 七. Go语法

- 什么是Go运行时？

Go 运行时，也称为Go runtime。

它在那里？其本身就是每个Go程序的一部分，它会跟你的源码一起编译并连接到目标程序中。即便你只是写了一个hello world程序，这个程序中也包含了runtime的实现。

它在我的程序中具体负责什么？runtime负责实现Go的垃圾收集、并发、内存堆栈管理以及Go语言的其他关键功能。

它的代码在哪里？它大部分以标准库的形式存放在每个Go发布版的源码中。

- 包的空导入有什么作用？

像下面代码这样的包导入方式被称为“空导入”：

```
import _ "foo"
```


空导入也是导入，意味着我们将依赖foo这个路径下的包。但由于是空导入，我们并**没有显式使用**这个包中的任何语法元素。那么空导入的意义是什么呢？由于依赖foo包，程序初始化的时候会沿着包的依赖链初始化foo包，我们在08里会讲到包的初始化会按照常量->变量->init函数的次序进行。通常实践中空导入意味着期望依赖包的init函数得到执行，这个init函数中有我们需要的逻辑。

- 老师，每个文件的包名怎么命名？根据目录来吗？

包名可以任意命名，没有限制，但社区公认的好的包名通常为一个小写单词。一个目录下仅允许存放一个包。通常一个优秀的实践

是包名与目录名相同。但也有很多项目没有遵守这个约定俗成的规则。

- 专栏中经常提到“字面值”？怎么理解字面值的含义呢？

字面值(literal)就是源码中的一个固定的值，它直接写在源码中，不可变，且不需经过任何计算我们就能从字面上看出其“值”。在编程语言中，通常一个字面值都可以从其字面上大致推断出其类型。另外字面值可以用于初始化变量，也可以作为常量的值。

- 老师，同一个包内有多个源文件的话，这个包是将所有源文件的常量、变量、init函数汇集到一起，然后按常量->变量->init这样的顺序进行初始化，还是按每个源文件走一遍“常量->变量->init”这样的顺序？

我在macbook pro go1.17版本下的实测情况是Go会先按文件传入的顺序，分别初始化每个文件常量与变量，然后再分别调用各个文件中的init函数。比如说：如果一个包pkg1有两个文件file1.go和file2.go，那么实测的初始化顺序就是：“file1中的常量 -> file1中的变量 -> file2中常量 -> file2中变量 -> file1中init函数 -> file2中init函数”。

- 老师，怎么理解“协作式”、“非协作式”调度呢？

协作式指的是大家都按事先定义好的规则来，比如：一个goroutine执行完后，退出，让出p，然后下一个goroutine被调度到p上运行。这样做

的缺点就在于**是否让出p的决定权在goroutine手里**。一旦某个goroutine不主动让出p或执行时间较长，那么后面的goroutine只能等着，没有方法让前者让出p，导致延迟甚至饿死。

而非协作就是由go runtime来决定一个goroutine运行多长时间，如果你不主动让出，对不起，我有手段可以抢占你，把你踢出去，让后面的goroutine进来运行

- Go语言的goroutine与传统的coroutine(协程)是不是一个东西？

传统理解的coroutine一般是面向协作式，而非抢占式。像python中通过yield关键字创建的协程，与主routine之间是在一个线程上实现的切换执行，从设计角度是通过coroutine实现了并发(concurrency)，但其实它们还是串行执行的，不会真正并行(paralellism)，即便在多核处理器上。

基于上面的理解，我们就可以意识到goroutine并非传统意义上的coroutine，是支持抢占的，而且也必须依赖抢占实现runtime对goroutine的调度

。它更像thread，可以绑定不同的cpu核并行执行（如果是在多核处理器上的话）。同时基于goroutine的设计也会一种并发的设计。

而goroutine与thread又不同，goroutine是在用户层(相较于os的内核层）调度的，os并不知道其存在，goroutine的切换相对轻量。而thread是os

来调度的，切换代价更高一些。

所以在专栏中要么直接用goroutine，要么将goroutine称为“轻量级线程”，而不是协程(coroutine)。

- 请教老师，接口类型装箱过程为什么普遍要把原来的值复制一份到data？（除了staticuint64s等特例）直接用原来的值不行吗，还能提升点性

能？

好问题！假设按照你说的，接口类型装箱时中直接用原先的值，那么由于不同类型的原值大小不一，interface类型在runtime中的表示一定是采用(type, ptr)的二元组，而ptr指向的是原值的地址。这样的情况下，看个例子：

```
func foo(i interface{}) {
i.(int) = 8
}
var a int = 6
var i interface{} = a
i.(int) = 7
println(a) // a = 7 这似乎还说得过去。
```


但是如果将i传递给上面的函数foo：

```
foo(i)
```


foo对i的修改将都反映到a上：

println(a) // a = 8

这样依赖就与Go参数传递值拷贝的语义有悖。

- 突然想到一个问题，为什么很多语言都选择默认值传递方式。比如 c，python，go，java 都是值传递。 请教老师默认值传递的好处是什么，为什么这些大佬设计语言时不默认为引用传递。值传递要copy数据不是麻烦了吗？

好问题！引用传递其实本质也是值传递，只是传递的是指针/地址或像切片这样的“描述符”。

- 老师，Go团队为什么要故意把map的遍历次序设置为随机？

这一话题要追溯到Go 1.0版本发布的时候，从[Go 1.0版本的发布文档](https://go.dev/doc/go1)中，我们能找到如下内容：

```
The old language specification did not define the order of iteration for maps, and in practice it differed across hardware platforms. This caused tests that iterated over maps to be fragile and non-portable, with the unpleasant property that a test might always pass on one machine but break on another.
In Go 1, the order in which elements are visited when iterating over a map using a for range statement is defined to be unpredictable, even if the same loop is run multiple times with the same map. Code should not assume that the elements are visited in any particular order.
This change means that code that depends on iteration order is very likely to break early and be fixed long before it becomes a problem. Just as important, it allows the map implementation to ensure better map balancing even when programs are using range loops to select an element from a map.
```


翻译过来，大致意思就是：1.0版本之前的语言规范中没有规定map的迭代次序，从而导致在实践中的一些糟糕的开发运行体验。于是Go团队选

择故意在map中加入随机迭代功能，这样一旦出现开发人员依赖key迭代顺序的错误行为，这一行为导致的问题在开发和测试早期就能被及时发现，而不会出现在生产运行环境中导致更大的危害。

- c语言借助宏定义字面值的形式作为常量类型具有不安全性，这个不安全性怎么理解呢？

这里的不安全性主要指类型安全。

我们需要先说一下什么是类型安全。类型安全是一个计算机科学中的概念，主要指编程语言阻止或防止类型错误的程度水平。比如将一个字符串类型变量传递给一个接受int类型参数的函数时，语言编译器是否能检测出问题并尽早阻止问题发生。

如果你学过C语言，你就知道宏是在预处理阶段仅仅是做的字符串替换。也就是说宏定义的所谓常量就是一个“字符串”，没有携带任何类型信息，即便对一个函数原型为int Foo(int num)的函数进行如下调用：

```
#define NUM "5"
void Foo(int num) {
printf("num = %d\n", num);
}
int main() {
Foo(NUM);
}
```


调用中的NUM在预处理阶段被替换为”5″，但预处理过程也不会有任何报错，因为预处理阶段没有“类型”的概念。

这样问题就被漏到了编译期间。编译器是否能捕捉到这个问题？不一定。在我的gcc上会给出warning：。

```
$gcc testmacro.c
testmacro.c:12:7: warning: incompatible pointer to integer conversion passing 'char [2]' to parameter of type 'int'
[-Wint-conversion]
Foo(NUM);
^~~
testmacro.c:5:15: note: expanded from macro 'NUM'
#define NUM "5"
^~~
testmacro.c:7:14: note: passing argument to parameter 'num' here
void Foo(int num) {
^
1 warning generated.
```


但是如果程序员忽略warning，这部分错误就会留到 程序运行期间。

运行这个例子：

```
$a.out
num = 62984116
```


问题最终还是发生了。

但在Go中，这种问题是不会发生的，任何类型不匹配的问题都会被Go编译器以“错误”论处！

- hmap这个结构中的extra字段， 在key和value都不是指针的情况下，会存储所有的overflow bucket的指针。什么当key和value都不是指针的情况下，会将bucket中的overflow指针全部放到extra字段存储？

在Go项目源码(Go 1.17版本)的 src/cmd/compile/internal/reflectdata/reflect.go中：

```
func MapBucketType(t *types.Type) *types.Type
```


这个函数实现中，我们可以勾勒出一个bucket桶的结构：

```
//伪代码
type bucket struct {
tophash
keys
values
overflow pointer
}
```


不过这个overflow pointer有两种情况：

```
// If keys and elems have no pointers, the map implementation
// can keep a list of overflow pointers on the side so that
// buckets can be marked as having no pointers.
// Arrange for the bucket to have no pointers by changing
// the type of the overflow field to uintptr in this case.
// See comment on hmap.overflow in runtime/map.go.
otyp := types.Types[types.TUNSAFEPTR]
if !elemtype.HasPointers() && !keytype.HasPointers() {
otyp = types.Types[types.TUINTPTR]
}
```


当key和value中都没有指针时，比如map[int]int。此时考虑到gc优化，编译器将overflow的类型设置为uintptr，这样就可以将bucket分配到无需gc扫描的mem span中。

但uintptr是一个整型，无法被GC识别，这样一来overflow 整个uintptr指向的overflow bucket就没有指向它的指针，这样gc就会将overflow bucket视为unreachable的mem块而将其gc掉。为了避免这种情况，hmap中的extra此时就会指向上面这类bucket的overflow bucket，保证key和value中都不含指针时，overflow bucket依旧可以不被gc。

- 为啥说type M map[int]string、type S []string 这种是根据类型字面值定义来新类型呢？ map[int]string 和[]string 也是一种复合类型，感觉并不是字面值？

map[int]string、[]string这种由已知类型组合而形成的类型被称为type literal，中文译为“类型字面值”, 这个是引用自go语法规范中的术语。go spec原文：”A type may also be specified using a type literal, which composes a type from existing types.” (go 1.19版本)

```
TypeLit = ArrayType | StructType | PointerType | FunctionType | InterfaceType |
SliceType | MapType | ChannelType .
```


## 八. Go程序设计

- 专栏中提到的“一动一静共同构成了Go 应用程序的骨架”中的一动一静指的是什么？该如何理解

关于“一动一静”，“动”主要指程序的并发设计层面，如何设计去管理和控制Goroutine。当程序运行起来后，真正“动”的是一个一个Goroutine。而“静”，则是Go源码中的实体以及它们之间的耦合关系。

- Go方法的本质是一个以方法的 receiver 参数作为第一个参数的普通函数函数是第一等公民，那大家都写函数就行了，方法存在的意义是啥呢？

我可以将其转换为另外一个几乎等价的问题：我们知道c++的方法(成员函数)本质就是以编译器插入的一个this指针作为首个参数的普通函数。那么大家为什么不直接用c的函数，非要用面向对象的c++呢？

其实你的问题本质上是一个**编程范式演进的过程**。Go类型+方法(类比于c++的类+方法)和OO范式一样，是一种“封装”概念的实现，即隐藏自身状态，仅提供方法供调用者对其状态进行正确改变操作，防止其他事物对其进行错误的状态改变操作。

## 九. Go标准库

- printf 能格式化字符串，换行就要手动添加 “\n”，println 又不能格式化字符串。我想知道为什么要这样的设计？在看我来这就是特别反人类的设定，Rust 的 println!(“{}”, a); 才是符合直觉的。

这个问题我是这么看的，printf是go提供的标准格式化io的函数，它能实现你所期望的所有功能。与c语言的printf是对等的。但println这个函数你可以看成是一种“语法糖”，它本身就是一个特例，你可以用go doc看看println的manual，println原语义就是使用一种默认的格式输出数据到stdout上。你认同这种默认格式，你就使用println，简化你的代码。否则，你就用printf就好了。

- ListenAndServe的第二个参数为什么要定义成接口类型？如果定义成函数类型，不就可以不用强转，直接传入了吗？

首先http包的ListenAndServe函数的第二个参数较少使用，一般传递为nil。这就意味着默认使用Handler为http包的DefaultServeMux。

其次，将ListenAndServe函数的第二个参数设置为接口类型，就是为了扩展所需的。

如果第二个参数只是一个函数类型，那么那些与http.Server配套的Mux、middleware等就很难实现了。现在的各种Mux、middleware都是基于Handler这个接口类型实现的。

## 十. Go工具链与工程实践

- 谈谈支持Go的VS Code的Copilot插件

copilot插件我还没体验过，如果真的如你所言那么强大，那也是Go语言和Go开发者的一大幸事

## 十一. 其他

- 命令式语言一般是指哪些语言呢？

所谓“命令式语言”是英文imperative languages的一种翻译。命令式的语言的一个特点就是程序员要完成是一件事，需要自己一步一步告诉机器如何做，即把执行步骤用编程语言的语法罗列出来。如今主流的编程语言，如c, c++, java, go, python, ruby等，无论是否是静态语言还是动态语言，无论是否支持面向对象编程，本质上都是命令式语言。

那什么不是命令式语言呢？与命令式语言相对的是**声明式语言**，最常见的就是SQL，它的特点是你只要给出你想要的，语言引擎知道该执行什么步骤。历史上还有一种叫prolog的逻辑编程语言也是声明式的，如果对prolog感兴趣，可以看看我参与翻译的[《七周七语言》](https://book.douban.com/subject/10555435/)一书。

- 对29讲中的一个示例输出结果的疑问

问题详情：

```
eif: (0x10b38c0,0x10e9b30)
err: (0x10eb690,0x10e9b30)
eif = err: true
eface: {_type:0x10b38c0 data:0x10e9b30}
_type: {size:8 ptrdata:0 hash:1156555957 tflag:15 align:8 fieldAlign:8 kind:2 equal:0x10032e0 gcdata:0x10e9a60 str:4946 ptrToThis:58496}
data: bad error
iface: {tab:0x10eb690 data:0x10e9b30}
itab: {inter:0x10b5e20 _type:0x10b38c0 hash:1156555957 _:[0 0 0 0] fun:[17454976]}
inter: {typ:{size:16 ptrdata:16 hash:235953867 tflag:7 align:8 fieldAlign:8 kind:20 equal:0x10034c0 gcdata:0x10d2418 str:3666 ptrToThis:26848} pkgpath:{bytes:<nil>} mhdr:[{name:2592 ityp:43520}]}
_type: {size:8 ptrdata:0 hash:1156555957 tflag:15 align:8 fieldAlign:8 kind:2 equal:0x10032e0 gcdata:0x10e9a60 str:4946 ptrToThis:58496}
fun: [0x10a5780(17454976),]
data: bad error
```


请问为什么data会是bad error不应该是5吗？

解答：

为什么输出bad error而不是5，是因为我们的dumpT函数的实现：

```
func dumpT(dataOfIface unsafe.Pointer) {
var p *T = (*T)(dataOfIface)
fmt.Printf("\t data: %+v\n", *p)
}
```


这里的Printf使用了%+v。

在标准库fmt包的manual（https://pkg.go.dev/fmt）中有，当verb为%v时，如果操作数实现了error接口，那么Printf将会调用这个操作数的Error方法将其转换为字符串。 原文：If an operand implements the error interface, the Error method will be invoked to convert the object to a string.

所以这里输出的是bad error。

可以再举一个简单的例子：

```
package main
import "fmt"
type T int
func (t T) Error() string {
return "bad error"
}
func main() {
var t = T(5)
fmt.Printf("%d\n", t) // 5
fmt.Printf("%v\n", t) // bad error
}
```


感谢 Tony 老师，受益匪浅，解答了自举等各种常见问题。