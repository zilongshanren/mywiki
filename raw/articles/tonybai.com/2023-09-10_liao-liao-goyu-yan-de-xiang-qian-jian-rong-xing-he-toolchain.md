---
title: 聊聊Go语言的向前兼容性和toolchain规则
url: https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/
published: '2023-09-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Go语言的向前兼容性和toolchain规则

![](../../assets/56521ec63797c1f1.png)


[本文永久链接](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule) – https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule

Go语言在发展演进过程中一直十分注重向后兼容性(backward compatibility)，在[Go 1.0版本发布](https://go.dev/blog/go1)之初就发布了[Go1兼容性承诺](https://go.dev/doc/go1compat)，简单来说就是保证使用新版本Go(比如[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/))可以正常编译和运行老版本的Go代码(比如使用[Go 1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)语法编写的go代码)，不会出现breaking change([其实也不是绝对的不会出现](https://go.dev/blog/compat))。

但是在Go 1.21版本之前，Go语言在向前兼容性方面却存在一定的不确定性问题。Go 1.21版本对此进行了改进，并引入了go toolchain规则。本文就和大家详细聊聊Go语言的向前兼容性以及Go 1.21中新引入的toolchain的使用规则。

## 1. Go 1.21版本之前的向前兼容性问题

在Go 1.21版本之前，Go module中的go directive用于声明建议的Go版本，但并不强制实施。例如:

```
// go.mod
module demo1
go 1.20
```


上面go.mod文件中的go directive表示建议使用[Go 1.20及以上版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)编译本module代码，但并不强制禁止使用低于1.20版本的Go对module进行编译。你也可以使用[Go 1.19版本](https://tonybai.com/2022/08/22/some-changes-in-go-1-19)，甚至是[Go 1.15版本](https://tonybai.com/2020/10/11/some-changes-in-go-1-15/)编译这个module的代码。

但Go官方对于这种使用低版本(比如L)编译器编译go directive为高版本(比如H)的Go module的结果没有作出任何承诺和保证，**其结果也是不确定的**。

如果你比较幸运，在module中没有使用高版本(从L+1到H)引入go的新语法特性，那么编译是可以通过的。

如果你更加幸运，你module中的代码没有使用到任何从L+1到H版本中带有语法行为变更、bug或安全漏洞的代码，那么编译出的可执行程序运行起来也可以是正常的。

相反，你可能会遇到编译失败、运行失败甚至运行时行为出现breaking change的问题，而这些都是**不确定的**。

有gopher可能会说：我自己的代码可以控制，我可以保证避免掉这些问题。但如果你的module有外部依赖，你能保证你的依赖不存在这种向前兼容性的问题吗！

向前兼容性问题会导致Go开发者的体验不佳！因此，从Go 1.21版本开始，Go团队在向前兼容性方面对Go进行了改善，尽量以确定性代替上述的问题带来的不确定性。

下面我们就来看看Go 1.21版本在向前兼容性方面的策略调整。

## 2. Go 1.21版本后的向前兼容性策略

Go从[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)引入go module，在[go 1.16版本](https://tonybai.com/2021/02/25/some-changes-in-go-1-16)，[go module构建模式](https://go.dev/ref/mod)正式成为默认构建模式，替代了原先的GOPATH构建模式。

通过go module，结合[语义导入版本(semantic import versioning)](https://research.swtch.com/vgo-import)、[最小版本选择(Minimal version selection)](https://research.swtch.com/vgo-mvs)等机制，go build可以实现精确的依赖管控。

Go 1.21版本后的向前兼容性策略的调整就是参考了go module对依赖的管理方法：即**将go版本和go toolchain版本作为一个module的“依赖”来管理**。如果你真正理解了这个，那理解后面那些具体的规则就容易多了！

如果Russ Cox当初设计Go module就想到了今天这个思路，估计就会直接使用go.mod文件中的require语法像管理依赖module那样来管理go version和go toolchain了：

```
// go.mod (假想的)
module demo1
require (
go 1.20.5
toolchain go1.21.1
)
require (
github.com/gomodule/redigo v1.8.5
github.com/google/gops v0.3.19
github.com/panjf2000/ants v1.2.1
)
```


但时间无法倒流，历史不能重来，Russ Cox现在只能使用go directive和toolchain directive来提供对go版本和go工具链的依赖信息：

```
// go.mod
module demo1
go 1.20.5
toolchain 1.21.1
```


同时和使用go get可以改变go.mod的require块中的依赖的版本一样，通过go get也可以修改go.mod中go和toolchain指示的版本：

```
$go get go@1.21.1
$go get toolchain@go1.22.1
```


基于上述策略调整，为解决向前兼容不确定性的问题，Go从1.21版本开始，改变了go.mod中go directive的语义：它不再是建议，而是指定了module最小可用的Go版本。

这样在仅使用本地go工具链的情况下，如果Go编译器版本低于go.mod中的go版本，将无法编译代码：

```
// go.mod
module demo1
go 1.21.1 // 指定最小可用版本为Go 1.21.1
$GOTOOLCHAIN=local go build
go: go.mod requires go >= 1.21.1 (running go 1.21.0; GOTOOLCHAIN=local)
```


细心的读者可能会注意到了，这里我用了一个前提：“在仅使用本地go工具链的情况下(即设置了GOTOOLCHAIN=local)”，在Go 1.21版本之前，我们遇到的都属于这种情况。遇到这种情况后，我们一般的作法是手动下载对应版本的Go工具链(比如这里的go 1.21.1)，然后用新版工具链重新编译。

Go团队考虑到手动管理go工具链带来的体验不佳问题，在Go 1.21版本及以后，go还提供了自动Go工具链管理，如果go发现本地工具链版本低于go module要求的最低go版本，那么go会自动下载高版本的go工具链，缓存到go module cache中(不会覆盖本地安装的go工具链)，并用新下载的go工具链对module进行编译构建：

```
// go.mod
module demo1
go 1.21.1 // 指定最小可用版本为Go 1.21.1
$go build
go: downloading go1.21.1 (darwin/amd64)
```


注：从兼容性方面考虑，如果go.mod中没有显式的用go指示go版本，那么默认go版本为1.16。


对应module有依赖的情况，比如下图：

![](../../assets/54e67bb6ca113a9a.png)


这里要正确编译图中的main module，我们至少需要go 1.21.0版本，这个版本是main所有依赖中version最大的那个。

当然最终选择哪个版本的go工具链对module进行编译，则有一个选择决策的过程。

go module构建模式下，go工具链选择依赖module的版本时有一套机制，比如最小版本选择等，Go 1.21以后，go工具链版本的选择，也有一套类似的逻辑。接下来我们就来简单看一下。

## 3. module依赖的Go toolchain版本的选择过程

我们先来回顾一下go module中依赖module的版本选择机制：最小版本选择(mvs)，下面的图是讲解这个机制时经常引用的图：

![](../../assets/60a3c600b7ad8603.png)



以module C的版本选择为例，A依赖C 1.3，B依赖C 1.4，那么满足应用依赖需求的最小版本就是1.4。如果选择1.3，则不满足B对依赖的要求。

对Go toolchain的选择过程也遵循mvs方法，我们把前面的那个例子拿过来：

![](../../assets/54e67bb6ca113a9a.png)


现在我们帮这个例子选择go toolchain版本。

注：如果go.mod中没有显式用toolchain指示工具链版本，那我们可以认为go.mod中有一个隐含的toolchain指示版本，该版本与go directive指示的版本一致。


上面的例子中对toolchain version的最高要求为module D的go 1.21.0，当startup toolchain(执行的那个go命令的版本)得到这个信息后，就会在当前**可用的toolchain版本列表**中选出满足go 1.21.0的最小版本的go toolchain，然后会有一个叫Go toolchain switches(Go工具链切换)的过程，切换后，选出的新版go toolchain会继续后面的工作(编译和链接)。例如，如果可用的toolchain版本有如下三个：

- go 1.22.7
- go 1.21.3
- go 1.21.5

那么startup toolchain会根据mvs原则选出满足go 1.21.0的最小版本，即go 1.21.3。

这里大家可能会马上问：什么是可用的toolchain版本？别急！接下来我们就来回答这个问题。

## 4. GOTOOLCHAIN环境变量与toolchain版本选择

是否执行自动工具链下载和缓存、Go toolchain switches(Go工具链切换)以及切换的工具链的版本取决于GOTOOLCHAIN环境变量的设置、go.mod中go和toolchain指示的版本。

当go命令捆绑的工具链与module的go.mod的go或工具链版本一样时或更新时，go命令会使用自己的捆绑工具链。例如，当在main module的go.mod包含有go 1.21.0时，如果go命令绑定的工具链是Go 1.21.3版本，那么将继续使用初始toolchain的版本，即Go 1.21.3。

而如果go.mod中的go版本写着go 1.21.9，那么go命令捆绑的工具链版本1.21.3显然不能满足要求，那此时就要看GOTOOLCHAIN环境变量的配置。

GOTOOLCHAIN的设置以及对结果的影响略复杂，下面是GOTOOLCHAIN的多种设置形式以及对toolchain选择的影响说明(以下示例中本地go命令捆绑的工具链版本为Go 1.21.0)：

- \<name>

例如，GOTOOLCHAIN=go1.21.0。go命令将始终运行该特定版本的go工具链。如果本地存在该版本工具链，就使用本地的。如果不存在，会下载、缓存起来并使用。如果go.mod中的工具链版本高于name版本，则停止编译：

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=go1.21.0 go build
go: go.mod requires go >= 1.23.1 (running go 1.21.0; GOTOOLCHAIN=go1.21.0)
```


- \<name>+auto

当GOTOOLCHAIN设置为\<name>+auto时，go命令会根据需要选择并运行较新的Go版本。具体来说，它会查询go.mod文件中的工具链版本和go version。如果go.mod 文件中有toolchain行，且toolchain指示的版本比默认的Go工具链(name)新，那么系统就会调用toolchain指示的工具链版本；反之会使用默认工具链。

当本地不存在决策后的工具链版本时，会自动下载、缓存，并使用该缓存工具链进行后续编译。

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=go1.24.1+auto go build
go: downloading go1.24.1 (darwin/amd64) // 使用name指定工具链，但该工具链本地不存在，于是下载。
$GOTOOLCHAIN=go1.20.1+auto go build
go: downloading go1.23.1 (darwin/amd64) // 使用go.mod中的版本的工具链
```


- \<name>+path

当GOTOOLCHAIN设置为\<name>+path时，go命令会根据需要选择并运行较新的Go版本。具体来说，它会查询go.mod文件中的工具链版本和go version。如果go.mod 文件中有toolchain行，且toolchain指示的版本比默认的Go工具链(name)新，那么系统就会调用toolchain指示的工具链版本；反之会使用默认工具链。当使用\<name>+path时，如果决策得到的工具链版本在PATH路径下没有找到，那么go命令执行过程将终止。

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=go1.24.1+path go build // 使用name指定工具链，但该工具链本地不存在，于是编译停止
go: cannot find "go1.24.1" in PATH
$GOTOOLCHAIN=go1.20.1+path go build // 使用go.mod中的版本的工具链，但该工具链本地不存在，于是编译停止
go: cannot find "go1.23.1" in PATH
```


- auto (等价于 local+auto，这也是默认值)

auto的语义是当go.mod中工具链版本低于go命令捆绑的工具链版本，则使用go命令运行捆绑的工具链；反之，自动下载对应的工具链版本，缓存起来并使用。

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=auto go build
go: downloading go1.23.1 (darwin/amd64)
```


- path (等价于 local+path)

path的语义是当go.mod中工具链版本低于go命令捆绑的工具链版本，则使用go命令运行捆绑的工具链；反之，在PATH中找到满足go.mod中工具链版本的go版本。如果没找到，则会停止编译过程：

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=path go build
go: cannot find "go1.23.1" in PATH
```


- local

当GOTOOLCHAIN设置为local时，go命令总是运行捆绑的 Go 工具链。如果go.mod中工具链版本高于local的版本，则会停止编译过程。

```
$cat go.mod
module demo1
go 1.23.1
toolchain go1.23.1
$GOTOOLCHAIN=local go build
go: go.mod requires go >= 1.23.1 (running go 1.21.0; GOTOOLCHAIN=local)
```


就像之前说的，当Go工具在编译module依赖项时发现当前go toolchain版本无法满足要求时，会进行go toolchain switches(切换)，切换的过程就是从可用的go toolchain列表中取出一个最适合的。

那么“可用的go toolchain列表”究竟是如何组成的呢？ go命令有三个候选版本(以当前发布的最新版Go 1.21.1为例，这些版本也是Go当前承诺提供support的版本)：

- 尚未发布的Go语言版本的最新候选版本（1.22rc1）
- 最近发布的 Go 语言版本的最新补丁 (1.21.1)
- 上一个Go语言版本的最新补丁版本(1.20.8)。

当GOTOOLCHAIN设置为带auto形式的值的时候，Go会下载这些版本；当GOTOOLCHAIN设置为代path形式的值的时候，Go会在PATH路径搜索适合的go工具链列表。

接下来，go会用mvs(最小版本选择)来确定究竟使用哪个toolchain版本。Go toolchain reference中就有这样一个例子。

假设example.com/widget@v1.2.3需要Go 1.24rc1或更高版本。go命令会获取可用工具链列表，并发现两个最新Go工具链的最新补丁版本是Go 1.28.3和Go 1.27.9，候选版本Go 1.29rc2也可用。在这种情况下，go 命令会选择Go 1.27.9。

如果 widget 需要 Go 1.28或更高版本，go命令会选择 Go 1.28.3，因为 Go 1.27.9 太旧了。如果widget需要Go 1.29或更高版本，go命令会选择Go 1.29rc2，因为Go 1.27.9和Go 1.28.3都太老了。

## 5. 小结

Go 1.21通过增强go语句语义和添加工具链管理，大幅改进了Go语言的向前兼容性。开发者可以放心使用新语言特性，无需担心旧版本编译器带来的问题。go命令会自动处理不同module使用不同go版本和不同工具链版本的情况，使用Go语言变得更简单。

总之，要理解本文内容，重要的是要把握住一点：Go 1.21版本对Go向前兼容性的改进是参考了go module对依赖的管理方法：即**将go版本和go toolchain版本作为一个module的“依赖”来管理**。

## 6. 参考资料

[Forward Compatibility and Toolchain Management in Go 1.21](https://go.dev/blog/toolchain)– https://go.dev/blog/toolchain[Go Toolchains reference](https://go.dev/doc/toolchain)– https://go.dev/doc/toolchain

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