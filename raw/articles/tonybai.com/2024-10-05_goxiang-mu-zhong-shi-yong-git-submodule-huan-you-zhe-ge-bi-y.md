---
title: Go项目中使用Git Submodule，还有这个必要吗？
url: https://tonybai.com/2024/10/05/using-git-submodules-in-go-projects/
published: '2024-10-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go项目中使用Git Submodule，还有这个必要吗？

![](../../assets/bddf0331343bf73a.png)


[本文永久链接](https://tonybai.com/2024/10/05/using-git-submodules-in-go-projects) – https://tonybai.com/2024/10/05/using-git-submodules-in-go-projects

在软件开发中，依赖管理一直是一个重要的议题，特别是在像Go这样的编程语言中，随着项目的扩展，如何有效管理依赖变得至关重要。Git Submodule作为Git的一个重要功能，允许在一个Git仓库中嵌入另一个仓库，从而方便地管理跨项目的代码共享。然而，Go语言引入的Go Module机制似乎已经解决了依赖管理的问题，那么在Go项目中，是否还有使用Git Submodule的必要呢？本文将简单探讨一下Go项目中Git Submodule的使用方法，并分析它是否还值得使用。

## 1. Git Submodule是什么？

Git Submodule是Git版本管理工具提供的一个功能，允许你将一个Git仓库作为另一个Git仓库(主仓库)的子目录。主仓库通过记录Submodule的URL和commit hash来追踪Submodule。当你克隆一个包含Submodule的仓库时，需要额外的步骤来初始化和更新Submodule。

下面是一个将github.com/rsc/pdf仓库作为git submodule的示例。

我们先建立主仓库：

```
$mkdir main-project
$cd main-project
$go mod init main-project
$git init
$git add -A
$git commit -m"initial import" .
[master (root-commit) 8227e65] initial import
1 file changed, 3 insertions(+)
create mode 100644 go.mod
```


接下来，我们来添加submodule：

```
$git submodule add https://github.com/rsc/pdf.git
Cloning into '/Users/tonybai/Test/Go/submodule/main-project/pdf'...
remote: Enumerating objects: 48, done.
remote: Counting objects: 100% (30/30), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 48 (delta 21), reused 21 (delta 21), pack-reused 18 (from 1)
Unpacking objects: 100% (48/48), done.
$git commit -m "Add rsc/pdf as a submodule"
[master 2778170] Add rsc/pdf as a submodule
2 files changed, 4 insertions(+)
create mode 100644 .gitmodules
create mode 160000 pdf
```


git submodule在主仓库的顶层目录下创建一个.gitmodules文件：

```
$cat .gitmodules
[submodule "pdf"]
path = pdf
url = https://github.com/rsc/pdf.git
```


pdf子目录下的.git不再是目录而是一个文件，其内容指示了pdf仓库的git元数据目录的位置，即主仓库下的.git/modules/pdf下：

```
$cat pdf/.git
gitdir: ../.git/modules/pdf
```


git submodule这种机制的主要用途是当多个项目之间有共享代码时，避免将共享的代码直接复制到每个项目中，而是通过Submodule来引用外部仓库。这种方式使得共享代码的版本控制更加明确和独立，也方便了项目之间的更新、管理与版本控制。

通过git submodule status可以查看主仓库下各个submodule的当前状态：

```
$git submodule status
c47d69cf462f804ff58ca63c61a8fb2aed76587e pdf (v0.1.0-1-gc47d69c)
```


通过git submodule update还可以更新各个submodule到最新版本。 但通常在主仓库中会锁定Submodule的特定版本，通过锁定Submodule的版本，可以确保主仓库使用的是经过测试和验证的Submodule代码，这减少了因Submodule更新而导致的意外问题。同时，锁定版本还可以确保所有开发者和构建环境都使用完全相同版本的Submodule，这对于保证构建的一致性和可重现性至关重要。版本锁定让你还可以精确控制何时更新Submodule，你可以在准备好处理潜在的变更和进行必要的测试时，有计划地更新Submodule版本。submodule的版本锁定可以通过下面命令组合实现：

```
cd path/to/submodule
git checkout <specific-commit-hash>
cd -
git add path/to/submodule
git commit -m "Lock submodule to specific version"
```


这个提交会更新主仓库中记录的Submodule版本，其他克隆主仓库的人在初始化和更新Submodule时，就会自动获取到这个特定版本。

在以Git为版本管理工具的项目中，Submodule在以下一些场景中还是很有用的：

- 在多项目依赖场景下，我们可以使用Submodule共享公共库；
- 在大型单一仓库中，Submodule有助于我们模块化管理各个子项目；
- 统一对Submodule的版本进行严格管理，避免在更新时引入未测试的新代码。

submodule虽然可以解决一些问题，但由于增加了项目管理复杂度以及学习成本，应用算不上广泛，但也不乏一些知名的开源项目在使用，比如[git项目](https://github.com/git/git)自身、[openssl](https://github.com/openssl/openssl)、[qemu](https://github.com/qemu/qemu)等。

不过，对于Go项目而言，Go Modules是Go在Go 1.11引入的新的官方依赖管理机制，它通过go.mod文件声明依赖关系，通过go.sum文件确保依赖的完整性，实现了构建的可重现性。那么，在Go项目中还有必要引入sub modules吗？

这里我们先不下结论，而是先来看看Go项目引入submodule后该如何使用呢。

## 2. Go项目的Git Submodule使用方法

在前面我们在本地建立了一个main-project，然后将rsc/pdf作为submodule导入到了main-project中，main-project是一个Go项目，它的go.mod如下：

```
// main-project/go.mod
module main-project
go 1.23.0
```


我们现在就继续使用这个示例来看看Go项目中git submodule的使用方法。

我们先来看一种错误的使用方法：**使用相对路径**。

我们在main-project下建立一个main.go的源文件：

```
// main-project/main.go
package main
import (
_ "./pdf"
)
func main() {
println("ok")
}
```


建完后，整个main-project的目录布局如下：

```
$tree -F
.
├── go.mod
├── main.go
└── pdf/
├── LICENSE
├── README.md
├── lex.go
├── name.go
├── page.go
├── pdfpasswd/
│ └── main.go
├── ps.go
├── read.go
└── text.go
```


在第一版main.go中，我们期望使用相对路径来导入submomdule中的pdf包，运行main.go，我们得到下面结果：

```
$go run main.go
main.go:4:2: "./pdf" is relative, but relative import paths are not supported in module mode
```


我们看到：在go module构建模式下，Go已经**不再支持以相对路径导入Go包了**！但是如果我们直接通过rsc.io/pdf这个路径导入，那显然使用的就不是submodule中的pdf包了。

下面我们试试**第二种方法**，即将pdf目录看成main-project的子目录，**将pdf包看成是main-project这个module下的一个包**，这样pdf包在main-project这个module下的导入路径就变成了main-project/pdf：

```
// main-project/main.go
package main
import (
_ "main-project/pdf"
)
func main() {
println("ok")
}
```


这次构建和运行main.go，我们将得到正确的预期结果。

到这里，我们似乎**又找到了go module之外go项目依赖管理的新方法**，并且这种方法特别适合当某些依赖项目尚未发布，还无法直接通过Go Module导入的库，甚至是一些永远不会发布的内部库或私有库。这种方法让pdf看起来是main-project的一部分，但实际上pdf包的版本却是需要开发人员自己通过git submodule命令管理的，pdf包的版本无法用go.mod(和go.sum)控制，因为**它被视为是main-project的一部分了，而不是外部依赖包**。

如果你不想将其视为main-project的一部分，还想将其以外部依赖的方式管理起来，那就需要**利用到go module的replace或go.work了**。不过这种方法的前提是submodule下必须是一个go module，即有自己的go.mod。rsc.io/pdf包是一个legacy package，还没有自己的go.mod，我们先在本地pdf目录下为其添加一个go.mod：go mod init rsc.io/pdf。

接下来，我们先来简单看看用replace如何实现导入pdf包，我们需要修改一下main-project/go.mod：

```
// main-project/go.mod
module main-project
go 1.23.0
require rsc.io/pdf v0.1.1
replace rsc.io/pdf => ./pdf
```


这里我们用replace指示符将rsc.io/pdf替换为本地pdf目录下的go module，这样修改后，我们运行main.go也会得到正确的结果。

另外我们还可以使用[go.work](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18)来导入pdf，下面命令初始化一个go.work：

```
$go work init .
```


编辑go.work，添加workspace包含的路径：

```
go 1.23.0
use (
.
./pdf
)
```


这样go编译器会默认在当前目录和pdf目录下搜索rsc.io/pdf模块，运行main.go也是ok的。

相对于将pdf包看成是main-project module下的一个包并用main-project/pdf这个内部依赖的包导入路径的方法，使用replace或go.work的好处在于一旦pdf包得以发布，main.go可以无需修改pdf包导入路径，并可以基于go.mod精确管理pdf包的版本。

## 3. 小结

那么我们在Go项目中到底是否有必要使用sub modules呢？我们来小结一下。

总的来说，在大多数情况下，Go Modules确实已经覆盖了Git Submodule在Go项目中的主要功能，甚至做的更好，比如：Go Modules提供了更细粒度的版本控制，能自动解析和下载依赖，并也可以确保了构建的可重现性。因此，对于大多数Go项目而言，使用Go Modules已经足够满足依赖管理需求，而无需再使用git submodule。 并且，在Go项目以及Go社区的实践中，应对类似共享未发布的依赖包的场景(git submodule适用的场景)，使用replace或go.work是比较主流的实践，或者说go.work以及replace就是为了这种情况而添加的。

当然如果组织/公司内部尚未构建可以很好地支持[内部Go项目间依赖包获取、导入和管理](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)的基础设施，那么git submodule不失为一种可以在内部Go项目中实施的可行的依赖版本管理和控制方案。

最后，无论选择使用Git Submodule、Go Modules，还是两者结合，最重要的是要确保项目结构清晰，依赖关系明确，以便于团队协作和项目维护。

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
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论