---
title: 小厂内部私有Go module拉取方案3
url: https://tonybai.com/2023/03/03/the-approach-to-go-get-private-go-module-in-house-part3/
published: '2023-03-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 小厂内部私有Go module拉取方案3

![](../../assets/eeb8d5c4f7051fbd.png)


[本文永久链接](https://tonybai.com/2023/03/03/the-approach-to-go-get-private-go-module-in-house-part3) – https://tonybai.com/2023/03/03/the-approach-to-go-get-private-go-module-in-house-part3

## 1. 缘起

我们的Go团队这两年完全是按照之前写的[《小厂内部私有Go module拉取方案》](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)和[《小厂内部私有Go module拉取方案（续）》](https://tonybai.com/2022/06/18/the-approach-to-go-get-private-go-module-in-house-part2)中的方案搭建的内部拉取私有仓库的基础设施，总体感觉不错，目前也没有什么大问题。

唯一麻烦一点的，就像[《小厂内部私有Go module拉取方案》](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)中提到的，当新增一些用作私有依赖包的repo时，govanityurls的vanity.yml需要手动更新或通过工具自动更新。维护这样一套设施，开发人员肯定不喜欢去做。

月初一位同事的主机发现无法通过内部的GOPROXY server拉取私有module，虽然事后证明这很是网络层面的问题，但也引发我的思考，在统一代理之外是否有拉取私有module的补充方案？恰好前些天，组内一童鞋分享了[Rust](https://tonybai.com/tag/rust)直接用内部自建的gitlab上的一个repo作为依赖的方法，只需要在cargo.toml中做简单配置：

```
foo-rs = {git = "http://192.168.10.10/ard/foo-rs", branch = "master"}
```


基于go module目前的机制是否可以支持类似Rust这种相对优雅的方案呢？本着当时对go.mod配置与go get的认知一时没有想出来:(。不过心中也大致给这样的方案画出了一个框框：

- 基于现有go.mod语法
- 改动最小
- 用go.mod而非go.work，这样可提交到代码库做版本管理，所有组员均可使用

我想到了基于go mod replace来做，当然需要对replace做一些扩展，于是我向go官方项目提交了[proposal](https://github.com/golang/go/issues/58736)！

## 2. 提案(proposal)

[提案](https://github.com/golang/go/issues/58736)的核心就是扩展go mod的replace语法，让replace的target支持一个remote的vcs仓库，下面是一个例子：

```
module github.com/bigwhite/demo
go 1.20
require (
mycompany.com/go/common v1.1.0
)
replace mycompany.com/go/common v1.1.0 => 192.168.10.159/ard/go/common v1.1.0
//或 replace mycompany.com/go/common => 192.168.10.159/ard/go/common
//或 replace mycompany.com/go/common => 192.168.10.159/ard/go/common v1.1.0
//或 replace mycompany.com/go/common v1.1.0 => 192.168.10.159/ard/go/common
```


这样我们既可保留我们为私有module自定义的cannoical import paths（如mycompany.com/go/common)，又可以方便基于自建vcs server拉取私有module。

## 3. 反转

我的提案提出没两个小时就被close了，我去看了一下详情，[seankhliao](https://github.com/seankhliao)回复：**Go现在已经支持这种用法**，并给出一个例子：

```
192.168.10.159/ard/go/common.git
```


我不确定seankhliao是否完全理解了我的提案，但他的回复还是让我开始怀疑我是否遗漏了什么。于是我又去重新学习了一下[go module的reference](https://go.dev/ref/mod#private-module-proxy-direct)以及[go cmd的reference](https://pkg.go.dev/cmd/go#hdr-Remote_import_paths)，之后脑子中形成了一个待确认的方案。

当前go.mod的replace指示符语法如下：

```
replace module-path [module-version] => replacement-path [replacement-version]
```


其中的replacement-path [replacement-version]构成target部分，目前支持两种target：

一种是module path，如：

```
replace example.com/othermodule => example.com/othermodule v1.2.3
```


另外一种是本地文件系统中的路径：

```
replace example.com/othermodule => ../othermodule
```


需要注意的是当replacement-path使用module path时必须带有replacement-version，下面的例子会导致go编译或运行命令报错：

```
replace example.com/othermodule v1.2.3 => example.com/othermodule
```


以前我总以为当replacement-path使用module path时，这个module path必须是那种带有域名的repo地址，根据seankhliao的例子，这块似乎也可以是一个诸如：“192.168.10.159/ard/go/common.git”的remote repo，如果是这样，那么即便不使用统一的内部go proxy，我们也可以直接从内部的自建vcs server上拉取private module了，下面我们就来验证一下这个方案。

## 4. 方案的确认试验

下面是试验环境的拓扑：

![](../../assets/9e0ed6a2931330f1.png)


这个拓扑与带有统一go proxy代理的方案完全不同：

- 对于外部的public module，我们采用外部public go proxy(比如：goproxy.io或goproxy.cn等)去拉取；
- 对于托管在内部vcs server的private module，我们采用直连(direct)方式拉取；
- 对于托管在github上的private module(使用private repo)，我们也采用直连(direct)方式拉取。

显然我们的新方案需要解决的是后面两种情况。

为了更直观地说明新方案，我们假设我们的一个go应用依赖了三个private包，他们的情况分别是：

- privatemodule1

repo放在内部gitlab上，其自定义cannoical import path为：mycompany.com/go/privatemodule1，实际地址为http://10.10.30.30/ard/incubators/privatemodule1.git

```
$tree -L 1 -F privatemodule1
privatemodule1
├── go.mod
├── privatemodule1.go
└── README.md
$cat privatemodule1/go.mod
module mycompany.com/go/privatemodule1
go 1.19
$cat privatemodule1/privatemodule1.go
package privatemodule1
import "fmt"
func F() {
fmt.Println("invoke F of mycompany.com/go/privatemodule1")
}
```


- privatemodule2

repo放在github的private repo中，其自定义cannoical import path为：mycompany.com/go/privatemodule2，实际地址为https://github.com/bigwhite/privatemodule2

```
$tree -L 1 -F privatemodule2
privatemodule2
├── go.mod
├── privatemodule2.go
└── README.md
$cat privatemodule2/go.mod
module mycompany.com/go/privatemodule2
go 1.19
$cat privatemodule2/privatemodule2.go
package privatemodule2
import "fmt"
func F() {
fmt.Println("invoke F of mycompany.com/go/privatemodule2")
}
```


- privatemodule3

repo放在github的private repo中，如：github.com/bigwhite/privatemodule3，但无自定义cannoical import path。

```
$tree -L 1 -F privatemodule3
privatemodule3
├── go.mod
├── privatemodule3.go
└── README.md
$cat privatemodule3/go.mod
module github.com/bigwhite/privatemodule3
go 1.19
$cat privatemodule3/privatemodule3.go
package privatemodule3
import "fmt"
func F() {
fmt.Println("invoke F of github.com/bigwhite/privatemodule3")
}
```


这三种情况应该可以覆盖日常Go开发的绝大多数private module依赖的情况了。下面我们分别看看如何获取这三类private module，我们先从最简单的privatemodule3开始。

### 1) 拉取github.com/bigwhite/privatemodule3

我们先建立依赖privatemodule3的go app：

```
$cat go.mod
module app
go 1.19
$cat app.go
import (
"github.com/bigwhite/privatemodule3"
)
func main() {
privatemodule3.F()
}
```


此时GOPROXY和GOPRIVATE的设置为：

```
$echo $GOPROXY
https://goproxy.io|direct
$echo $GOPRIVATE
github.com/bigwhite/privatemodule3
```


这样可以保证go工具链通过直连方式去拉取privatemodule3。

当我们试图用go mod tidy命令去拉取privatemodule3时，你可能会遇到如下错误：

```
$go mod tidy
go: finding module for package github.com/bigwhite/privatemodule3
app imports
github.com/bigwhite/privatemodule3: module github.com/bigwhite/privatemodule3: git ls-remote -q origin in /home/tonybai/go/pkg/mod/cache/vcs/2caadc923a575b0b63719d0d8b47b67a3559b4dbae40951b750f317880784ada: exit status 128:
fatal: unable to access 'https://github.com/bigwhite/privatemodule3/': GnuTLS recv error (-54): Error in the pull function.
```


这是因为[go get默认使用https方式拉取repo](https://go.dev/doc/faq#git_https)。如果你没有配置.netrc的方式访问github.com或没有将https请求转换为git+ssh请求，那么**即便你在github的personal profile下配置了SSH key，你仍然会遇到上述错误**！

解决方法有两种：

- 如果你已经在github personal profile中配置了SSH key，那么你可以通过.gitconfig将https请求替换为git+ssh请求

配置方式为在~/.gitconfig中添加如下内容：

```
[url "git@github.com:"]
insteadOf = https://github.com/
```


- 如果你操作github仓库时想使用的personal access token，那么你可以通过配置~/.netrc通过github对go get https请求的鉴权

配置方式为在~/.netrc中添加如下内容：

```
machine github.com
login user
password your_personal_access_token
```


上面两种方式二选一即可，无论是哪种方式，配置ok后，再执行go mod tidy，你将成功拉取github.com上面的私有module，就像下面示例中输出的结果那样：

```
$go mod tidy
go: finding module for package github.com/bigwhite/privatemodule3
go: downloading github.com/bigwhite/privatemodule3 v0.0.0-20230227061700-3762215e798f
go: found github.com/bigwhite/privatemodule3 in github.com/bigwhite/privatemodule3 v0.0.0-20230227061700-3762215e798f
$go run app.go
invoke F of github.com/bigwhite/privatemodule3
```


在下面的示例中，我们针对github.com上的私有module将使用.gitconfig将https请求替换为git+ssh的方式，之后就不赘述了。

注：在国内通过https请求访问github.com时，连通率较低。而git+ssh的方式，则一般都能拉取成功。


### 2) 拉取位于github.com上的私有module：mycompany.com/go/privatemodule2

接下来，我们来拉取位于github.com上的私有module：privatemodule2，与第一种情况不同的是，这次privatemodule2有了自己的cannoical import path，即mycompany.com/go/privatemodule2。我们来看看app.go的变化：

```
// app.go
package main
import (
"github.com/bigwhite/privatemodule3"
"mycompany.com/go/privatemodule2"
)
func main() {
privatemodule3.F()
privatemodule2.F()
}
```


我们将mycompany.com/go和privatemodule2加入到GOPRIVATE中：

```
$echo $GOPRIVATE
github.com/bigwhite/privatemodule3,mycompany.com/go,github.com/bigwhite/privatemodule2
```


此时，由于mycompany.com这个域名并不存在(假设不存在)，所以你执行go mod tidy拉取privatemodule2时势必会出现类似下面的错误：

```
$go mod tidy
go: finding module for package mycompany.com/go/privatemodule2
app imports
mycompany.com/go/privatemodule2: cannot find module providing package mycompany.com/go/privatemodule2: unrecognized import path "mycompany.com/go/privatemodule2": https fetch: Get "https://mycompany.com/go/privatemodule2?go-get=1": dial tcp 52.5.196.34:443: i/o timeout
```


我们的方案是使用replace指示符将mycompany.com/go/privatemodule2替换为私有repo：github.com/bigwhite/privatemodule2：

```
//go.mod
module app
go 1.19
require (
github.com/bigwhite/privatemodule3 v0.0.0-20230227061700-3762215e798f
mycompany.com/go/privatemodule2 v1.0.0
)
replace mycompany.com/go/privatemodule2 v1.0.0 => github.com/bigwhite/privatemodule2 v0.0.0-20230227061454-a2de3aaa7b27
```


前面提到过replace的target如果使用module path，其必须带上replacement version，那么这里的v0.0.0-20230227061454-a2de3aaa7b27是从何而来的呢？这个的确是一个**比较烦的事情**，不过我们可以通过go list来获取：

```
$go list -m github.com/bigwhite/privatemodule2@latest
github.com/bigwhite/privatemodule2 v0.0.0-20230227061454-a2de3aaa7b27
```


注：如果将来privatemodule2有了tag，那么我们就不需使用伪版本号来作为replacement version了。另外这里require中的privatemodule2使用的v1.0.0是一个虚拟的版本号，只是为了满足go.mod的语法要求，真正的版本是replacement version。


接下来的事情就与预期的一致了：

```
$go mod tidy
go: downloading github.com/bigwhite/privatemodule2 v0.0.0-20230227061454-a2de3aaa7b27
$go run app.go
invoke F of github.com/bigwhite/privatemodule3
invoke F of mycompany.com/go/privatemodule2
```


### 3) 拉取位于内部gitlab上的私有module：mycompany.com/go/privatemodule1

最后，我们来拉取位于内部gitlab上的私有module：privatemodule1，与第两种情况相同的是，这次privatemodule1也有自己的cannoical import path，即mycompany.com/go/privatemodule1。我们来看看app.go的变化：

```
// app.go
package main
import (
"github.com/bigwhite/privatemodule3"
"mycompany.com/go/privatemodule2"
"mycompany.com/go/privatemodule1"
)
func main() {
privatemodule3.F()
privatemodule2.F()
privatemodule1.F()
}
```


针对内部的gitlab vcs server，我们可以简单的使用.netrc中配置personal access token的方式来使用https请求，配置方法见上面。

go.mod变为：

```
module app
go 1.19
require (
github.com/bigwhite/privatemodule3 v0.0.0-20230227061700-3762215e798f
mycompany.com/go/privatemodule1 v1.0.0
mycompany.com/go/privatemodule2 v1.0.0
)
replace (
mycompany.com/go/privatemodule1 v1.0.0 => 10.10.30.30/ard/incubators/privatemodule1.git v0.0.0-20230227061032-c4a6ea813d1a
mycompany.com/go/privatemodule2 v1.0.0 => github.com/bigwhite/privatemodule2 v0.0.0-20230227061454-a2de3aaa7b27
)
```


我们需要将10.10.30.30加入到GOPRIVATE中，这样可以提高获取效率(否则go get会先尝试通过go proxy server获取)：

```
$echo $GOPRIVATE
github.com/bigwhite/privatemodule3,mycompany.com/go,10.10.30.30,github.com/bigwhite/privatemodule2
```


这里还需要明确一下privatemodule1的伪版本号(v0.0.0-20230227061032-c4a6ea813d1a)的获取方法：

```
$go list -m 10.10.30.30/ard/incubators/privatemodule1.git@latest
10.10.30.30/ard/incubators/privatemodule1.git v0.0.0-20230227061032-c4a6ea813d1a
```


注：如果你的gitlab server没有开启https，那么需要设置export GOINSECURE=10.10.30.30。


接下来的事情就也与预期的一致了：

```
$go mod tidy
go: downloading 10.10.30.30/ard/incubators/privatemodule1.git v0.0.0-20230227061032-c4a6ea813d1a
$go run app.go
invoke F of github.com/bigwhite/privatemodule3
invoke F of mycompany.com/go/privatemodule2
invoke F of mycompany.com/go/privatemodule1
```


## 5. 小结

综上，基于当前的go.mod的语法，我们可以实现各种情况下的private module拉取，而无需使用统一的内部go proxy服务。不过，从整个过程来看，这个方案仍然不完美，主要是因为replacement部分使用的是module path，这要求必须搭配replacement version，而这个replacement version的获得方式比较麻烦，尤其是在没有目标repo尚没有tag的情况下。

不过该方案可作为统一go proxy服务方案之外的补充方案。

Go官方也还会继续改进对private module拉取的支持，目前有两个issue可继续跟踪：

- proposal: cmd/go: allow GOPRIVATE to provide source repository URI – https://github.com/golang/go/issues/45611
- proposal: cmd/go: extend syntax go.mod to allow overriding fetch protocol – https://github.com/golang/go/issues/39536

本文涉及代码可以在[这里](https://github.com/bigwhite/experiments/blob/master/private-modules)下载 – https://github.com/bigwhite/experiments/blob/master/private-modules

## 6. 参考资料

- https://go.dev/ref/mod#private-module-proxy-direct
- https://pkg.go.dev/cmd/go#hdr-Remote_import_paths
- https://go.dev/doc/faq#git_https

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论