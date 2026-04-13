---
title: Go module机制下升级major版本号的实践
url: https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/
published: '2019-06-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go module机制下升级major版本号的实践

[Go module机制](https://tip.golang.org/cmd/go/#hdr-Module_proxy_protocol)在[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)引入，虽然也伴随着不小的质疑声，但总体上Go社区多数Gopher是接受go module的，很多标杆式的Go项目(比如kubernetes、kubernetes client-go等)也都逐渐转向了Go module，并且Gopher也在向core team反馈了自己的建议和问题。Go core team也在go module最初设计的基础上持续进行着改进，比如：即将到来的Go 1.13版本中将增加默认[GOPROXY(https://proxy.golang.org)](https://groups.google.com/forum/#!topic/golang-dev/4Kw_OfGa7cc)、GOSUMDB(sum.golang.org)；增加GONOPROXY、GONOSUMDB以应对私有module的处理；不断丰富的[go mod子命令功能](https://tip.golang.org/cmd/go/#hdr-Module_proxy_protocol)等。

随着Go module应用的日益逐步广泛和深入，Gopher们也开始遇到一些最初使用Go module时未曾遇到过的问题，比如升级major版本号（这是由于多数Go project仍处于untag的状态或者1.x.x状态，因此在go module引入初期，少有gopher遇到该类问题）。这篇文章我们就来简单看看如何在go module机制下面升级库的主版本号(major version number)。

## 一. Go module的“semantic import versioning”

在Russ Cox关于go module的系列论述文章[“semantic import versioning”](https://research.swtch.com/vgo-import)一文中，Russ说明了Go import包兼容性的总原则：

```
如果新旧版本的包使用相同的导入路径(import path)，那么新包与旧包是兼容的。
```


也就是说如果新旧两个包不兼容，那么应该采用不同的导入路径。

因此，Russ采用了将“major版本”作为导入路径的一部分的设计。这种设计支持在同一个项目或go source文件中import同一个module下的package的不同版本。同一个package虽然包名字相同，但是import path不同。**vN**作为import path的一部分将用于区分包的不同版本。同时在同一个源文件中，我们可以使用包别名的方式来区分同一个包的不同版本，比如：

```
import (
"github.com/bigwhite/foo/bar"
barV2 "github.com/bigwhite/foo/v2/bar"
... ...
)
```


go module的这种设计对Go包的consumer(包的使用者)来说似乎并未有太多额外工作，但是这给Go包的author们带来了一定的复杂性，他们需要考虑在go module机制下如何将自己的Go module升级major version。稍有不慎，可能就会导致自身代码库的混乱或者package consumer侧无法通过编译或执行行为的混乱。

下面我们就从go package author的角度实践一下究竟该如何做module major版本号的升级。Go module为go package author提供了两种major version升级的方案，我们下面逐一看一下。我们的实验环境基于[go 1.12.5](https://tonybai.com/2019/03/02/some-changes-in-go-1-12/) (ubuntu 16.04)。

## 二. 使用“major branch”方案

“major branch”方案对于多数gopher来说是一个过渡比较自然的方案，它通过建立vN分支并基于vN分支打vN.x.x的tag的方式做major version的升级。当然是否建立vN分支以及打vN.x.x tag都是一个可选的操作。

我们在bitbucket.org上建立一个公共仓库：bitbucket.org/bigwhite/modules-major-branch，其初始结构和代码如下(注意：此时本地开发环境中GO111MODULE=on)：

```
# tree -LF 2 modules-major-branch
modules-major-branch
├── foo/
│ └── foo.go
├── go.mod
└── README.md
1 directory, 3 files
//go.mod
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch
go 1.12
// foo.go
package foo
import "fmt"
func Foo() {
fmt.Println("foo.Foo of module: bitbucket.org/bigwhite/modules-major-branch pre-v1")
}
```


接下来，我们建立modules-major-branch/foo包的消费者项目：modules-major-branch-test

```
# tree -LF 1 ./modules-major-branch-test/
./modules-major-branch-test/
├── go.mod
├── go.sum
└── main.go
0 directories, 3 files
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch-test
go 1.12
# cat main.go
package main
import (
"bitbucket.org/bigwhite/modules-major-branch/foo"
)
func main() {
foo.Foo()
}
```


我们run一下“消费者”：

```
# go run main.go
go: finding bitbucket.org/bigwhite/modules-major-branch/foo latest
go: finding bitbucket.org/bigwhite/modules-major-branch latest
go: downloading bitbucket.org/bigwhite/modules-major-branch v0.0.0-20190602132049-2d924da2e295
go: extracting bitbucket.org/bigwhite/modules-major-branch v0.0.0-20190602132049-2d924da2e295
foo.Foo of module: bitbucket.org/bigwhite/modules-major-branch pre-v1
```


我们看到在这个阶段消费成功。

作为modules-major-branch的author，随着module功能演进，modules-major-branch到达了发布1.0版本的节点：

```
# cat foo/foo.go
package foo
import "fmt"
func Foo() {
fmt.Println("foo.Foo of module: bitbucket.org/bigwhite/modules-major-branch v1.0.0")
}
# git tag v1.0.0
# git push --tag origin master
```


接下来，我们让consumer升级对modules-major-branch/foo的依赖到v1.0.0。这种升级是不会自动进行，是需要consumer的开发者自己决策后手工进行的，否则会给开发者带来困惑。我们通过go mod edit命令修改consumer的require：

```
# go mod edit -require=bitbucket.org/bigwhite/modules-major-branch@v1.0.0
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch-test
go 1.12
require bitbucket.org/bigwhite/modules-major-branch v1.0.0
```


我们来运行一下升级依赖后的程序：

```
# go run main.go
go: finding bitbucket.org/bigwhite/modules-major-branch v1.0.0
go: downloading bitbucket.org/bigwhite/modules-major-branch v1.0.0
go: extracting bitbucket.org/bigwhite/modules-major-branch v1.0.0
foo.Foo of module: bitbucket.org/bigwhite/modules-major-branch v1.0.0
```


从pre-v1到v1在最新的go module机制中还算不上major版本的升级，接下来我们就来看看foo包的作者应该如何对modules-major-branch module做出不兼容的升级：v1 -> v2。

当modules-major-branch module即将做出不兼容升级时，一般会为当前版本建立维护分支(比如：v1分支，并在v1分支上继续对v1版本进行维护、打补丁)，然后再在master分支上做出不兼容的修改。

```
# git checkout -b v1
# git checkout master
# cat foo/foo.go
package foo
import "fmt"
func Foo2() {
fmt.Println("foo.Foo2 of module: bitbucket.org/bigwhite/modules-major-branch v2.0.0")
}
```


从代码可以看到，在master分支上，我们删除了foo包中的Foo函数，新增了Foo2函数。但仅做这些还不够。在本文一开始我们就提到过原则：如果新旧两个包不兼容，那么应该采用不同的导入路径。我们为modules-major-branch module做出了不兼容的修改，也需要modules-major-branch module有着不同的导入路径，我们需要修改modules-major-branch module的module根路径：

```
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch/v2
go 1.12
# git tag v2.0.0
# git push --tag origin master
```


我们在module根路径后面加上了v2，并基于master建立了tag: v2.0.0。

我们再来看看consumer端应该如何应对modules-major-branch module的不兼容修改。如果consumer要使用最新的Foo2函数的话，我们需要对main.go做出如下改动：

```
//modules-major-branch-test/main.go
package main
import (
"bitbucket.org/bigwhite/modules-major-branch/v2/foo"
)
func main() {
foo.Foo2()
}
```


接下来我们不需要手工修改modules-major-branch-test的go.mod中依赖，直接运行go run即可：

```
# go run main.go
go: finding bitbucket.org/bigwhite/modules-major-branch/v2/foo latest
go: finding bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0
go: downloading bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0
go: extracting bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0
foo.Foo2 of module: bitbucket.org/bigwhite/modules-major-branch v2.0.0
```


我们看到go编译器会自动发现依赖变更，并下载对应的包并更新go.mod和go.num：

```
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch-test
go 1.12
require (
bitbucket.org/bigwhite/modules-major-branch v1.0.0
bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0 // indirect
)
```


modules-major-branch-test此时已经不再需要依赖v1.0.0了，我们可以通过go mod tidy清理一下go.mod中的依赖：

```
# go mod tidy
# cat go.mod
module bitbucket.org/bigwhite/modules-major-branch-test
go 1.12
require bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0
```


我们看到：现在就只剩下对modules-major-branch v2的依赖了。

后续modules-major-branch可以在master分支上持续演进，直到又有不兼容改动时，可以基于master建立v2维护分支，master分支将升级为v3(module)。

再小结一下：

对包的作者而言，升级major版本号需要：

-
升级module的根路径，增加vN

-
建立vN.x.x形式的tag（可选，如果不打tag，go会在consumer的go.mod中使用伪版本号，比如：bitbucket.org/bigwhite/modules-major-branch/v2 v2.0.0-20190603050009-28a5b8da279e）


如果modules-major-branch内部有相互的包引用，那么在升级major号的时候，这些包的import路径也要增加vN，否则就会存在在高major version的代码中引用低major version包代码的情况，这也是包作者最容易忽略的事情。github.com/marwan-at-work/mod是一个为module作者提供的升级/降级major version号的工具，它可以帮助包作者方便地自动修改项目内所有源文件中的import path。有gopher已经[提出希望go官方提供upgrade/downgrade的支持](https://github.com/golang/go/issues/32014)，但目前core team尚未明确是否增加。

对于consumer而言，升级依赖包的major版本号，只需要在import包时在import path中增加vN即可，当然代码中也要针对不兼容的部分进行修改，然后go工具会自动下载相关包。

## 三. 使用 “major subdirectory”方案

go module机制还提供了一种我个人觉得较为怪异的方案或者说用起来不那么自然的方案，那就是利用子目录分割不同主版本。如果某个module目前已经演化到v3版本了，那么这个module所在仓库的目录结构应该是这样的：

```
# tree modules-major-subdir
modules-major-subdir
├── bar
│ └── bar.go
├── go.mod
├── v2
│ ├── bar
│ │ └── bar.go
│ └── go.mod
└── v3
├── bar
│ └── bar.go
└── go.mod
```


这里直接用vN作为子目录名字，在代码仓库中将不同版本module放置在不同的subdir中，这样即便不打tag，通过subdir也能找到对应版本的module包。以上图中的v2为例，该子目录下go.mod如下：

```
# cat go.mod
module bitbucket.org/bigwhite/modules-major-subdir/v2
go 1.12
```


v3也是类似。在各自子目录中，module的根路径都是带有vN扩展的。

接下来，我们就来创建consumer来分别调用不同版本的modules-major-subdir/bar包。和modules-major-branch-test类似，我们建立modules-major-subdir-test来作为consumer调用modules-major-subdir/bar包：

```
// modules-major-subdir-test
# cat go.mod
module bitbucket.org/bigwhite/modules-major-subdir-test
go 1.12
# cat main.go
package main
import (
"bitbucket.org/bigwhite/modules-major-subdir/bar"
)
func main() {
bar.Bar()
}
```


运行一下consumer：

```
# go run main.go
go: finding bitbucket.org/bigwhite/modules-major-subdir/bar latest
go: finding bitbucket.org/bigwhite/modules-major-subdir latest
go: downloading bitbucket.org/bigwhite/modules-major-subdir v0.0.0-20190603053114-50b15f581aba
go: extracting bitbucket.org/bigwhite/modules-major-subdir v0.0.0-20190603053114-50b15f581aba
bar.Bar of module: bitbucket.org/bigwhite/modules-major-subdir
```


我们修改main.go，调用v2版本bar包中Bar2函数：

```
package main
import (
"bitbucket.org/bigwhite/modules-major-subdir/v2/bar"
)
func main() {
bar.Bar2()
}
```


再次运行main.go：

```
# go run main.go
go: finding bitbucket.org/bigwhite/modules-major-subdir v0.0.0-20190603053114-50b15f581aba
go: downloading bitbucket.org/bigwhite/modules-major-subdir v0.0.0-20190603053114-50b15f581aba
go: extracting bitbucket.org/bigwhite/modules-major-subdir v0.0.0-20190603053114-50b15f581aba
go: finding bitbucket.org/bigwhite/modules-major-subdir/v2/bar latest
go: finding bitbucket.org/bigwhite/modules-major-subdir/v2 latest
go: downloading bitbucket.org/bigwhite/modules-major-subdir/v2 v2.0.0-20190603063223-4be5d54167e9
go: extracting bitbucket.org/bigwhite/modules-major-subdir/v2 v2.0.0-20190603063223-4be5d54167e9
bar.Bar2 of module: bitbucket.org/bigwhite/modules-major-subdir v2
```


我们看到：go编译器自动找到了位于modules-major-subdir仓库下v2子目录下的v2版本bar包。

从demo来看，似乎这种通过subdir方式来实现major version升级的方式更为“简单”一些。但笔者总感觉这种方式有些“怪”，尤其是在与tag交叉使用时可能会带来一些困惑，其他主流语言也鲜有使用这种方式进行major version升级的。另外一旦使用这种方式，似乎也很难利用git工具在不同major版本之间进行代码的merge（复用）了。

另外和major branch方案一样，如果module内部有相互的包引用，那么在升级major号的时候，这些包的import路径也要增加vN，否则也会存在在高major version的代码中引用低major version包代码的情况。

## 四. 小结

Go module作为主流语言依赖管理思路之外的一个“探索性”创新，势必在初期要有一段坎坷的道路要走。好事多磨，相信经过Go 1.11~Go 1.13三个版本的改进以及社区在工具方面对go module的逐渐的完善的支持，Go module会成为gopher日常Go开发的一柄利器，彻底解决Go的包依赖问题。

上述demo源码可在bitbucket.org/bigwhite下找到。

另外这里要提一点：国内的码云(gitee.com)目前对go module major version升级支持的还有问题。同样的操作，但在gitee.com下总是提示：**“go.mod has post-v0 module path”**。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

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

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

国内可以直接使用 goproxy.io