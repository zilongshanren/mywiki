---
title: Go 1.16中值得关注的几个变化
url: https://tonybai.com/2021/02/25/some-changes-in-go-1-16/
published: '2021-02-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.16中值得关注的几个变化

![img{512x368}](../../assets/e8411a97ed917d10.png)


辛丑牛年初七开工大吉的日子(2021.2.18)，Go核心开发团队为中国Gopher们献上了大礼 – [Go 1.16版本正式发布了](https://mp.weixin.qq.com/s/7tYi-61teL0kBmWz7q2SGw)！国内Gopher可以在[Go中国官网上](https://golang.google.cn/dl/)下载到Go 1.16在各个平台的安装包：

![img{512x368}](../../assets/efb1de07e1822381.png)


2020年双12，Go 1.16进入freeze状态，即不再接受新feature，仅fix bug、编写文档和接受安全更新等，那时我曾写过一篇名为[《Go 1.16新功能特性不完全前瞻》](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)的文章。当时Go 1.16的[发布说明](https://tip.golang.org/doc/go1.16)尚处于早期草稿阶段，要了解Go 1.16功能特性都有哪些变化，只能结合当时的release note以及从[Go 1.16里程碑](https://github.com/golang/go/issues?q=is%3Aissue+milestone%3AGo1.16+is%3Aclosed)中的issue列表中挖掘。

如今Go 1.16版本正式发布了，和当时相比，Go 1.16又有哪些变化呢？在这篇文章中，我们就来一起详细分析一下Go 1.16中那些值得关注的重要变化！

### 一. 语言规范

如果你是Go语言新手，想必你一定很期待一个大版本的发布会带来许多让人激动人心的语言特性。但是Go语言在这方面肯定会让你“失望”的。伴随着Go 1.0版本一起发布的[Go1兼容性承诺](https://tip.golang.org/doc/go1compat)给Go语言的规范加了一个“框框”，从Go 1.0到[Go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)版本，Go语言对语言规范的变更屈指可数，因此资深Gopher在阅读Go版本的release notes时总是很自然的略过这一章节，因为这一章节通常都是如下面这样的描述：

![img{512x368}](../../assets/f8c09cd2263bec27.png)


这就是[Go的设计哲学：简单](https://www.imooc.com/read/87/article/2321)！绝不轻易向语言中添加新语法元素增加语言的复杂性。除非是那些社区呼声很高并且是Go核心团队认可的。我们也可以将Go从1.0到Go 1.16这段时间称为“Go憋大招”的阶段，因为就在Go团队发布1.16版本之前不久，[Go泛型提案](https://mp.weixin.qq.com/s/Cnko3hrrcFKpsfdlj3yXdQ)正式被Go核心团队接受(Accepted)：

![img{512x368}](../../assets/e3ca7b40701f5ffe.png)


这意味着什么呢？这意味着在2022年2月份(Go 1.18)，Gopher们将迎来Go有史以来最大一次语言语法变更并且**这种变更依然是符合Go1兼容性承诺的**，这将避免Go社区出现Python3给Python社区带去的那种“割裂”。不过就像[《“能力越大，责任越大” – Go语言之父详解将于Go 1.18发布的Go泛型》](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)一文中Go语言之父[Robert Griesemer](https://github.com/griesemer)所说的那样：**泛型引入了抽象，但滥用抽象而没有解决实际问题将带来不必要的复杂性，请三思而后行**! 离泛型的落地还有一年时间，就让我们耐心等待吧！

### 二. Go对各平台/OS支持的变更

**Go语言具有良好的 可移植性，对各主流平台和OS的支持十分全面和及时**，Go官博曾

[发布过一篇文章](https://mp.weixin.qq.com/s/FQWMwZnT8xmCGe1Ing_luQ)，简要列出了自Go1以来对各主流平台和OS的支持情况：

- Go1（2012年3月）支持原始系统(译注：上面提到的两种操作系统和三种架构)以及64位和32位x86上的FreeBSD、NetBSD和OpenBSD，以及32位x86上的Plan9。
- Go 1.3（2014年6月）增加了对64位x86上Solaris的支持。
[Go 1.4](https://tonybai.com/2014/11/04/some-changes-in-go-1-4/)（2014年12月）增加了对32位ARM上Android和64位x86上Plan9的支持。[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)（2015年8月）增加了对64位ARM和64位PowerPC上的Linux以及32位和64位ARM上的iOS的支持。[Go 1.6](https://tonybai.com/2016/02/21/some-changes-in-go-1-6/)（2016年2月）增加了对64位MIPS上的Linux，以及32位x86上的Android的支持。它还增加了32位ARM上的Linux官方二进制下载，主要用于RaspberryPi系统。[Go 1.7](https://tonybai.com/2016/06/21/some-changes-in-go-1-7/)（2016年8月）增加了对的z系统（S390x）上Linux和32位x86上Plan9的支持。[Go 1.8](https://tonybai.com/2017/02/03/some-changes-in-go-1-8/)（2017年2月）增加了对32位MIPS上Linux的支持，并且它增加了64位PowerPC和z系统上Linux的官方二进制下载。[Go 1.9](https://tonybai.com/2017/07/14/some-changes-in-go-1-9/)（2017年8月）增加了对64位ARM上Linux的官方二进制下载。[Go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)（2018年2月）增加了对32位ARM上Windows10 IoT Core的支持，如RaspberryPi3。它还增加了对64位PowerPC上AIX的支持。[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14)（2019年2月）增加了对64位RISC-V上Linux的支持。

[Go 1.7版本](https://tonybai.com/2016/06/21/some-changes-in-go-1-7/)中新增的**go tool dist list**命令还可以帮助我们快速了解各个版本究竟支持哪些平台以及OS的组合。下面是Go 1.16版本该命令的输出：

```
$go tool dist list
aix/ppc64
android/386
android/amd64
android/arm
android/arm64
darwin/amd64
darwin/arm64
dragonfly/amd64
freebsd/386
freebsd/amd64
freebsd/arm
freebsd/arm64
illumos/amd64
ios/amd64
ios/arm64
js/wasm
linux/386
linux/amd64
linux/arm
linux/arm64
linux/mips
linux/mips64
linux/mips64le
linux/mipsle
linux/ppc64
linux/ppc64le
linux/riscv64
linux/s390x
netbsd/386
netbsd/amd64
netbsd/arm
netbsd/arm64
openbsd/386
openbsd/amd64
openbsd/arm
openbsd/arm64
openbsd/mips64
plan9/386
plan9/amd64
plan9/arm
solaris/amd64
windows/386
windows/amd64
windows/arm
```


通常我不太会过多关注每次Go版本发布时关于可移植性方面的内容，这次将可移植性单独作为章节主要是因为Go 1.16发布之前的**Apple M1芯片事件**！

![img{512x368}](../../assets/18cc7c14b0f39fae.jpg)


苹果公司再次放弃Intel x86芯片而改用自造的基于Arm64的M1芯片引发业界激烈争论。但现实是搭载Arm64 M1芯片的苹果笔记本已经大量上市，对于编程语言开发团队来说，能做的只有尽快支持这一平台。因此，Go团队给出了在Go 1.16版本中增加对Mac M1的原生支持。

在Go 1.16版本之前，Go也支持darwin/arm64的组合，但那更多是为了构建在iOS上运行的Go应用(利用[gomobile](https://github.com/golang/mobile))。

Go 1.16做了进一步的细分：将darwin/arm64组合改为apple M1专用；而构建在iOS上运行的Go应用则使用ios/arm64。同时，Go 1.16还增加了ios/amd64组合用于支持在MacOS(amd64)上运行的[iOS模拟器中运行Go应用](https://tip.golang.org/misc/ios/README)。

另外还值得一提的是在OpenBSD上，Go应用的系统调用需要通过libc发起，而不能再绕过libc而直接使用汇编指令了，这是出于对未来OpenBSD的一些兼容性要求考虑才做出的决定。

### 三. Go module-aware模式成为默认！

在泛型落地前，Go module依旧是这些年Go语言改进的重点(虽不是语言规范特性)。在Go 1.16版本中，Go module-aware模式成为了默认模式(另一种则是传统的gopath模式)。module-aware模式成为默认意味着什么呢？意味着GO111MODULE的值默认为on了。

自从Go 1.11加入go module，不同go版本在GO111MODULE为不同值的情况下开启的构建模式几经变化，上一次go module-aware模式的行为有较大变更还是在[Go 1.13版本](https://mp.weixin.qq.com/s/Txqvanb17LYQYgohNiUHig)中。这里将Go 1.13版本之前、Go 1.13版本以及Go 1.16版本在GO111MODULE为不同值的情况下的行为做一下对比，这样我们可以更好的理解go 1.16中module-aware模式下的行为特性，下面我们就来做一下比对：

| GO111MODULE | < Go 1.13 | Go 1.13 | Go 1.16 |
|---|---|---|---|
| on | 任何路径下都开启module-aware模式 | 任何路径下都开启module-aware模式 | 【默认值】：任何路径下都开启module-aware模式 |
| auto | 【默认值】：使用GOPATH mode还是module-aware mode，取决于要构建的源码目录所在位置以及是否包含go.mod文件。如果要构建的源码目录不在以GOPATH/src为根的目录体系下，且包含go.mod文件(两个条件缺一不可)，那么使用module-aware mode；否则使用传统的GOPATH mode。 | 【默认值】：只要当前目录或父目录下有go.mod文件时，就开启module-aware模式，无论源码目录是否在GOPATH外面 | 只有当前目录或父目录下有go.mod文件时，就开启module-aware模式，无论源码目录是否在GOPATH外面 |
| off | gopath模式 | gopath模式 | gopath模式 |

我们看到在Go 1.16模式下，依然可以回归到gopath模式。但Go核心团队已经决定拒绝[“继续保留GOPATH mode”的提案](https://github.com/golang/go/issues/37755)，并计划在Go 1.17版本中彻底取消gopath mode，仅保留go module-aware mode：

![img{512x368}](../../assets/b3a0e0eafb77d087.png)


虽然目前仍有项目没有转换到go module下，但根据调查，大多数项目已经选择拥抱go module并完成了转换工作，因此笔者认为即便Go 1.17真的取消了GOPATH mode，对整个Go社区的影响也不会太大了。

Go 1.16中，go module机制还有其他几个变化，这里逐一来看一下：

#### 1. go build/run命令不再自动更新go.mod和go.sum了

为了能更清晰看出Go 1.16与之前版本的差异，我们准备了一个小程序：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/go-modules/helloworld/go.mod
module github.com/bigwhite/helloworld
go 1.16
// github.com/bigwhite/experiments/blob/master/go1.16-examples/go-modules/helloworld/helloworld.go
package main
import "github.com/sirupsen/logrus"
func main() {
logrus.Println("Hello, World")
}
```


我们使用[go 1.15版本](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)构建一下该程序：

```
$go build
go: finding module for package github.com/sirupsen/logrus
go: downloading github.com/sirupsen/logrus v1.8.0
go: found github.com/sirupsen/logrus in github.com/sirupsen/logrus v1.8.0
$cat go.mod
module github.com/bigwhite/helloworld
go 1.16
require github.com/sirupsen/logrus v1.8.0
$cat go.sum
github.com/davecgh/go-spew v1.1.1/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/magefile/mage v1.10.0/go.mod h1:z5UZb/iS3GoOSn0JgWuiw7dxlurVYTu+/jHXqQg881A=
github.com/pmezard/go-difflib v1.0.0/go.mod h1:iKH77koFhYxTK1pcRnkKkqfTogsbg7gZNVY4sRDYZ/4=
github.com/sirupsen/logrus v1.8.0 h1:nfhvjKcUMhBMVqbKHJlk5RPrrfYr/NMo3692g0dwfWU=
github.com/sirupsen/logrus v1.8.0/go.mod h1:4GuYW9TZmE769R5STWrRakJc4UqQ3+QQ95fyz7ENv1A=
github.com/stretchr/testify v1.2.2/go.mod h1:a8OnRcib4nhh0OaRAV+Yts87kKdq0PP7pXfy6kDkUVs=
golang.org/x/sys v0.0.0-20191026070338-33540a1f6037 h1:YyJpGZS1sBuBCzLAR1VEpK193GlqGZbnPFnPV/5Rsb4=
golang.org/x/sys v0.0.0-20191026070338-33540a1f6037/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
```


在Go 1.15版本中，go build会自动分析源码中的依赖，如果go.mod中没有对该依赖的require，则会自动添加require，同时会将go.sum中将相关包(特定版本)的校验信息写入。

我们将上述helloworld恢复到初始状态，再用go 1.16来build一次：

```
$go build
helloworld.go:3:8: no required module provides package github.com/sirupsen/logrus; to add it:
go get github.com/sirupsen/logrus
```


我们看到go build没有成功，而是给出错误：go.mod中没有对logrus的require，并给出添加对logrus的require的方法(go get github.com/sirupsen/logrus)。

我们就按照go build给出的提示执行go get：

```
$go get github.com/sirupsen/logrus
go: downloading github.com/magefile/mage v1.10.0
go get: added github.com/sirupsen/logrus v1.8.0
$cat go.mod
module github.com/bigwhite/helloworld
go 1.16
require github.com/sirupsen/logrus v1.8.0 // indirect
$cat go.sum
github.com/davecgh/go-spew v1.1.1/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/magefile/mage v1.10.0 h1:3HiXzCUY12kh9bIuyXShaVe529fJfyqoVM42o/uom2g=
github.com/magefile/mage v1.10.0/go.mod h1:z5UZb/iS3GoOSn0JgWuiw7dxlurVYTu+/jHXqQg881A=
github.com/pmezard/go-difflib v1.0.0/go.mod h1:iKH77koFhYxTK1pcRnkKkqfTogsbg7gZNVY4sRDYZ/4=
github.com/sirupsen/logrus v1.8.0 h1:nfhvjKcUMhBMVqbKHJlk5RPrrfYr/NMo3692g0dwfWU=
github.com/sirupsen/logrus v1.8.0/go.mod h1:4GuYW9TZmE769R5STWrRakJc4UqQ3+QQ95fyz7ENv1A=
github.com/stretchr/testify v1.2.2/go.mod h1:a8OnRcib4nhh0OaRAV+Yts87kKdq0PP7pXfy6kDkUVs=
golang.org/x/sys v0.0.0-20191026070338-33540a1f6037 h1:YyJpGZS1sBuBCzLAR1VEpK193GlqGZbnPFnPV/5Rsb4=
golang.org/x/sys v0.0.0-20191026070338-33540a1f6037/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
$go build
//ok
```


我们看到go build并不会向go 1.15及之前版本那样做出有“副作用”的动作：自动修改go.mod和go.sum，而是提示开发人员显式通过go get来添加缺少的包/module，即便是[依赖包major版本升级](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)亦是如此。

从自动更新go.mod，到通过提供-mod=readonly选项来避免自动更新go.mod，再到Go 1.16的禁止自动更新go.mod，笔者认为这个变化是Go不喜“隐式转型”的一种延续，即尽量不支持任何可能让开发者产生疑惑或surprise的隐式行为（就像隐式转型），取而代之的是要用一种显式的方式去完成(就像必须显式转型那样)。

我们也看到在go 1.16中，添加或更新go.mod中的依赖，只有显式使用go get。go mod tidy依旧会执行对go.mod的清理，即也可以修改go.mod。

#### 2. 推荐使用go install安装Go可执行文件

在gopath mode下，go install基本“隐身”了，它能做的事情基本都被go get“越俎代庖”了。在go module时代初期，go install更是没有了地位。但Go团队现在想逐步恢复go install的角色：安装Go可执行文件！在Go 1.16中，当go install后面的包携带特定版本号时，go install将忽略当前go.mod中的依赖信息而直接编译安装可执行文件：

```
// go install回将gopls v0.6.5安装到GOBIN下
$go install golang.org/x/tools/gopls@v0.6.5
```


并且后续，Go团队会让go get将专注于分析依赖，并获取go包/module，更新go.mod/go.sum，而[不再具有安装可执行Go程序的行为能力](https://github.com/golang/go/issues/43684)，这样go get和go install就会各司其职，Gopher们也不会再被两者的重叠行为所迷惑了。现在如果不想go get编译安装，可使用go get -d。

#### 3. 作废module的特定版本

在[《如何作废一个已发布的Go module版本，我来告诉你！》](https://mp.weixin.qq.com/s/fg84g4OzSgoHDGbvVDbMKg)一文中，我曾详细探讨了Go引入module后如何作废一个已发布的go module版本。当时已经知晓Go 1.16会在go.mod中增加[retract指示符](https://github.com/golang/mod/commit/c0d644d00ab849f4506f17a98a5740bf0feff020)，因此也给出了在Go 1.16下retract一个module版本的原理和例子(基于当时的go tip)。

Go 1.16正式版在工具的输出提示方面做了进一步的优化，让开发人员体验更为友好。我们还是以一个简单的例子来看看在Go 1.16中作废一个module版本的过程吧。

在我的bitbucket账户下有一个名为m2的Go module(https://bitbucket.org/bigwhite/m2/)，当前它的版本为v1.0.0：

```
// bitbucket.org/bigwhite/m2
$cat go.mod
module bitbucket.org/bigwhite/m2
go 1.15
$cat m2.go
package m2
import "fmt"
func M2() {
fmt.Println("This is m2.M2 - v1.0.0")
}
```


我们在本地建立一个m2的消费者：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/go-modules/retract
$cat go.mod
module github.com/bigwhite/retractdemo
go 1.16
$cat main.go
package main
import "bitbucket.org/bigwhite/m2"
func main() {
m2.M2()
}
```


运行这个消费者：

```
$go run main.go
main.go:3:8: no required module provides package bitbucket.org/bigwhite/m2; to add it:
go get bitbucket.org/bigwhite/m2
```


由于上面提到的原因，go run不会隐式修改go.mod，因此我们需要手工go get m2：

```
$go get bitbucket.org/bigwhite/m2
go: downloading bitbucket.org/bigwhite/m2 v1.0.0
go get: added bitbucket.org/bigwhite/m2 v1.0.0
```


再来运行消费者，我们将看到以下运行成功的结果：

```
$go run main.go
This is m2.M2 - v1.0.0
```


现在m2的作者对m2打了小补丁，版本升级到了v1.0.1。这时消费者通过go list命令可以看到m2的最新版本(前提：go proxy server上已经cache了最新的v1.0.1)：

```
$go list -m -u all
github.com/bigwhite/retractdemo
bitbucket.org/bigwhite/m2 v1.0.0 [v1.0.1]
```


消费者可以通过go get将对m2的依赖升级到最新的v1.0.1：

```
$go get bitbucket.org/bigwhite/m2@v1.0.1
go get: upgraded bitbucket.org/bigwhite/m2 v1.0.0 => v1.0.1
$go run main.go
This is m2.M2 - v1.0.1
```


m2作者收到issue，有人指出v1.0.1版本有安全漏洞，m2作者确认了该漏洞，但此时v1.0.1版已经发布并被缓存到各大go proxy server上，已经无法撤回。m2作者便想到了Go 1.16中引入的retract指示符，于是它在m2的go.mod用retract指示符做了如下更新：

```
$cat go.mod
module bitbucket.org/bigwhite/m2
// 存在安全漏洞
retract v1.0.1
go 1.15
```


并将此次更新作为v1.0.2发布了出去！

之后，当消费者使用go list查看m2是否有最新更新时，便会看到retract提示：(前提：go proxy server上已经cache了最新的v1.0.2)

```
$go list -m -u all
github.com/bigwhite/retractdemo
bitbucket.org/bigwhite/m2 v1.0.1 (retracted) [v1.0.2]
```


执行go get会收到带有更详尽信息的retract提示和问题解决建议：

```
$go get .
go: warning: bitbucket.org/bigwhite/m2@v1.0.1: retracted by module author: 存在安全漏洞
go: to switch to the latest unretracted version, run:
go get bitbucket.org/bigwhite/m2@latest
```


于是消费者按照提示执行go get bitbucket.org/bigwhite/m2@latest：

```
$go get bitbucket.org/bigwhite/m2@latest
go get: upgraded bitbucket.org/bigwhite/m2 v1.0.1 => v1.0.2
$cat go.mod
module github.com/bigwhite/retractdemo
go 1.16
require bitbucket.org/bigwhite/m2 v1.0.2
$go run main.go
This is m2.M2 - v1.0.2
```


到此，retract的使命终于完成了！

#### 4. 引入GOVCS环境变量，控制module源码获取所使用的版本控制工具

出于安全考虑，Go 1.16引入GOVCS环境变量，用于在go命令直接从代码托管站点获取源码时对所使用的版本控制工具进行约束，如果是从go proxy server获取源码，那么GOVCS将不起作用，因为go工具与go proxy server之间使用的是[GOPROXY协议](https://tip.golang.org/ref/mod#goproxy-protocol)。

GOVCS的默认值为public:git|hg,private:all，即对所有公共module允许采用git或hg获取源码，而对私有module则不限制版本控制工具的使用。

如果要允许使用所有工具，可像下面这样设置GOVCS：

```
GOVCS=*:all
```


如果要禁止使用任何版本控制工具去直接获取源码（不通过go proxy），那么可以像下面这样设置GOVCS:

```
GOVCS=*:off
```


#### 5. 有关go module的文档更新

自打[Go 1.14版本](https://mp.weixin.qq.com/s/PVxdtvSXgNpiD65TUo-TCg)宣布go module生产可用后，Go核心团队在说服和帮助Go社区全面拥抱go module的方面不可谓不努力。在文档方面亦是如此，最初有关go module的文档仅局限于go build命令相关以及[有关go module的wiki](https://github.com/golang/go/wiki/Modules)。随着go module日益成熟，go.mod格式的日益稳定，Go团队在1.16版本中还将go module相关文档升级到go reference的层次，与go language ref等并列：

![img{512x368}](../../assets/d8b1d42f4abd7644.png)


我们看到有关go module的ref文档包括：

[Go Modules Reference](https://tip.golang.org/ref/mod)https://tip.golang.org/ref/mod[go.mod file reference](https://tip.golang.org/doc/modules/gomod-ref)https://tip.golang.org/doc/modules/gomod-ref

官方还编写了[详细的Go module日常开发时的使用方法](https://tip.golang.org/doc/#developing-modules)，包括：开发与发布module、module发布与版本管理工作流、升级major号等。

![img{512x368}](../../assets/ca908886f47b354a.png)


**建议每个gopher都要将这些文档仔细阅读一遍，以更为深入了解和使用go module**。

### 四. 编译器与运行时

#### 1. runtime/metrics包

在[《Go 1.16新功能特性不完全前瞻》](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)一文中，我们提到过：Go 1.16 新增了runtime/metrics包，以替代runtime.ReadMemStats和debug.ReadGCStats输出runtime的各种度量数据，这个包更通用稳定，性能也更好。限于篇幅这里不展开，后续可能会以单独的文章讲解这个新包。

#### 2. GODEBUG环境变量支持跟踪包init函数的消耗

GODEBUG=inittrace=1这个特性也保留在了Go 1.16正式版当中了。当GODEBUG环境变量包含inittrace=1时，Go运行时将会报告各个源代码文件中的init函数的执行时间和内存开辟消耗情况。我们用上面的helloworld示例(github.com/bigwhite/experiments/blob/master/go1.16-examples/go-modules/helloworld)来看看该特性的效果：

```
$go build
$GODEBUG=inittrace=1 ./helloworld
init internal/bytealg @0.006 ms, 0 ms clock, 0 bytes, 0 allocs
init runtime @0.037 ms, 0.031 ms clock, 0 bytes, 0 allocs
init errors @0.29 ms, 0.005 ms clock, 0 bytes, 0 allocs
init math @0.31 ms, 0 ms clock, 0 bytes, 0 allocs
init strconv @0.33 ms, 0.002 ms clock, 32 bytes, 2 allocs
init sync @0.35 ms, 0.003 ms clock, 16 bytes, 1 allocs
init unicode @0.37 ms, 0.10 ms clock, 24568 bytes, 30 allocs
init reflect @0.49 ms, 0.002 ms clock, 0 bytes, 0 allocs
init io @0.51 ms, 0.003 ms clock, 144 bytes, 9 allocs
init internal/oserror @0.53 ms, 0 ms clock, 80 bytes, 5 allocs
init syscall @0.55 ms, 0.010 ms clock, 752 bytes, 2 allocs
init time @0.58 ms, 0.010 ms clock, 384 bytes, 8 allocs
init path @0.60 ms, 0 ms clock, 16 bytes, 1 allocs
init io/fs @0.62 ms, 0.002 ms clock, 16 bytes, 1 allocs
init internal/poll @0.63 ms, 0.001 ms clock, 64 bytes, 4 allocs
init os @0.65 ms, 0.089 ms clock, 4472 bytes, 20 allocs
init fmt @0.77 ms, 0.006 ms clock, 32 bytes, 2 allocs
init bytes @0.84 ms, 0.004 ms clock, 48 bytes, 3 allocs
init context @0.87 ms, 0 ms clock, 128 bytes, 4 allocs
init encoding/binary @0.89 ms, 0.002 ms clock, 16 bytes, 1 allocs
init encoding/base64 @0.90 ms, 0.015 ms clock, 1408 bytes, 4 allocs
init encoding/json @0.93 ms, 0.002 ms clock, 32 bytes, 2 allocs
init log @0.95 ms, 0 ms clock, 80 bytes, 1 allocs
init golang.org/x/sys/unix @0.96 ms, 0.002 ms clock, 48 bytes, 1 allocs
init bufio @0.98 ms, 0 ms clock, 176 bytes, 11 allocs
init github.com/sirupsen/logrus @0.99 ms, 0.009 ms clock, 312 bytes, 5 allocs
INFO[0000] Hello, World
```


以下面这行为例：

```
init fmt @0.77 ms, 0.006 ms clock, 32 bytes, 2 allocs
```


- 0.77ms表示的是自从程序启动后到fmt包init执行所过去的时间(以ms为单位)
- 0.006 ms clock表示fmt包init函数执行的时间(以ms为单位)
- 312 bytes表示fmt包init函数在heap上分配的内存大小；
- 5 allocs表示的是fmt包init函数在heap上执行内存分配操作的次数。

#### 3. Go runtime默认使用MADV_DONTNEED

Go 1.15版本时，我们可以通过GODEBUG=madvdontneed=1让Go runtime使用MADV_DONTNEED替代MADV_FREE达到更积极的将不用的内存释放给OS的效果(如果使用MADV_FREE，只有OS内存压力很大时，才会真正回收内存)，这将使得通过top查看到的常驻系统内存(RSS或RES)指标更实时也更真实反映当前Go进程对os内存的实际占用情况(仅使用linux)。

在Go 1.16版本中，Go runtime将MADV_DONTNEED作为默认值了，我们可以用一个小例子来对比一下这种变化：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/runtime/memalloc.go
package main
import "time"
func allocMem() []byte {
b := make([]byte, 1024*1024*1) //1M
return b
}
func main() {
for i := 0; i < 100000; i++ {
_ = allocMem()
time.Sleep(500 * time.Millisecond)
}
}
```


我们在linux上使用go 1.16版本编译该程序，考虑到优化和inline的作用，我们在编译时关闭优化和内联：

```
$go build -gcflags "-l -N" memalloc.go
```


接下来，我们分两次运行该程序，并使用top监控其RES指标值：

```
$./memalloc
$ top -p 9273
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
9273 root 20 0 704264 5840 856 S 0.0 0.3 0:00.03 memalloc
9273 root 20 0 704264 3728 856 S 0.0 0.2 0:00.05 memalloc
... ...
$GODEBUG=madvdontneed=0 ./memalloc
$ top -p 9415
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
9415 root 20 0 704264 5624 856 S 0.0 0.3 0:00.03 memalloc
9415 root 20 0 704264 5624 856 S 0.0 0.3 0:00.05 memalloc
```


我们看到默认运行的memalloc(开启MADV_DONTNEED)，RES很积极的变化，当上一次显示5840，下一秒内存就被归还给OS，RES变为3728。而关闭MADV_DONTNEED（GODEBUG=madvdontneed=0）的memalloc，OS就会很lazy的回收内存，RES一直显示5624这个值。

#### 4. Go链接器的进一步进行[现代化改造](https://golang.org/s/better-linker)

新一代Go链接器的更新计划从Go 1.15版本开始，在Go 1.15版本链接器的性能、资源占用、最终二进制文件大小等方面都有了一定幅度的优化提升。Go 1.16版本延续了这一势头：相比于Go 1.15，官方宣称(在linux上)性能有20%-25%的提升，资源占用下降5%-15%。更为直观的是编译出的二进制文件的size，我实测了一下文件大小下降10%以上：

```
-rwxr-xr-x 1 tonybai staff 22M 2 21 23:03 my-large-app-demo*
-rwxr-xr-x 1 tonybai staff 25M 2 21 23:02 my-large-app-demo-go1.15*
```


并且和Go 1.15的链接器优化仅针对amd64平台和基于ELF格式的OS不同，**这次的链接器优化已经扩展到所有平台和os组合上**。

### 五. 标准库

#### 1. io/fs包

Go 1.16标准库新增io/fs包，并定义了一个fs.File接口用于表示一个只读文件树(tree of file)的抽象。之所以要[加入io/fs包并新增fs.File接口](https://github.com/golang/go/issues/41190)源于对[嵌入静态资源文件(embed static asset)的实现需求](https://github.com/golang/go/issues/41191)。虽说实现embed功能特性是直接原因，但io/fs的加入也不是“临时起意”，早在很多年前的godoc实现时，对一个抽象的文件系统接口的需求就已经被提了出来并给出了实现：

![](../../assets/29564c4e0009bcbc.png)


最终这份实现以godoc工具的[vfs包](https://github.com/golang/tools/tree/master/godoc/vfs)的形式一直长期存在着。虽然它的实现有些复杂，抽象程度不够，但却对[io/fs包的设计](https://github.com/golang/proposal/blob/master/design/draft-iofs.md)有着重要的参考价值。同时也部分弥补了[Rob Pike老爷子当年没有将os.File设计为interface的遗憾](https://github.com/golang/go/issues/14106)，[Ian Lance Taylor 2013年提出的增加VFS层的想法](https://github.com/golang/go/issues/5636)也一并得以实现。

io/fs包的两个最重要的接口如下：

```
// $GOROOT/src/io/fs/fs.go
// An FS provides access to a hierarchical file system.
//
// The FS interface is the minimum implementation required of the file system.
// A file system may implement additional interfaces,
// such as ReadFileFS, to provide additional or optimized functionality.
type FS interface {
// Open opens the named file.
//
// When Open returns an error, it should be of type *PathError
// with the Op field set to "open", the Path field set to name,
// and the Err field describing the problem.
//
// Open should reject attempts to open names that do not satisfy
// ValidPath(name), returning a *PathError with Err set to
// ErrInvalid or ErrNotExist.
Open(name string) (File, error)
}
// A File provides access to a single file.
// The File interface is the minimum implementation required of the file.
// A file may implement additional interfaces, such as
// ReadDirFile, ReaderAt, or Seeker, to provide additional or optimized functionality.
type File interface {
Stat() (FileInfo, error)
Read([]byte) (int, error)
Close() error
}
```


FS接口代表虚拟文件系统的最小抽象，File接口则是虚拟文件的最小抽象，我们可以基于这两个接口进行扩展以及对接现有的一些实现。io/fs包也给出了一些扩展FS的“样例”：

![](../../assets/b8198b8ae9f3aa9d.png)


这两个接口的设计也是“Go秉持定义小接口惯例”的延续(更多关于这方面的内容，可以参考我的专栏文章[《定义小接口是Go惯例》](https://www.imooc.com/read/87/article/2425))。

io/fs包的加入也契合了Go社区对vfs的需求，在Go团队决定加入io/fs并提交实现后，社区做出了积极的反应，在github上我们能看到好多为各类对象提供针对io/fs.FS接口实现的项目：

![](../../assets/eda860494f8b78d4.png)


io/fs.FS和File接口在后续Go演进过程中会像io.Writer和io.Reader一样成为Gopher们在操作类文件树时最爱的接口。

#### 2. embed包

在[《Go 1.16新功能特性不完全前瞻》](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)一文中我们曾重点说了Go 1.16将支持在Go二进制文件中嵌入静态文件并给出了一个在webserver中嵌入文本文件的例子：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/stdlib/embed/webserver/hello.txt
hello, go 1.16
// github.com/bigwhite/experiments/blob/master/go1.16-examples/stdlib/embed/webserver/main.go
package main
import (
_ "embed"
"net/http"
)
//go:embed hello.txt
var s string
func main() {
http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
w.Write([]byte(s))
}))
http.ListenAndServe(":8080", nil)
}
```


我们看到在这个例子，通过//go:embed hello.txt，我们可以轻易地将hello.txt的内容存储在包级变量s中，而s将作为每个http request的应答返回给客户端。

[在Go二进制文件中嵌入静态资源文件](https://github.com/golang/go/issues/41191)是Go核心团队对社区广泛需求的积极回应。在go 1.16以前，Go社区开源的类嵌入静态文件的项目不下十多个，在Russ Cox[关于embed的设计草案](https://github.com/golang/proposal/blob/master/design/draft-embed.md)中，他就列了十多个：

- github.com/jteeuwen/go-bindata(主流实现)
- github.com/alecthomas/gobundle
- github.com/GeertJohan/go.rice
- github.com/go-playground/statics
- github.com/gobuffalo/packr
- github.com/knadh/stuffbin
- github.com/mjibson/esc
- github.com/omeid/go-resources
- github.com/phogolabs/parcello
- github.com/pyros2097/go-embed
- github.com/rakyll/statik
- github.com/shurcooL/vfsgen
- github.com/UnnoTed/fileb0x
- github.com/wlbr/templify
- perkeep.org/pkg/fileembed

Go1.16原生支持嵌入并且给出一种开发者体验良好的实现方案，这对Go社区是一种极大的鼓励，也是Go团队重视社区声音的重要表现。

笔者认为embed机制是Go 1.16中玩法最多的一种机制，也是极具新玩法挖掘潜力的机制。在embed加入Go tip不久，很多Gopher就已经“脑洞大开”：

有通过embed嵌入版本号的：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/stdlib/embed/version/main.go
package main
import (
_ "embed"
"fmt"
"strings"
)
var (
Version string = strings.TrimSpace(version)
//go:embed version.txt
version string
)
func main() {
fmt.Printf("Version %q\n", Version)
}
// github.com/bigwhite/experiments/blob/master/go1.16-examples/stdlib/embed/version/version.txt
v1.0.1
```


有通过embed打印自身源码的：

```
// github.com/bigwhite/experiments/blob/master/go1.16-examples/stdlib/embed/printself/main.go
package main
import (
_ "embed"
"fmt"
)
//go:embed main.go
var src string
func main() {
fmt.Print(src)
}
```


更是有[将一个完整的、复杂的带有js支持的web站点直接嵌入到go二进制文件中的示例](https://blog.lawrencejones.dev/golang-embed/)，鉴于篇幅，这里就不一一列举了。

Go擅长于Web服务，而embed机制的引入粗略来看，可以大大简化web服务中资源文件的部署，估计这也是之前社区青睐各种静态资源文件嵌入项目的原因。embed估计也会成为Go 1.16中最被gopher们喜爱的功能特性。

不过embed机制的实现目前有如下一些局限：

- 仅支持在包级变量前使用//go:embed指示符，还不支持在函数/方法内的局部变量上应用embed指示符（当然我们可以通过将包级变量赋值给局部变量来过渡一下）；
- 使用//go:embed指示符的包必须以空导入的方式导入embed包，二者是成对出现的，缺一不可；

#### 3. net包的变化

在Go 1.16之前，我们检测在一个已关闭的网络上进行I/O操作或在I/O完成前网络被关闭的情况，只能通过匹配字符串”use of closed network connection”的方式来进行。之前的版本没有针对这个错误定义“哨兵错误变量”(更多关于哨兵错误变量的内容，可以参考我的专栏文章[《别笑！这就是 Go 的错误处理哲学》](https://www.imooc.com/read/87/article/2433))，Go 1.16增加了ErrClosed这个“哨兵错误变量”，我们可以通过errors.Is(err, net.ErrClosed)来检测是否是上述错误情况。

### 六. 小结

从Go 1.16版本变更的功能特性中，我看到了Go团队更加重视社区的声音，这也是Go团队一直持续努力的目标。在最新的Go proposal review meeting的结论中，我们还看到了这样的一个[proposal](https://github.com/golang/go/issues/43931)被accept：

![](../../assets/1a6409897dd9084d.png)


要知道这个proposal的提议是将在Go 1.18才会落地的泛型实现分支merge到Go项目master分支，也就是说在Go 1.17中就会包含“不会发布的”泛型部分实现，这在之前是不可能实现的(之前，新proposal必须有原型实现的分支，实现并经过社区测试与Go核心委员会评估后才会在特定版本merge到master分支)。虽说泛型的开发有其特殊情况，但能被accept，这恰证明了Go社区的声音在Go核心团队日益受到重视。

**如果你还没有升级到Go 1.16，那么现在正是时候**。

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.16-examples)下载。https://github.com/bigwhite/experiments/tree/master/go1.16-examples

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

考虑到部落尚处于推广期，这里仍然为大家准备了新人优惠券，虽然优惠幅度有所下降，但依然物超所值，早到早享哦！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！目前该技术专栏正在新春促销！关注我的个人公众号“iamtonybai”，发送“go专栏活动”即可获取专栏专属优惠码，可在订阅专栏时抵扣20元哦(2021.2月末前有效)。

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论