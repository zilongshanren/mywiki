---
title: 一文告诉你如何抢先体验Go泛型
url: https://tonybai.com/2020/11/28/httpstonybai-com20201128how-to-experience-go-generics-first/
published: '2020-11-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文告诉你如何抢先体验Go泛型

![img{512x368}](../../assets/81f0ed78d584c86b.png)


本文首发于我主持的[“Gopher部落”知识星球](https://articles.zsxq.com/id_bjzje91weqn7.html)，欢迎大家加入星球，一起学习Go语言！年底前8.8折优惠，不要错过哦！

![](../../assets/d3fad3142fe3cc39.png)


2020年11月22日，Go核心开发团队技术负责人[Russ Cox](http://swtch.com/%7Ersc/)在[golang-dev论坛](https://groups.google.com/g/golang-dev/c/U7eW9i0cqmo/m/ffs0tyIYBAAJ?pli=1)上确认了Go泛型将在Go 1.18落地(2022.2)：

![img{512x368}](../../assets/7809268ea46b9f51.png)


这对于那些迫切期盼go加入泛型的gopher来说无疑是一个重大利好消息！不过，泛型是把双刃剑！泛型的加入势必会让Go语言的复杂性大幅提升。我很是担心Go加入泛型后会像C++模板那样被“滥用”而形成很多**奇技淫巧**，这显然不是Go项目组想看到的。因此他们现在在宣传泛型时都是比较谨慎的。[Robert Griesemer](https://github.com/griesemer)在[GopherCon 2020](https://www.gophercon.com/)大会上演讲[“Typing [Generic] Go”](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)中明确给出了Go泛型的使用时机：

- 可增强静态类型安全性的时候
- 可以更高效的使用内存的时候
- 可以(显著的)提升性能的时候

虽然这不能完全避免滥用，但至少表明了Go团队对泛型使用的态度。[“能力越大，责任越大”](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)，大家在使用泛型时务必**三思而后行**！

现在，Go泛型已经处于“箭在弦上不得不发”的状态，作为Gopher，我们能做的就是拥抱它！

离Go 1.18发布还有一年多的时间，对于极其渴望支持泛型的gopher来说，这个时间有点长！好在Go项目组已经提供了一些抢先体验Go泛型语法的方法，这里我们就来全面介绍一下，小伙伴们可以根据自己的情况任选一种抢先体验Go泛型！

### 1. Go泛型在线playground

2020.6月末，Ian Lance Taylor和Robert Griesemer在Go官方博客发表了文章[《The Next Step for Generics》](http://blog.golang.org/generics-next-step)，介绍了Go泛型工作的最新进展。同时，Go团队还推出了可以[在线试验Go泛型语法的playground](https://go2goplay.golang.org)：https://go2goplay.golang.org：

![img{512x368}](../../assets/0490fa49f5fcfcff.png)


通过该在线playground，我们可以体验最新的Go泛型语法并查看编译和运行结果。

在线playground的好处就在于可以随时随地访问和体验，体验设备也不局限于计算机，甚至可以使用手机/平板终端。不过**该playground在国内访问不畅**，并且体验仅局限于单文件的形式，对于复杂一些的项目无法支持。

### 2. 基于源码编译出go2go工具

Go项目在**dev.go2go**分支上加入了Go泛型语法的实现，我们可以在本地基于Go项目源码构建出可以用于体验Go泛型的go2go工具。

要想构建go2go工具，我们**首先就需要下载Go项目源码**。但截至目前，[Go项目仓库](https://github.com/golang/go)**github.com/golang/go**有45000多次提交，在国内以20k/s的速度clone这个仓库那是相当耗时费力，还不一定有好结果（经常断连，一断连，就要重新来过）。当然如果你有高速vpn则另当别论了。这里介绍一个下载github上Go项目源码的过渡方法：**利用gitee(码云)建立Go仓库镜像库，然后从码云以2M/s速度下载**。步骤如下：

-
在gitee上建立一个公共仓库，比如：

**gitee.com/bigwhite/go**，在建立仓库时选择“导入现有库”，填入现有库的地址：**https:///github.com/golang.go.git**，之后，强大的“码云”就会帮助我们快速同步了。 -
之后我们就可以从码云clone这个仓库：

**gitee.com/bigwhite/go**，2M/s的速度，一分钟内就完成clone。并且码云支持强制从源仓库github.com/golang/go同步最新更新到镜像仓库，十分方便。

```
$git clone https://gitee.com/bigwhite/go.git
```


既然我已经在码云建立的go仓库的镜像，各位小伙伴儿们就可以直接clone我的公共库(https://gitee.com/bigwhite/go)来获取go仓库源码了。


接下来，我们来构建go2go工具，主要步骤如下(当前环境为ubuntu，并已安装的go的版本为[go 1.15.4](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ) linux/amd64)：

- 切换到dev.go2go分支

```
// 进入下载后的go仓库源码目录(我这里为~/.bin/go)
$git checkout dev.go2go
Branch 'dev.go2go' set up to track remote branch 'dev.go2go' from 'origin'.
Switched to a new branch 'dev.go2go'
```


注：ubuntu需安装

build-essential(apt-get install build-essential)，否则在go源码编译过程可能会出现“fatal error: stdlib.h: No such file or directory”的错误。

- 编译dev.go2go分支源码

Go源码编译是“一键式”的，并且速度非常快！进入到Go项目源码下的src目录(cd ~/.bin/go/src)，执行下面命令：

```
$./all.bash
Building Go cmd/dist using /root/.bin/go1.15.4. (go1.15.4 linux/amd64)
Building Go toolchain1 using /root/.bin/go1.15.4.
Building Go bootstrap cmd/go (go_bootstrap) using Go toolchain1.
Building Go toolchain2 using go_bootstrap and Go toolchain1.
Building Go toolchain3 using go_bootstrap and Go toolchain2.
Building packages and commands for linux/amd64.
... ...
ALL TESTS PASSED
---
Installed Go for linux/amd64 in /root/.bin/go
Installed commands in /root/.bin/go/bin
*** You need to add /root/.bin/go/bin to your PATH.
```


构建后的可执行文件go与gofmt被放在了bin目录下(~/go/bin)，为方便使用，我们最好将其所在路径配置到**PATH**环境变量中。。

- 验证构建结果

```
$go version
go version devel +440f144a10 Tue Nov 24 01:29:01 2020 +0000 linux/amd64
```


如果看到上面结果，说明构建是ok的。

接下来，我们就来使用构建出的go工具体验一下编译运行一个使用泛型语法编写的源文件**sort.go2**：

```
// sort.go2
package main
import (
"fmt"
"sort"
)
type Lang struct {
Name string
Rank int
}
type sliceFn[T any] struct {
s []T
cmp func(T, T) bool
}
func (s sliceFn[T]) Len() int { return len(s.s) }
func (s sliceFn[T]) Less(i, j int) bool { return s.cmp(s.s[i], s.s[j]) }
func (s sliceFn[T]) Swap(i, j int) { s.s[i], s.s[j] = s.s[j], s.s[i] }
func SliceFn[T any](s []T, cmp func(T, T) bool) {
sort.Sort(sliceFn[T]{s, cmp})
}
func main() {
langs := []Lang{
{"rust", 2},
{"go", 1},
{"swift", 3},
}
SliceFn(langs, func(p1, p2 Lang) bool { return p1.Rank < p2.Rank })
fmt.Println(langs) // [{go 1} {rust 2} {swift 3}]
}
```


go2go是以go tool的一个子命令形式存在的，它支持编译和运行以**.go2**为后缀的Go源文件，如果让它编译和运行**.go**文件，它会报如下错误：

```
$go tool go2go run sort.go
Go file sort.go was not created by go2go
```


编译运行上面的sort.go2的命令和结果如下：

```
$go tool go2go run sort.go2
[{go 1} {rust 2} {swift 3}]
```


有小伙伴可能会说，这个例子也是单一源文件，太简单！那我们接下来就整一个稍复杂些的。go2go这个子命令自带了一些复杂的Go泛型包，这些包的源码被放在了Go仓库源码的**src/cmd/go2go/testdata**下面：

```
$tree -LF 2 go2path
go2path
└── src/
├── alg/
├── chans/
├── constraints/
├── graph/
├── gsort/
├── list/
├── maps/
├── metrics/
├── orderedmap/
├── sets/
└── slices/
```


go2go目前仅支持gopath mode，还不支持[module-ware mode](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)。go2go支持专用的GO2PATH环境变量用于指示GOPATH路径，也可以用传统的GOPATH环境变量。为了使用go2go自带的那些样例源码包，我们需要将GOPATH或GO2PATH设置为**\$GOROOT/src/cmd/go2go/testdata/go2path**。我们在go2path路径下建立我们的样例repo：

```
$tree -LF 5 go2path
go2path
└── src/
│ ... ...
├── github.com/
│ └── bigwhite/
│ └── gsort-demo/
│ └── demo.go2
│ ... ...
└── slices/
├── slices.go2
└── slices_test.go2
// demo.go2
package main
import (
"fmt"
"gsort"
)
type Lang struct {
Name string
Rank int
}
func main() {
langs := []Lang{
{"rust", 2},
{"go", 1},
{"swift", 3},
}
gsort.SliceFn(langs, func(p1, p2 Lang) bool { return p1.Rank < p2.Rank })
fmt.Println(langs)
}
```


我们可以用两种方法运行demo.go2：

```
// 设置GO2PATH：
~/.bin/go/src/cmd/go2go/testdata/go2path/src/github.com/bigwhite/gsort-demo$ GO2PATH=$GOROOT/src/cmd/go2go/testdata/go2path go tool go2go run demo.go2
[{go 1} {rust 2} {swift 3}]
或
// 设置GOPATH和关闭GO111MODULE：
~/.bin/go/src/cmd/go2go/testdata/go2path/src/github.com/bigwhite/gsort-demo$ GOPATH=$GOROOT/src/cmd/go2go/testdata/go2path GO111MODULE=off go tool go2go run demo.go2
[{go 1} {rust 2} {swift 3}]
```


通过源码构建go2go工具的方法是体验Go泛型最基本的方法，我们还可以定期更新Go项目源码以体验泛型草案的最新变化。我们还可以通过**go doc cmd/go2go**来查看go2go命令的文档。

### 3. 使用go2go的docker容器

如果觉得使用源码构建本地可用的go2go工具依然“门槛高”或者繁琐，那么可以利用一些gopher已经上传的现成的docker容器来构建使用了泛型语法的*.go2文件。这里使用的是**levonet/golang:go2go**：

```
$docker pull levonet/golang:go2go
```


- 使用go2go容器编译运行单个*.go2文件

我们还以上面那个sort.go2为例，该文件可以放在任意目录下，然后我们在该文件所在目录下执行下面命令即可编译运行它：

```
$ docker run --rm -v "$PWD":/go/src/myapp -w /go/src/myapp levonet/golang:go2go go tool go2go run sort.go2
[{go 1} {rust 2} {swift 3}]
```


这句docker run命令的含义是：将宿主机当前工作目录(即sort.go2所在目录)挂载到容器中的**/go/src/myapp**下面，并将**/go/src/myapp**作为当前工作目录，执行**go tool go2go run sort.go2**。

对于复杂的如上面的github.com/bigwhite/gsort-demo的例子，通过docker容器一样可以编译，只不过命令复杂一些：

```
~/temp/github.com $docker run --rm -v "$PWD":/usr/local/lib/go/src/cmd/go2go/testdata/go2path/src/github.com -w /usr/local/lib/go/src/cmd/go2go/testdata/go2path/src/github.com/bigwhite/gsort-demo -e GO2PATH="/usr/local/lib/go/src/cmd/go2go/testdata/go2path" levonet/golang:go2go go tool go2go run demo.go2
[{go 1} {rust 2} {swift 3}]
```


我们将github.com目录放在任意目录下，比如：~/temp，然后将当前目录挂载到容器的**/usr/local/lib/go/src/cmd/go2go/testdata/go2path/src/github.com**目录下，设定工作目录为**/usr/local/lib/go/src/cmd/go2go/testdata/go2path/src/github.com/bigwhite/gsort-demo**，然后为容器新增以环境变量**GO2PATH**，这样我们就可以编译运行demo.go2了。

注1：容器中的GOROOT为/usr/local/lib/go


### 4. 使用Goland体验Go泛型

著名Go语言IDE产品goland也[宣布支持体验最新的Go泛型语法](https://blog.jetbrains.com/go/2020/11/24/experimenting-with-go-type-parameters-generics-in-goland/)，由于笔者很少使用图形化的IDE，因此各位小伙伴可自行通过这篇博客https://blog.jetbrains.com/go/2020/11/24/experimenting-with-go-type-parameters-generics-in-goland/来了解具体情况。

### 5. 参考资料

- levonet/golang – https://hub.docker.com/r/levonet/golang
- dev.go2go branch – https://go.googlesource.com/go/+/refs/heads/dev.go2go/README.go2go.md

**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，感谢小伙伴们学习支持！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论