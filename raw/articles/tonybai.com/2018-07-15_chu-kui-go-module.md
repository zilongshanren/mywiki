---
title: 初窥Go module
url: https://tonybai.com/2018/07/15/hello-go-module/
published: '2018-07-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 初窥Go module

自2007年“三巨头（[Robert Griesemer](https://github.com/griesemer), [Rob Pike](https://en.wikipedia.org/wiki/Rob_Pike), [Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)）”提出设计和实现[Go语言](https://tonybai.com/tag/go)以来，[Go语言](https://golang.org)已经发展和演化了[十余年](https://tonybai.com/2017/09/24/go-ten-years-and-climbing/)了。这十余年来，Go取得了巨大的成就，先后在2009年和2016年当选[TIOBE](https://www.tiobe.com/tiobe-index/)年度最佳编程语言，并在全世界范围内拥有数量庞大的拥趸。不过和其他主流编程语言一样，Go语言也不是完美的，不能满足所有开发者的“口味”。这些年来Go在“包依赖管理”和“缺少泛型”两个方面饱受诟病，它们也是Go粉们最希望Go核心Team重点完善的两个方面。

今年(2018)年初，Go核心Team的技术leader，也是Go Team最早期成员之一的[Russ Cox](https://research.swtch.com/)在[个人博客](https://research.swtch.com/)上连续发表了[七篇文章](https://research.swtch.com/vgo)，系统阐述了Go team解决“包依赖管理”的技术方案: [vgo](https://github.com/golang/vgo)。vgo的主要思路包括：[Semantic Import Versioning](https://research.swtch.com/vgo-import)、[Minimal Version Selection](https://research.swtch.com/vgo-mvs)、[引入Go module](https://research.swtch.com/vgo-module)等。这七篇文章的发布引发了Go社区激烈地争论，尤其是MVS(最小版本选择)与目前主流的依赖版本选择方法的相悖让很多传统Go包管理工具的维护者“不满”，尤其是“准官方工具”：[dep](https://tonybai.com/tag/dep)。vgo方案的提出也意味着dep项目的生命周期即将进入尾声。

5月份，Russ Cox的[Proposal “cmd/go: add package version support to Go toolchain”](https://github.com/golang/go/issues/24301)被accepted，这周五早些时候Russ Cox[将vgo的代码merge到Go主干](https://github.com/golang/go/commit/f7248f05946c1804b5519d0b3eb0db054dc9c5d6)，并将这套机制正式命名为“go module”。由于vgo项目本身就是一个实验原型，merge到主干后，**vgo这个术语以及vgo项目的使命也就就此结束了**。后续Go modules机制将直接在Go主干上继续演化。

Go modules是go team在解决包依赖管理方面的一次勇敢尝试，无论如何，对Go语言来说都是一个好事。在本篇文章中，我们就一起来看看这个新引入的go modules机制。

## 一. 建立试验环境

由于加入go modules experiment机制的Go 1.11版本尚未正式发布，且[go 1.11 beta1版本](https://github.com/golang/go/releases/tag/go1.11beta1)发布在go modules merge到主干之前，因此我们要进行go module试验只能使用Go tip版本，即主干上的最新版本。我们需要通过编译Go源码包的方式获得支持go module的go编译器：

编译[Go项目源码](https://github.com/golang/go)的前提是你已经安装了一个发布版，比如[Go 1.10.3](https://github.com/golang/go/releases/tag/go1.10.3)。然后按照下面步骤执行即可：

```
$ git clone https://github.com/golang/go.git
$ mv go go-tip
$ cd go-tip
$ ./all.bash
Building Go cmd/dist using /root/.bin/go1.10.2.
Building Go toolchain1 using /root/.bin/go1.10.2.
Building Go bootstrap cmd/go (go_bootstrap) using Go toolchain1.
Building Go toolchain2 using go_bootstrap and Go toolchain1.
Building Go toolchain3 using go_bootstrap and Go toolchain2.
Building packages and commands for linux/amd64.
##### Testing packages.
ok archive/tar 0.026s
... ...
##### API check
ALL TESTS PASSED
---
Installed Go for linux/amd64 in /root/.bin/go-tip
Installed commands in /root/.bin/go-tip/bin
*** You need to add /root/.bin/go-tip/bin to your PATH.
```


验证源码编译方式的安装结果：

```
# ./go version
go version devel +a241922 Fri Jul 13 00:03:31 2018 +0000 linux/amd64
```


查看有关go module的手册：

```
$ ./go help mod
usage: go mod [-v] [maintenance flags]
Mod performs module maintenance operations as specified by the
following flags, which may be combined.
The -v flag enables additional output about operations performed.
The first group of operations provide low-level editing operations
for manipulating go.mod from the command line or in scripts or
other tools. They read only go.mod itself; they do not look up any
information about the modules involved.
The -init flag initializes and writes a new go.mod to the current directory,
in effect creating a new module rooted at the current directory.
The file go.mod must not already exist.
If possible, mod will guess the module path from import comments
(see 'go help importpath') or from version control configuration.
To override this guess, use the -module flag.
(Without -init, mod applies to the current module.)
The -module flag changes (or, with -init, sets) the module's path
(the go.mod file's module line).
... ...
```


无法通过编译源码的方式获取go tip版的小伙伴们也不用着急，在后续即将发布的go 1.11 beta2版本中将会包含对go modules的支持，到时候按常规方式安装beta2即可体验go modules。

## 二. 传统Go构建以及包依赖管理的回顾

Go在构建设计方面深受Google内部开发实践的影响，比如go get的设计就深受[Google内部单一代码仓库(single monorepo)和基于主干(trunk/mainline based)的开发模型](https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/pdf)的影响：只获取Trunk/mainline代码和版本无感知。

![img{512x368}](../../assets/62f91277d1772de9.png)


Google内部基于主干的开发模型：


– 所有开发人员基于主干trunk/mainline开发：提交到trunk或从trunk获取最新的代码（同步到本地workspace）

– 版本发布时，建立Release branch，release branch实质上就是某一个时刻主干代码的快照；

– 必须同步到release branch上的bug fix和增强改进代码也通常是先在主干上提交(commit)，然后再cherry-pick到release branch上

我们知道go get获取的代码会放在$GOPATH/src下面，而go build会在$GOROOT/src和$GOPATH/src下面按照import path去搜索package，由于go get 获取的都是各个package repo的trunk/mainline的代码，因此，[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)之前的Go compiler都是基于目标Go程序依赖包的trunk/mainline代码去编译的。这样的机制带来的问题是显而易见的，至少包括：

- 因依赖包的trunk的变化，导致不同人获取和编译你的包/程序时得到的结果实质是不同的，即不能实现reproduceable build
- 因依赖包的trunk的变化，引入不兼容的实现，导致你的包/程序无法通过编译
- 因依赖包演进而无法通过编译，导致你的包/程序无法通过编译

为了实现reporduceable build，Go 1.5引入了[Vendor机制](https://tonybai.com/2015/07/31/understand-go15-vendor/)，Go编译器会优先在vendor下搜索依赖的第三方包，这样如果开发者将特定版本的依赖包存放在vendor下面并提交到code repo，那么所有人理论上都会得到同样的编译结果，从而实现reporduceable build。

在Go 1.5发布后的若干年，gopher们把注意力都集中在如何利用vendor解决包依赖问题，从手工添加依赖到vendor、手工更新依赖，到一众包依赖管理工具的诞生：比如: [govendor](https://github.com/kardianos/govendor)、[glide](https://github.com/Masterminds/glide)以及号称准官方工具的[dep](https://github.com/golang/dep)，努力地尝试着按照当今主流思路解决着诸如：“钻石型依赖”等难题。

正当gopher认为dep将“顺理成章”地升级为go toolchain一部分的时候，vgo横空出世，并通过对“Semantic Import Versioning”和”Minimal Version Selected”的设定，在原Go tools上简单快速地实现了Go原生的包依赖管理方案 。vgo就是go module的前身。

## 三. go modules定义、experiment开关以及“依赖管理”的工作模式

**通常**我们会在一个repo(仓库)中创建一组Go package，repo的路径比如：github.com/bigwhite/gocmpp会作为go package的导入路径(import path)，Go 1.11给这样的一组在同一repo下面的packages赋予了一个新的抽象概念: module，并启用一个新的文件go.mod记录module的元信息。

不过一个repo对应一个module这种说法其实并不精确也并不正确，一个repo当然可以拥有多个module，很多公司或组织是喜欢用monorepo的，这样势必有在单一的monorepo建立多个module的需求，显然go modules也是支持这种情况的。

![img{512x368}](../../assets/e625095b699c52a8.png)


图：single repo，single module

![img{512x368}](../../assets/d417408f620bc8d0.png)


图：single monorepo，multiple modules

是时候上代码了！

我们在~/test下建立hello目录（注意：$GOPATH=~/go，显然hello目录并不在GOPATH下面）。hello.go的代码如下：

```
// hello.go
package main
import "bitbucket.org/bigwhite/c"
func main() {
c.CallC()
}
```


我们构建一下hello.go这个源码文件：

```
# go build hello.go
hello.go:3:8: cannot find package "bitbucket.org/bigwhite/c" in any of:
/root/.bin/go-tip/src/bitbucket.org/bigwhite/c (from $GOROOT)
/root/go/src/bitbucket.org/bigwhite/c (from $GOPATH)
```


构建错误！错误原因很明了：在本地的GOPATH下并没有找到bitbucket.org/bigwhite/c路径的package c。传统fix这个问题的方法是手工将package c通过go get下载到本地(并且go get会自动下载package c所依赖的package d)：

```
# go get bitbucket.org/bigwhite/c
# go run hello.go
call C: master branch
--> call D:
call D: master branch
--> call D end
```


这种我们最熟悉的Go compiler从$GOPATH下(以及vendor目录下)搜索目标程序的依赖包的模式称为：**“GOPATH mode”**。

GOPATH是Go最初设计的产物，在Go语言快速发展的今天，人们日益发现GOPATH似乎不那么重要了，尤其是在引入vendor以及诸多包管理工具后。并且GOPATH的设置还会让Go语言新手感到些许困惑，提高了入门的门槛。Go core team也一直在寻求“去GOPATH”的方案，当然这一过程是循序渐进的。[Go 1.8](https://tonybai.com/2017/02/03/some-changes-in-go-1-8/)版本中，如果开发者没有显式设置GOPATH，Go会赋予GOPATH一个默认值（在linux上为$HOME/go）。虽说不用再设置GOPATH，但GOPATH还是事实存在的，它在go toolchain中依旧发挥着至关重要的作用。

Go module的引入在Go 1.8版本上更进了一步，它引入了一种新的依赖管理mode：“module-aware mode”。在该mode下，某源码树(通常是一个repo)的顶层目录下会放置一个go.mod文件，每个go.mod文件定义了一个module，而放置go.mod文件的目录被称为module root目录（通常对应一个repo的root目录，但不是必须的）。module root目录以及其子目录下的所有Go package均归属于该module，除了那些自身包含go.mod文件的子目录。

在“module-aware mode”下，go编译器将不再在GOPATH下面以及vendor下面搜索目标程序依赖的第三方Go packages。我们来看一下在“module-aware mode”下hello.go的构建过程：

我们首先在~/test/hello下创建go.mod:

```
// go.mod
module hello
```


然后构建hello.go

```
# go build hello.go
go: finding bitbucket.org/bigwhite/d v0.0.0-20180714005150-3e3f9af80a02
go: finding bitbucket.org/bigwhite/c v0.0.0-20180714063616-861b08fcd24b
go: downloading bitbucket.org/bigwhite/c v0.0.0-20180714063616-861b08fcd24b
go: downloading bitbucket.org/bigwhite/d v0.0.0-20180714005150-3e3f9af80a02
# ./hello
call C: master branch
--> call D:
call D: master branch
--> call D end
```


我们看到go compiler并没有去使用之前已经下载到GOPATH下的bitbucket.org/bigwhite/c和bitbucket.org/bigwhite/d，而是主动下载了这两个包并成功编译。我们看看执行go build后go.mod文件的内容：

```
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v0.0.0-20180714063616-861b08fcd24b
bitbucket.org/bigwhite/d v0.0.0-20180714005150-3e3f9af80a02 // indirect
)
```


我们看到go compiler分析出了hello module的依赖，将其放入go.mod的require区域。由于c、d两个package均没有版本发布(打tag)，因此go compiler使用了c、d的当前最新版，并以Pseudo-versions的形式记录之。并且我们看到：hello module并没有直接依赖d package，因此在d的记录后面通过注释形式标记了indirect，即非直接依赖，也就是传递依赖。

在“module-aware mode”下，go compiler将下载的依赖包缓存在$GOPATH/pkg/mod下面：

```
// $GOPATH/pkg/mod
# tree -L 3
.
├── bitbucket.org
│ └── bigwhite
│ ├── c@v0.0.0-20180714063616-861b08fcd24b
│ └── d@v0.0.0-20180714005150-3e3f9af80a02
├── cache
│ ├── download
│ │ ├── bitbucket.org
│ │ ├── golang.org
│ │ └── rsc.io
│ └── vcs
│ ├── 064503657de46d4574a6ab937a7a3b88fee03aec15729f7493a3dc8e35cc6d80
│ ├── 064503657de46d4574a6ab937a7a3b88fee03aec15729f7493a3dc8e35cc6d80.info
│ ├── 0c8659d2f971b567bc9bd6644073413a1534735b75ea8a6f1d4ee4121f78fa5b
... ...
```


我们看到c、d两个package也是按照“版本”进行缓存的，便于后续在“module-aware mode”下进行包构建使用。

Go modules机制在go 1.11中是experiment feature，按照Go的惯例，在新的experiment feature首次加入时，都会有一个特性开关，go modules也不例外，**GO111MODULE**这个临时的环境变量就是go module特性的experiment开关。GO111MODULE有三个值：auto、on和off，默认值为auto。**GO111MODULE**的值会直接影响Go compiler的“依赖管理”模式的选择（是GOPATH mode还是module-aware mode），我们详细来看一下：

-
当GO111MODULE的值为off时，go modules experiment feature关闭，go compiler显然会始终使用

**GOPATH mode**，即无论要构建的源码目录是否在GOPATH路径下，go compiler都会在传统的GOPATH和vendor目录(仅支持在gopath目录下的package)下搜索目标程序依赖的go package； -
当GO111MODULE的值为on时（export GO111MODULE=on），go modules experiment feature始终开启，与off相反，go compiler会始终使用

**module-aware mode**，即无论要构建的源码目录是否在GOPATH路径下，go compiler都**不会**在传统的GOPATH和vendor目录下搜索目标程序依赖的go package，而是在go mod命令的缓存目录($GOPATH/pkg/mod）下搜索对应版本的依赖package； -
当GO111MODULE的值为auto时(不显式设置即为auto)，也就是我们在上面的例子中所展现的那样：使用GOPATH mode还是module-aware mode，取决于要构建的源码目录所在位置以及是否包含go.mod文件。如果要构建的源码目录不在以GOPATH/src为根的目录体系下，且包含go.mod文件(两个条件缺一不可)，那么使用module-aware mode；否则使用传统的GOPATH mode。


## 四. go modules的依赖版本选择

### 1. build list和main module

go.mod文件一旦创建后，它的内容将会被go toolchain全面掌控。go toolchain会在各类命令执行时，比如go get、go build、go mod等修改和维护go.mod文件。

之前的例子中，hello module依赖的c、d(indirect)两个包均没有显式的版本信息（比如: v1.x.x），因此go mod使用Pseudo-versions机制来生成和记录c, d的“版本”，我们可以通过下面命令查看到这些信息：

```
# go list -m -json all
{
"Path": "hello",
"Main": true,
"Dir": "/root/test/hello"
}
{
"Path": "bitbucket.org/bigwhite/c",
"Version": "v0.0.0-20180714063616-861b08fcd24b",
"Time": "2018-07-14T06:36:16Z",
"Dir": "/root/go/pkg/mod/bitbucket.org/bigwhite/c@v0.0.0-20180714063616-861b08fcd24b"
}
{
"Path": "bitbucket.org/bigwhite/d",
"Version": "v0.0.0-20180714005150-3e3f9af80a02",
"Time": "2018-07-14T00:51:50Z",
"Indirect": true,
"Dir": "/root/go/pkg/mod/bitbucket.org/bigwhite/d@v0.0.0-20180714005150-3e3f9af80a02"
}
```


go list -m输出的信息被称为**build list**，也就是构建当前module所要构建的所有相关package（及版本）的列表。在输出信息中我们看到 “Main”: true这一信息，标识当前的module为**“main module”**。所谓main module，即是go build命令执行时所在当前目录所归属的那个module，go命令会在当前目录、当前目录的父目录、父目录的父目录…等下面寻找go.mod文件，所找到的第一个go.mod文件对应的module即为main module。如果没有找到go.mod，go命令会提示下面错误信息：

```
# go build test/hello/hello.go
go: cannot find main module root; see 'go help modules'
```


当然我们也可以使用下面命令简略输出build list：

```
# go list -m all
hello
bitbucket.org/bigwhite/c v0.0.0-20180714063616-861b08fcd24b
bitbucket.org/bigwhite/d v0.0.0-20180714005150-3e3f9af80a02
```


### 2. module requirement

现在我们给c、d两个package打上版本信息：

```
package c:
v1.0.0
v1.1.0
v1.2.0
package d:
v1.0.0
v1.1.0
v1.2.0
v1.3.0
```


然后清除掉$GOPATH/pkg/mod目录，并将hello.mod重新置为初始状态（只包含module字段）。接下来，我们再来构建一次hello.go:

```
// ~/test/hello目录下
# go build hello.go
go: finding bitbucket.org/bigwhite/c v1.2.0
go: downloading bitbucket.org/bigwhite/c v1.2.0
go: finding bitbucket.org/bigwhite/d v1.3.0
go: downloading bitbucket.org/bigwhite/d v1.3.0
# ./hello
call C: v1.2.0
--> call D:
call D: v1.3.0
--> call D end
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.2.0 // indirect (c package被标记为indirect，这似乎是当前版本的一个bug)
bitbucket.org/bigwhite/d v1.3.0 // indirect
)
```


我们看到，再一次初始构建hello module时，Go compiler不再用最新的commit revision所对应的Pseudo-version，而是使用了c、d两个package的最新发布版（c:v1.2.0，d: v1.3.0）。

如果我们对使用的c、d版本有特殊约束，比如：我们使用package c的v1.0.0，package d的v1.1.0版本，我们可以通过go mod -require来操作go.mod文件，更新go.mod文件中的require段的信息：

```
# go mod -require=bitbucket.org/bigwhite/c@v1.0.0
# go mod -require=bitbucket.org/bigwhite/d@v1.1.0
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.0.0 // indirect
bitbucket.org/bigwhite/d v1.1.0 // indirect
)
# go build hello.go
go: finding bitbucket.org/bigwhite/d v1.1.0
go: finding bitbucket.org/bigwhite/c v1.0.0
go: downloading bitbucket.org/bigwhite/c v1.0.0
go: downloading bitbucket.org/bigwhite/d v1.1.0
# ./hello
call C: v1.0.0
--> call D:
call D: v1.1.0
--> call D end
```


我们看到由于我们显式地修改了对package c、d两个包的版本依赖约束，go build构建时会去下载package c的v1.0.0和package d的v1.1.0版本并完成构建。

### 3. module query

除了通过传入package@version给go mod -requirement来精确“指示”module依赖之外，go mod还支持query表达式，比如：

```
# go mod -require='bitbucket.org/bigwhite/c@>=v1.1.0'
```


go mod会对query表达式做求值，得出build list使用的package c的版本:

```
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.1.0
bitbucket.org/bigwhite/d v1.1.0 // indirect
)
# go build hello.go
go: downloading bitbucket.org/bigwhite/c v1.1.0
# ./hello
call C: v1.1.0
--> call D:
call D: v1.1.0
--> call D end
```


go mod对module query进行求值的算法是“选择最接近于比较目标的版本(tagged version)”。以上面例子为例：

```
query text: >=v1.1.0
比较的目标版本为v1.1.0
比较形式：>=
```


因此，满足这一query的最接近于比较目标的版本(tagged version)就是v1.1.0。

如果我们给package d增加一个约束“小于v1.3.0”，我们再来看看go mod的选择：

```
# go mod -require='bitbucket.org/bigwhite/d@<v1.3.0'
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.1.0 // indirect
bitbucket.org/bigwhite/d <v1.3.0
)
# go build hello.go
go: finding bitbucket.org/bigwhite/d v1.2.0
go: downloading bitbucket.org/bigwhite/d v1.2.0
# ./hello
call C: v1.1.0
--> call D:
call D: v1.2.0
--> call D end
```


我们看到go mod选择了package d的v1.2.0版本，根据module query的求值算法，v1.2.0恰是最接近于“小于v1.3.0”的tagged version。

用下面这幅示意图来呈现这一算法更为直观一些：

![img{512x368}](../../assets/5f14b4f13a3c0e2a.png)


### 4. minimal version selection(mvs)

到目前为止，我们所使用的example都是最最简单的，hello module所依赖的package c和package d并没有自己的go.mod，也没有定义自己的requirements。对于复杂的包依赖场景，Russ Cox在[“Minimal Version Selection”](https://research.swtch.com/vgo-mvs)一文中给过形象的算法解释(注意：这个算法仅是便于人类理解，但是性能低下，真正的实现并非按照这个算法实现)：

![img{512x368}](../../assets/4cf100295cf94d25.png)


例子情景

![img{512x368}](../../assets/434c1ce1b3836534.png)


算法的形象解释

MVS以build list为中心，从一个空的build list集合开始，先加入main module(A1)，然后递归计算main module的build list，我们看到在这个过程中，先得到C 1.2的build list，然后是B 1.2的build list，去重合并后形成A1的rough build list，选择集合中每个module的最新version，最终形成A1的build list。

我们改造一下我们的例子，让它变得复杂些！

首先，我们为package c添加go.mod文件，并为其打一个新版本：v1.3.0：

```
//bitbucket.org/bigwhite/c/go.mod
module bitbucket.org/bigwhite/c
require (
bitbucket.org/bigwhite/d v1.2.0
)
```


在module bitbucket.org/bigwhite/c的module文件中，我们为其添加一个requirment: bitbucket.org/bigwhite/d@v1.2.0。

接下来，我们将hello module重置为初始状态，并删除$GOPATH/pkg/mod目录。我们修改一下hello module的hello.go如下：

```
package main
import "bitbucket.org/bigwhite/c"
import "bitbucket.org/bigwhite/d"
func main() {
c.CallC()
d.CallD()
}
```


我们让hello module也直接调用package d，并且我们在初始情况下，给hello module添加一个requirement:

```
module hello
require (
bitbucket.org/bigwhite/d v1.3.0
)
```


好了，这次我们再来构建一下hello module：

```
# go build hello.go
go: finding bitbucket.org/bigwhite/d v1.3.0
go: downloading bitbucket.org/bigwhite/d v1.3.0
go: finding bitbucket.org/bigwhite/c v1.3.0
go: downloading bitbucket.org/bigwhite/c v1.3.0
go: finding bitbucket.org/bigwhite/d v1.2.0
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.3.0 // indirect
bitbucket.org/bigwhite/d v1.3.0 // indirect
)
# ./hello
call C: v1.3.0
--> call D:
call D: v1.3.0
--> call D end
call D: v1.3.0
```


我们看到经过mvs算法后，go compiler最终选择了d v1.3.0版本。这里也模仿Russ Cox的图解给出hello module的mvs解析示意图(不过我这个例子还是比较simple)：

![img{512x368}](../../assets/66b097f5b9857799.png)


### 5. 使用package d的v2版本

按照语义化版本规范，当出现不兼容性的变化时，需要升级版本中的major值，而go modules允许在import path中出现v2这样的带有major版本号的路径，表示所用的package为v2版本下的实现。我们甚至可以同时使用一个package的v0/v1和v2两个版本的实现。我们依旧使用上面的例子来实操一下如何在hello module中使用package d的两个版本的代码。

我们首先需要为package d建立module文件：go.mod，并标识出当前的module为：bitbucket.org/bigwhite/d/v2（为了保持与v0/v1各自独立演进，可通过branch的方式来实现），然后基于该版本打v2.0.0 tag。

```
// bitbucket.org/bigwhite/d
#cat go.mod
module bitbucket.org/bigwhite/d/v2
```


改造一下hello module，import d的v2版本：

```
// hello.go
package main
import "bitbucket.org/bigwhite/c"
import "bitbucket.org/bigwhite/d/v2"
func main() {
c.CallC()
d.CallD()
}
```


清理hello module的go.mod，仅保留对package c的requirement:

```
module hello
require (
bitbucket.org/bigwhite/c v1.3.0
)
```


清理$GOPATH/pkg/mod目录，然后重新构建hello module：

```
# go build hello.go
go: finding bitbucket.org/bigwhite/c v1.3.0
go: finding bitbucket.org/bigwhite/d v1.2.0
go: downloading bitbucket.org/bigwhite/c v1.3.0
go: downloading bitbucket.org/bigwhite/d v1.2.0
go: finding bitbucket.org/bigwhite/d/v2 v2.0.0
go: downloading bitbucket.org/bigwhite/d/v2 v2.0.0
# cat go.mod
module hello
require (
bitbucket.org/bigwhite/c v1.3.0 // indirect
bitbucket.org/bigwhite/d/v2 v2.0.0 // indirect
)
# ./hello
call C: v1.3.0
--> call D:
call D: v1.2.0
--> call D end
call D: v2.0.0
```


我们看到c package依然使用的是d的v1.2.0版本，而main中使用的package d已经是v2.0.0版本了。

## 五. go modules与vendor

在最初的设计中，Russ Cox是想彻底废除掉[vendor](http://tonybai.com/2015/07/31/understand-go15-vendor/)的，但在社区的反馈下，vendor得以保留，这也是为了兼容Go 1.11之前的版本。

Go modules支持通过下面命令将某个module的所有依赖保存一份copy到root module dir的vendor下:

```
# go mod -vendor
# ls
go.mod go.sum hello.go vendor/
# cd vendor
# ls
bitbucket.org/ modules.txt
# cat modules.txt
# bitbucket.org/bigwhite/c v1.3.0
bitbucket.org/bigwhite/c
# bitbucket.org/bigwhite/d v1.2.0
bitbucket.org/bigwhite/d
# bitbucket.org/bigwhite/d/v2 v2.0.0
bitbucket.org/bigwhite/d/v2
# tree .
.
├── bitbucket.org
│ └── bigwhite
│ ├── c
│ │ ├── c.go
│ │ ├── go.mod
│ │ └── README.md
│ └── d
│ ├── d.go
│ ├── README.md
│ └── v2
│ ├── d.go
│ ├── go.mod
│ └── README.md
└── modules.txt
5 directories, 9 files
```


这样即便在go modules的**module-aware mode**模式下，我们依然可以只用vendor下的package来构建hello module。比如：我们先删除掉$GOPATH/pkg/mod目录，然后执行：

```
# go build -getmode=vendor hello.go
# ./hello
call C: v1.3.0
--> call D:
call D: v1.2.0
--> call D end
call D: v2.0.0
```


当然生成的vendor目录还可以兼容go 1.11之前的go compiler。不过由于go 1.11之前的go compiler不支持在GOPATH之外使用vendor机制，因此我们需要将hello目录copy到$GOPATH/src下面，再用go 1.10.2版本的compiler编译它：

```
# go version
go version go1.10.2 linux/amd64
~/test/hello# go build hello.go
hello.go:3:8: cannot find package "bitbucket.org/bigwhite/c" in any of:
/root/.bin/go1.10.2/src/bitbucket.org/bigwhite/c (from $GOROOT)
/root/go/src/bitbucket.org/bigwhite/c (from $GOPATH)
hello.go:4:8: cannot find package "bitbucket.org/bigwhite/d/v2" in any of:
/root/.bin/go1.10.2/src/bitbucket.org/bigwhite/d/v2 (from $GOROOT)
/root/go/src/bitbucket.org/bigwhite/d/v2 (from $GOPATH)
# cp -r hello ~/go/src
# cd ~/go/src/hello
# go build hello.go
# ./hello
call C: v1.3.0
--> call D:
call D: v1.2.0
--> call D end
call D: v2.0.0
```


编译输出和程序的执行结果均符合预期。

## 六. 小结

go modules刚刚merge到go trunk中，问题还会有很多。merge后很多gopher也提出了诸多问题，可以在[这里](https://github.com/golang/go/issues?q=is%3Aissue+is%3Aopen+label%3Amodules)查到。当然哪位朋友如果也遇到了go modules的问题，也可以在go官方issue上提出来，帮助go team尽快更好地完善go 1.11的go modules机制。

go module的加入应该算是go 1.11版本最大的变化，go module的内容很多，短时间内我的理解也可能存在偏差和错误，欢迎广大gopher们交流指正。

参考资料：

[go modules have landed](https://groups.google.com/forum/#!msg/golang-dev/a5PqQuBljF4/61QK4JdtBgAJ)需科学上网访问[Go & Versioning](https://research.swtch.com/vgo)- go help mod

[51短信平台](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

第五节最后一个例子build不是出错了吗？找不到包

那是因为go 1.11之前的版本不支持在$GOPATH之外使用vendor啊。所以报错。将代码（包括vendor目录) copy到$GOPATH/src下面编译就ok了啊。

现在go1.11正式版已经发布了，好像mod是在pkg目录下面

嗯。go 1.11beta2之后russ cox对go module又做了很多改动。这篇文章仅适用于go 1.11beta2。go 1.11 中go module也是experiment feature。也许在Go 1.12成为正式feature时相比于go 1.11可能还会有些许变换。

vscode-go 插件目前有没有支持Go module的办法？

从vscode-go最新的changelog和issue来看，目前它还不支持module。很多工具还不支持module，因为之前go module一直的active dev中，命令形式经常变化。go 1.11发布后算是暂时稳定，各个工具也才开始考虑如何支持，这个需要时间。

Goland 支持了，vscode看来还需要一段时间

因依赖包的trunk的变化，导致不同人获取和编译你的包/程序时得到的结果实质是不同的，即不能实现reproduceable build

====

这句话怎么理解，不同人获取和编译你的包／程序时得到的结果实质是不同的？ ，

如果trunk变化了，大家go get 一下，那么编译的都是变化后的trunk，结果是一样的。

假设我们的代码是A依赖第三方包B。甲程序员9:00 go get A并编译A，此时B的trunk的revision为001。10:00B的author在B trunk提交了新代码，B代码的trunk revision进化到002。11点时乙程序员go get A并编译A。显然甲乙两个人得到的编译后的A可执行程序并不相同，因为虽然同为B trunk，但trunk上的代码已经不同了。并且大多数情况，在go build之前很少会执行 go get。这样就不能实现reproduceable build。

我的项目依赖的包全部缓存在了 $GOPATH/pkg/mod/ 目录下了。并不是文中说的 $GOPATH/src/mod/ 。请问这种出现这种情况的原因是什么？

应该是发布时用全局替换命令替换错了，应该是$GOPATH/pkg/mod/ 目录下，而不是$GOPATH/src/mod目录。文章中已经改过来了，谢谢报出问题。

Tony老师，微信公众号，搞一个二维码啊

我的微信公众号iamtonybai有二维码啊，就在blog页面的右侧边栏里。难道还不够醒目:)

在使用GOMODULE时往往会出现Internal Server Error或Timeout等问题。

GOPROXY能够在一定程度上解决在拉取诸如 golang.org/x 包的时候产生的超时问题，也可以在一定程度上解决由于项目改名、迁移、删除等原因导致的404问题。

但是需要注意的是，使用GOPROXY将导致你无法拉取私有储存库。

现在，GOS解决了这个问题。 https://github.com/storyicon/gos