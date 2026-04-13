---
title: Go标准库flag包的“小陷阱”
url: https://tonybai.com/2021/04/12/pitfall-in-std-flag-pkg/
published: '2021-04-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go标准库flag包的“小陷阱”

![](../../assets/e96e49435a46d2ef.png)


[本文永久链接](https://tonybai.com/2021/04/12/pitfall-in-std-flag-pkg) – https://tonybai.com/2021/04/12/pitfall-in-std-flag-pkg

[Go语言号称“自带电池(battery-included)”](https://www.imooc.com/read/87/article/2341)，这意味着Go标准库可开箱即用，为Gopher提供了功能丰富的常用工具包，足以应付多数日常开发所需。尤其在Go语言擅长的领域，Go标准库工具包更是有着广泛的应用。下图是[Go官方2020年用户调查](https://blog.golang.org/survey2020-results)的结果：

![](../../assets/bf329a24786dd061.png)


我们看到cli([command-line interface](http://en.wikipedia.org/wiki/Command-line_interface))领域开发占据了Go语言应用的Top2位置，仅次于开发API/RPC服务。而普通cli应用的开发总是离不开标准库的flag包。

flag包估计是很多gopher入门go语言的**必经之路**。flag使用起来十分简单，功能也不差，常规的命令行程序的flag形式它都支持，比如下面这个示例程序：

```
// flag_demo1.go
package main
import (
"flag"
"fmt"
)
var (
n = flag.Int("n", 1234, "help message for flag n")
)
func main() {
flag.Parse()
fmt.Printf("n=%d\n", *n)
}
```


flag_demo1仅支持一个cmd flag: -n。我们可以像下面这样使用flag_demo1这个cli程序，为变量n传值：

```
$go build flag_demo1.go
$./flag_demo1
n=1234 //默认值
$./flag_demo1 -n 1111
n=1111
$./flag_demo1 --n 1111
n=1111 // --n和-n是等价的
$./flag_demo1 -n=2222
n=2222
$./flag_demo1 --n=2222
n=2222
```


我们看到，我们可以使用下面四种形式为一个整型flag变量传参数：

- -n value
- –n value
- -n=value
- –n=value

无论使用哪种形式，它们起到的效果是等价的。

但是当我们将flag放置在cli应用的最后面时，我们要小心了：

```
$./flag_demo1 show -n=2222
n=1234
```


我们看到虽然我们在命令行因公flag_demo1的参数列表中进行了-n=2222的参数传递，但flag_demo1的flag包直接**无视了这次参数传递**，而将变量n置为默认值1234了。

这是因为flag包的命令行参数的解析逻辑是：当碰到第一个非flag参数时，便停止解析。上面命令行执行时传入的“show”并非flag_demo1的flag参数，因此flag包就会在解析完show后停止后面命令行参数(-n=2222)的解析，于是上述命令行就等价于：

```
$./flag_demo1 show
n=1234
```


那么n=1234就不足为奇了！这被我称为**flag包的第一个“小陷阱”**。不仅像“show”这样的非flag参数可以阻断flag包对命令行参数列表的继续解析，单独存在的“-”和“–”也具有同样的“阻断功能”：

```
$./flag_demo1 -- -n=2222
n=1234
$./flag_demo1 - -n=2222
n=1234
```


我们也常在命令行flag参数中使用bool类的参数值，比如下面示例：

```
// flag_demo2.go
package main
import (
"flag"
"fmt"
)
var (
n = flag.Int("n", 1234, "int value for flag n")
b1 = flag.Bool("b1", false, "bool value for flag b1")
b2 = flag.Bool("b2", false, "bool value for flag b2")
)
func main() {
flag.Parse()
fmt.Printf("n=%d\n", *n)
fmt.Printf("b1=%t\n", *b1)
fmt.Printf("b2=%t\n", *b2)
}
```


这个示例中有两个bool型flag参数和一个int型flag参数，我们来运行一下该cli应用：

```
$go build flag_demo2.go
$./flag_demo2 -b1 true -b2 true -n 2222
n=1234
b1=true
b2=false
```


运行的输出似乎与预期结果不符啊！为什么b2变量的值依旧为false，变量n的值为啥不是2222？难道在多个flag参数下，flag包有bug？其实不是的！

问题就在于bool类型flag参数的特殊性。由于一些原因，bool类型flag参数不支持“-arg value”形式，只支持下面两种形式：

```
-arg
-arg=value
```


我们按bool类型flag参数的正确传递方法再运行一下上面的flag_demo2：

```
$./flag_demo2 -b1=true -b2=true -n 2222
n=2222
b1=true
b2=true
```


这回的输出与预期吻合。

但细心的朋友可能会发现，之前的错误用法：

```
$./flag_demo2 -b1 true -b2 true -n 2222
```


十分有迷惑性！因为变量b1的输出值是符合预期的，这让人误以为flag参数的传递方法是正确无误的。这种“错觉”让gopher不知不觉地掉入了**flag包的第二个“陷阱”**中。而上面的错误flag参数值传递实质上等价于：

```
$./flag_demo2 -b1
```


这就是为什么b1=true，而b2和n均为默认值的原因了！

flag包是我们日常最广泛使用的标准库包之一，因此务必了解flag包可能被误用的情况，别掉入flag包的“小陷阱”中！**陷阱虽小，出事是大**，希望这里的分享能帮助大家在日常绕过这些“陷阱”！

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖>中，欢迎小伙伴们订阅学习！

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

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论