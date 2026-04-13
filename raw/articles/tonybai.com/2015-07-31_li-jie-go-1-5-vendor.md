---
title: 理解Go 1.5 vendor
url: https://tonybai.com/2015/07/31/understand-go15-vendor/
published: '2015-07-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解Go 1.5 vendor

[Go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)中(目前最新版本go1.5beta3)加入了一个experimental feature: **vendor/**。这个feature不是[Go 1.5](https://tip.golang.org/doc/go1.5)的正式功能，但却是Go Authors们在解决Go被外界诟病的包依赖管理的道路上的一次重要尝试。目前关于Go vendor机制的资料有限，主要的包括如下几个：

1、Russ Cox在[Golang-dev group](https://groups.google.com/forum/#!forum/golang-dev)上的一个名 为"[proposal: external packages](https://groups.google.com/d/topic/golang-dev/74zjMON9glU /discussion)" topic上的reply。

2、Go 1.5beta版发布后Russ Cox根据上面topic整理的一个[doc](https://golang.org/s/go15vendor)。

3、medium.com上一篇名为“[Go 1.5 vendor/ experiment](https://medium.com/@freeformz/go-1-5-s-vendor-experiment-fd3e830f52c3)"的文章。

但由于Go 1.5稳定版还未发布(最新消息是2015.8月中旬发布)，因此估计真正采用vendor的repo尚没有。但既然是Go官方解决方案，后续从 expreimental变成official的可能性就很大（Russ的初步计划：如果试验顺利，1.6版本默认 GO15VENDOREXPERIMENT="1"；1.7中将去掉GO15VENDOREXPERIMENT环境变量）。因此对于Gophers们，搞 清楚vendor还是很必要的。本文就和大家一起来理解下vendor这个新feature。

**一、vendor由来**

[Go](http://tonybai.com/tag/go)第三方包依赖和管理的问题由来已久，民间知名的解决方案就有[godep](https://github.com/tools/godep)、 [gb](https://github.com/constabulary/gb)等。这次Go team在推出vendor前已经在Golang-dev group上做了长时间的调研，最终Russ Cox在[Keith Rarick](https://github.com/kr)的proposal的基础上做了改良，形成了Go 1.5中的vendor。

Russ Cox基于前期调研的结果，给出了vendor机制的群众意见基础：

– 不rewrite gopath

– go tool来解决

– go get兼容

– 可reproduce building process

并给出了vendor机制的"4行"诠释：

If there is a source directory d/vendor, then, when compiling a source file within the subtree rooted at d, import "p" is interpreted as import "d/vendor/p" if that exists.

When there are multiple possible resolutions,the most specific (longest) path wins.

The short form must always be used: no import path can contain “/vendor/” explicitly.

Import comments are ignored in vendored packages.

这四行诠释在group中引起了强烈的讨论，短小精悍的背后是理解上的不小差异。我们下面逐一举例理解。

**二、vendor基本样例**

Russ Cox诠释中的第一条是vendor机制的基础。粗犷的理解就是如果有如下这样的目录结构：

d/

vendor/

p/

p.go

mypkg/

main.go

如果mypkg/main.go中有"import p"，那么这个p就会被go工具解析为"d/vendor/p"，而不是$GOPATH/src/p。

现在我们就来复现这个例子，我们在go15-vendor-examples/src/basic下建立如上目录结构（其中go15-vendor-examples为GOPATH路径）：

$ls -R

d/

./d:

mypkg/ vendor/

./d/mypkg:

main.go

./d/vendor:

p/

./d/vendor/p:

p.go

其中main.go代码如下：

//main.go

package main

import "p"

func main() {

p.P()

}

p.go代码如下：

//p.go

package p

import "fmt"

func P() {

fmt.Println("P in d/vendor/p")

}

在未开启vendor时，我们编译d/mypkg/main.go会得到如下错误结果：

$ go build main.go

main.go:3:8: cannot find package "p" in any of:

/Users/tony/.bin/go15beta3/src/p (from $GOROOT)

/Users/tony/OpenSource/github.com/experiments/go15-vendor-examples/src/p (from $GOPATH)

错误原因很显然：go编译器无法找到package p，d/vendor下的p此时无效。

这时开启vendor：export GO15VENDOREXPERIMENT=1，我们再来编译执行一次：

$go run main.go

P in d/vendor/p

开启了vendor机制的go tool在d/vendor下找到了package p。

也就是说拥有了vendor后，你的project依赖的第三方包统统放在vendor/下就好了。这样go get时会将第三方包同时download下来，使得你的project无论被下载到那里都可以无需依赖目标环境而编译通过(reproduce the building process)。

**三、嵌套vendor**

那么问题来了！如果vendor中的第三方包中也包含了vendor目录，go tool是如何choose第三方包的呢？我们来看看下面目录结构(go15-vendor-examples/src/embeded)：

d/

vendor/

p/

p.go

q/

q.go

vendor/

p/

p.go

mypkg/

main.go

embeded目录下出现了嵌套vendor结构：main.go依赖的q包本身还有一个vendor目录，该vendor目录下有一个p包，这样我们就有了两个p包。到底go工具会选择哪个p包呢？显然为了验证一些结论，我们源文件也要变化一下：

d/vendor/p/p.go的代码不变。

//d/vendor/q/q.go

package q

import (

"fmt"

"p"

)

func Q() {

fmt.Println("Q in d/vendor/q")

p.P()

}

//d/vendor/q/vendor/p/p.go

package p

import "fmt"

func P() {

fmt.Println("P in d/vendor/q/vendor/p")

}

//mypkg/main.go

package main

import (

"p"

"q"

)

func main() {

p.P()

fmt.Println("")

q.Q()

}

目录和代码编排完毕，我们就来到了见证奇迹的时刻了！我们执行一下main.go：

$go run main.go

P in d/vendor/p

Q in d/vendor/q

P in d/vendor/q/vendor/p

可以看出main.go中最终引用的是d/vendor/p，而q.Q()中调用的p.P()则是d/vendor/q/vendor/p包的实现。go tool到底是如何在嵌套vendor情况下选择包的呢？我们回到Russ Cox关于vendor诠释内容的第二条：

When there are multiple possible resolutions,the most specific (longest) path wins.

这句话很简略，但却引来的巨大争论。"longest path wins"让人迷惑不解。如果仅仅从字面含义来看，上面main.go的执行结果更应该是：

P in d/vendor/q/vendor/p

Q in d/vendor/q

P in d/vendor/q/vendor/p

d/vendor/q/vendor/p可比d/vendor/p路径更long，但go tool显然并未这么做。它到底是怎么做的呢？talk is cheap, show you the code。我们粗略翻看一下go tool的实现代码：

在$GOROOT/src/cmd/go/pkg.go中有一个方法vendoredImportPath,这个方法在go tool中广泛被使用：

// vendoredImportPath returns the expansion of path when it appears in parent.

// If parent is x/y/z, then path might expand to x/y/z/vendor/path, x/y/vendor/path,

// x/vendor/path, vendor/path, or else stay x/y/z if none of those exist.

// vendoredImportPath returns the expanded path or, if no expansion is found, the original.

// If no expansion is found, vendoredImportPath also returns a list of vendor directories

// it searched along the way, to help prepare a useful error message should path turn

// out not to exist.

func vendoredImportPath(parent *Package, path string) (found string, searched []string)

这个方法的doc讲述的很清楚，这个方法返回所有可能的vendor path，以parentpath为x/y/z为例：

x/y/z作为parentpath输入后，返回的vendorpath包括：


x/y/z/vendor/path

x/y/vendor/path

x/vendor/path

vendor/path

这么说还不是很直观，我们结合我们的embeded vendor的例子来说明一下，为什么结果是像上面那样！go tool是如何resolve p包的！我们模仿go tool对main.go代码进行编译（此时vendor已经开启）。

根据go程序的package init顺序，go tool首先编译p包。如何找到p包呢？此时的编译对象是d/mypkg/main.go，于是乎parent = d/mypkg，经过vendordImportPath处理，可能的vendor路径为：

d/mypkg/vendor

d/vendor

但只有d/vendor/下存在p包，于是go tool将p包resolve为d/vendor/p，于是下面的p.P()就会输出：

P in d/vendor/p

接下来初始化q包。与p类似，go tool对main.go代码进行编译，此时的编译对象是d/mypkg/main.go，于是乎parent = d/mypkg，经过vendordImportPath处理，可能的vendor路径为：

d/mypkg/vendor

d/vendor

但只有d/vendor/下存在q包，于是乎go tool将q包resolve为d/vendor/q，由于q包自身还依赖p包，于是go tool继续对q中依赖的p包进行选择，此时go tool的编译对象变为了d/vendor/q/q.go，parent = d/vendor/q，于是经过vendordImportPath处理，可能的vendor路径为：

d/vendor/q/vendor

d/vendor/vendor

d/vendor

存在p包的路径包括：

d/vendor/q/vendor/p

d/vendor/p

此时按照Russ Cox的诠释2：choose longest，于是go tool选择了d/vendor/q/vendor/p，于是q.Q()中的p.P()输出的内容就是:

"P in d/vendor/q/vendor/p"

如果目录结构足够复杂，这个resolve过程也是蛮繁琐的，但按照这个思路依然是可以分析出正确的包的。

另外vendoredImportPath传入的parent x/y/z并不是一个绝对路径，而是一个相对于$GOPATH/src的路径。

BTW，上述测试样例代码在[这里](https://github.com/bigwhite/experiments/tree/master/go15-vendor-examples)可以下载到。

**四、**第三和第四条

最难理解的第二条已经pass了，剩下两条就比较好理解了。

The short form must always be used: no import path can contain “/vendor/” explicitly.

这条就是说，你在源码中不用理会vendor这个路径的存在，该怎么import包就怎么import，不要出现import "d/vendor/p"的情况。vendor是由go tool隐式处理的。

Import comments are ignored in vendored packages.

[go 1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)引入了canonical imports机制，如:

package pdf // import "rsc.io/pdf"

如果你引用的pdf不是来自rsc.io/pdf，那么编译器会报错。但由于vendor机制的存在，go tool不会校验vendor中package的import path是否与canonical import路径是否一致了。

**五、问题**

根据小节三中的分析，对于vendor中包的resolving过程类似是一个recursive(递归）过程。

main.go中的p使用d/vendor/p；而q.go中的p使用的是d/vendor/q/vendor/p，这样就会存在一个问题：一个工程中存 在着两个版本的p包，这也许不会带来问题，也许也会是问题的根源，但目前来看从go tool的视角来看似乎没有更好的办法。Russ Cox期望大家良好设计工程布局，作为lib的包不携带vendor更佳。

这样一个project内的所有vendor都集中在顶层vendor里面。就像下面这样：

d/

vendor/

q/

p/

… …

mypkg1

main.go

mypkg2

main.go

… …

另外Go vendor不支持第三方包的版本管理，没有类似godep的Godeps.json这样的存储包元信息的文件。不过目前已经有第三方的[vendor specs](https://github.com/kardianos/vendor-spec)放在了github上，之前Go team的Brad Fizpatrick也在Golang-dev上征集过类似的方案，不知未来vendor是否会支持。

**六、vendor vs. internal**

在golang-dev有人提到：有了vendor，internal似乎没用了。这显然是混淆了internal和vendor所要解决的问题。

internal故名思议：内部包，不是对所有源文件都可见的。vendor是存储和管理外部依赖包，更类似于external，里面的包都是copy自 外部的，工程内所有源文件均可import vendor中的包。另外internal在1.4版本中已经加入到go核心，是不可能轻易去除的，虽然到目前为止我们还没能亲自体会到internal 包的作用。

在《[Go 1.5中值得关注的几个变化](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)》一文中我提到过go 1.5 beta1似乎“不支持”internal，beta3发布后，我又试了试看beta3是否支持internal包。

结果是beta3中，build依旧不报错。但go list -json会提示错误：

"DepsErrors": [

{

"ImportStack": [

"otherpkg",

"mypkg/internal/foo"

],

"Pos": "",

"Err": "use of internal package not allowed"

}

]

难道真的要到最终go 1.5版本才会让internal包发挥作用?

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

“Russ Cox期望大家良好设计工程布局，作为lib的包不携带vendor更佳”，这个恐怕不现实，可能只有最基础的包才能做到。

赞 写的不错