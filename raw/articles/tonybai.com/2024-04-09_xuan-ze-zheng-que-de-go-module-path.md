---
title: 选择正确的Go Module Path
url: https://tonybai.com/2024/04/09/choose-the-right-go-module-path/
published: '2024-04-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 选择正确的Go Module Path

![](../../assets/882dc830453ee005.png)


[本文永久链接](https://tonybai.com/2024/04/09/choose-the-right-go-module-path) – https://tonybai.com/2024/04/09/choose-the-right-go-module-path

最近我在查看项目代码时，注意到有人在go.mod文件中将module path写为com.example.foo了。根据这个写法，相信屏幕前的读者也可以推断出这位开发人员可能是从Java阵营转到Go的。实际开发中可能有很多开发者会使用类似的内容作为module path，但这显然不是Go的推荐写法或惯用法。

在这篇简短的文章中，我就来介绍一下module path对Go源码构建、包导入路径以及开发协作的影响，以及符合惯例的module path应该是什么样子的。

我们先来复习一下什么是Go module path。

## 1. 什么是module path

在Go语言中，module path（模块路径）是指在Go开发中用来标识和定位模块的唯一字符串，用于指定在远程仓库或本地文件系统中存储模块代码的位置。

module path在go.mod文件中定义，比如下面这个示例：

```
// go.mod
module github.com/user/module
go 1.21.1
```


我们看到：一个典型的模块路径是一个URL格式字符串，可能是类似于github.com/user/module的形式，其中github.com/user/module就是module path。

在Go语言中，模块（module）是一种组织和管理代码的方式，也是Go代码版本管理的基本单元，我们可以在模块路径中包含主版本信息，比如：

```
// go.mod
module github.com/user/module/v2
go 1.21.1
```


这表明该模块为v2版本，与前面的github.com/user/module是不向后兼容的两个模块。模块的使用者可以同时导入这两个不兼容的模块下的包，比如：

```
import (
"github.com/user/module/foo"
foov2 "github.com/user/module/v2/foo"
)
```


那么module path的选取和使用，对Go开发有何影响呢？我们继续向下看。

## 2. module path的影响

### 2.1 指示Go module网络位置

前面提到过，在Go语言中，我们通常使用模块的存储库地址作为模块路径的基础。这样做的好处是，Go编译器可以直接通过模块路径确定模块在网络上的位置，并从指定的位置下载需要的代码。这使得在使用第三方模块时非常方便，开发者只需要指定模块的路径，Go工具链就能够自动处理依赖关系，下载并编译所需的模块代码。

例如，如果一个模块的路径是github.com/user/module，那么Go工具链（尤其是Go编译器)就会认为该模块的代码存储在GitHub上的user用户下的module仓库中。当Go工具链需要引入该模块时，它会根据这个路径通过goproxy或直接去GitHub上下载相应的代码。

这种基于存储库地址的模块路径设计简化了模块的管理和依赖关系的处理，使得在Go项目中使用第三方模块变得更加方便和可靠。

### 2.2 对Go包路径的影响

Go module下的包的导入路径为module path+到包所在目录的相对路径，以module path为github.com/user/module的module下的pkg/foo目录下的包为例，foo包的导入路径为github.com/user/module/pkg/foo。

而如果像本文开头那样，使用com.example.foo作为module path，那么foo包的导入路径就变为了com.example.foo/pkg/foo，这显然难以理解，同时，com.example.foo这样的Java模式的字符串也无法指示go module的网络位置。

### 2.3 对编译的影响

module path对编译的影响体现在两方面：

首先，Go编译时通过module path来查找依赖的模块。如果Go module path不正确或不完整，那么编译可能会失败。非idiomatic的Go module path可能导致编译错误或难以诊断的问题。

其次，module path会影响采用go build默认构建出的二进制文件的名字，比如如果一个module path为github.com/user/mymodule，那么在该module下执行go build（不使用-o命令行标志），默认得到的二进制文件名为mymodule。

但如果module path为com.example.foo，那么得到的二进制文件名就为com.example.foo，这显然不是我们想要的。

### 2.4 对开发者协作的影响

Go模块路径的命名对开发者之间的协作也有着重要的影响，主要体现在两方面：

- 唯一性和命名空间

模块路径应当保持唯一，以避免与其他模块产生冲突。通常情况下，使用域名作为模块路径的一部分可以确保全球唯一性。在团队内部，也可以基于公司或组织的名称来命名模块路径，以确保模块的唯一性。

- 依赖管理

使用清晰、有意义、可以指示位置和版本的模块路径可以帮助开发者更好地管理依赖关系。当其他开发者在引入你的模块时，他们可以通过模块路径来确定正确的依赖版本，以及如何与你的模块进行集成。

## 3. 如何选择一个好的module path

通过上面的秒数，其实我们已经可以勾勒出一个好的module path的画像了。当然这也是Go社区的最佳实践。

通常情况下，module path应该基于模块的存储库地址，并使用简短、易于理解的路径。

就像前面提到的那样，如果你的module存储在GitHub上并可公开，那么module path一般是github.com/user/module。

如果你的module公司内部，不能公开的，那么可以使用一个私有的存储库地址，例如：company.com/dept/go/module。

无论公开的，还是私有的，你都可以定制module path，这方面的方案可以参考我之前编写的有关[定制Go module的拉取方案](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)。

如果是仅在本地使用的日常练习项目，那么Go module path的使用可以宽松一些，可以无需在乎其对go module网络位置、开发者协作的影响，可使用像demo这样的单个词的module path，仅注意下其对包路径和编译结果的影响即可。

## 4. 小结

综上，我们看到：Go module path对Go module网络位置、包路径、编译和开发者协作都有重要影响。遵循Go社区的最佳实践，选择一个好的Go module path可以提高代码可读性和可维护性，并简化多人协作，帮助Go开发者更好地使用Go模块系统。

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
- Gopher Daily – https://gopherdaily.tonybai.com

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论