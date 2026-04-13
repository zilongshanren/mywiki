---
title: Go项目初始化不再困扰你：gonew全方位解析
url: https://tonybai.com/2023/08/11/introduction-to-the-gonew-tool/
published: '2023-08-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go项目初始化不再困扰你：gonew全方位解析

![](../../assets/07e8878a01489f82.png)


[本文永久链接](https://tonybai.com/2023/08/11/introduction-to-the-gonew-tool) – https://tonybai.com/2023/08/11/introduction-to-the-gonew-tool

近日，[Go官博介绍了一个名为gonew的新工具](https://go.dev/blog/gonew)。该工具支持基于go project template clone并创建一个属于你的Go项目。gonew工具的引入大幅简化了Go项目的创建，同时由于对自定义项目模板的支持，也可以提高Go项目的标准化水平。gonew工具刚刚被放入[Go工具项目代码仓库](https://github.com/golang/tools/tree/master/cmd/gonew)，目前还处于实验阶段，后续可能会增加新特性，但当前的核心特性(core functionality)会持续保留。

本文将针对gonew目前的特性做简要说明，以供大家参考。

## 1. 起源

Go team为何要引入gonew这个工具呢？按照[Russ Cox的说法](https://github.com/golang/go/discussions/61669#discussion-5459972)，Go team经常收到一些Go用户关于使用某种”go new”功能的要求，即以某种基本的项目模板来创建一个新Go module。于是Russ Cox私下里编写了一个实现了这类核心功能特性的小工具：rsc.io/tmp/gonew。该工具的逻辑非常简单，主要就是**下载一个模板module，更改其module path，并将其放到本地的一个新目录中**。Russ在google内部宣传该工具后，Google内部的一些团队便定制了一些模板(template)，尤其是ServiceWeaver团队的响应尤为积极。这一切最终让Russ决定引入[golang.org/x/tools/cmd/gonew](https://github.com/golang/tools/tree/master/cmd/gonew)。

我们接下来看看gonew究竟长什么样子，能做什么！

## 2. 安装和使用gonew

### 2.1 安装gonew

我们执行下面命令便可以相当容易的将gonew安装到本地(如果设置了GOPATH，那么该工具会安装到GOPATH/bin下)：

```
$go install golang.org/x/tools/cmd/gonew@latest
go: downloading golang.org/x/tools v0.12.0
go: downloading golang.org/x/mod v0.12.0
```


执行一下gonew：

```
$gonew
usage: gonew srcmod[@version] [dstmod [dir]]
See https://pkg.go.dev/golang.org/x/tools/cmd/gonew.
```


### 2.2 使用gonew创建新项目

下面是用gonew创建新项目的两个典型场景：

- 基于模板创建“同名module”项目

以golang.org/x/example/helloserver模板为例，我们基于该模板通过gonew创建一个新项目：

```
$gonew golang.org/x/example/helloserver
gonew: initialized golang.org/x/example/helloserver in ./helloserver
```


探索一下该项目：

```
$ cd helloserver/
$ ls
LICENSE go.mod server.go
$ git status
fatal: Not a git repository (or any of the parent directories): .git
$ cat go.mod
module golang.org/x/example/helloserver
go 1.19
```


我们发现gonew仅是将helloserver模板项目下载到本地（显然不会包含原模板项目的git仓库目录(.git)），且go module的名字也未被改变。

很多人会问：这样的gonew用法用在什么场景中呢？Russ Cox给出了应用场景：

```
$ gonew book.com/mybook-examples
```


这个用法适用于在本地创建某图书作者的样例代码项目。

- 基于模板创建新module项目

这里我们基于helloserver项目模板创建我们自己的github.com/bigwhite/myhelloserver module项目：

```
$ gonew golang.org/x/example/helloserver github.com/bigwhite/myhelloserver
gonew: initialized github.com/bigwhite/myhelloserver in ./myhelloserver
```


同样探索一下新创建的项目：

```
$ cd myhelloserver/
$ ls
LICENSE go.mod server.go
$ cat go.mod
module github.com/bigwhite/myhelloserver
go 1.19
```


我们看到：和第一种用法不同的是，这次go.mod中的module path被改为我们期望的module path。

这种用法应该是gonew最常用的场景。

根据gonew的命令说明，它还支持基于模板项目的特定版本来创建新项目，并支持指定本地存放新项目的路径，这里就不演示了。

## 3. gonew的项目模板

gonew中提到的项目模板并不神秘，它就是一个go module，这个module具有一些脚手架代码，其存在的目的就是被复用。

google提供了一些模板示例，比如：go team的[hello](https://github.com/golang/example/tree/master/hello)、[hellserver](https://github.com/golang/example/tree/master/helloserver)和[outyet](https://github.com/golang/example/tree/master/outyet)；ServiceWeaver提供的[template](https://github.com/ServiceWeaver/template)等。

在gonew出现前，可能很多组织就是这么做的，会定义一些Go脚手架项目作为模板，供大家创建go新项目时参考。Go社区也有很多相似gonew的开源工具，在[gonew的讨论帖](https://github.com/golang/go/discussions/61669)中，很多人晒了自己的类gonew项目。

有了gonew以后，建立组织级Go项目模板库将会成为提升组织内go项目初始化效率的重要手段，这样做后，组织级go项目标准化程度会得到大幅提升。

## 4. gonew与Go项目标准布局

可能很多Gopher和我一样，在第一眼看到Go官博关于gonew的文章标题时，以为Go team终于官宣了Go项目的标准布局，并基于gonew工具来创建采用标准布局的新项目。可但我深入读下去后，发现并非如此。

gonew并没有规定Go项目标准布局。gonew是开放性，只要是合法的go module项目都可以作为template在创建新项目时使用。这体现了gonew工具的灵活性和可扩展性，至于将来go team是否会定义一系列的“标准布局”模板还是未知数。

关于Go项目标准布局的思考，请参考我的

[极客时间专栏《Go语言第一课》]的第5讲“标准先行：Go项目的布局标准是什么？”。

## 5. 小结

gonew工具简化了Go项目初始创建的复杂度，并且基于一些符合Go最佳实践的项目模板，Go初学者可以分分钟得到符合Go最佳实践的目录布局的Go项目。公司和组织层面也可以通过定义专属Go模板来满足组织和公司的内部需要，提高go新项目的创建效率以及提升Go项目布局的标准化程度。新的Go项目的布局的标准化程度提高后，对组织内CI/CD流水线也会更加友好。

gonew的推出得到了社区的欢迎，社区也反馈gonew对快速启动项目很有帮助并提出了一些扩展建议。Russ Cox也说了：**不排除在Go后续版本中将gonew升级为go new的可能性**。

让我们一起拭目以待吧！

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论