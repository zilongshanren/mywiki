---
title: Go中被闭包捕获的变量何时会被回收
url: https://tonybai.com/2021/08/09/when-variables-captured-by-closures-are-recycled-in-go/
published: '2021-08-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go中被闭包捕获的变量何时会被回收

![](../../assets/9d5f7de28f03796a.png)


[本文永久链接](https://tonybai.com/2021/08/09/when-variables-captured-by-closures-are-recycled-in-go) – https://tonybai.com/2021/08/09/when-variables-captured-by-closures-are-recycled-in-go

### 1. Go函数闭包

Go语言原生提供了对闭包(closure)的支持。在Go语言中，闭包就是[函数字面值](https://tip.golang.org/ref/spec#Function_literals)。Go规范中是这样诠释闭包的：

函数字面值(function literals)是闭包：它们可以引用其包裹函数(surrounding function)中定义的变量。然后，这些变量在包裹函数和函数字面值之间共享，只要它们可以被访问，它们就会继续存在。


闭包在Go语言中有着广泛的应用，最常见的就是与go关键字一起联合使用创建一个新goroutine，比如下面标准库中net/http包中的一段代码：

```
// $GOROOT/src/net/http/fileTransport.go
00 func (t fileTransport) RoundTrip(req *Request) (resp *Response, err error) {
01 rw, resc := newPopulateResponseWriter()
02 go func() {
03 t.fh.ServeHTTP(rw, req)
04 rw.finish()
05 }()
06 return <-resc, nil
07 }
```


上面这段代码中的RoundTrip方法就是使用go关键字结合闭包创建了一个新的goroutine，并且在这个goroutine中运行的函数还引用了本属于其外部包裹函数的变量：t、rw和req，或者说两者共享这些变量。

原本仅在RoundTrip方法内部使用的变量一旦被“共享”给了其他函数，那么它就无法在栈上分配了，[逃逸到堆上](https://mp.weixin.qq.com/s/ALzzT1kQ3VfYQly1LT7mQw)是确定性事件。

那么问题来了！这些被引用或叫**被闭包捕获**的分配在堆上的外部变量何时能被回收呢？也许上面的例子还十分容易理解，当新创建的goroutine执行完毕后，这些变量就可以回收了。那么下面的闭包函数呢？

```
func foo() func(int) int {
i := []int{0: 10, 1: 11, 15: 128}
return func(n int) int {
n+=i[0]
return n
}
}
```


在这个foo函数中，被闭包函数捕获的长度为16的切片变量i何时可以被回收呢？

注：我们定义闭包时，喜欢用引用外部包裹函数的变量这种说法，但在

[Go编译器的实现代码]中，使用的是capture var，翻译过来就是“被捕获的变量”，所以这里也用了“捕获”一词来表示那些被闭包共享使用的外部包裹函数甚至是更外层函数中的变量。

foo函数的返回值类型是一个函数，也就是说foo函数的本地变量i被foo返回的新创建的闭包函数所捕获，i不会被回收。通常一个堆上的内存对象有明确的引用它的对象或指向它的地址的指针，该对象才会继续存活，当其不可达(unreachable)时，即再没有引用它的对象或指向它的指针时才会被GC回收。

那么，变量i究竟是被谁引用了呢？变量i将在何时被回收呢？

我们先回头看一个非闭包的一般函数：

```
func f1() []int {
i := []int{0: 10, 1: 11, 15: 128}
return i
}
func f2() {
sl := f1()
sl[0] = sl[0] + 10
fmt.Println(sl)
}
func main() {
f2()
}
```


我们看到f1将自己的局部切片变量i返回后，该变量被f2函数中的sl所引用，f2函数执行完成后，切片变量i将变成unreachable，GC将回收该变量对应的堆内存。

如果换成闭包函数，比如前面的foo函数，我们很大可能是这么来用的：

```
// https://github.com/bigwhite/experiments/tree/master/closure/closure1.go
1 package main
2
3 import "fmt"
4
5 func foo() func(int) int {
6 i := []int{0: 10, 1: 11, 15: 128}
7 return func(n int) int {
8 n += i[0]
9 return n
10 }
11 }
12
13 func bar() {
14 f := foo()
15 a := f(5)
16 fmt.Println(a)
17 }
18
19 func main() {
20 bar()
21 g := foo()
22 b := g(6)
23 fmt.Println(b)
24 }
```


在这里例子中，只要闭包函数中引用了foo函数的本地变量。这突然让我想起了“[在Go中，函数也是一等公民的特性](https://www.imooc.com/read/87/article/2420)”。难道是闭包函数这一对象引用了foo函数的本地变量? 那么闭包函数在内存布局上是如何引用到foo函数的本地整型切片变量i的呢？闭包函数在内存布局中被映射为什么了呢？

如果一门编程语言对某种语言元素的创建和使用没有限制，我们可以像对待值(value)一样对待这种语法元素，那么我们就称这种语法元素是这门编程语言的“一等公民”。


### 2. Go闭包函数对象

要解答这个问题，我们只能寻求[Go汇编](https://tip.golang.org/doc/asm)的帮助。我们生成上面的closure1.go的汇编代码(我们使用go 1.16.5版本Go编译器)：

```
$go tool compile -S closure1.go > closure1.s
```


在汇编代码中，我们找到closure1.go中第7行创建一个闭包函数所对应的汇编代码：

```
// https://github.com/bigwhite/experiments/tree/master/closure/closure1.s
0x0052 00082 (closure1.go:7) LEAQ type.noalg.struct { F uintptr; "".i []int }(SB), CX
0x0059 00089 (closure1.go:7) MOVQ CX, (SP)
0x005d 00093 (closure1.go:7) PCDATA $1, $1
0x005d 00093 (closure1.go:7) NOP
0x0060 00096 (closure1.go:7) CALL runtime.newobject(SB)
0x0065 00101 (closure1.go:7) MOVQ 8(SP), AX
0x006a 00106 (closure1.go:7) LEAQ "".foo.func1(SB), CX
0x0071 00113 (closure1.go:7) MOVQ CX, (AX)
0x0074 00116 (closure1.go:7) MOVQ $16, 16(AX)
0x007c 00124 (closure1.go:7) MOVQ $16, 24(AX)
0x0084 00132 (closure1.go:7) PCDATA $0, $-2
0x0084 00132 (closure1.go:7) CMPL runtime.writeBarrier(SB), $0
0x008b 00139 (closure1.go:7) JNE 165
0x008d 00141 (closure1.go:7) MOVQ ""..autotmp_7+16(SP), CX
0x0092 00146 (closure1.go:7) MOVQ CX, 8(AX)
0x0096 00150 (closure1.go:7) PCDATA $0, $-1
0x0096 00150 (closure1.go:7) MOVQ AX, "".~r0+40(SP)
0x009b 00155 (closure1.go:7) MOVQ 24(SP), BP
0x00a0 00160 (closure1.go:7) ADDQ $32, SP
0x00a4 00164 (closure1.go:7) RET
0x00a5 00165 (closure1.go:7) PCDATA $0, $-2
0x00a5 00165 (closure1.go:7) LEAQ 8(AX), DI
0x00a9 00169 (closure1.go:7) MOVQ ""..autotmp_7+16(SP), CX
0x00ae 00174 (closure1.go:7) CALL runtime.gcWriteBarrierCX(SB)
0x00b3 00179 (closure1.go:7) JMP 150
0x00b5 00181 (closure1.go:7) NOP
```


汇编总是晦涩难懂。我们重点看第一行：

```
0x0052 00082 (closure1.go:7) LEAQ type.noalg.struct { F uintptr; "".i []int }(SB), CX
```


我们看到对应到Go源码中创建闭包函数的第7行，这行汇编代码大致意思是将一个结构体对象的地址放入CX。我们把这个结构体对象摘录出来：

```
struct {
F uintptr
i []int
}
```


这个结构体对象是哪里来的呢？显然是Go编译器根据闭包函数的“特征”创建出来的。其中的F就是闭包函数自身的地址，毕竟是函数，这个地址与一般函数的地址应该是在一个内存区域（比如rodata的只读数据区），那么整型切片变量i呢？难道这就是闭包函数所捕获的那个Foo函数本地变量i。没错！正是它。如果不信，我们可以再定义一个捕获更多变量的闭包函数来验证一下。

下面是一个捕获3个整型变量的闭包函数的生成函数：

```
// https://github.com/bigwhite/experiments/tree/master/closure/closure2.go
func foo() func(int) int {
var a, b, c int = 11, 12, 13
return func(n int) int {
a += n
b += n
c += n
return a + b + c
}
}
```


其对应的汇编代码中那个闭包函数结构为：

```
0x0084 00132 (closure2.go:10) LEAQ type.noalg.struct { F uintptr; "".a *int; "".b *int; "".c *int }(SB), CX
```


将该结构体提取出来，即：

```
struct {
F uintptr
a *int
b *int
c *int
}
```


到这里，我们证实了**引用了包裹函数本地变量的正是闭包函数自身，即编译器为其在内存中建立的闭包函数结构体对象**。通过unsafe包，我们甚至可以输出这个闭包函数对象。以closure2.go为例，我们来尝试一下，如下面代码所示。

```
// https://github.com/bigwhite/experiments/tree/master/closure/closure2.go
func foo() func(int) int {
var a, b, c int = 11, 12, 13
return func(n int) int {
a += n
b += n
c += n
return a + b + c
}
}
type closure struct {
f uintptr
a *int
b *int
c *int
}
func bar() {
f := foo()
f(5)
pc := *(**closure)(unsafe.Pointer(&f))
fmt.Printf("%#v\n", *pc)
fmt.Printf("a=%d, b=%d,c=%d\n", *pc.a, *pc.b, *pc.c)
f(6)
fmt.Printf("a=%d, b=%d,c=%d\n", *pc.a, *pc.b, *pc.c)
}
```


在上面代码中，我们参考汇编的输出定义了closure这个结构体来对应内存中的闭包函数对象(每种闭包对象都是不同的，一个技巧就是参考汇编输出的对象来定义)，通过unsafe的地址转换，我们将内存中的闭包对象映射到closure结构体实例上。运行上面程序，我们可以得到如下输出：

```
$go run closure2.go
main.closure{f:0x10a4d80, a:(*int)(0xc000118000), b:(*int)(0xc000118008), c:(*int)(0xc000118010)}
a=16, b=17,c=18
a=22, b=23,c=24
```


在上面的例子中，闭包函数捕获了外部变量a、b和c，这些变量实质上被编译器创建的闭包内存对象所引用。当我们调用foo函数时，闭包函数对象创建（其地址赋值给变量f)。这样，f对象一直引用着变量a、b和c。只有当f被回收，a、b和c才会因unreachable而被回收。

如果我们在闭包函数中仅仅是对捕获的外部变量进行只读操作，那么闭包函数对象不会存储这些变量的指针，而仅会做一份值拷贝。当然，如果某个变量被一个函数中创建的多个闭包所捕获，并且有的只读，有的修改，那么闭包函数对象还是会存储该变量的地址的。

了解了闭包函数的本质，我们再来看本文标题中的问题就容易多了。其答案就是**在捕捉变量的闭包函数对象被回收后，如果这些被捕捉的变量没有其他引用，它们将变为unreachable的，后续就会被GC回收了**。

### 3. 小结

我们回顾一下文章开头引用的Go语言规范中对闭包诠释中提到的一句话：“只要它们可以被访问，它们就会继续存在”。现在看来，我们可以将其理解为：**只要闭包函数对象存在，其捕获的那些变量就会存在，就不会被回收**。

闭包函数的这种机制决定了我们在日常使用过程中也要时刻考虑着闭包函数所捕获的变量可能的“延迟回收”。如果某个场景下，闭包引用的变量占用内存较大，且闭包函数对象被创建出的数量很多且因业务需要延迟很久才会被执行(比如定时器场景)，这就会导致堆内存可能长期处于高水位，我们要考虑内存容量是否能承受这样的水位，如果不能，则要考虑更换实现方案了。

本文涉及的所有代码可以从[这里下载](https://github.com/bigwhite/experiments/tree/master/closure)：https://github.com/bigwhite/experiments/tree/master/closure

### 4. 参考资料

- 深入理解函数闭包 – https://zhuanlan.zhihu.com/p/56750616
- Go语言高级编程 – https://github.com/chai2010/advanced-go-programming-book/blob/master/ch3-asm/ch3-06-func-again.md#366-闭包函数

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

© 2021, [bigwhite](https://tonybai.com). 版权所有.

No related posts.

悟了 感谢tony老师

不客气，有收获就好:)