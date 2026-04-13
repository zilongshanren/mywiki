---
title: 如何作废一个已发布的Go module版本，我来告诉你！
url: https://tonybai.com/2020/12/26/how-to-deprecate-a-published-version-of-some-specific-go-module/
published: '2020-12-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 如何作废一个已发布的Go module版本，我来告诉你！

![img{512x368}](../../assets/8afae8b1ef58f8cf.png)


Go语言自诞生以来，一路走到今天已经[经历了11个年头了](https://mp.weixin.qq.com/s/woQeEQUhOLJ7KSE5rm5q6g)。其包依赖管理机制也从无到有，从[vendor](https://mp.weixin.qq.com/s/ZbPvC0bR5H4a3-k2BFLC1w)演化成了如今的[Go module](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)。Go module从[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)进入gopher们视野，到目前的[Go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)，其改进和优化一直在持续。在即将到来的[Go 1.16](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)中，Go module将成为默认包依赖管理模式(即默认GO111MODULE=on)。但即便如此，我们在进行go module的实践过程中依然还会遇到一些“棘手”的问题，本文就将针对一个Go module实践中的具体问题做深入描述，并告诉你目前可用的最佳解决方案（也许在go module的后续演进过程中可能会有更好的解决方案或干脆消除掉这个机制上的问题）。

### 1. 一不小心将一个处于broken状态的module发布了出去

人总是会犯错的，作为Go包/module的作者，我们偶尔也会出现这样的低级错误：**将一个处于broken状态的module发布了出去**。比如：**bitbucket.org/bigwhite/m1**是我维护的一个module(专为此文创建的公共go module)，它目前已经进化到v1.0.1版本了：

```
// bitbucket.org/bigwhite/m1/main.go
package m1
import "fmt"
func M1() {
fmt.Println("This is m1.M1 - v1.0.1")
}
```


m1这个module有两个消费者：c1和c2，它们依赖的也都是m1的v1.0.1版本：

```
// c1的go.mod
module github.com/bigwhite/c1
go 1.14
require bitbucket.org/bigwhite/m1 v1.0.1
// c1的main.go
package main
import (
"fmt"
"bitbucket.org/bigwhite/m1"
)
func main() {
fmt.Println("This is c1")
m1.M1()
}
// c2的go.mod
module github.com/bigwhite/c2
go 1.14
require bitbucket.org/bigwhite/m1 v1.0.1
// c2的main.go
package main
import (
"fmt"
"bitbucket.org/bigwhite/m1"
)
func main() {
fmt.Println("This is c2")
m1.M1()
}
```


c1和c2所在的Go开发环境均使用下面的GOPROXY设置：

```
export GOPROXY=https://goproxy.cn,direct
```


我们用一幅示意图来描述当前的状态：

![img{512x368}](../../assets/3851e7476308d969.png)


以c1为例，构建并运行c1：

```
// c1的module root目录下
$go build
go: finding module for package bitbucket.org/bigwhite/m1
go: downloading bitbucket.org/bigwhite/m1 v1.0.1
go: found bitbucket.org/bigwhite/m1 in bitbucket.org/bigwhite/m1 v1.0.1
$./c1
This is c1
This is m1.M1 - v1.0.1
```


接下来，作为m1的作者，我犯了一个低级错误：将更新了的但却无法编译成功的m1打标签为v1.0.2发布了出去：

```
// bitbucket.org/bigwhite/m1的m1.go
package m1
import "fmt"
func M1() {
var a int // 编译器错误：a declared but not used
fmt.Println("This is m1.M1 - v1.0.2")
}
// 在m1的module root目录下
$git commit -m"update m1 to v1.0.2(broken)" .
[master af1dd21] update m1 to v1.0.2(broken)
1 file changed, 2 insertions(+), 1 deletion(-)
$git tag -m"tag v1.0.2(broken)" v1.0.2
$git push --tag origin master
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 492 bytes | 492.00 KiB/s, done.
Total 4 (delta 1), reused 0 (delta 0)
cTo https://bitbucket.org/bigwhite/m1.git
911bbc5..af1dd21 master -> master
* [new tag] v1.0.2 -> v1.0.2
```


就这样，我一不小心将一个处于broken状态的module版本m1@v1.0.2发布了出去！此时此刻，m1的v1.0.2版本还仅存在于其源仓库站点上，即**bitbucket/bigwhite/m1**中，**在任何一个GoProxy服务器上还尚无该版本的缓存**。

### 2. 发布处于broken状态的module对“消费者”的影响

依赖m1的两个项目c1和c2此时依赖的仍然是m1@v1.0.1版本，如未显式升级对m1的依赖，c1和c2的构建不会受到处于broken状态的module v1.0.2版本的影响。

并且此时此刻，由于m1@v1.0.2尚未被GoProxy服务器所缓存，在GOPROXY开启的情况下，go list是查不到m1有可升级的版本的：

```
// 以c2为例：
$go list -m -u all
github.com/bigwhite/c2
bitbucket.org/bigwhite/m1 v1.0.1
```


但如若绕开GOPROXY，那么go list则可以查找到m1的最新版本为v1.0.2(我们通过设置GONOPROXY来使得go list查询m1的源仓库而不是代理服务器上的缓存)：

```
$GONOPROXY="bitbucket.org/bigwhite/m1" go list -m -u all
github.com/bigwhite/c2
bitbucket.org/bigwhite/m1 v1.0.1 [v1.0.2]
```


此时，如若某个m1的消费者在GOPROXY开启的情况下显式更新对m1版本的依赖，以c2如此操作为例：

```
$ go get bitbucket.org/bigwhite/m1@v1.0.2
go: downloading bitbucket.org/bigwhite/m1 v1.0.2
# bitbucket.org/bigwhite/m1
/root/go/pkg/mod/bitbucket.org/bigwhite/m1@v1.0.2/m1.go:6:6: a declared but not used
```


c2对m1依赖版本的显式更新，触发了GOPROXY对m1@v1.0.2版本的缓存，上述操作后，当前的状态如下示意图：

![img{512x368}](../../assets/84ff99e0cdf9b6a3.png)


这之后，其他m1的消费者，比如c1，便能够在GOPROXY开启的情况下查询到m1存在新版本v1.0.2，即使它是broken的：

```
// 以c1为例：
$go list -m -u all
github.com/bigwhite/c1
bitbucket.org/bigwhite/m1 v1.0.1 [v1.0.2]
```


一旦broken的m1版本(v1.0.2)进入到Proxy的缓存，那么其“危害性”便“大肆传播”开了。此时module m1的新消费者都将受到影响！比如这里我们引入一个新的消费者c3(同样设置GOPROXY为goproxy.cn)：

```
// c3的main.go
package main
import (
"fmt"
"bitbucket.org/bigwhite/m1"
)
func main() {
fmt.Println("This is c3")
m1.M1()
}
```


c3的首次构建就会报错：

```
// c3下：
$go build
go: finding module for package bitbucket.org/bigwhite/m1
go: found bitbucket.org/bigwhite/m1 in bitbucket.org/bigwhite/m1 v1.0.2
# bitbucket.org/bigwhite/m1
/root/go/pkg/mod/bitbucket.org/bigwhite/m1@v1.0.2/m1.go:6:6: a declared but not used
```


下面是当前问题的最新状态图：

![img{512x368}](../../assets/147b4594102cb61c.png)


### 3. 如何作废掉已发布的那个module版本

如果在GOPATH时代，废掉一个之前发的包版本是分分钟的事情，因为那时包消费者依赖的都是latest commit。包作者只要fix掉问题、提交并重新发布即可。

但是在go module时代，作废掉一个已经发布了的go module版本，还真不是一件能轻易做好的事情。这很大程度是源于大量Go module代理服务器的存在。下面我们来看看可能的问题解决方法：

#### 1) 重新发布broken的module版本

要解决上述问题，Go包作者们的一个很直接的解决方法是：**重新发布broken的module版本**。但这样做真的能生效么？

如果所有m1的消费者都通过m1所在代码托管服务器(bitbucket)获取m1的特定版本，那么这种方法还真能解决掉这个问题。m1的作者仅需删除掉远程的tag: v1.0.2，在本地fix掉问题，然后重新tag v1.0.2并push发布到bitbucket上的仓库中即可。这样，对于已经get到broken v1.0.2的消费者来说，只需清除掉本地的module cache(go clean -modcache)，再重新构建即可；对于m1的新消费者，直接得到的就是重新发布后的v1.0.2版本。

但现实的情况时，Go在[1.13版本](https://mp.weixin.qq.com/s/Txqvanb17LYQYgohNiUHig)中就将GOPROXY的默认值设置为**https://proxy.golang.org,direct**了，国内我们通常使用七牛云的代理：goproxy.cn。因此，一旦一个module版本被发布，当某个消费者通过其配置的goproxy获取该版本时，该版本就会在短时间内被缓存在对应的代理服务器上。后续通过该goproxy服务器获取那个版本的m1时，请求不会再回到m1所在的源代码托管服务器，这样即便m1的源服务器上的v1.0.2版本得到了重新发布，那么散布在各个goproxy服务器上的broken v1.0.2依旧存在，并且被“传播”到各个m1消费者的开发环境中，而重新发布后的v1.0.2版本却得不到“传播”的机会：

![img{512x368}](../../assets/d10a22156bd398ea.png)


因此，从消费者的角度看，m1的v1.0.2版本依旧是一个broken的版本，**m1作者的解决措施无效**！

很多人问，即便m1的作者删除了v1.0.2这个发布版本，各大goproxy服务器上的broken v1.0.2版本是否也会被删除呢？遗憾的告诉你：不会。

Goproxy服务器当初的一个设计目标就是尽可能的缓存更多包/module。即便某个module的源码仓库都被删除了，这个module的各个版本依旧缓存在goproxy服务器上，这个module的消费者依然可以正常获取该module并顺利构建。因此，goproxy服务器当前的实现都没有主动删掉某个module缓存的特性。

#### 2) 发布module的新patch版本

面对上述问题，Go社区当前的最佳实践就是**发布module的新patch版本**。以上面m1为例，我们废除掉v1.0.2，在本地修正问题后，直接打v1.0.3标签，并发布push到远程代码服务器上。这样整体状态就变成了下面示意图中样子了：

![img{512x368}](../../assets/bf9404c62eff1fe0.png)


- 对于依赖m1@v1.0.1版本的c1，在未手工更新依赖版本的情况下，它仍然可以保持成功的构建；
- 对于m1的新消费者，比如c4，它首次构建时使用的就是m1的最新patch版v1.0.3，成功跨过了作废的v1.0.2并成功完成构建；
- 对于之前曾依赖v1.0.2版本的消费者c2来说，此时需要手工介入才能解决问题。我们在c2环境手工升级依赖版本到v1.0.3，这样c2也会得到成功构建。

### 4. Go 1.16增加retract指示符用于标识作废的module版本

上述的**发布module的新patch版本**的解决方法其实仍存在两个问题：

- 消费者如何发现m1发布了v1.0.3？
- 消费者如何知晓m1的作者将v1.0.2版本作废掉了？

根据前面的描述，如果尚无消费者手工下载v1.0.3，那么proxy server上不会有v1.0.3版本的缓存，在本地通过go list -u -m all 也查不到v1.0.3的存在，除非是在设置GONOPROXY=bitbucket.org/bigwhite/m1前提下的go list查询。

另外在[go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)及以前版本中，Go原生并没有提供标识某个版本作废的机制，在[Go 1.16](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)中，module的作者可以在自己module的go.mod中使用[retract指示符](https://github.com/golang/mod/commit/c0d644d00ab849f4506f17a98a5740bf0feff020)标识出哪些版本为作废的，不推荐使用的。语法形式如下：

```
// go.mod
retract v1.0.0 // single version
retract [v1.1.0, v1.2.0] // closed interval
```


我们还用m1为例，我们将m1的go.mod更新为如下内容：

```
//m1的go.mod
module bitbucket.org/bigwhite/m1
go 1.16
retract v1.0.2
```


将其放入v1.0.3标签中并发布！现在m1的消费者c2要查看m1是否有最新版本时，可以查看到以下内容(c2本地环境使用go1.16版本)：

```
$GONOPROXY=bitbucket.org/bigwhite/m1 go list -m -u all
github.com/bigwhite/c5
bitbucket.org/bigwhite/m1 v1.0.2 (retracted) [v1.0.3]
```


从go list的输出结果中，我们看到了v1.0.2版本上有了retracted的提示，提示该版本已经被m1的作者作废了，不应该再使用，应升级为v1.0.3。但retracted仅仅是一个提示作用，并不影响go build的结果，c2环境(之前在go.mod中依赖m1的v1.0.2)下的go build不会自动绕过v1.0.2，除非显式更新到v1.0.3。

**“Gopher部落”知识星球开球了**！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！78元简直就是白菜价，简直就是白piao! 欢迎大家订阅！

![](../../assets/d8e58987c0d3be58.png)


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