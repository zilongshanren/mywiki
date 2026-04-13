---
title: 切换到Go 1.18后的第一件事：将interface{}全部替换为any
url: https://tonybai.com/2021/12/18/replace-empty-interface-with-any-first-after-switching-to-go-1-18/
published: '2021-12-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 切换到Go 1.18后的第一件事：将interface{}全部替换为any

![](../../assets/57e971fcd58d4e23.png)


[本文永久链接](https://tonybai.com/2021/12/18/replace-empty-interface-with-any-first-after-switching-to-go-1-18) – https://tonybai.com/2021/12/18/replace-empty-interface-with-any-first-after-switching-to-go-1-18

伴随着[Go 1.18 beta1版本的发布](https://mp.weixin.qq.com/s/Zthy6IAxGC10Q7q2N3gqMQ)，很多Gopher已经迫不及待地下载该版本并体验其中的新特性了！

![](../../assets/f298601236c9c892.png)


Go 1.18 beta1到手后，**你想做的第一件事是什么呢**？ 说到这里，很多人会问：**这是什么梗**？

这个梗来自于Russ Cox在2021年12月1日[对Go语言项目的一次commit](https://github.com/golang/go/commit/2580d0e08d5e9f979b943758d3c49877fb2324cb)：

![](../../assets/d2cd7a8170e4e3a8.jpeg)


从commit log可以看出，这次change主要是**将Go语言项目src目录下代码中的所有interface{}都替换为any**。只要学过Go的小伙伴儿们都知道: interface{}在Go中被称为“空接口(empty interface)”，所有类型都实现了空接口interface{}，任意类型T的实例都可以赋值给空接口类型变量：

```
var t T // T可以是任意Go类型
var i interface{} = t
var j interface{} = &t
```


那么为什么Go团队要在Go 1.18 beta1发布之前，将interface{}全部替换为any呢？any又是啥？我们翻看Go 1.18 beta1代码后，在builtin/builtin.go中找到了any类型的定义：

```
// $GOROOT/src/builtin/builtin.go
// any is an alias for interface{} and is equivalent to interface{} in all ways.
type any = interface{}
```


我们看到**any就是一个interface{}的type alias，它与interface{}完全等价**。那为啥要增加any，换掉interface{}呢？我觉得主要还是考虑到[Go 1.18加入泛型](https://mp.weixin.qq.com/s/_4p1wyo3eKEaCU_9GNdkLA)后的影响，看下面两个使用了泛型语法的函数声明：

```
func f[T1 any, T2 comparable, T3 any](t1 T1, t2 T2) T3 { }
func f[T1 interface{}, T2 comparable, T3 interface{}](t1 T1, t2 T2) T3 { }
```


Go泛型增加了type parameter，如果在类型参数声明区域继续使用interface{}，我们看到，函数声明部分就会显得十分冗长，给开发者的感官体验上就不那么舒服。另外interface类型在Go 1.18引入泛型后，身兼另外一个职责：**定义类型参数的约束(constraints)**，使用any这样的名字与新职责更匹配。于是Go 1.18就引入了interface{}的type alias，并做了全局替换。

当然这种事情有人爱，就有人反对：

![](../../assets/5417e0c1ca7aeb46.png)


不过，我们也看到多数gopher还是喜欢any而不喜欢interface{}的“冗长”的。

既然Go语言项目自身都这么做了，作为Gopher而言，我们有义务响应号召，在切换到Go 1.18开始就着手将代码中的interface{}统统换成any。那怎么换呢？简单的很！[gofmt大法搞定一切](https://www.imooc.com/read/87/article/2376)！下面是具体步骤：

- 查看当前项目下的interface{}使用情况

```
$find . -name "*.go"|xargs grep "interface{}"
// 如要排除掉vendor
$find . -name "*.go"|grep -v vendor|xargs grep "interface{}"
```


- 查看此次替换会影响到的源文件列表

```
$gofmt -l -r 'interface{} -> any' .
// 如要排除掉vendor
$gofmt -l -r 'interface{} -> any' .|grep -v vendor
```


- 实施全局替换

```
$gofmt -w -r 'interface{} -> any' .
// 如要排除掉vendor目录
$find . -name "*.go"|grep -v vendor|xargs gofmt -w -r 'interface{} -> any'
```


注意：gofmt不会替换注释中的interface{}


最后，可以使用下面名了检查替换情况：

```
$find . -name "*.go"|xargs grep "interface{}"
```


一段时间后…..

**你可能觉得你有些“冲动”了**！虽然Go 1.18支持any，但Go 1.17及之前的版本不支持啊，团队内部除非步调一致的全部升级到go 1.18，否则其他组员可能就无法编译你提交的用any换掉interface{}的代码了！怎么办？

考虑到兼容Go 1.18之前直至Go 1.9版本，我们可以用条件编译来解决这个问题。看下面例子：

```
// https://github.com/bigwhite/experiments/tree/master/emptyinterface2any
$tree emptyinterface2any
emptyinterface2any
├── any.go
├── demo
├── go.mod
├── main.go
├── pkg1
│ ├── any.go
│ └── pkg1.go
└── pkg2
├── any.go
└── pkg2.go
```


这个emptyinterface2any demo项目中，所有interface{}都换成了any。我们用go 1.18构建这个demo自然没有问题。但是如果用Go 1.17或之前的版本，那么就会得到“any未定义”的错误。为了兼容老版本，我们在每个包的下面都加入一个any.go文件：

```
// https://github.com/bigwhite/experiments/tree/master/emptyinterface2any/any.go
// +build !go1.18
//go:build !go1.18
package main
type any = interface{}
```


我们看到在这个文件中，我们加入了[编译约束指示信息](https://pkg.go.dev/cmd/go#hdr-Build_constraints)，通过这些信息告诉编译器：这个源文件仅在Go 1.18版本之前的版本构建时才参与编译，Go 1.18编译时，不参与编译。这样当使用Go 1.17及之前的版本编译时，该文件参与编译，相当于我们自定义了一个any别名类型。

这个方案适用于[Go 1.9，Go 1.17]范围内的Go版本，因为type alias语法是在[Go 1.9版本](https://tonybai.com/2017/07/14/some-changes-in-go-1-9/)中引入的。

这下你可以无后顾之忧的提交你的代码了，虽然增加any.go并用编译约束的方式麻烦点^_^。不过这也是临时的，一旦全部迁移到Go 1.18以及后续版本，这些临时措施就可以撤掉了(删除所有any.go)。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论