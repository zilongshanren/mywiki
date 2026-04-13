---
title: 如何查看历史版本的Go文档？嘘！答案我只告诉你！
url: https://tonybai.com/2020/12/15/how-to-see-the-manual-of-go-history-version/
published: '2020-12-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 如何查看历史版本的Go文档？嘘！答案我只告诉你！

![img{512x368}](../../assets/9286cf5998c9d766.png)


[Go语言自开源至今已经11个年头了](https://mp.weixin.qq.com/s/woQeEQUhOLJ7KSE5rm5q6g)！截至本文发稿时，目前[最新的Go版本为1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)，Go核心开发团队正紧锣密鼓的进行着[Go 1.16版本](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)的开发（现阶段主要是修复bug），该版本将在2021年2月份正式发布。

Go以“自带电池(battery included)”而为人所知，除了Go标准库的全面和强大之外，Go工具链的丰富和易用在主流编程语言中也是位列“执牛耳者”之列的，而Go文档查看工具就在Go工具链之列中。

查看文档是Gopher们日常必不可少的开发活动之一。Go语言从诞生那天起就十分重视项目文档的建设，除了在Go官方网站(https://golang.org)可以查看到最新稳定发布版（当前是[Go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)）的文档之外，在**tip.golang.org**上还可以查看到项目主线分支（master）上最新开发版本（非稳定版）的文档。

**那么问题来了！如果想查看Go的某个历史版本（比如： Go 1.9）的文档，我应该如何做呢**？别急！在这篇文章中，我将告诉你答案。

### 1. 利用go doc，可行，但非最优

从Go发布1.0版本开始，Go就将整个Go项目文档加入到Go发行版中，这样开发人员在本地安装Go的同时也拥有了一份完整的Go项目文档。

除了在发行版中集成所有文档，从[1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5)开始，Go还将文档查看工具集成到其工具链当中(即**go doc**)，使之成为Go工具链不可分割的一部分，这也再次体现了文档在Go语言中的重要性。自go doc在1.5版本加入Go工具链之后，它就和go get、go build一样成为了Gopher们每日必用的go命令，也成为了**Go包文档的“百科全书”**。

不过利用go doc，我们只能查看当前本地的go版本的文档。如果当前本地环境的Go版本为[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)，那么所有go doc输出的文档内容均来自Go 1.14版本。如果我们要查看Go 1.9版本的文档，我们需要将本地环境的Go版本“切换”到Go 1.9才可以。

“切换”的方法有很多，笔者习惯通过重新设置\$GOROOT的方式在多个Go版本间切换：

```
$export GOROOT=~/.bin/go1.9.7
$export PATH=$GOROOT/bin:$GOPATH
$go version
go version go1.9.7 darwin/amd64
$go doc http.Request
```


我们看到：“切换”后再执行的go doc的输出结果均来自Go 1.9版本了。

不过这种方法比较繁琐，需要切换本地环境中的go版本，并且没法像官方站点那样通过图形化的方式查阅go文档，这显然不是最优方案，我们继续往下看。

### 2. 使用godoc建立历史版本的Web化文档中心

很多接触Go语言较早的gopher都知道，在go doc之前，还有一个像gofmt一样随着Go安装包一起发布的文档查看工具，它就是**godoc**，也就是说godoc在Go世界的存在历史比go doc还要悠久。在Go 1.5版本增加go doc工具后，godoc与go doc就一直并存在Go中。这种情况一直持续到[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)。在Go 1.13版本中，godoc就不再和go、gofmt一起内置在Go安装包中发布了。godoc被挪到Go扩展工具链中，我们可以通过下面命令单独安装godoc：

```
$go get golang.org/x/tools/cmd/godoc
```


和命令行go doc工具不同的是，godoc实质上是一个web服务，它会在本地建立起一个web形式的Go文档中心，当我们执行下面命令时这个文档中心服务就启动了：

```
$godoc -http=localhost:6060
```


在浏览器地址栏输入`http://localhost:6060`

，打开Go文档中心首页：

![img{512x368}](../../assets/67fab30c810a8499.png)


我们看到godoc将\$GOROOT下面的内容以web页面的形似呈现给开发者，同时我们看到首页顶部的菜单与Go官方主页的菜单也基本如出一辙。点击“Packages”可以打开Go包参考文档页面：

![img{512x368}](../../assets/fd26cd73b8b93e3c.png)


Go包参考文档页面将包分为几类：标准库包(Standard library)、第三方包(Third party)和其它包(Other packages)，其中的第三方包就是本地\$GOPATH下面的各个包。

不过，默认情况下godoc建立的Go文档中心对应的文档版本也是本地环境当前的Go版本，即如果当前本地安装的Go版本为go 1.14，那么godoc所呈现的就是go 1.14稳定版对应的文档。 那么如果我想查看一下旧版本的文档，比如Go 1.9.7版本的文档，我该如何做呢？首先我们需要下载go 1.9.7版本的安装包（因为正如前面所说的，go文档是随着安装包一起发布的），将其解压到本地目录下，比如是/Users/tonybai/.bin/go1.9.7，接下来我们执行如下命令：

```
$godoc -goroot /Users/tonybai/.bin/go1.9.7 -http=localhost:6060
```


我们用**-goroot**命令行选项显式告诉godoc从哪个路径加载Go文档数据，这样godoc建立的文档中心中的文档版本就是Go 1.9.7的了。

我们看到，通过godoc，我们不仅无需切换本地环境中的go版本，我们还建立起了像golang.org那样的图形化的历史go版本的文档中心。这也是截至目前为止查看Go历史版本版本文档的**最佳方法**了！

更多关于常用Go工具链的**高级用法**的内容请参看我在慕课网上出品的Go进阶技术专栏[《改善Go语言编程质量的50个有效实践》](https://www.imooc.com/read/87)。本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![img{512x368}](../../assets/018ff45f7e150fca.png)


**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

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
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论