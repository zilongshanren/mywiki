---
title: Go语言包管理简史
url: https://tonybai.com/2019/09/21/brief-history-of-go-package-management/
published: '2019-09-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言包管理简史

![img{512x368}](../../assets/18b542d4b21aed9b.png)


包管理是Go一直被诟病做得不好的功能之一。先前版本（[go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)之前）的主要缺点之一是go get是缺乏对依赖包版本的管理和对可复制构建(reproducible build)的支持。Go社区已经开发了一些包管理器和工具作为版本化包依赖的事实标准解决方案，如[glide](https://github.com/Masterminds/glide)，[dep](https://tonybai.com/2017/06/08/first-glimpse-of-dep)以及一些[辅助工具](https://github.com/golang/go/wiki/PackageManagementTools)等。

“我在生产构建中使用go get。” – 没有人这么说过。


Go语言的包管理实现可追溯到Google公司内的代码依赖管理（Google将内部所有源代码都存放在一个巨大的单体存储库中）。我们来分析一下在”Go module”之前Go语言的包管理工具都出了什么问题。

- 依赖包的版本化
- 依赖包的本地缓存(vendor)
- GOPATH的必要性

## 依赖包的版本化

go get默认情况下不支持包版本控制。go软件包管理的第一版实现背后的想法是-不需要包版本控制，不需要第三方包存储库，您可以从当前分支中构建所有内容。

在[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)之前的版本中，添加依赖项意味着将该依赖项的源代码仓库克隆到$GOPATH下面。就是这样，没有版本的概念。版本始终指向克隆时刻的主分支。出现了另一个主要问题是，当不同的项目需要依赖包的不同版本时，Go包管理工具无法实现。

## 依赖包的本地缓存(vendor)

依赖包本地缓存通常是指相关依赖包与项目存储在同一位置。这通常意味着将您的依赖项源码也提交到源管理系统中，例如Git。

考虑这样一种情况- A使用依赖项B，而B使用了C版本在1.5版本中引入一个功能，这时B必须确保A在构建时使用的也是C 1.5或更高版本。在[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)之前的版本中，没有一种机制可以在不重写导入路径的情况下将依赖包代码与命令绑定在一起。

## GOPATH的必要性

GOPATH存在的主要原因有两个：

- 在Go中，import声明通过其完全限定的导入路径来引用包。GOPATH存在可以方便Go工具计算GOPATH/src内的任何目录所涉及软件包的绝对导入路径。
- 它是Go get命令存储包依赖项的位置。

这有什么问题？

- GOPATH 不允许开发人员像其他语言一样选择任意喜欢的目录签出项目的源代码。
- 此外，GOPATH不允许开发人员同时检出某个项目（或其依赖项）的多个副本。

## Go Module介绍

[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)引入了对[Go模块](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)(module)的初步支持。下面摘自Go Wiki：

一个模块是一组相关的Go包的集合，这个包集合被当做一个独立的单元进行统一版本管理。模块精确记录了依赖要求并支持创建可复制的构建。


Go模块带来了三个重要的内置功能：

- go.mod文件，它与package.json或Pipfile文件的功能类似。
- 机器生成的传递依赖项描述文件 – go.sum。
- 不再有GOPATH限制。模块可以位于任何路径中。

```
$ go help mod
Go mod provides access to operations on modules.
Note that support for modules is built into all the go commands,
not just 'go mod'. For example, day-to-day adding, removing, upgrading,
and downgrading of dependencies should be done using 'go get'.
See 'go help modules' for an overview of module functionality.
Usage:
go mod <command> [arguments]
The commands are:
download download modules to local cache
edit edit go.mod from tools or scripts
graph print module requirement graph
init initialize new module in current directory
tidy add missing and remove unused modules
vendor make vendored copy of dependencies
verify verify dependencies have expected content
why explain why packages or modules are needed
Use "go help mod <command>" for more information about a command.
```


更多相关讨论在[这里](https://groups.google.com/forum/#!topic/golang-dev/a5PqQuBljF4)。

## 迁移到Go Module

要使用Go模块，请更新Go到1.11及以上版本。由于不再需要GOPATH，因此可以通过以下两种方式之一激活模块支持(译注：下面的行为仅适用于Go 1.11~[Go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12/)，[Go 1.13版本](https://tip.golang.org/doc/go1.13)默认开启Go module，无论是否在GOPATH下，除非GO111MODULE=off)：

- 在GOPATH/src之外的目录中调用Go命令，并在当前目录中存在一个有效的go.mod文件。
- 如果源码在GOPATH之下，Go模块将不起作用。要改变此行为，请设置环境变量GO111MODULE=on后再调用Go命令。

让我们通过以下简单的步骤开始迁移：

-
由于GOPATH不再必要的了，将module移出GOPATH。

-
在项目根目录中，创建初始模块定义 – go mod init github.com/username/repository。go mod还会自动转换现有的包管理器（如dep和Gopkg，glide以及

[其他六种](https://tip.golang.org/pkg/cmd/go/internal/modconv/?m=all#pkg-variables)）的依赖关系。这将创建一个名为go.mod的文件，该文件存储了模块名以及模块的依赖项及其版本。

```
$ cat go.mod
module github.com/deepsourcelabs/cli
go 1.12
require (
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e
github.com/getsentry/raven-go v0.2.0
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9
)
```


- 运行go build会创建一个go.sum文件，其中包含特定模块版本的内容的预期校验和。这是为了确保这些模块将来的下载内容与第一次下载是相同的。请注意，go.sum不是锁文件。

```
$ cat go.sum
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e h1:9574pc8MX6rF/QyO14SPHhM5KKIOo9fkb/1ifuYMTKU=
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e/go.mod h1:GJKEexRPVJrBSOjoqN5VNOIKJ5Q3RViH6eu3puDRwx4=
github.com/getsentry/raven-go v0.2.0 h1:no+xWJRb5ZI7eE8TWgIq1jLulQiIoLG0IfYxv5JYMGs=
github.com/getsentry/raven-go v0.2.0/go.mod h1:KungGk8q33+aIAZUIVWZDr2OfAEBsO49PX4NzFV5kcQ=
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9 h1:dIsTcVF0w9viTLHXUEkDI7cXITMe+M/MRRM2MwisVow=
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9/go.mod h1:bwawxfHBFNV+L2hUp1rHADufV3IMtnDRdf1r5NINEl0=
```


关于版本控制的注意事项：为了保持向后兼容性，如果模块的版本为v2或更高版本，则模板的主版本必须以/vN的形式被包含在go.mod文件中使用的模块路径的末尾。比如：module github.com/username/repository/v2


## 日常命令

### 列出依赖项

go list -m all 列出当前模块及其所有依赖项。

```
$ go list -m all
github.com/deepsourcelabs/cli
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e
github.com/getsentry/raven-go v0.2.0
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9
```


在go list输出中，当前模块（也称为主模块）始终是第一行，其后是路径排序所有依赖模块。


### 列出软件包的可用版本

go list -m -versions github.com/username/repository 列出软件包的可用版本。

```
$ go list -m -versions github.com/getsentry/raven-go
github.com/getsentry/raven-go v0.1.0 v0.1.1 v0.1.2 v0.2.0
```


### 添加依赖

添加依赖项是隐式的。在代码中导入依赖项后，运行go build或go test命令将获取模块的最新版本并将其添加到go.mod文件中。如果要显式添加依赖项，请运行go get github.com/username/repository。

### 依赖项的升级/降级

go get github.com/username/repository@vx.x.x下载并设置依赖项和更新go.mod文件的特定版本。

```
$ go get github.com/getsentry/raven-go@v0.1.2
go: finding github.com/getsentry/raven-go v0.1.2
go: downloading github.com/getsentry/raven-go v0.1.2
go: extracting github.com/getsentry/raven-go v0.1.2
$ cat go.mod
module github.com/deepsourcelabs/marvin-go
go 1.12
require (
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e
github.com/getsentry/raven-go v0.1.2
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9
)
$ cat go.sum
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e h1:9574pc8MX6rF/QyO14SPHhM5KKIOo9fkb/1ifuYMTKU=
github.com/certifi/gocertifi v0.0.0-20190410005359-59a85de7f35e/go.mod h1:GJKEexRPVJrBSOjoqN5VNOIKJ5Q3RViH6eu3puDRwx4=
github.com/getsentry/raven-go v0.1.2 h1:4V0z512S5mZXiBvmW2RbuZBSIY1sEdMNsPjpx2zwtSE=
github.com/getsentry/raven-go v0.1.2/go.mod h1:KungGk8q33+aIAZUIVWZDr2OfAEBsO49PX4NzFV5kcQ=
github.com/getsentry/raven-go v0.2.0 h1:no+xWJRb5ZI7eE8TWgIq1jLulQiIoLG0IfYxv5JYMGs=
github.com/getsentry/raven-go v0.2.0/go.mod h1:KungGk8q33+aIAZUIVWZDr2OfAEBsO49PX4NzFV5kcQ=
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9 h1:dIsTcVF0w9viTLHXUEkDI7cXITMe+M/MRRM2MwisVow=
github.com/pkg/errors v0.0.0-20190227000051-27936f6d90f9/go.mod h1:bwawxfHBFNV+L2hUp1rHADufV3IMtnDRdf1r5NINEl0=
```


### vendor依赖项

使用模块时，go命令将完全忽略vendor目录。为了向后兼容旧版Go，或确保将用于构建的所有文件一起存储在单个文件树中，请运行go mod vendor。

这将在主模块的根目录中创建一个vendor目录，并将依赖模块中的所有软件包存储在该目录中。

注意：要使用主模块的顶级vendor目录进行构建，请运行’go build -mod=vendor’。


### 删除未使用的依赖项

go mod tidy将删除未使用的依赖项并更新go.mod文件。

## 常见问题解答

-
GOPATH不再需要了？


是，永别了GOPATH。 -
默认情况下拉取哪个版本？


go.mod文件和go命令通常将语义版本用作描述模块版本的标准形式，以便可以比较版本以确定哪个版本应早于或晚于其他版本。v1.2.3通过在基础源存储库中标记(tag)修订来引入类似的模块版本。未标记(untag)的修订版可以使用“伪版本”之类的来引用：v0.0.0-yyyymmddhhmmss-abcdefabcdef，其中时间是UTC的提交时间，最后的后缀是提交哈希的前缀。 -
go.sum应该被检入到版本库中吗？


是。

鉴于本人近期较忙，又不希望让博客长草，近一段时间会挑选翻译一些笔者认为比较优秀的外文文章分享给大家。

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

> 运行go build会创建一个go.sum文件，其中包含特定模块版本的内容的预期校验和。这是为了确保这些模块将来的下载内容与第一次下载是相同的。请注意，go.sum不是锁文件。

这不就是锁文件的作用么

go.sum与类似dep的Gopkg.lock文件有区别。不知道您是否细致看过其中的内容：

go.sum内容节选：

github.com/beorn7/perks v0.0.0-20180321164747-3a771d992973/go.mod h1:Dwedo/Wpr24TaqPxmxbtue+5NUziq4I4S80YR8gNf3Q=

github.com/beorn7/perks v1.0.0/go.mod h1:KWe93zE9D1o94FZ5RNwFwVgaQK1VOXiVxmqh+CedLV8=

github.com/beorn7/perks v1.0.1/go.mod h1:G2ZrVWU2WbWT9wwq4/hrbKbnv/1ERSJQ0ibhJ6rlkpw=

我们看到，go.sum中对同一个module可能有多个版本，并存储不同版本的”校验值“；而lock文件仅仅会存一个固定的版本:

[[projects]]

branch = “master”

name = “github.com/bwmarrin/snowflake”

packages = ["."]

revision = “7d434bc4d8a584a6b7998a91e28380786b02cb00″

因此，go.sum实质是用来check，防止下载的module被串改。go.mod起到了原Gopkg.toml和Gopkg.lock的双重作用。