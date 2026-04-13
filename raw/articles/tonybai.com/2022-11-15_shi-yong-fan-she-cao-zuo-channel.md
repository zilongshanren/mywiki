---
title: 使用反射操作channel
url: https://tonybai.com/2022/11/15/using-reflect-to-manipulate-channels/
published: '2022-11-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用反射操作channel

![](../../assets/9033c179fb383990.png)


[本文永久链接](https://tonybai.com/2022/11/15/using-reflect-to-manipulate-channels) – https://tonybai.com/2022/11/15/using-reflect-to-manipulate-channels

今年教师节极客时间送给讲师4999 SVIP卡，一直没顾过来用，上周激活后在极客时间的众多精品课和专栏中徜徉，收获颇丰。尤其是在拜读鸟窝老师的[《Go并发编程实战课》](http://gk.link/a/11OCq) 后，get到一个以前从未用过的“技能点”：**使用reflect操作channel**，这里整理一下，把它分享给大家。

### 1. channel常规语法的“限制”

Go语言实现了基于CSP（Communicating Sequential Processes）理论的并发方案。方案包含两个重要元素，一个是Goroutine，它是Go应用并发设计的基本构建与执行单元；另一个就是channel，它在并发模型中扮演着重要的角色。channel既可以用来实现Goroutine间的通信，还可以实现Goroutine间的同步。

我们先来简要回顾一下有关channel的常规语法。

我们可以通过make(chan T, n)创建元素类型为T、容量为n的channel类型实例，比如：

```
ch1 := make(chan int) // 创建一个无缓冲的channel实例ch1
ch2 := make(chan int, 5) // 创建一个带缓冲的channel实例ch2
```


Go提供了“<-”操作符用于对channel类型变量进行发送与接收操作，下面是一些对上述channel ch1和ch2进行收发操作的代码示例：

```
ch1 <- 13 // 将整型字面值13发送到无缓冲channel类型变量ch1中
n := <- ch1 // 从无缓冲channel类型变量ch1中接收一个整型值存储到整型变量n中
ch2 <- 17 // 将整型字面值17发送到带缓冲channel类型变量ch2中
m := <- ch2 // 从带缓冲channel类型变量ch2中接收一个整型值存储到整型变量m中
```


Go不仅提供了单独操作channel的语法，还提供了可以同时对多个channel进行操作的select-case语法，比如下面代码：

```
select {
case x := <-ch1: // 从channel ch1接收数据
... ...
case y, ok := <-ch2: // 从channel ch2接收数据，并根据ok值判断ch2是否已经关闭
... ...
case ch3 <- z: // 将z值发送到channel ch3中:
... ...
default: // 当上面case中的channel通信均无法实施时，执行该默认分支
}
```


我们看到：**select语法中的case数量必须是固定的**，我们只能把事先要交给select“监听”的channel准备好，在select语句中平铺开才可以。这就是select语句常规语法的限制，即**select语法不支持动态的case集合**。如果我们要监听的channel个数是不确定的，且在运行时会动态变化，那么select语法将无法满足我们的要求。

那怎么突破这一限制呢？鸟窝老师告诉我们用[reflect包](https://tonybai.com/2021/04/19/variable-operation-using-reflection-in-go)。

### 2. reflect.Select和reflect.SelectCase

很多朋友可能和我一样，因为没有使用过reflect包操作channel，就会以为reflect操作channel的能力是Go新版本才提供的，但实则不然。reflect包中用于操作channel的函数Select以及其切片参数的元素类型SelectCase早在Go 1.1版本就加入到Go语言中了，有下图为证：

![](../../assets/8f3772b21063dd05.png)


那么如何使用这一“古老”的机制呢？我们一起来看一些例子。

首先我们来看**第一种情况**，也是最好理解的一种情况，**即从一个动态的channel集合进行receive operations的select**，下面是示例代码：

```
// github.com/bigwhite/experiments/tree/master/reflect-operate-channel/select-recv/main.go
package main
import (
"fmt"
"math/rand"
"reflect"
"sync"
"time"
)
func main() {
var wg sync.WaitGroup
wg.Add(2)
var rchs []chan int
for i := 0; i < 10; i++ {
rchs = append(rchs, make(chan int))
}
// 创建SelectCase
var cases = createRecvCases(rchs)
// 消费者goroutine
go func() {
defer wg.Done()
for {
chosen, recv, ok := reflect.Select(cases)
if ok {
fmt.Printf("recv from channel [%d], val=%v\n", chosen, recv)
continue
}
// one of the channels is closed, exit the goroutine
fmt.Printf("channel [%d] closed, select goroutine exit\n", chosen)
return
}
}()
// 生产者goroutine
go func() {
defer wg.Done()
var n int
s := rand.NewSource(time.Now().Unix())
r := rand.New(s)
for i := 0; i < 10; i++ {
n = r.Intn(10)
rchs[n] <- n
}
close(rchs[n])
}()
wg.Wait()
}
func createRecvCases(rchs []chan int) []reflect.SelectCase {
var cases []reflect.SelectCase
// 创建recv case
for _, ch := range rchs {
cases = append(cases, reflect.SelectCase{
Dir: reflect.SelectRecv,
Chan: reflect.ValueOf(ch),
})
}
return cases
}
```


在这个例子中，我们通过createRecvCases这个函数创建一个元素类型为reflect.SelectCase的切片，之后使用reflect.Select可以监听这个切片集合，就像常规select语法那样，从有数据的recv Channel集合中随机选出一个返回。

reflect.SelectCase有三个字段：

```
// $GOROOT/src/reflect/value.go
type SelectCase struct {
Dir SelectDir // direction of case
Chan Value // channel to use (for send or receive)
Send Value // value to send (for send)
}
```


其中Dir字段的值是一个“枚举”，枚举值如下：

```
// $GOROOT/src/reflect/value.go
const (
_ SelectDir = iota
SelectSend // case Chan <- Send
SelectRecv // case <-Chan:
SelectDefault // default
)
```


从常量名我们也可以看出，Dir用于标识case的类型，SelectRecv表示这是一个从channel做receive操作的case，SelectSend表示这是一个向channel做send操作的case；SelectDefault则表示这是一个default case。

构建好SelectCase的切片后，我们就可以将其传给reflect.Select了。Select函数的语义与select关键字语义是一致的，它会监听传入的所有SelectCase，以上面示例为例，如果所有channel都没有数据，那么reflect.Select会阻塞，直到某个channel有数据或关闭。

Select函数有三个返回值：

```
// $GOROOT/src/reflect/value.go
func Select(cases []SelectCase) (chosen int, recv Value, recvOK bool)
```


对于上面示例而言，如果监听的某个case有数据了，那么Select的返回值chosen中存储了该channel在cases切片中的下标，recv中存储了从channel收到的值，recvOK等价于comma, ok模式的ok，当正常接收到由send channel操作发送的值时，recvOK为true，如果channel被close了，recvOK为false。

上面的示例启动了两个goroutine，一个goroutine充当消费者，由reflect.Select监听一组channel，当某个channel关闭时，该goroutine退出；另外一个goroutine则是随机的向这些channel中发送数据，发送10次后，关闭其中某个channel通知消费者退出。

我们运行一下该示例程序，得到如下结果：

```
$go run main.go
recv from channel [1], val=1
recv from channel [4], val=4
recv from channel [5], val=5
recv from channel [8], val=8
recv from channel [1], val=1
recv from channel [1], val=1
recv from channel [8], val=8
recv from channel [3], val=3
recv from channel [5], val=5
recv from channel [9], val=9
channel [9] closed, select goroutine exit
```


我们日常编码时经常会在select语句中加上default分支，以防止select完全阻塞，下面我们就来改造一下示例，让其增加对default分支的支持：

```
// github.com/bigwhite/experiments/tree/master/reflect-operate-channel/select-recv-with-default/main.go
package main
import (
"fmt"
"math/rand"
"reflect"
"sync"
"time"
)
func main() {
var wg sync.WaitGroup
wg.Add(2)
var rchs []chan int
for i := 0; i < 10; i++ {
rchs = append(rchs, make(chan int))
}
// 创建SelectCase
var cases = createRecvCases(rchs, true)
// 消费者goroutine
go func() {
defer wg.Done()
for {
chosen, recv, ok := reflect.Select(cases)
if cases[chosen].Dir == reflect.SelectDefault {
fmt.Println("choose the default")
continue
}
if ok {
fmt.Printf("recv from channel [%d], val=%v\n", chosen, recv)
continue
}
// one of the channels is closed, exit the goroutine
fmt.Printf("channel [%d] closed, select goroutine exit\n", chosen)
return
}
}()
// 生产者goroutine
go func() {
defer wg.Done()
var n int
s := rand.NewSource(time.Now().Unix())
r := rand.New(s)
for i := 0; i < 10; i++ {
n = r.Intn(10)
rchs[n] <- n
}
close(rchs[n])
}()
wg.Wait()
}
func createRecvCases(rchs []chan int, withDefault bool) []reflect.SelectCase {
var cases []reflect.SelectCase
// 创建recv case
for _, ch := range rchs {
cases = append(cases, reflect.SelectCase{
Dir: reflect.SelectRecv,
Chan: reflect.ValueOf(ch),
})
}
if withDefault {
cases = append(cases, reflect.SelectCase{
Dir: reflect.SelectDefault,
Chan: reflect.Value{},
Send: reflect.Value{},
})
}
return cases
}
```


在这个示例中，我们的createRecvCases函数增加了一个withDefault布尔型参数，当withDefault为true时，返回的cases切片中将包含一个default case。我们看到，创建defaultCase时，Chan和Send两个字段需要传入空的reflect.Value。

在消费者goroutine中，我们通过选出的case的Dir字段是否为reflect.SelectDefault来判定是否default case被选出，其余的处理逻辑不变，我们运行一下这个示例：

```
$go run main.go
recv from channel [8], val=8
recv from channel [8], val=8
choose the default
choose the default
choose the default
choose the default
choose the default
recv from channel [1], val=1
choose the default
choose the default
choose the default
recv from channel [3], val=3
recv from channel [6], val=6
choose the default
choose the default
recv from channel [0], val=0
choose the default
choose the default
choose the default
recv from channel [5], val=5
recv from channel [2], val=2
choose the default
choose the default
choose the default
recv from channel [2], val=2
choose the default
choose the default
recv from channel [2], val=2
choose the default
choose the default
channel [2] closed, select goroutine exit
```


我们看到，default case被选择的几率还是蛮大的。

最后，我们再来看看如何使用reflect包向channel中发送数据，看下面示例代码：

```
// github.com/bigwhite/experiments/tree/master/reflect-operate-channel/select-send/main.go
package main
import (
"fmt"
"reflect"
"sync"
)
func main() {
var wg sync.WaitGroup
wg.Add(2)
ch0, ch1, ch2 := make(chan int), make(chan int), make(chan int)
var schs = []chan int{ch0, ch1, ch2}
// 创建SelectCase
var cases = createCases(schs)
// 生产者goroutine
go func() {
defer wg.Done()
for range cases {
chosen, _, _ := reflect.Select(cases)
fmt.Printf("send to channel [%d], val=%v\n", chosen, cases[chosen].Send)
cases[chosen].Chan = reflect.Value{}
}
fmt.Println("select goroutine exit")
return
}()
// 消费者goroutine
go func() {
defer wg.Done()
for range schs {
var v int
select {
case v = <-ch0:
fmt.Printf("recv %d from ch0\n", v)
case v = <-ch1:
fmt.Printf("recv %d from ch1\n", v)
case v = <-ch2:
fmt.Printf("recv %d from ch2\n", v)
}
}
}()
wg.Wait()
}
func createCases(schs []chan int) []reflect.SelectCase {
var cases []reflect.SelectCase
// 创建send case
for i, ch := range schs {
n := i + 100
cases = append(cases, reflect.SelectCase{
Dir: reflect.SelectSend,
Chan: reflect.ValueOf(ch),
Send: reflect.ValueOf(n),
})
}
return cases
}
```


在这个示例中，我们针对三个channel：ch0，ch1和ch2创建了写操作的SelectCase，每个SelectCase的Send字段都被赋予了要发送给该channel的值，这里使用了“100+下标号”。

生产者goroutine中有一个“与众不同”的地方，那就是每次某个写操作触发后，我都将该SelectCase中的Chan重置为一个空Value，以防止下次该channel被重新选出：

```
cases[chosen].Chan = reflect.Value{}
```


运行一下该示例，我们得到：

```
$go run main.go
recv 101 from ch1
send to channel [1], val=101
send to channel [0], val=100
recv 100 from ch0
recv 102 from ch2
send to channel [2], val=102
select goroutine exit
```


通过上面的几个例子我们看到，reflect.Select有着与select等价的语义，且还支持动态增删和修改case，功能不可为不强大，现在还剩一点要care，那就是它的执行性能如何呢？我们接着往下看。

### 3. reflect.Select的性能

我们用benchmark test来对比一下常规select与reflect.Select在执行性能上的差别，下面是benchmark代码：

```
// github.com/bigwhite/experiments/tree/master/reflect-operate-channel/select-benchmark/benchmark_test.go
package main
import (
"reflect"
"testing"
)
func createCases(rchs []chan int) []reflect.SelectCase {
var cases []reflect.SelectCase
// 创建recv case
for _, ch := range rchs {
cases = append(cases, reflect.SelectCase{
Dir: reflect.SelectRecv,
Chan: reflect.ValueOf(ch),
})
}
return cases
}
func BenchmarkSelect(b *testing.B) {
var c1 = make(chan int)
var c2 = make(chan int)
var c3 = make(chan int)
go func() {
for {
c1 <- 1
}
}()
go func() {
for {
c2 <- 2
}
}()
go func() {
for {
c3 <- 3
}
}()
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
select {
case <-c1:
case <-c2:
case <-c3:
}
}
}
func BenchmarkReflectSelect(b *testing.B) {
var c1 = make(chan int)
var c2 = make(chan int)
var c3 = make(chan int)
go func() {
for {
c1 <- 1
}
}()
go func() {
for {
c2 <- 2
}
}()
go func() {
for {
c3 <- 3
}
}()
chs := createCases([]chan int{c1, c2, c3})
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
_, _, _ = reflect.Select(chs)
}
}
```


运行一下该benchmark：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/experiments/reflect-operate-channel/select-benchmark
... ...
BenchmarkSelect-8 2765396 427.8 ns/op 0 B/op 0 allocs/op
BenchmarkReflectSelect-8 1839706 806.0 ns/op 112 B/op 6 allocs/op
PASS
ok github.com/bigwhite/experiments/reflect-operate-channel/select-benchmark 3.779s
```


我们看到：reflect.Select的执行效率相对于select还是要差的，并且在其执行过程中还要做额外的内存分配。

### 4. 小结

本文介绍了reflect.Select与SelectCase的结构以及如何使用它们在不同场景下操作channel。但大多数情况下，我们是不需要使用reflect.Select，常规select语法足以满足我们的要求。并且reflect.Select有对cases数量的约束，最大支持65536个cases，虽然这个约束对于大多数场合而言足够用了。

本文涉及的示例源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/reflect-operate-channel)下载。

![](../../assets/89e5a36694056fe5.png)


[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感谢分享，原来chan也可以反射使用，受益匪浅。