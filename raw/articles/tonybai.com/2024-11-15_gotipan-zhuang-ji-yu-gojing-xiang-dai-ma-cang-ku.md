---
title: Gotip安装：基于Go镜像代码仓库
url: https://tonybai.com/2024/11/15/install-gotip-using-go-repo-mirror/
published: '2024-11-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gotip安装：基于Go镜像代码仓库

![](../../assets/fd410fe31f043194.png)


[本文永久链接](https://tonybai.com/2024/11/15/install-gotip-using-go-repo-mirror) – https://tonybai.com/2024/11/15/install-gotip-using-go-repo-mirror

在《[Go map使用Swiss Table重新实现，性能最高提升近50%](https://mp.weixin.qq.com/s/-1dUOhN5saXApwTdiNgSHA)》一文中，我曾使用过Gotip版本对基于Swiss table的新map实现做过benchmark测试。

有过几年Go开发经验的Gopher都知道Gotip版本是啥，但一些初学者可能并不十分清楚。Gotip版本可以理解为**Go语言的devel版本**，是支持开发者全面体验Go最新特性的主流方法之一，而另外一种方法则是通过[Go官网提供的在线Playground(选择Go dev branch，如下图)](https://go.dev/play/)体验：

![](../../assets/3aca29f8452ead50.png)


不过通过Go playground方法体验Go最新特性会受到各种限制，比如只能体验单一源文件、无法跑benchmark test等。

Gotip本质上就是**基于Go repo最新主干代码进行构建的Go版本**，为了降低Gopher体验Go最新特性的门槛，Go团队让大家可以通过go install来安装Gotip。如今我们只需两行命令(前提是你的机器上已经有了某个版本的Go)就可以将Gotip安装到自己的机器上：

```
$go install golang.org/dl/gotip@latest
$gotip download
```


然而，Gotip版本的本质决定了它在国内的安装过程不会一帆风顺。你在国内执行上述的第二条命令时，很可能会看到如下输出：

```
$ gotip download
正克隆到 '/root/sdk/gotip'...
fatal: 无法访问 'https://go.googlesource.com/go/'：Failed connect to go.googlesource.com:443; 连接超时
gotip: failed to clone git repository: exit status 128
```


这表明gotip尝试从Google的Go代码仓库克隆代码到本地，但由于众所周知的原因，这一过程常常会失败。

如果屏幕前的你拥有高速的加速器，那么你现在就可以关闭窗口，无需再阅读下面的内容了。但如果你没有，或者你需要在没有加速器的服务器或PC上使用Gotip，那还是请继续读下去。

现在问题就摆在你我面前：如何能让Gotip能成功clone到Go源码呢？一个很容易想到的思路：**让Gotip从其他可达的地方clone Go源码不就行了吗**？

假设这个思路可行，需要满足以下两个条件：

- Gotip支持从其他地方clone Go源码
- 国内有一个可达的、快速的Go源码mirror仓库

我们评估一下可行性，先来看第一个条件。Gotip支持传入某些命令行参数并从其他地方clone Go源码么？看看它的usage吧！

```
$gotip
gotip: not downloaded. Run 'gotip download' to install to /root/sdk/gotip
$gotip -h
gotip: not downloaded. Run 'gotip download' to install to /root/sdk/gotip
$gotip download 2 3 4
gotip: usage: gotip download [CL number | branch name]
```


我们看到：官方版gotip的usage隐藏“很深”啊(有改进空间哦)！并且，gotip并不支持传入任何mirror仓库的命令行标志或参数。不过好在gotip是开源的，在github.com/golang/dl下可以找到gotip的源码，我们只需要fork并修改一下应该就可以了。

那么第二个条件呢？国内是否有一个可达的、快速的Go源码mirror仓库呢？很遗憾，没有现成的。不过，我们可以手工从github.com/golang/go上下载仓库，然后再push到国内任一家代码托管站点上即可，虽然这么做有些费时费力。好在，国内的码云(gitee.com)提供了一个导入外部仓库并同步的功能，我们可以在码云上直接导入github.com/golang/go，比如我这里就建立了一个公共库并同步了golang/go：gitee.com/bigwhite/go：

![](../../assets/26462df429a5ad8a.png)


综上这个方案是可行的。

接下来就是将上面的方案思路付诸实现了。我fork了github.com/golang/dl到[github.com/bigwhite/dl](https://github.com/bigwhite/dl)，然后修改了其中的internal/version/gotip.go文件：将https://go.googlesource.com/go改为了https://gitee.com/bigwhite/go.git。

![](../../assets/2e720db437565252.png)


接下来，我们就可以通过下面命令构建一个自己定制的gotip：

```
$go build -o gotip-gitee golang.org/dl/gotip
```


这里要注意的是：直接go build golang.org/dl/gotip会报错，因为在顶层目录下存在了gotip这个子目录，与目标可执行文件重名了，所以这里重命名了目标可执行文件。为了方便，我又在github.com/bigwhite/dl下加了一个Makefile，大家只需执行make gotip即可。

注：这是一个很好的向Go项目贡献自己代码的机会，大家可以向Go项目提交PR，为gotip增加类似-m (mirror site)的命令行参数，以支持从第三方Go repo镜像站点下载Go源码并完成gotip的构建和安装过程。


接下来我们就来继续gotip的安装过程：

```
$ ./gotip-gitee download
正克隆到 '/root/sdk/gotip'...
remote: Enumerating objects: 14793, done.
remote: Counting objects: 100% (14793/14793), done.
remote: Compressing objects: 100% (11974/11974), done.
remote: Total 14793 (delta 2629), reused 10541 (delta 2221), pack-reused 0
接收对象中: 100% (14793/14793), 29.30 MiB | 9.50 MiB/s, 完成.
处理 delta 中: 100% (2629/2629), 完成.
Updating the go development tree...
来自 https://gitee.com/bigwhite/go
* branch master -> FETCH_HEAD
HEAD 目前位于 84e58c8 cmd/internal/obj: add tool to generate Cnames string
Building Go cmd/dist using /root/.bin/go1.23.0. (go1.23.0 linux/amd64)
Building Go toolchain1 using /root/.bin/go1.23.0.
Building Go bootstrap cmd/go (go_bootstrap) using Go toolchain1.
Building Go toolchain2 using go_bootstrap and Go toolchain1.
Building Go toolchain3 using go_bootstrap and Go toolchain2.
Building packages and commands for linux/amd64.
---
Installed Go for linux/amd64 in /root/sdk/gotip
Installed commands in /root/sdk/gotip/bin
Success. You may now run 'gotip'!
```


这个编译和安装过程大概仅花费2-3分钟左右，非常快！一旦gotip安装完毕，你就可以直接使用gotip版本，体验Go最新特性了!

```
$ gotip version
go version devel go1.24-84e58c8 Wed Nov 13 05:02:13 2024 +0000 linux/amd64
```


我们来小结一下！在这篇文章中，我提供了一种在国内安装gotip版本的方法，供大家参考而已。如果你不喜欢使用gitee.com上的mirror仓库，你也可以直接使用[github上的go镜像仓库](https://github.com/golang/go)，如果你觉得访问github还比较顺畅的话。

当然屏幕前的读者可能有比我这里更好、更方便地在国内安装gotip版本的方法，也欢迎大家在评论区留言交流！

注：如果你采用我的方法安装gotip，请自行在gitee.com上建立Go仓库的mirror仓库并按需同步。


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