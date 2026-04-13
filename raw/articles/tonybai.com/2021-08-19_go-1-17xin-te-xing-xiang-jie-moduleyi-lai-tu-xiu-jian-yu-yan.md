---
title: Go 1.17新特性详解：module依赖图修剪与延迟module加载
url: https://tonybai.com/2021/08/19/go-module-changes-in-go-1-17/
published: '2021-08-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.17新特性详解：module依赖图修剪与延迟module加载

![](../../assets/83efed00cb88993a.png)


[本文永久链接](https://tonybai.com/2021/08/19/go-module-changes-in-go-1-17) – https://tonybai.com/2021/08/19/go-module-changes-in-go-1-17

[Go module](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)的引入终于让Go语言有了自己的包依赖管理标准机制与工具，虽说它的引入与推广过程略显坎坷，但不得不承认[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)及之后的每一次Go版本发布，Go module都在进步！在[Go 1.17版本](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)中亦是如此，本篇我们就来详细聊聊在Go 1.17版本中Go module都有哪些重要的变化。

### 1. module依赖图修剪

本文的标题暗示了Go 1.17中go module的两个主要变化。[module依赖图修剪(module graph pruning)](https://tip.golang.org/ref/mod#graph-pruning)是[延迟module加载(lazy module loading)](https://tip.golang.org/ref/mod#lazy-loading)的基础。

我们以下图中的例子来解释一下什么是module graph pruning。

![](../../assets/2fcf1fd38d4935fc.png)


注：上图中的例子来自于Go 1.17源码中的src/cmd/go/testdata/script/mod_lazy_new_import.txt，通过执行

[txtar工具]，我们可以将该txt转换为mod_lazy_new_import.txt中所描述的示例结构，转换命令为: txtar -x < \$GOROOT/src/cmd/go/testdata/script/mod_lazy_new_import.txt 。

在上面这个示例中，main module中的lazy.go导入了module a的package x，后者则导入了module b；并且module a还有一个package y，该包导入了module c。通过go mod graph命令我们可以得到main module的module graph，如图右上。

现在问题来了！package y是因为自身是module a的一部分而被main module所依赖，它没有为main module的构建做出任何“代码级贡献”；同理，package y所依赖的module c亦是如此。但是在Go 1.17之前的版本中，如果Go编译器找不到module c，那么main module的构建将会失败，这会让开发者们觉得不够合理！

我们回到上图对应的示例。在Go 1.16.5下，我们看看该示例的go.mod如下：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/module/demo1/go.mod
module example.com/lazy
go 1.15
require example.com/a v0.1.0
replace (
example.com/a v0.1.0 => ./a
example.com/b v0.1.0 => ./b
example.com/c v0.1.0 => ./c1
example.com/c v0.2.0 => ./c2
)
```


我们只需关注require块中的内容，下面的replace块儿主要是为了示例能找到各种依赖module而设置的。我们知道在[Go 1.16](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)及以前支持Go module的版本所建立的go module中，其中的go.mod在go mod tidy后，require块儿中保留的都是[main module](https://tip.golang.org/ref/mod#glos-main-module)的[直接依赖(direct dependency)](https://tip.golang.org/ref/mod#glos-direct-dependency)（[在某些情况下，也会记录indirect依赖](https://tip.golang.org/ref/mod#go-mod-file-require)，这些依赖会在行尾用indirect指示符明示），因此在这里我们看不到main module的间接依赖以及它们的版本，我们可以用go mod graph来查看module依赖图，如下面命令及输出：

```
$go mod graph
example.com/lazy example.com/a@v0.1.0
example.com/a@v0.1.0 example.com/b@v0.1.0
example.com/a@v0.1.0 example.com/c@v0.1.0
```


这个go mod graph的输出与我们在上面图中右上角所画的module graph是一致的。此时，如果我们将replace中的第三行删除(example.com/c v0.1.0 => ./c1这一行)，即让Go编译器找不到module c@v0.1.0，那么我们构建main modue时将得到下面的错误提示：

```
$go build
go: example.com/a@v0.1.0 requires
example.com/c@v0.1.0: missing go.sum entry; to add it:
go mod download example.com/c
```


现在我们将执行权限交给Go 1.17！我们需要对go.mod做一些修改（将go.mod中的go 1.15改为go 1.17），这样Go 1.17才能起到作用。接下来，我们执行go mod tidy，让Go 1.17重新构建go.mod：

```
$go mod tidy
$cat go.mod
module example.com/lazy
go 1.17
require example.com/a v0.1.0
require example.com/b v0.1.0 // indirect
replace (
example.com/a v0.1.0 => ./a
example.com/b v0.1.0 => ./b
example.com/c v0.1.0 => ./c1
example.com/c v0.2.0 => ./c2
)
```


我们看到执行go mod tidy之后，go.mod发生了变化：增加了一个require语句块，记录了main module的间接依赖：module b@v0.10。

现在，我们也同样将go.mod replace块中的第三行删除(example.com/c v0.1.0 => ./c1这一行)，我们再来用go 1.17构建一次main module，这一次我们没有看到Go编译器的错误提示。也就是说在构建过程中，Go编译器所看到的main module依赖图中并没有module c@v0.1.0。由于module c并没有为main module的构建提供“代码级贡献”，Go命令将其从module依赖图中剪除，Go编译器使用的真实的依赖图如上图右下角所示(pruned module graph)。

这种将那些“占着茅坑不拉屎”、对构建完全没有“贡献”的间接依赖module从构建时使用的依赖图中修剪掉的过程，就被称为**module依赖图修剪**。

之所以要这么做，就是因为[Go社区反馈了较多的这方面的问题](https://go.googlesource.com/proposal/+/master/design/36460-lazy-module-loading.md)。这么做的好处是显而易见的：**我们再也不用为那些没有对构建没有做出任何“代码级贡献”但又容易出现各种“问题”的module的埋单了**。

但module依赖图修剪也带来了一个副作用，那就是go.mod文件size的变大。因为Go 1.17版本后，每次go mod tidy，go命令都会对main module的依赖做一次深度扫描(deepening scan)，并将main module的所有直接和间接依赖都记录在go.mod中。考虑到内容较多，go 1.17将直接依赖和间接依赖分别放在两个不同的require块儿中。

我们以[gnet](https://github.com/panjf2000/gnet)为例，Go 1.17版本之前的go.mod如下：

```
module github.com/panjf2000/gnet
go 1.16
require (
github.com/BurntSushi/toml v0.3.1 // indirect
github.com/panjf2000/ants/v2 v2.4.6
github.com/stretchr/testify v1.7.0
github.com/valyala/bytebufferpool v1.0.0
go.uber.org/atomic v1.8.0 // indirect
go.uber.org/multierr v1.7.0 // indirect
go.uber.org/zap v1.18.1
golang.org/x/sys v0.0.0-20210630005230-0f9fa26af87c
gopkg.in/natefinch/lumberjack.v2 v2.0.0
)
// Go module checksum mismatch, see https://github.com/panjf2000/gnet/issues/219
// retract v1.4.5
```


使用Go 1.17重新mod tidy后，go.mod内容如下：

```
module github.com/panjf2000/gnet
go 1.17
require (
github.com/BurntSushi/toml v0.3.1 // indirect
github.com/panjf2000/ants/v2 v2.4.6
github.com/stretchr/testify v1.7.0
github.com/valyala/bytebufferpool v1.0.0
go.uber.org/atomic v1.8.0 // indirect
go.uber.org/multierr v1.7.0 // indirect
go.uber.org/zap v1.18.1
golang.org/x/sys v0.0.0-20210630005230-0f9fa26af87c
gopkg.in/natefinch/lumberjack.v2 v2.0.0
)
require (
github.com/davecgh/go-spew v1.1.1 // indirect
github.com/pmezard/go-difflib v1.0.0 // indirect
gopkg.in/yaml.v3 v3.0.0-20210107192922-496545a6307b // indirect
)
```


我们看到go 1.17后，go.mod中的main module的依赖分成了两个require块儿，第一个是直接依赖，第二个是间接依赖。但我们看到第一个require中也有包含indirect指示符的依赖。Go关于indirect指示符的使用总是很让人迷惑。关于究竟在Go 1.17中的require中如何使用indirect指示符，可以在[这个讨论](https://github.com/golang/go/issues/45965#issuecomment-844439392)中找到一些线索。

Go 1.17后go.mod中存储了main module的所有依赖module列表，这似乎也是Go项目第一次有了项目依赖的完整列表，这是不是让你想起了其他主流语言构架系统中的那个lock文件。虽然go.mod不是lock文件，但有了完整依赖列表，至少我们可以像其他语言的lock文件那样，知晓当前Go项目所有依赖的精确版本了。

### 2. 延迟module加载(lazy module loading)

有了module依赖图修剪作为铺垫，[延迟module加载](https://tip.golang.org/ref/mod#lazy-loading)就相对好理解了。其含义就是**那些在完整的module graph(complete module graph)中，但不在pruned module graph中的module的go.mod不会被go命令加载**。

### 3. module deprecation注释

在[Go 1.16版本在go.mod中加入retract](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)以支持作废某个module的特定版本后，go 1.17更进一步地[在go.mod中增加了 Deprecated注释](https://tip.golang.org/ref/mod#go-mod-file-module-deprecation)，以帮助go module作者作废自己的module。go module作者只需在自己的go.mod中的module声明上面用

**// Deprecated: comment**对module做出注释，就像下面这样：

```
// Deprecated: use example.com/mod/v2 instead.
module example.com/mod
```


对于那些使用了被废弃的module的go项目，go list、go get命令都会给出warning。

注意和retract不同，我们不能用Deprecated去作废minor或patch版本，Deprecated是用来作废整个module的。但不同major版本的module被视为不同的module。因此，go module作者一般像上面例子中那样，在Deprecated注释中提示升级到更新的版本，比如：v2版本。

### 4. 其他一些改变

- 如果一个main module的go.mod中没有go版本指示符，go 1.17版本的go命令会将其默认为go 1.11版本;
- 如果一个module的依赖module没有go.mod或该依赖module的go.mod中没有go指示符，go 1.17版本的go命令会将其go.mod中的版本指示符默认为go 1.16，而不是go命令的版本；
- 如果main module的go.mod中go版本指示符的值为go 1.17及以上版本，那么go mod vendor会在vendor/modules.txt中记录被vendor的module使用的go version，见下面对比：

main module的go.mod中go version < 1.17：

```
# github.com/BurntSushi/toml v0.3.1
## explicit
# github.com/davecgh/go-spew v1.1.1
github.com/davecgh/go-spew/spew
# github.com/panjf2000/ants/v2 v2.4.6
## explicit
github.com/panjf2000/ants/v2
github.com/panjf2000/ants/v2/internal
# github.com/pmezard/go-difflib v1.0.0
github.com/pmezard/go-difflib/difflib
# github.com/stretchr/testify v1.7.0
## explicit
github.com/stretchr/testify/assert
github.com/stretchr/testify/require
# github.com/valyala/bytebufferpool v1.0.0
## explicit
github.com/valyala/bytebufferpool
... ...
```


main module的go.mod中go version >= 1.17：

```
// vendor/modules.txt
# github.com/BurntSushi/toml v0.3.1
## explicit
# github.com/davecgh/go-spew v1.1.1
## explicit
github.com/davecgh/go-spew/spew
# github.com/panjf2000/ants/v2 v2.4.6
## explicit; go 1.14
github.com/panjf2000/ants/v2
github.com/panjf2000/ants/v2/internal
# github.com/pmezard/go-difflib v1.0.0
## explicit
github.com/pmezard/go-difflib/difflib
# github.com/stretchr/testify v1.7.0
## explicit; go 1.13
github.com/stretchr/testify/assert
github.com/stretchr/testify/require
# github.com/valyala/bytebufferpool v1.0.0
... ...
```


- 如果main module go.mod中go version指示版本>= go 1.17，那么go mod vendor将忽略各个依赖包中的go.mod和go.sum，这两个文件将不会出现在vendor目录下的各个被vendor的module目录中。

### 5. 小结

Go 1.17通过对构建时使用的module graph的修剪，让我们再也不用为那些对项目没有代码级贡献但又极容易给构建过程带来麻烦的依赖所烦恼了。新版go.mod的格式还让我们拥有了一份完整的项目依赖列表，这种直观让开发者有一种安全和踏实的感觉。

本文涉及的所有代码可以从[这里下载](https://github.com/bigwhite/experiments/tree/master/go1.17-examples)：https://github.com/bigwhite/experiments/tree/master/go1.17-examples

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


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

© 2021 – 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论