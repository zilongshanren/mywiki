---
title: 记一次go panic问题的解决过程
url: https://tonybai.com/2019/04/04/notes-about-fixing-a-go-panic-problem/
published: '2019-04-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 记一次go panic问题的解决过程

## 一. Panic问题概述

本周收到客户在bugclose上填写的一个issue：添加一个下发通道后，pushd程序panic并退出了！程序panic时输出的stacktrace信息摘录如下：

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x8ca449]
goroutine 266900 [running]:
pkg.tonybai.com/smspush/vendor/github.com/bigwhite/gocmpp.(*Client).Connect(0xc42040c7f0, 0xc4203d29c0, 0x11, 0xc420423256, 0x6, 0xc420423260, 0x8, 0x37e11d600, 0x0, 0x0)
/root/.go/src/pkg.tonybai.com/smspush/vendor/github.com/bigwhite/gocmpp/client.go:79 +0x239
pkg.tonybai.com/smspush/pkg/pushd/pusher.cmpp2Login(0xc4203d29c0, 0x11, 0xc420423256, 0x6, 0xc420423260, 0x8, 0x37e11d600, 0xc4203d29c0, 0x11, 0x73)
/root/.go/src/pkg.tonybai.com/smspush/pkg/pushd/pusher/cmpp2_handler.go:25 +0x9a
pkg.tonybai.com/smspush/pkg/pushd/pusher.newCMPP2Loop(0xc42071f800, 0x4, 0xaaecd8)
/root/.go/src/pkg.tonybai.com/smspush/pkg/pushd/pusher/cmpp2_handler.go:65 +0x226
pkg.tonybai.com/smspush/pkg/pushd/pusher.(*tchanSession).Run(0xc42071f800, 0xaba7c3, 0x17)
/root/.go/src/pkg.tonybai.com/smspush/pkg/pushd/pusher/session.go:52 +0x98
pkg.tonybai.com/smspush/pkg/pushd/pusher.(*gateway).addSession.func1(0xc4200881a0, 0xc42071f800, 0xc42040c700)
/root/.go/src/pkg.tonybai.com/smspush/pkg/pushd/pusher/gateway.go:61 +0x11e
created by pkg.tonybai.com/smspush/pkg/pushd/pusher.(*gateway).addSession
/root/.go/src/pkg.tonybai.com/smspush/pkg/pushd/pusher/gateway.go:58 +0x350
```


印象中近大半年用[Go](https://tonybai.com/tag/go)写的程序，遇到panic情况不多。上一次是因为原生map变量的并发访问导致的panic，那次panic一眼就看到问题所在了。但这次又是因为啥呢？

## 二. 分析和debug过程

这个问题在印象中似乎出现过，不过由于当初没有复现，客户环境中又没有panic信息提供，那时没能定位和解决，后来问题并没有出现，显然这个问题是有一定“随机属性”。

对于panic，我们首先检查直接导致panic发生的那一行代码：

```
/root/.go/src/pkg.tonybai.com/smspush/vendor/github.com/bigwhite/gocmpp/client.go:79 +0x239
```


下面是client.go 79行周围的代码片段：

![img{512x368}](../../assets/07bec4cf40f37976.png)


也许是疏忽大意，当时瞅了一眼后，就断定这块没有问题（更多从业务协议层面考虑），这也直接导致后面绕了一个大圈子才查到”真凶”。如果您还没看出来问题，那继续往下看。

定式思维让我认为很可能是函数栈中的内存问题，于是我开始调查panic输出的函数调用栈中参数是否正确。

要想知道函数调用栈中参数传递是否有问题，先要知晓panic后输出的栈帧信息都是什么！比如下面panic dump信息中参数中的各种magic number都代表什么！

```
gocmpp.(*Client).Connect(0xc42040c7f0, 0xc4203d29c0, 0x11, 0xc420423256, 0x6, 0xc420423260, 0x8, 0x37e11d600, 0x0, 0x0)
pusher.cmpp2Login(0xc4203d29c0, 0x11, 0xc420423256, 0x6, 0xc420423260, 0x8, 0x37e11d600, 0xc4203d29c0, 0x11, 0x73)
pusher.newCMPP2Loop(0xc42071f800, 0x4, 0xaaecd8)
```


在Joe Shaw的[《Understanding Go panic output》](https://www.joeshaw.org/understanding-go-panic-output/)和William Kennedy的[《Stack Traces In Go》](https://www.ardanlabs.com/blog/2015/01/stack-traces-in-go.html)中有针对Stack trace输出信息的解析。关于Stack trace输出信息的识别，总体遵循几个要点：

-
stack trace中每个函数/方法后面的“参数数值”个数与函数/方法原型的参数个数不是一一对应的；

-
stack trace中每个函数/方法后面的“参数数值”是按照函数/方法原型参数列表中从左到右的参数类型的内存布局逐一展开的; 每个数值占用一个word(64位平台下面为8字节)

-
如果是method，则第一个参数是receiver自身。如果reciever是指针类型，则第一个参数数值就是一个指针地址；如果是非指针的实例，则stack trace会按照其内存布局输出；

-
函数/方法返回值放在stack trace的“参数数值”列表的后面；如果有多个返回值，则同样按从左到右顺序，按照返回值类型的内存布局输出；

-
指针类型参数：占用stack trace的“参数数值”列表的1个位置；数值表示指针值，也是指针指向的对象的地址；

-
string类型参数：由于string在内存中由两个字(word)表示，第一个字是数据指针，第二个字是string的长度，因此在stack trace的“参数数值”列表中将占用两个位置；

-
slice类型参数：由于slice类型在内存中由三个字表示，第一个word是数据指针，第二个word是len，第三个字是cap，因此在stack trace的“参数数值”列表中将占用三个位置；

-
内建整型(int,rune,byte)：由于按word逐个输出，对于类型长度不足一个Word的参数，会做合并处理；比如：一个函数有5个int16类型的参数，那么在stack trace的信息中，这5个参数将占用stack trace的“参数数值”列表中的两个位置；第一个位置是前4个参数的“合体”，第二个位置则是最后那个int16类型的参数值。

-
struct类型参数: 会按照struct中字段的内存布局顺序在stack trace中展开。

-
interface类型参数：由于interface类型在内存中由两部分组成，一部分是接口类型的参数指针，一部分是接口值的参数指针，因此interface类型参数将用stack trace的“参数数值”列表中的两个位置。

-
stack trace输出的信息是在函数调用过程中的“快照”信息，因此一些输出数值看似不合理，但是由于其并不是最终值，所以问题不一定发生在这些参数身上，比如：返回值参数。


结合上面要点、函数/方法原型以及stack trace的输出，我们来“定位”一下stack trace输出的各个“参数”的含义：

cmpp2Login和Connect的原型以及调用关系如下：

```
func cmpp2Login(dstAddr, user, password string, connectTimeout time.Duration) (*cmpp.Client, error)
func (cli *Client) Connect(servAddr, user, password string, timeout time.Duration) error
func cmpp2Login(dstAddr, user, password string, connectTimeout time.Duration) (*cmpp.Client, error) {
c := cmpp.NewClient(cmpp.V21)
return c, c.Connect(dstAddr, user, password, connectTimeout)
}
```


对照后，我们得出下面对应关系：

```
pusher.cmpp2Login(
0xc4203d29c0, // dstAddr的data pointer
0x11, // dstAddr string的length
0xc420423256, // user 的data pointer
0x6, // user string的length
0xc420423260, // password的data pointer
0x8, // password string的length
0x37e11d600, // connectTimeout
0xc4203d29c0, // 返回值：Client的指针
0x11, // 返回值：error接口的type pointer
0x73) // 返回值：error接口的data pointer
gocmpp.(*Client).Connect(
0xc42040c7f0, //cli的指针
0xc4203d29c0, //servAddr string的data pointer
0x11, //servAddr string的 length
0xc420423256, // user string的data pointer
0x6, // user string的length
0xc420423260, // password的data pointer
0x8, // password string的length
0x37e11d600, // timeout
0x0, // 返回值：error接口的type pointer
0x0) // 返回值：error接口的data pointer
```


在这里，cmpp2Login的dstAddr、user、password、connectTimeout这些输入参数值都非常正常；看起来不正常的两个返回值在栈帧中的值其实意义不大，因为connect没有返回，所以这些值处于“非最终态”；而Connect执行到第79行panic，因此其返回值error的两个值也是处于“中间状态”。

这样一来，似乎没有参数是错误的！

## 三. 回到起点，捉住“真凶”

在反复查看代码和对比stack trace的参数列表后，依然没有找到蛛丝马迹。遂决定平复心情，从头再来，回到起点！

```
var ok bool
var status uint8
if cli.typ == V20 || cli.typ == V21 {
var rsp *Cmpp2ConnRspPkt
rsp, ok = p.(*Cmpp2ConnRspPkt)
status = rsp.Status
} else {
var rsp *Cmpp3ConnRspPkt
rsp, ok = p.(*Cmpp3ConnRspPkt)
status = uint8(rsp.Status) <------ 79行
}
if !ok {
err = ErrRespNotMatch
return err
}
```


又反复看了这段代码！程序正常执行时都是经过这段代码的，都是正常的。为何随机爆出panic呢？79行如果要panic，显然是rsp为nil或其他非法地址。但rsp是由p进行type assertion而来的！难道是type assertion失败了！！！

从正常业务流程来看，这里是不会失败的！这也是当初这里没有立即检查ok这个bool值的原因。但是特殊情况下，也就是当tcp连接建立后，conn包发出后，对方未必返回是conn response包，很可能是其他包回来（比如active test），这样就会导致这块的type assertion失败！这也与这个问题随机发生的情况吻合！

而且当初保留了“ok”，而不是用”_”代替，说明设计思路中是存在返回的包不是conn response包的情况。看来是当初coding时逻辑混乱了:(

这就是问题所在了！**教训：type assertion后一定要在检查ok这个bool值之后再决定是否使用assertion之后的变量**。

## 四. 其他

借着这个问题的解决过程，再多说一句 stacktrace。在[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)及以后版本中，go compiler做了更深入的优化，很多“简单”的函数或方法会被自动inline(内联)了，函数一旦内联化了，那么在stack trace中我们就无法看到栈帧信息了，就会看到如下在栈帧信息中存在省略号的情况：

```
$go run stacktrace.go
panic: panic in foo
goroutine 1 [running]:
main.(*Y).foo(...)
/Users/tony/test/go/stacktrace/stacktrace2.go:32
main.main()
/Users/tony/test/go/stacktrace/stacktrace.go:51 +0x39
exit status 2
```


可以使用-gcflags=”-l”来告诉编译器不要inline。至于是否要这么做，就要看debug和性能之间您是如何权衡的了。

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

这个一眼就能看出吧……ok后面必然会有个if的，你这里没有

内联的函数也会有栈帧的

当局者迷吧，调试三年前的代码难免疏漏。另外内联函数最初是无法在stack traceback信息中出现的；后来这个问题fix了。inline函数的函数名出现在stack traceback中。但参数列表只会显示（…)。go 1.11及后续版本均是如此。

哈哈，有ok先判断ok，这个坑我也踩过。

“关于Stack trace输出信息的识别，总体遵循几个要点：”

这部分规则，在苹果的M系列芯片上似乎有些差别？我无法在M1芯片的机器上复现出这些结果，也无法找到更多的解释，想问问Tony有没有更多的研究

我手里没有M1机器，M1是arm64的cpu架构，在stack trace输出上估计会有差别，你那边输出的是什么信息呢？

此外，你用的go版本是多少？较新版本的go引入了更多的优化，一些函数很容易被inline掉，那样就看不到函数调用栈信息了。go build -gcflags ‘-l -N’ xxx.go来关闭优化。此外，我看到较新版本的go在输出栈跟踪信息做的更好了，比如：

func Example(slice []string, str string, i int) {

panic(“Want stack trace”)

}

这样的函数输出的栈跟踪信息：

goroutine 1 [running]:

main.Example({0xc00004a730, 0×2, 0×4}, {0×1064942, 0×5}, 0xa)

/Users/tonybai/test/go/stacktrace/trace1.go:9 +0×45

main.main()

/Users/tonybai/test/go/stacktrace/trace1.go:5 +0×85

你可以看到，go将slice、string这样的参数类型用大括号将其内部组成括起来，方便大家区别查看了。

调用栈的参数有时候会带着问号，这是啥意思

找到了，是go 1.18新增的，如果是栈传参的话，panic打印出的参数可能是不确定的，不确定的参数会带上问号

手动点赞！