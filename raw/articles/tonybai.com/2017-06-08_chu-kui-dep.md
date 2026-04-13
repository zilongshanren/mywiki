---
title: 初窥dep
url: https://tonybai.com/2017/06/08/first-glimpse-of-dep/
published: '2017-06-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 初窥dep

[Go语言](http://tonybai.com/tag/go)程序组织和构建的基本单元是[Package](http://tonybai.com/2015/03/09/understanding-import-packages/)，但Go语言官方却没有提供一款“像样的”Package Management Tool(包管理工具)。随着Go语言在全球范围内应用的愈加广泛，缺少官方包管理工具这一问题变得日益突出。

2016年[GopherCon大会](https://www.gophercon.com/)后，在[Go官方](https://golang.org/)的组织下，一个旨在改善Go包管理的[commitee](https://groups.google.com/forum/#!topic/go-package-management)成立了，共同应对Go在package management上遇到的各种问题。经过各种脑洞和讨论后，该commitee在若干月后发布了“[Package Management Proposal](https://groups.google.com/forum/#!topic/go-package-management/P8TehVoFLjg)”，并启动了最有可能被接纳为官方包管理工具的项目[dep](https://github.com/golang/dep)的设计和开发。2017年年初，dep项目正式对外开放。截至目前，dep发布了[v0.1.0版本](https://github.com/golang/dep/releases/tag/v0.1.0)，并处于alpha测试阶段。

可以说，dep的进展还是蛮快的。按照dep官方说法，dep目前的[manifest和lock文件格式](https://github.com/golang/dep/blob/master/FAQ.md#what-is-the-difference-between-gopkgtoml-the-manifest-and-gopkglock-the-lock)已经stable，并保证向后兼容。同时，dep实现了“自举”，即dep使用自己作为自己的包管理工具。由于dep的“特殊身份”，虽然dep离成熟尚远，但dep的进展也吸引了诸多gopher的目光，很多组织已经开始将package management tool迁移为dep，为dep进行早期测试。

这里，我也打算“尝尝鲜”，在本篇文章中和大家一起窥探和试用一下dep。

## 一、Go包管理的演进历史

### 1、go get

在管窥dep之前，我们先来简单看看Go语言包管理的演进历史。首当其冲的就是go get。

Go语言新手在初次接触Go语言时会感觉到Go语言的package获取真的是很方便：只需一行go get xxx，github.com上的大量go package就可以随你取用。 但随着对Go语言使用的深入，人们会发现go get给我们带来方便的同时，也带来了不少的麻烦。go get本质上是[git](https://git-scm.com/)、[hg](https://www.mercurial-scm.org/)等这些[vcs](https://en.wikipedia.org/wiki/Version_control)工具的高级wrapper。对于使用git的go package来说，go get的实质就是将package git clone到本地的特定目录下（$GOPATH/src），同时go get可以自动解析包的依赖，并自动下载相关依赖包。

go get机制的设计很大程度上源于Google公司内部的单一root的代码仓库的开发模式，并且似乎google内部各个project/repository的master分支上的代码都是被认为stable的，因此go get仅仅支持获取master branch上的latest代码，没有指定version、branch或revision的能力。而在Google公司以外的世界里，这样的做法会给gopher带来不便：依赖的第三方包总是在变。一旦第三方包提交了无法正常build或接口不兼容的代码，依赖方立即就会受到影响。

而gopher们又恰恰希望自己项目所依赖的第三方包能受到自己的控制，而不是随意变化。这样，[godep](https://github.com/tools/godep)、[gb](https://getgb.io/)、[glide](https://github.com/Masterminds/glide)等一批第三方包管理工具出现了。

以应用最为广泛的[godep](http://tonybai.com/2014/10/30/a-hole-of-godep/)为例。为了能让第三方依赖包“稳定下来”，实现项目的reproduceble build，godep将项目当前依赖包的版本信息记录在Godeps/Godeps.json中，并将依赖包的相关版本存放在Godeps/_workspace中。在编译时(godep go build)godep通过临时修改GOPATH环境变量的方法让go编译器使用缓存在Godeps/_workspace下的项目依赖的特定版本的第三方包，这样保证了项目不再受制于依赖的第三方包的master branch上的latest代码的变动了。

不过，godep的“版本管理”本质上是通过缓存第三方库的某个revision的快照实现的，这种方式依然让人感觉难于管理。同时，通过对GOPATH的“偷梁换柱”的方式实现使用Godeps/_workspace中的第三方库的快照进行编译也无法兼容Go原生编译器，必须使用godep go xxx来进行。

为此，Go进一步[引入vendor机制](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)来*减少gopher在包管理问题上的心智负担*。

### 2、vendor机制

Go team也一直在关注Go语言包依赖的问题，尤其是在[Go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)实现自举的情况下，官方同样在1.5版本中推出了[vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)。vendor机制是[Russ Cox](https://swtch.com/~rsc/)在[Go 1.5发布](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)前期以一个experiment feature身份紧急加入到go中的([go 1.6](http://tonybai.com/2016/02/21/some-changes-in-go-1-6/)脱离experiment身份)。vendor标准化了项目依赖的第三方库的存放位置（不再需要Godeps/_workspace了），同时也无需对GOPATH环境变量进行“偷梁换柱”了，go compiler原生优先感知和使用vendor下缓存的第三方包。

不过即便有了vendor的支持，vendor内第三方依赖包的代码的管理依旧是不规范的，要么是手动的，要么是借助godep这样的第三方包管理工具。目前自举后的Go代码本身也引入了vendor，不过go项目自身对vendor中代码的管理方式也是[手动更新](https://github.com/golang/go/commit/554d49af61574bfacd3b106fd5c20aba4a1f1201)，Go自身并未使用任何第三方的包管理工具。

题外话：作为一门语言的标准库，应该是使用这门语言的开发者所使用的所有lib依赖的根依赖。但在go中，go标准库居然还要依赖golang.org/x/目录下的包，既然能被std lib依赖，那么说明其已经成熟，那为何不把x内的stable的库挪到std lib中呢？这点着实让人有些不解。


```
~/.bin/go18/src/vendor/golang_org/x]$ls
crypto/ net/ text/
```


从Go官方角度出发，官方go包依赖的解决方案的下一步就应该是解决对vendor下的第三方包如何进行管理的问题：*依赖包的分析、记录和获取等，进而实现项目的reproducible build*。dep就是用来做这事儿的。

## 二、dep简介

go package management commitee的牵头人物是微服务框架[go-kit](https://github.com/go-kit/kit)作者[Peter Bourgon](https://github.com/peterbourgon)，但当前主导dep开发的是[sam boyer](https://github.com/sdboyer)，sam也是dep底层包依赖分析引擎-[gps](https://github.com/sdboyer/gps)的作者。

和其他一些第三方Go包管理工具有所不同，dep在进行active dev前是经过commitee深思熟虑的，包括：[features](https://docs.google.com/document/d/1JNP6DgSK-c6KqveIhQk-n_HAw3hsZkL-okoleM43NgA/edit)、[user story](https://docs.google.com/document/d/1wT8e8wBHMrSRHY4UF_60GCgyWGqvYye4THvaDARPySs/edit)等都在事前做了初步设计。如果你拜读这些文档，你可能会觉得解决包依赖问题，还是[蛮复杂的](https://research.swtch.com/version-sat)。不过，对于这些工具的使用者来说，我们面对的是一些十分简化的交互接口。

### 1、安装dep

dep是标准的go cli程序，执行一条命令即完成安装：

```
# go get -u github.com/golang/dep/cmd/dep
# dep help
dep is a tool for managing dependencies for Go projects
Usage: dep <command>
Commands:
init Initialize a new project with manifest and lock files
status Report the status of the project's dependencies
ensure Ensure a dependency is safely vendored in the project
prune Prune the vendor tree of unused packages
Examples:
dep init set up a new project
dep ensure install the project's dependencies
dep ensure -update update the locked versions of all dependencies
dep ensure github.com/pkg/errors add a dependency to the project
Use "dep help [command]" for more information about a command.
```


在我的测试环境中，go的版本为1.8；dep的版本为commit d31c621c3381b9bebc7c10b1ac7849a96c21f2c3。

注意：由于dep还在active dev过程中且处于alpha测试阶段，因此本文中执行的dep命令、命令行为以及输出结果在后续dep版本中很可能会有变动，甚至是很大变动。


### 2、dep一般工作流

安装好dep后，我们就来看看使用dep的一般工作流。我们首先准备一个demo程序：

```
//depdemo/main.go
package main
import (
"net/http"
"go.uber.org/zap"
"github.com/beego/mux"
)
func main() {
logger, _ := zap.NewProduction()
defer logger.Sync()
sugar := logger.Sugar()
mx := mux.New()
mx.Handler("GET", "/", http.FileServer(http.Dir(".")))
sugar.Fatal(http.ListenAndServe("127.0.0.1:8080", mx))
}
```


#### a) dep init

如果一个项目要使用dep进行包管理，那么首先需要在这个项目的根下执行dep init。在这里，我们对depdemo进行dep改造。

在depdemo目录下，执行dep init：

```
# dep init -v
Searching GOPATH for projects...
Using master as constraint for direct dep github.com/beego/mux
Locking in master (626af65) for direct dep github.com/beego/mux
Following dependencies were not found in GOPATH. Dep will use the most recent versions of these projects.
go.uber.org/zap
Root project is "github.com/bigwhite/experiments/depdemo"
1 transitively valid internal packages
2 external packages imported from 2 projects
(0) ✓ select (root)
(1) ? attempt github.com/beego/mux with 1 pkgs; at least 1 versions to try
(1) try github.com/beego/mux@master
(1) ✓ select github.com/beego/mux@master w/1 pkgs
(2) ? attempt go.uber.org/zap with 1 pkgs; 12 versions to try
(2) try go.uber.org/zap@v1.4.0
(2) ✓ select go.uber.org/zap@v1.4.0 w/7 pkgs
(3) ? attempt go.uber.org/atomic with 1 pkgs; 6 versions to try
(3) try go.uber.org/atomic@v1.2.0
(3) ✓ select go.uber.org/atomic@v1.2.0 w/1 pkgs
✓ found solution with 9 packages from 3 projects
Solver wall times by segment:
b-source-exists: 1.090607387s
b-deduce-proj-root: 288.126482ms
b-list-pkgs: 131.059753ms
b-gmal: 114.716587ms
select-atom: 337.787µs
satisfy: 298.743µs
select-root: 292.889µs
new-atom: 257.256µs
b-list-versions: 42.408µs
other: 22.307µs
TOTAL: 1.625761599s
```


当前阶段，dep init命令的执行效率的确不高，因此需要你耐心的等待一会儿。如果你的project依赖的外部包很多，那么等待的时间可能会很长。并且由于dep会下载依赖包，对于国内的朋友来说，一旦下载qiang外的包，那么dep可能会“阻塞”在那里！

dep init大致会做这么几件事：

- 利用gps分析当前代码包中的包依赖关系；
- 将分析出的项目包的直接依赖(即main.go显式import的第三方包，direct dependency)约束(constraint)写入项目根目录下的Gopkg.toml文件中；
- 将项目依赖的所有第三方包（包括直接依赖和传递依赖transitive dependency）在满足Gopkg.toml中约束范围内的最新version/branch/revision信息写入Gopkg.lock文件中；
- 创建root vendor目录，并且以Gopkg.lock为输入，将其中的包（精确checkout 到revision）下载到项目root vendor下面。

执行完dep init后，dep会在当前目录下生成若干文件：

```
├── Gopkg.lock
├── Gopkg.toml
├── main.go
└── vendor/
```


我们逐一来看一下：

Gopkg.toml：

```
[[constraint]]
branch = "master"
name = "github.com/beego/mux"
[[constraint]]
name = "go.uber.org/zap"
version = "1.4.0"
```


Gopkg.toml记录了depdemo/main.go的两个direct dependency：mux和zap。通过gps的分析（可以参见上面init执行时输出的详细分析过程日志），dep确定的依赖版本约束为：mux的master分支、zap的1.4.0 version。

生成的Gopkg.lock中则记录了depdemo/main.go在上述约束下的所有依赖的可用的最新版本：

```
Gopkg.lock:
[[projects]]
branch = "master"
name = "github.com/beego/mux"
packages = ["."]
revision = "626af652714cc0092f492644e298e5f3ac7db31a"
[[projects]]
name = "go.uber.org/atomic"
packages = ["."]
revision = "4e336646b2ef9fc6e47be8e21594178f98e5ebcf"
version = "v1.2.0"
[[projects]]
name = "go.uber.org/zap"
packages = [".","buffer","internal/bufferpool","internal/color","internal/exit","internal/multierror","zapcore"]
revision = "fab453050a7a08c35f31fc5fff6f2dbd962285ab"
version = "v1.4.0"
[solve-meta]
analyzer-name = "dep"
analyzer-version = 1
inputs-digest = "77d32776fdc88e1025460023bef70534c5457bdc89b817c9bab2b2cf7cccb22f"
solver-name = "gps-cdcl"
solver-version = 1
```


vendor目录下，则是lock文件中各个依赖包的本地clone：

```
# tree -L 2 vendor
vendor
├── github.com
│ └── beego
└── go.uber.org
├── atomic
└── zap
```


至此，dep init完毕，相关依赖包也已经被vendor，你可以使用go build/install进行程序构建了。

#### b)、提交Gopkg.toml和Gopkg.lock

如果你对dep自动分析出来的各种约束和依赖的版本没有异议，那么这里就可以将Gopkg.toml和Gopkg.lock作为项目源码的一部分提交到代码库中了。这样其他人在下载了你的代码后，可以通过dep直接下载lock文件中的第三方包版本，并存在vendor里。这样就使得无论在何处，项目构建的依赖库理论上都是一致的，实现reproduceable build。

是否需要提交vendor下的依赖包代码到代码仓库？这取决于你。提交vendor的好处是即便没有dep，也可以实现真正的reproduceable build。但vendor的提交会让你的代码库变得异常庞大，且更新vendor时，大量的diff会影响到你对代码的review。下面的内容我们以不提交vendor为前提。

#### c)、dep ensure

现在我们的depdemo已经加入了Gopkg.toml和Gopkg.lock。这时，如果你将depdemo clone到你的本地，你还无法进行reproduceable build，因为这时vendor还不存在。这时我们需要执行下面命令来根据Gopkg.toml和Gopkg.lock中的数据构建vendor目录和同步里面的包：

```
# dep ensure
# ls -F
Gopkg.lock Gopkg.toml main.go vendor/
```


ensure成功后，你就可以进行reproduceable build了。

我们可以通过dep status查看当前的依赖情况(包括direct and transitive dependency)：

```
# dep status
PROJECT CONSTRAINT VERSION REVISION LATEST PKGS USED
github.com/beego/mux branch master branch master 626af65 626af65 1
go.uber.org/atomic * v1.2.0 4e33664 4e33664 1
go.uber.org/zap ^1.4.0 v1.4.0 fab4530 fab4530 7
```


#### d) 指定约束

dep init生成的Gopkg.toml中的约束是否是我们预期的呢？这个还真不一定。比如：我们将对zap的约束手工改为1.3.0：

```
//Gopkg.toml
... ...
[[constraint]]
name = "go.uber.org/zap"
version = "<=1.3.0"
```


执行dep ensure后，查看status:

```
# dep status
PROJECT CONSTRAINT VERSION REVISION LATEST PKGS USED
github.com/beego/mux branch master branch master 626af65 626af65 1
go.uber.org/atomic * v1.2.0 4e33664 4e33664 1
go.uber.org/zap <=1.3.0 v1.4.0 fab4530 fab4530 7
```


不过，此时Gopkg.lock中的zap version依旧是v1.4.0，并没有修改。要想更新lock和vendor下的数据，我们需要给ensure加上一个-update参数：

```
# dep ensure -update
# git diff Gopkg.lock
diff --git a/depdemo/Gopkg.lock b/depdemo/Gopkg.lock
index fce53dc..7fe3640 100644
--- a/depdemo/Gopkg.lock
+++ b/depdemo/Gopkg.lock
@@ -16,12 +16,12 @@
[[projects]]
name = "go.uber.org/zap"
packages = [".","buffer","internal/bufferpool","internal/color","internal/exit","internal/multierror","zapcore"]
- revision = "fab453050a7a08c35f31fc5fff6f2dbd962285ab"
- version = "v1.4.0"
+ revision = "6a4e056f2cc954cfec3581729e758909604b3f76"
+ version = "v1.3.0"
[solve-meta]
analyzer-name = "dep"
analyzer-version = 1
- inputs-digest = "77d32776fdc88e1025460023bef70534c5457bdc89b817c9bab2b2cf7cccb22f"
+ inputs-digest = "b09c1497771f6fe7cdfcf61ab1a026ccc909f4801c08f2c25f186f93f14526b0"
solver-name = "gps-cdcl"
solver-version = 1
```


-update让dep ensure尝试去保证并同步Gopkg.lock和vendor目录下的数据，将Gopkg.lock下的zap的version改为Gopkg.toml下约束的最大值，即v1.3.0，同时更新vendor下的zap代码。

#### e) 指定依赖

我们也可以直接更新dependency，这将影响Gopkg.lock和vendor下的数据，但Gopkg.toml不会被修改：

```
# dep ensure 'go.uber.org/zap@<1.4.0'
# git diff
diff --git a/depdemo/Gopkg.lock b/depdemo/Gopkg.lock
index fce53dc..3b17b9b 100644
--- a/depdemo/Gopkg.lock
+++ b/depdemo/Gopkg.lock
@@ -16,12 +16,12 @@
[[projects]]
name = "go.uber.org/zap"
packages = [".","buffer","internal/bufferpool","internal/color","internal/exit","internal/multierror","zapcore"]
- revision = "fab453050a7a08c35f31fc5fff6f2dbd962285ab"
- version = "v1.4.0"
+ revision = "6a4e056f2cc954cfec3581729e758909604b3f76"
+ version = "v1.3.0"
[solve-meta]
analyzer-name = "dep"
analyzer-version = 1
- inputs-digest = "77d32776fdc88e1025460023bef70534c5457bdc89b817c9bab2b2cf7cccb22f"
+ inputs-digest = "3307cd7d5942d333c4263fddda66549ac802743402fe350c0403eb3657b33b0b"
solver-name = "gps-cdcl"
solver-version = 1
```


这种情况下会出现Gopkg.lock中的version不满足Gopkg.toml中约束的情况。这里也让我比较困惑！

## 三、dep探索

上面的dep使用基本工作流完全可以满足日常包管理的需求了。但对于喜欢求甚解的我来说，必要要探索一下dep背后的行为和原理。

### 1、dep init的两种不同结果

我们回到depdemo的初始状态，即起点：尚未生成dep metadata file的时刻。我们在两种情况下，分别执行dep init：

- $GOPATH/src下没有go.uber.org/zap

```
# dep init -v
Searching GOPATH for projects...
Using master as constraint for direct dep github.com/beego/mux
Locking in master (626af65) for direct dep github.com/beego/mux
Following dependencies were not found in GOPATH. Dep will use the most recent versions of these projects.
go.uber.org/zap
Root project is "github.com/bigwhite/experiments/depdemo"
1 transitively valid internal packages
2 external packages imported from 2 projects
... ...
# dep status
PROJECT CONSTRAINT VERSION REVISION LATEST PKGS USED
github.com/beego/mux branch master branch master 626af65 626af65 1
go.uber.org/atomic * v1.2.0 4e33664 4e33664 1
go.uber.org/zap ^1.4.0 v1.4.0 fab4530 fab4530 7
```


- $GOPATH/src下存在go.uber.org/zap

```
# dep init -v
Searching GOPATH for projects...
Using master as constraint for direct dep github.com/beego/mux
Locking in master (626af65) for direct dep github.com/beego/mux
Using master as constraint for direct dep go.uber.org/zap
Locking in master (b33459c) for direct dep go.uber.org/zap
Locking in master (908889c) for transitive dep go.uber.org/atomic
Root project is "github.com/bigwhite/experiments/depdemo"
1 transitively valid internal packages
2 external packages imported from 2 projects
... ...
# dep status
PROJECT CONSTRAINT VERSION REVISION LATEST PKGS USED
github.com/beego/mux branch master branch master 626af65 626af65 1
go.uber.org/atomic * branch master 908889c 4e33664 1
go.uber.org/zap branch master branch master b33459c b33459c 7
```


不知道大家发现两种情况下生成的结果的异同与否。我们只看两个dep status输出中的zap一行：

```
go.uber.org/zap ^1.4.0 v1.4.0 fab4530 fab4530 7
vs.
go.uber.org/zap branch master branch master b33459c b33459c 7
```


dep自动分析后得到截然不同的两个结果。

第一种情况，我们称之为dep init的network mode，即dep发现本地GOPATH下面没有zap，于是dep init通过network到upstream上查找zap，并“Dep will use the most recent versions of these projects”，即v1.4.0版本。

第二种情况，我们称之为dep init的GOPATH mode, 即dep发现本地GOPATH下面存在zap，于是dep init认定“Using master as constraint for direct dep go.uber.org/zap”，即master branch。

至于为何GOPATH mode下，dep init会选择master，我个人猜测是因为dep觉得既然你本地有zap，那很大可能zap master的稳定性是被你所接受了的。在“[dep: updated command spec](https://docs.google.com/document/d/1Qwa3jDKDh45t5qAGjRpeu3ZsAbkukIYDDmYJdMxH2uY/edit)”中，似乎dep init打算通过[增加一个-gopath的flag](https://github.com/golang/dep/pull/497)来区分两种工作模式，并将network mode作为默认工作mode。但目前我所使用的dep版本还没有实现这个功能，其默认工作方式依旧是先GOPATH mode，如果没有找到依赖包的存在，则针对该包实施network mode。

从这里也可以看得出来，对于dep init 输出的约束，你最好还是检视一下，看是否能接受，否则就通过上面提到的“指定约束”来更正dep的输出。

### 2、dep对项目的依赖包的cache

在进行上面的试验中，我们发现：在本地GOPATH/src下面没有zap的情况下，dep似乎是直接将zap get到本地vendor目录的，而不是先get到GOPATH/src下，在copy到vendor中。事实是什么样的呢？dep的确没有操作GOPATH/src目录，因为那是共享的。dep在$GOPATH/pkg/dep/sources下留了一块“自留地”，用于cache所有从network上下载的依赖包：

```
# ls -F $GOPATH/pkg/dep/sources/
https---github.com-beego-mux/ https---github.com-uber--go-atomic/ https---github.com-uber--go-zap/
# ls -aF /root/go/pkg/dep/sources/https---github.com-uber--go-zap
./ buffer/ config_test.go field.go .gitignore http_handler.go LICENSE.txt options.go sugar.go writer.go
../ CHANGELOG.md CONTRIBUTING.md field_test.go glide.lock http_handler_test.go logger_bench_test.go README.md sugar_test.go writer_test.go
array.go check_license.sh* doc.go flag.go glide.yaml internal/ logger.go .readme.tmpl time.go zapcore/
array_test.go common_test.go encoder.go flag_test.go global.go level.go logger_test.go stacktrace.go time_test.go zapgrpc/
benchmarks/ config.go encoder_test.go .git/ global_test.go level_test.go Makefile stacktrace_test.go .travis.yml zaptest/
```


dep对于依赖包的所以git请求均在这个缓存目录下进行。

### 3、 vendor flatten平坦化

go在[1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)加入[vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)时，是考虑到“钻石形依赖”中存在同一个依赖包的不同版本的。我们来看看dep是否支持这一点。我们设计了一个试验：

![img{512x368}](../../assets/ebdfa3bf4b88c66f.png)


我们建立一个这样的“钻石形”试验环境，foo依赖[a](https://bitbucket.org/bigwhite/a)、[b](https://bitbucket.org/bigwhite/b)两个包，而a、b两个包分别依赖f的不同版本（通过在a、b中的Gopkg.toml声明这种约束，见图中标注）。

下面是foo项目下面的main.go：

```
// foo/main.go
package main
import "bitbucket.org/bigwhite/b"
import "bitbucket.org/bigwhite/a"
func main() {
a.CallA()
b.CallB()
}
```


未引入dep前，我们来运行一下该代码：

```
$go run main.go
call A: master branch
--> call F:
call F: v1.1.0
--> call F end
call B: master branch
--> call F:
call F: v2.0.1
--> call F end
```


可以看到同样是f包的输出，由于a、b分别依赖f的不同版本，因此输出不同。

我们对foo进行一个dep 分析，看看dep给了我们什么结果：

```
$dep init -v
Searching GOPATH for projects...
Using master as constraint for direct dep bitbucket.org/bigwhite/a
Locking in master (9122a5d) for direct dep bitbucket.org/bigwhite/a
Using master as constraint for direct dep bitbucket.org/bigwhite/b
Locking in master (2415845) for direct dep bitbucket.org/bigwhite/b
Locking in master (971460c) for transitive dep bitbucket.org/bigwhite/f
Root project is "Foo"
1 transitively valid internal packages
2 external packages imported from 2 projects
... ...
No versions of bitbucket.org/bigwhite/b met constraints:
master: Could not introduce bitbucket.org/bigwhite/b@master, as it has a dependency on bitbucket.org/bigwhite/f with constraint ^2.0.0, which has no overlap with existing constraint ^1.1.0 from bitbucket.org/bigwhite/a@master
v2.0.0: Could not introduce bitbucket.org/bigwhite/b@v2.0.0, as it is not allowed by constraint master from project Foo.
v1.0.0: Could not introduce bitbucket.org/bigwhite/b@v1.0.0, as it is not allowed by constraint master from project Foo.
master: Could not introduce bitbucket.org/bigwhite/b@master, as it has a dependency on bitbucket.org/bigwhite/f with constraint ^2.0.0, which has no overlap with existing constraint ^1.1.0 from bitbucket.org/bigwhite/a@master
```


dep init运行失败。由于a依赖的f@^1.1.0和b依赖的f@^2.0.0两个约束之间没有交集，无法调和，dep无法solve这个依赖，于是init failed！

但失败背后还有一层原因，那就是dep的设计要求[flatten vendor](https://blog.gopheracademy.com/advent-2016/saga-go-dependency-management/)，即使用dep的项目只能有一个root vendor，所以直接依赖或传递依赖的包中包含vendor的，vendor目录也都会[被strip掉](https://blog.gopheracademy.com/advent-2016/saga-go-dependency-management/)。这样一旦依赖包中存在带有冲突的约束，那么dep init必将失败。

## 四、小结

dep一个重要feature就是支持[semver 2.0规范](http://semver.org/lang/zh-CN/)，不过semver的规则好多，不是这里能说清楚的，大家可以到[semver官方站细读规则](http://semver.org/lang/zh-CN/)，或者在[npm semver calculator](https://semver.npmjs.com/)这个站点直观感受semver规则带来的变化。

dep试验告一段落。从目前来看，dep已经进入可用阶段，建议有条件的童鞋能积极的使用dep，并为dep进行前期测试，发现问题提issue，为dep的快速完善出出力。

depdemo的代码在[这里](https://github.com/bigwhite/experiments/tree/master/depdemo)；a, b,f包的代码在[这里](https://bitbucket.org/bigwhite/a)、[这里](https://bitbucket.org/bigwhite/b)和[这里](https://bitbucket.org/bigwhite/f)。

## 五、参考资料

[dep FAQ](https://github.com/golang/dep/blob/master/FAQ.md)[dep roadmap](https://github.com/golang/dep/wiki/Roadmap)[dep updated command spec](https://docs.google.com/document/d/1Qwa3jDKDh45t5qAGjRpeu3ZsAbkukIYDDmYJdMxH2uY/edit)[dep features](https://docs.google.com/document/d/1JNP6DgSK-c6KqveIhQk-n_HAw3hsZkL-okoleM43NgA/edit#)[The Saga of Go Dependency Management](https://blog.gopheracademy.com/advent-2016/saga-go-dependency-management/)by sam boyer[gps for implementors](https://github.com/sdboyer/gps/wiki/gps-for-Implementors)

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不把x内的stable的库挪到std lib中的原因是go和golang.org/x/下面代码的compatibility要求是不一样的。

有些道理。不过stdlib依赖外部库总是让人感觉别扭的很。似乎没有一门其他语言有这种“风格”。

flatten的问题该如何解决？ 实际项目这种版本冲突基本上是一定的。

似乎只能人工解决喽。比如：将直接依赖的低版本约束升级，直到不冲突为止。

感谢分享！已推荐到《开发者头条》：https://toutiao.io/posts/09zl3c 欢迎点赞支持！

欢迎订阅《小弧光黑板报》https://toutiao.io/subject/458

没发现比glide好在哪里…