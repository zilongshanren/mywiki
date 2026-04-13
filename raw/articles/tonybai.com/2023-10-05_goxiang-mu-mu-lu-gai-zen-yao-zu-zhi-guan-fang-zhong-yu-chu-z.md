---
title: Go项目目录该怎么组织？官方终于出指南了！
url: https://tonybai.com/2023/10/05/the-official-guide-of-organizing-go-project/
published: '2023-10-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go项目目录该怎么组织？官方终于出指南了！

![](../../assets/70825021622abe1f.png)


[本文永久链接](https://tonybai.com/2023/10/05/the-official-guide-of-organizing-go-project) – https://tonybai.com/2023/10/05/the-official-guide-of-organizing-go-project

长久以来，在Go语言进阶的学习和实践之路上，Go项目目录究竟如何布局一直是困扰大家的一个问题，这是因为Go官方针对这个问题迟迟没有给出说法，更没有提供标准供大家参考。仅有Go语言项目技术负责人Russ Cox在一个开源项目的issue中给出了他[关于Go项目结构的最小标准布局的想法](https://github.com/golang-standards/project-layout/issues/117#issuecomment-828503689)。

熟悉我的博客/公众号的读者可能会知道，关于Go项目目录布局，[我在以往文章中曾写过多次](https://tonybai.com/2022/04/28/the-standard-layout-of-go-project)。在我的纸版书[《Go语言精进之路》](https://item.jd.com/13694000.html)、极客时间的专栏[Go语言第一课](http://gk.link/a/10AVZ)以及[Go高级工程师训练营](https://tonybai.com/wp-content/uploads/go-advanced-training-2023-1.png)中，对Go项目目录组织与布局方式也都有过全面系统地说明。

我虽然很努力为大家答疑，提供的建议也很具参考价值，但这仅是我的个人观点，权威性有限，大家依然期待Go官方的说法。

近期Go官方文档集合中新增了一篇名为[“Organizing a Go module”的文档](https://go.dev/doc/modules/layout)，细读之后，我发现这不就是大家期待已久的Go项目目录布局的官方指南吗！

在这篇文章中，我们就来看看这份[官方指南](https://go.dev/doc/modules/layout)，看看官方推荐的Go项目目录布局是什么样子的。

## 1. Go项目的类型

我们知道Go项目(project)一般有两类：library和executable。library是以构建库为目的的Go项目，而executable则是以构建二进制可执行文件为目的的Go项目。

“Organizing a Go module”这篇文档也是按照Go项目类型为Gopher提供项目布局建议的。这篇文档将library类的项目叫作package类，executable类的项目叫作command。下面的示意图展示了“Organizing a Go module”这篇文档的说明顺序：

![](../../assets/10d9bba70c69c2ca.png)


从图中看到，“Organizing a Go module”这篇文档总共给出7种项目的布局建议。接下来，我们就来逐一看一下。

## 2. 官方版Go项目目录布局指南

### 2.1 basic package

我们先从package类开始。最简单的package类的Go项目是**basic package**，下面就是一个basic package类的项目目录布局的示例：

```
project-root-directory/
├── go.mod
├── modname.go
└── modname_test.go
或
project-root-directory/
├── go.mod
├── modname.go
├── modname_test.go
├── auth.go
├── auth_test.go
├── hash.go
└── hash_test.go
```


我们看到basic package类项目非常简单，repo下面**只有一个导出package**，这个package包含一个或多个包源文件。以repo托管在github上为例，如果这个repo的url为github.com/someuser/modname，那么该repo下的module root和导出package的导入路径通常与repo url一致，都为github.com/someuser/modname。

你的代码要依赖该module，直接通过下面import语句便可以将该module导入：

```
import "github.com/someuser/modname"
```


注：本文的Go项目目录布局示例均来自或改自“Organizing a Go module”那篇文档。


### 2.2 basic command

和basic package一样，basic command类项目是以构建可执行二进制程序为目的的Go项目中最简单的一类。下面是basic command类项目的一个示例：

```
project-root-directory/
├── go.mod
└── main.go
或
project-root-directory/
├── go.mod
├── main.go
├── auth.go
├── auth_test.go
├── hash.go
└── hash_test.go
```


从示例我们可以看到，basic command类项目的repo下面只可构建出一个可执行文件，main函数放在main.go中，其他源文件也在repo根目录下，并同样放在main包中。

还是以repo托管在github上为例，如果这个repo的url为github.com/someuser/modname，那么我们可以通过下面命令安装这个command的可执行程序：

```
$go install github.com/someuser/modname@latest
```


### 2.3 package with supporting packages

稍复杂或规模稍大的一些package类项目，会将很多功能分拆到supporting packages中，并且通常项目作者是不希望导出这些supporting packages的，这样这些supporting packages便可以不作为暴露的API的一部分，后续重构和优化起来十分方便，对package的用户也是无感的。这样Go官方建议将这些supporting packages放入[internal目录](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)。

注：internal目录是

[Go 1.4版本]引入的机制，简单来说放在internal中的包是local的，不能导出到module之外，但module下的某些内部代码可以导入internal下的包。如今一般都会将internal放在项目的根目录下，所以项目下的所有代码都可以导入internal下的包。

下面是一个带有supporting packages的package类项目的目录布局示例：

```
project-root-directory/
├── go.mod
├── modname.go
├── modname_test.go
└── internal/
├── auth/
│ ├── auth.go
│ └── auth_test.go
└── hash/
├── hash.go
└── hash_test.go
```


modname.go或modname_test.go可以通过下面导入语句使用internal下面的包：

```
import "github.com/someuser/modname/internal/auth"
```


### 2.4 command with supporting packages

有了package with supporting packages的说明后，再来看command with supporting packages就更简单了，下面是一个示例：

```
project-root-directory/
├── go.mod
├── main.go
└── internal/
├── auth/
│ ├── auth.go
│ └── auth_test.go
└── hash/
├── hash.go
└── hash_test.go
```


和package with supporting packages不同的是，main.go使用的包名为main，这样Go编译器才能将其构建为command。

### 2.5 multiple packages

作为一个库项目，作者可能要暴露不止一个package，可能是多个packages。这不会给Go项目目录布局带来过多复杂性，我们只需多建立几个导出package的目录就ok了。下面是一个multiple packages的示例：

```
project-root-directory/
├── go.mod
├── modname.go
├── modname_test.go
├── auth/
│ ├── auth.go
│ ├── auth_test.go
│ └── token/
│ ├── token.go
│ └── token_test.go
├── hash/
│ ├── hash.go
│ └── hash_test.go
└── internal/
└── trace/
├── trace.go
└── trace_test.go
```


我们看到这个示例在repo(以托管在github.com/user/modname下为例)顶层放置了多个导出包：

```
github.com/user/modname
github.com/user/modname/auth
github.com/user/modname/hash
```


并且顶层的auth目录下还有一个二级的导出包token，其导入路径为：

```
github.com/user/modname/auth/token
```


所有这些导出包的supporting packages还是按惯例放在了internal目录下，比如：github.com/user/modname/internal/trace，这些包是local的，不能被该module之外的代码所依赖。

### 2.6 multiple commands

有multiple packages类型的项目，就会有multiple commands类的项目，下面是一个这类项目的示例：

```
project-root-directory/
├── go.mod
├── prog1/
│ └── main.go
├── prog2/
│ └── main.go
└── internal/
└── trace/
├── trace.go
└── trace_test.go
```


这个示例将每个command放置在一个单独的目录下(比如prog1、prog2等)，supporting packages和之前的建议一样，统一放到internal下面。这样我们可以通过下面步骤来编译command：

```
$go build github.com/someuser/modname/prog1
$go build github.com/someuser/modname/prog2
```


command的用户通过下面步骤可以安装这些命令：

```
$go install github.com/someuser/modname/prog1@latest
$go install github.com/someuser/modname/prog2@latest
```


### 2.7 multiple packages and commands

最后我们来看看最复杂的一种项目类型：multiple packages and commands，即在同一个项目下面，既有多个可导出的packages，又有多个commands。下面是一个此类复杂项目的示例：

```
project-root-directory/
├── go.mod
├── modname.go
├── modname_test.go
├── auth/
│ ├── auth.go
│ ├── auth_test.go
│ └── token/
│ ├── token.go
│ └── token_test.go
├── hash/
│ ├── hash.go
│ └── hash_test.go
├── internal/
│ └── trace/
│ ├── trace.go
│ └── trace_test.go
└── cmd/
├── prog1/
│ └── main.go
└── prog2/
└── main.go
```


我们看到：为了区分导出package和command，这个示例增加了一个专门用来存放command的cmd目录，prog1和prog2两个command都放在这个目录下。这也是Go语言的一个惯例。

这样，这个示例项目既导出了下面的包：

```
github.com/user/modname
github.com/user/modname/auth
github.com/user/modname/hash
```


又包含了两个可安装使用的command，用户按下面步骤安装即可：

```
$go install github.com/someuser/modname/cmd/prog1@latest
$go install github.com/someuser/modname/cmd/prog2@latest
```


## 3. 小结

经过对[“Organizing a Go module”的文档](https://go.dev/doc/modules/layout)这篇Go官方项目目录布局指南的学习，我发现指南中的建议与我个人在以往文章、书和专栏中对Go项目目录布局的建议非常相近，几乎一致，唯独不同的是在pkg目录的使用上。

在multiple packages类型项目中，如果要导出的package非常多，那么项目顶层目下会有大量的目录，这让项目顶层目录显得很“臃肿”，我个人建议将这些导出包统一放置到project-root-directory/pkg下面，这样项目顶层目录就会显得很简洁。

注：无论是“Organizing a Go module”这篇文档中的官方建议，还是我个人对Go项目目录布局的建议，针对的都是

Go项目的基础布局。而像很多Gopher经常问的采用DDD、clean architecture或Hexagonal Architecture(六边形架构)设计的项目的目录布局是一种业务层面的布局，是在基础布局之上进行再设计的，不在本篇的说明范围之内。

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