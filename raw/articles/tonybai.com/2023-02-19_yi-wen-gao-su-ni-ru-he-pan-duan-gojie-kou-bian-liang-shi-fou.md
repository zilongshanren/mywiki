---
title: 一文告诉你如何判断Go接口变量是否相等
url: https://tonybai.com/2023/02/19/how-to-determine-if-two-interface-vars-are-equal/
published: '2023-02-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文告诉你如何判断Go接口变量是否相等

![](../../assets/292eeb3df4c6c129.png)


[本文永久链接](https://tonybai.com/2023/02/19/how-to-determine-if-two-interface-vars-are-equal) – https://tonybai.com/2023/02/19/how-to-determine-if-two-interface-vars-are-equal

近日一位[《Go语言第一课》专栏](http://gk.link/a/10AVZ)的读者向我提出一个问题，[代码](https://go.dev/play/p/83f40N7UCtu)如下：

```
func main() {
printNonEmptyInterface1()
}
type T struct {
name string
}
func (t T) Error() string {
return "bad error"
}
func printNonEmptyInterface1() {
var err1 error // 非空接口类型
var err1ptr error // 非空接口类型
var err2 error // 非空接口类型
var err2ptr error // 非空接口类型
err1 = T{"eden"}
err1ptr = &T{"eden"}
err2 = T{"eden"}
err2ptr = &T{"eden"}
println("err1:", err1)
println("err2:", err2)
println("err1 = err2:", err1 == err2) // true
println("err1ptr:", err1ptr)
println("err2ptr:", err2ptr)
println("err1ptr = err2ptr:", err1ptr == err2ptr) // false
}
```


他的问题就是：“当动态类型是指针的时候，接口变量不相等；当动态类型不是指针的时候，接口变量相等，这个怎么理解呢？”。

这个问题让我想到了[Go FAQ](https://go.dev/doc/faq)中那个著名的“nil error != nil”问题，它给很多Go初学者带去了疑惑。让我们先回顾一下GO FAQ中的这个问题的例子代码：

```
type MyError struct {
error
}
var ErrBad = MyError{
error: errors.New("bad things happened"),
}
func bad() bool {
return false
}
func returnsError() error {
var p *MyError = nil
if bad() {
p = &ErrBad
}
return p
}
func main() {
err := returnsError()
if err != nil {
fmt.Printf("error occur: %+v\n", err)
return
}
fmt.Println("ok")
}
```


运行这个[例子](https://go.dev/play/p/AYGFHKSWFDa)，我们将得到：

```
error occur: <nil>
```


就“nil error != nil”这个疑问，给大家简单说说**如何判断两个接口类型变量是否相等**。

[Go开源已经13年多了](https://tonybai.com/2022/11/11/go-opensource-13-years/)！各种渠道的资料也很多了，往往大家稍微深入学习一下，就知道了Go的接口类型在运行时是这样表示的：

```
// $GOROOT/src/runtime/runtime2.go
type iface struct { // 非空接口类型的运行时表示
tab *itab
data unsafe.Pointer
}
type eface struct { // 空接口类型的运行时表示
_type *_type
data unsafe.Pointer
}
```


两个结构的共同点是它们都有两个指针字段，第一个字段功能相似，都是表示类型信息的，而第二个指针字段的功能也相同，都是指向当前赋值给该接口类型变量的动态类型变量的值。

这样一来，判断两个接口类型变量是否相等，就是要判断这运行时表示中的类型信息与data信息是否相等。我们可以使用Go内置的println函数来输出接口变量的运行时表示，Go编译器会在编译阶段根据要输出的参数的类型将println替换为特定的运行时函数，这些函数都定义在\$GOROOT/src/runtime/print.go文件中，而针对eface和iface类型的打印函数实现如下：

```
// $GOROOT/src/runtime/print.go
func printeface(e eface) {
print("(", e._type, ",", e.data, ")")
}
func printiface(i iface) {
print("(", i.tab, ",", i.data, ")")
}
```


我们从printeface和printiface的实现可以看出println会将接口类型变量的类型信息与data信息输出。我们以上面Go FAQ中的例子来说，如果用println输出returnsError返回的error类型变量并与error(nil)作比较，代码如下：

```
func main() {
err := returnsError()
println(err)
println(error(nil))
... ...
}
```


我们将得到下面输出：

```
(0x4b7318,0x0) // println(err)
(0x0,0x0) // println(error(nil))
```


我们看到error(nil)的类型信息部分为nil，而err的类型信息部分是不可空的，因此两者肯定是不相等的，这也是为什么这个例子会输出“意料之外”的“error occur:

我们再回到本文开头的那个例子，运行例子后，输出如下内容：

```
err1: (0x10c6cc0,0xc000092f20)
err2: (0x10c6cc0,0xc000092f40)
err1 = err2: true
err1ptr: (0x10c6c40,0xc000092f50)
err2ptr: (0x10c6c40,0xc000092f30)
err1ptr = err2ptr: false
```


我们看到无论接口变量的动态类型是采用指针的，还是采用非指针的，接口类型变量的类型信息部分都相同，data部分都不同。但为什么一个输出true，另外一个输出false呢？

为了找到真正原因，我用[lensm工具](https://github.com/loov/lensm)以图形化方式展示出汇编与源Go代码的对应关系：

![](../../assets/d46dc8cfb6ea3007.png)


注：lensm v0.0.3以前的版本对于

[Go 1.20版本]编译的程序不起作用，[无法显示汇编对应的source]。

从图中我们看到，无论是err1 == err2，还是err1ptr == err2ptr，Go都会**调用runtime.ifaceeq来进行比较**！我们来看一下ifaceeq的比较逻辑：

```
// $GOROOT/src/runtime/alg.go
func efaceeq(t *_type, x, y unsafe.Pointer) bool {
if t == nil {
return true
}
eq := t.equal
if eq == nil {
panic(errorString("comparing uncomparable type " + t.string()))
}
if isDirectIface(t) {
// Direct interface types are ptr, chan, map, func, and single-element structs/arrays thereof.
// Maps and funcs are not comparable, so they can't reach here.
// Ptrs, chans, and single-element items can be compared directly using ==.
return x == y
}
return eq(x, y)
}
func ifaceeq(tab *itab, x, y unsafe.Pointer) bool {
if tab == nil {
return true
}
t := tab._type
eq := t.equal
if eq == nil {
panic(errorString("comparing uncomparable type " + t.string()))
}
if isDirectIface(t) {
// See comment in efaceeq.
return x == y
}
return eq(x, y)
}
```


这回对于接口类型变量的相等性判断一目了然了(由efaceeq中isDirectIface函数下面的注释可见)！

在两个接口类型变量的类型信息(_type/tab字段)相同的情况下，对于动态类型为指针的类型(direct interface type的一种)，直接比对的是两个接口类型变量的类型指针；若为其他非指针类型(Go会额外分配内存存储，data为指向新内存块的指针)，则调用类型(_type)信息中的eq函数，eq函数的实现也都是对data解引用后的“==”相等性判断。当然就像Go FAQ中的例子那样，如果两个接口类型变量的类型信息(_type/tab字段)不同，那么两个接口类型变量肯定不等。

好了，这回文章开头的读者疑问可以得到解决了：

- err1和err2两个接口变量的动态类型都是T，因此比较的是data指向的内存块的值，虽然err1和err2的data字段指向的是两个内存块，但这两个内存块中的T对象值相同(实质就是一个string)，因此err1 == err2为true；
- err1ptr和err2ptr两个接口变量的动态类型都是*T，因此比较的直接就是data的值，显然data值不同，因此err1ptr == err2ptr为false。

这个问题也让我之前对接口变量的“偏差”理解得到了纠正，更多关于接口在运行时表示与接口变量相等性判断的内容大家可以参考[《Go语言第一课》专栏](http://gk.link/a/10AVZ)第29讲！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论