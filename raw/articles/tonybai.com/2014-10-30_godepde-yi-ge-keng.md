---
title: godep的一个“坑”
url: https://tonybai.com/2014/10/30/a-hole-of-godep/
published: '2014-10-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# godep的一个“坑”

很多人学习和使用[Golang](http://tonybai.com/tag/golang)一段时间后，都会被[golang](http://golang.org)的第三方包依赖版本搞得有些烦躁，golang设计者最初过于乐观的设计使得今天大 家不得不各自想办法解决这个问题。[godep](https://github.com/tools/godep)就是综合了多年第三方包依赖问题的解决方案后的一个趋向统一的方案，至少是在go get的设计没有进化前的一个比较不错的方案。

今天试用了一把godep，不过“体验”并不理想，这缘于我遇到了godep的一个“坑”，不过是那种你在正式项目中不一定遇到的“坑”，这里来说到说到。

按照godep官方使用说明的第一步，先下载godep：

$ go get github.com/tools/godep

$godep

Godep is a tool for managing Go package dependencies.

Usage:

godep command [arguments]

The commands are:

save list and copy dependencies into Godeps

go run the go tool in a sandbox

get download and install packages with specified dependencies

path print sandbox path for use in a GOPATH

restore check out listed dependency versions in GOPATH

update use different revision of selected packages

Use "godep help [command]" for more information about a command.

确认正确下载后，我们来准备一个测试例子，目录如下：

$GOPATH/

src/

tonybai.com/

foolib/

foo.go

fooapp/

main.go


//foo.go

package foo

func Add(a, b int) int {

return a + b

}

//main.go

package main

import (

"fmt"

foo "tonybai.com/foolib"

)

func main() {

fmt.Println(foo.Add(1, 3))

}

在fooapp下，编译执行程序：

$go run main.go

4

接下来godep登场，根据godep文档中得步骤，接下来我们应该在一个构建依赖关系完整的项目中执行godep save以保存依赖关系以及依赖的当前版本第三方包：

$godep save

godep: directory "/Users/tony/Test/GoToolsProjects/src" is not using a known version control system

godep: error loading dependencies

出错了！godep提示$GOPATH/src目录没有使用任何版本控制系统(not using a known version control system)。 奇怪啊！这个错误什么意思呢？难道使用godep还需要将$GOPATH/src整体作为一个Project纳入git or subversion repository中？无奈之下，我只能先这么做，再作观察。我在$GOPATH下执行git init，建立一个local git repository，然后将src add到这个repository中。

回到fooapp下，再次执行godep save，居然依旧是同样地错误结果。于是到godep的issues中去查，看看是否有人和我遇到了同样地问题！godep的[#116 issue](https://github.com/tools/godep/issues/116)中提到的问题恰恰和我的一致，不过这个issue一 直是open状态，也没有人comments。接着翻看一下godep的源码，godep依赖一些第三方包，save这个命令在分析版本控制工具库时也是 调用了多层外部包实现的，短时间内无法定位问题。

静想一下，godep是管理第三方包依赖关系的，而第三方包多是go get下载的，是不是foolib要放到repository中才行呢？于是尝试在foolib中建立git repository并做一次commit。第三次在fooapp下执行godep save，错误依旧！

难道fooapp也必须放在repository中？试试吧。在fooapp下init一个git repository，将fooapp下的main.go提交到repository中。再执行godep save：

$godep save

$ls -l

total 8

drwxr-xr-x 5 tony staff 170 10 30 22:01 Godeps/

-rw-r–r– 1 tony staff 103 10 30 21:44 main.go

这回成功了！godep save在fooapp下建立了Godeps目录，其结构如下：

$ls -R

Godeps.json Readme _workspace/

./_workspace:

src/

./_workspace/src:

tonybai.com/

./_workspace/src/tonybai.com:

foolib/

./_workspace/src/tonybai.com/foolib:

foolib.go

godep将当前版本的foolib copy到Godeps/_workspace下了。

Godeps.json记录了fooapp对foolib的依赖关系：

{

"ImportPath": "fooapp",

"GoVersion": "go1.3",

"Deps": [

{

"ImportPath": "tonybai.com/foolib",

"Rev": "**20a9c2a682537813d37847f2f270bf929672cc84**"

}

]

}

godep记录了foolib的当前revision number，这个number恰是我最新一次commit的hash code：

~/Test/GoToolsProjects/src/tonybai.com/foolib]$git log

commit **20a9c2a682537813d37847f2f270bf929672cc84**

Author: Tony Bai <bigwhite.cn@gmail.com>

Date: Thu Oct 30 22:00:25 2014 +0800

init

到这里让我觉得godep的设计思路有些与我的[buildc](http://github.com/bigwhite/buildc)（[C程序辅助构建工具](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)）的思路有些类似，只是godep做得更彻底：

1、godep将项目依赖统统放到项目的私有_workspace下，而buildc是共享的，通过project下的版本号配置区分依赖

2、godep将依赖管理到revision(修订号)级别，buildc只是根据version来区分依赖。

godep的辅助构建原理（godep go build main.go）通过一条命令即可看出来：

$godep go env

GOARCH="amd64"

GOBIN="/usr/local/go/bin"

GOCHAR="6"

GOEXE=""

GOHOSTARCH="amd64"

GOHOSTOS="darwin"

GOOS="darwin"

**GOPATH="/Users/tony/Test/GoToolsProjects/src/fooapp/Godeps/_workspace:/Users/tony/Test/GoToolsProjects"**

godep临时将_workspace放在GOPATH列表的前面，这样gc在编译时就会按顺序先在_workspace下面找依赖包，这样fooapp的私有依赖就会理所当然的被gc用到，即便在其他GOPATH路径下有同名包（可能是不同版本的）。

显然这也算是godep的一个小bug吧（或者是godep依赖的包的bug，目前不确认），毕竟提示的路径是不正确的，不应该提示"/Users/tony/Test/GoToolsProjects/src" is not using a known version control system，而应该是"/Users/tony/Test/GoToolsProjects/src/tonybai.com/foolib或"/Users/tony/Test/GoToolsProjects/src/fooapp没有版本控制系统的repository留存。

另外觉得godep的author应该把这个“坑”作为一个使用godep的前提进行说明，并在github主页给出明确展示，即便这个“坑”多数人可能不会遇到。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

为什么godep要依赖于版本控制 我新建的项目加了git init就正常了 godep save 也可以用了

godep需要记录你的project依赖的第三方库的git revision number，因此它需要本地的第三方库是一个完整的git repository clone。至于我文中遇到的问题，可能是个别现象，某些人遇到了，某些人没遇到。尚未分析godep源码，我也无法给出真实原因。

就看见出错了！成功了！想一想！具体怎么做的语无伦次！

加入版本控制之后save没有问题restore仍然报错，怎么解决，谢谢

最新版本godep还有restore错误么？这个没遇到过。可以说说详细错误情况

请问，这个问题：godep: Unable to find SrcRoot for package .，你有碰到过吗？

没遇到过。不过现在你们还在用godep么? 为什么不用go module机制(go 1.11引入)，又或至少用用dep(github.com/golang/dep)吧？