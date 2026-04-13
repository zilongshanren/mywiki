---
title: 使用reflect包在反射世界里读写各类型变量
url: https://tonybai.com/2021/04/19/variable-operation-using-reflection-in-go/
published: '2021-04-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用reflect包在反射世界里读写各类型变量

![](../../assets/94a01728a7bf7e07.png)


[本文永久链接](https://tonybai.com/2021/mm/dd/variable-operation-using-reflection-in-go) – https://tonybai.com/2021/mm/dd/variable-operation-using-reflection-in-go

Go在标准库中提供的[reflect包](https://www.imooc.com/read/87/article/2474)让Go程序具备[运行时的反射能力(reflection)](https://www.imooc.com/read/87/article/2474)，但这种反射能力也是一把“双刃剑”，它在解决一类特定问题方面具有优势，但也带来了逻辑不清晰、性能问题以及难于发现问题和调试等不足。不过从Go诞生伊始就随着Go一起发布的reflect包是Go不可或缺的重要能力，不管你是否使用，都要掌握使用reflect与类型系统交互的基本方法，比如**在反射的世界里如何读写各类型变量**。本文就来和大家快速过一遍使用reflect包读写Go基本类型变量、复合类型变量的方法以及它们的应用。

### 1. 基本类型

进入reflect世界的大门主要有两个：reflect.ValueOf和reflect.TypeOf。进入到反射世界，每个变量都能找到一个与自己的对应的reflect.Value，通过该Value我们可以读写真实世界的变量信息。这里主要和大家过一遍操作各类型变量值的方法，因此主要用到的是reflect.ValueOf。


Go原生基本类型(非复合类型)主要包括：

- 整型(int, int8, int16, int32(rune), int64, uint, uint8(byte), uint16, uint32, uint64)
- 浮点型(float32, float64)
- 复数类型(complex64, complex128)
- 布尔类型(bool)
- 字符串类型(string)

我们在反射的世界里如何获取这些类型变量的值，又或如何在反射的世界里修改这些变量的值呢？下面这个示例可以作为日常使用reflect读写Go基本类型变量的速查表：

```
// github.com/bigwhite/experiments/blob/master/vars-in-reflect/basic/main.go
package main
import (
"fmt"
"reflect"
)
func main() {
// 整型
var i int = 11
vi := reflect.ValueOf(i) // reflect Value of i
fmt.Printf("i = [%d], vi = [%d]\n", i, vi.Int()) // i = [11], vi = [11]
// vi.SetInt(11 + 100) // panic: reflect: reflect.Value.SetInt using unaddressable value
vai := reflect.ValueOf(&i) // reflect Value of Address of i
vi = vai.Elem()
fmt.Printf("i = [%d], vi = [%d]\n", i, vi.Int()) // i = [11], vi = [11]
vi.SetInt(11 + 100)
fmt.Printf("after set, i = [%d]\n", i) // after set, i = [111]
// 整型指针
i = 11
var pi *int = &i
vpi := reflect.ValueOf(pi) // reflect Value of pi
vi = vpi.Elem()
vi.SetInt(11 + 100)
fmt.Printf("after set, i = [%d]\n", i) // after set, i = [111]
// 浮点型
var f float64 = 3.1415
vaf := reflect.ValueOf(&f)
vf := vaf.Elem()
fmt.Printf("f = [%f], vf = [%f]\n", f, vf.Float()) // f = [3.141500], vf = [3.141500]
vf.SetFloat(100 + 3.1415)
fmt.Printf("after set, f = [%f]\n", f) // after set, f = [103.141500]
// 复数型
var c = complex(5.1, 6.2)
vac := reflect.ValueOf(&c)
vc := vac.Elem()
fmt.Printf("c = [%g], vc = [%g]\n", f, vc.Complex()) // c = [103.1415], vc = [(5.1+6.2i)]
vc.SetComplex(complex(105.1, 106.2))
fmt.Printf("after set, c = [%g]\n", c) // after set, c = [(105.1+106.2i)]
// 布尔类型
var b bool = true
vab := reflect.ValueOf(&b)
vb := vab.Elem()
fmt.Printf("b = [%t], vb = [%t]\n", b, vb.Bool()) // b = [true], vb = [true]
vb.SetBool(false)
fmt.Printf("after set, b = [%t]\n", b) // after set, b = [false]
// 字符串类型
var s string = "hello, reflect"
vas := reflect.ValueOf(&s)
vs := vas.Elem()
fmt.Printf("s = [%s], vs = [%s]\n", s, vs.String()) // s = [hello, reflect], vs = [hello, reflect]
vs.SetString("bye, reflect")
fmt.Printf("after set, s = [%s]\n", s) // after set, s = [bye, reflect]
}
```


我们看到：

-
原生基本类型变量通过reflect.ValueOf进入反射世界，如果最终要在反射世界修改原变量的值，那么传给ValueOf的不应该是变量自身，而是该变量的地址，指针类型除外。

-
进入反射世界后，利用reflect.Value的Elem方法获取指针/地址指向的真正存储变量值的Value实例，通过Value类型提供的各种“方法糖”读取变量的值，比如：reflect.Value.Int、reflect.Value.String、reflect.Value.Bool等。

-
同样，在反射世界中，我们通过reflect.Value的SetXXX系列方法在运行时设置相关变量的值，从而达到写变量的目的。


### 2. 复合类型

前面我们已经看到，使用reflect包在反射世界读写原生基本类型的变量还是相对容易的多的，接下来我们再来看看复合类型(Composite type)变量的读写。

Go中的复合类型包括：

- 数组
- 切片
- map
- 结构体
- channel

与基本类型变量不同，复合变量多由同构和异构的字段(field)或元素(element)组成，如何读写复合类型变量中的字段或元素的值才是我们需要考虑的问题。下面这个示例可作为日常使用reflect在反射世界里读写Go复合类型变量中字段或元素值的速查表：

```
// github.com/bigwhite/experiments/blob/master/vars-in-reflect/composite/main.go
package main
import (
"fmt"
"reflect"
"unsafe"
)
type Foo struct {
Name string
age int
}
func main() {
// 数组
var a = [5]int{1, 2, 3, 4, 5}
vaa := reflect.ValueOf(&a) // reflect Value of Address of arr
va := vaa.Elem()
va0 := va.Index(0)
fmt.Printf("a0 = [%d], va0 = [%d]\n", a[0], va0.Int()) // a0 = [1], va0 = [1]
va0.SetInt(100 + 1)
fmt.Printf("after set, a0 = [%d]\n", a[0]) // after set, a0 = [101]
// 切片
var s = []int{11, 12, 13}
vs := reflect.ValueOf(s)
vs0 := vs.Index(0)
fmt.Printf("s0 = [%d], vs0 = [%d]\n", s[0], vs0.Int()) // s0 = [11], vs0 = [11]
vs0.SetInt(100 + 11)
fmt.Printf("after set, s0 = [%d]\n", s[0]) // after set, s0 = [111]
// map
var m = map[int]string{
1: "tom",
2: "jerry",
3: "lucy",
}
vm := reflect.ValueOf(m)
vm_1_v := vm.MapIndex(reflect.ValueOf(1)) // the reflect Value of the value of key 1
fmt.Printf("m_1 = [%s], vm_1 = [%s]\n", m[1], vm_1_v.String()) // m_1 = [tom], vm_1 = [tom]
vm.SetMapIndex(reflect.ValueOf(1), reflect.ValueOf("tony"))
fmt.Printf("after set, m_1 = [%s]\n", m[1]) // after set, m_1 = [tony]
// 为map m新增一组key-value
vm.SetMapIndex(reflect.ValueOf(4), reflect.ValueOf("amy"))
fmt.Printf("after set, m = [%#v]\n", m) // after set, m = [map[int]string{1:"tony", 2:"jerry", 3:"lucy", 4:"amy"}]
// 结构体
var f = Foo{
Name: "lily",
age: 16,
}
vaf := reflect.ValueOf(&f)
vf := vaf.Elem()
field1 := vf.FieldByName("Name")
fmt.Printf("the Name of f = [%s]\n", field1.String()) // the Name of f = [lily]
field2 := vf.FieldByName("age")
fmt.Printf("the age of f = [%d]\n", field2.Int()) // the age of f = [16]
field1.SetString("ally")
// field2.SetInt(8) // panic: reflect: reflect.Value.SetInt using value obtained using unexported field
nAge := reflect.NewAt(field2.Type(), unsafe.Pointer(field2.UnsafeAddr())).Elem()
nAge.SetInt(8)
fmt.Printf("after set, f is [%#v]\n", f) // after set, f is [main.Foo{Name:"ally", age:8}]
// 接口
var g = Foo{
Name: "Jordan",
age: 40,
}
// 接口底层动态类型为复合类型变量
var i interface{} = &g
vi := reflect.ValueOf(i)
vg := vi.Elem()
field1 = vg.FieldByName("Name")
fmt.Printf("the Name of g = [%s]\n", field1.String()) // the Name of g = [Jordan]
field2 = vg.FieldByName("age")
fmt.Printf("the age of g = [%d]\n", field2.Int()) // the age of g = [40]
nAge = reflect.NewAt(field2.Type(), unsafe.Pointer(field2.UnsafeAddr())).Elem()
nAge.SetInt(50)
fmt.Printf("after set, g is [%#v]\n", g) // after set, g is [main.Foo{Name:"Jordan", age:50}]
// 接口底层动态类型为基本类型变量
var n = 5
i = &n
vi = reflect.ValueOf(i).Elem()
fmt.Printf("i = [%d], vi = [%d]\n", n, vi.Int()) // i = [5], vi = [5]
vi.SetInt(10)
fmt.Printf("after set, n is [%d]\n", n) // after set, n is [10]
// channel
var ch = make(chan int, 100)
vch := reflect.ValueOf(ch)
vch.Send(reflect.ValueOf(22))
j := <-ch
fmt.Printf("recv [%d] from channel\n", j) // recv [22] from channel
ch <- 33
vj, ok := vch.Recv()
fmt.Printf("recv [%d] ok[%t]\n", vj.Int(), ok) // recv [33] ok[true]
}
```


从上述示例，我们可以得到如下一些信息：

- 在反射的世界里，reflect包针对复合类型中的元素或字段的读写提供了相应的方法，比如针对数组、切片元素的Value.Index，针对map key-value的Value.MapIndex，针对结构体字段的Field、FieldByName，针对channel的Send和Recv。
- 切片、map和channel由于
[其底层实现为指针类型结构](https://www.imooc.com/read/87/article/2383)，我们可以直接利用其在反射世界中对应的Value在反射世界中修改其内部元素； - 对于结构体中的非导出字段(unexported field)，我们可以读取其值，但无法直接修改其值。在上面的示例中，我们通过下面的unsafe手段实现了对其的赋值：

```
nAge = reflect.NewAt(field2.Type(), unsafe.Pointer(field2.UnsafeAddr())).Elem()
nAge.SetInt(50)
```


我们通过reflect.NewAt创建了一个新Value实例，该实例表示指向field2地址的指针。然后通过Elem方法，我们得到该指针Value指向的对象的Value：nAge，实际就是field2变量。然后通过nAge设置的新值也将反映在field2的值上。这和上面基本类型那个示例中的vpi和vi的功用类似。

### 3. 获取系统资源描述符的值

reflect包的一大功用就是获取一些被封装在底层的系统资源描述符的值，比如：socket描述符、文件描述符。

#### a) 文件描述符

os.File提供了Fd方法用于获取文件对应的os底层的文件描述符的值。我们也可以使用反射来实现同样的功能：

```
// github.com/bigwhite/experiments/blob/master/vars-in-reflect/system-resource/file_fd.go
package main
import (
"fmt"
"os"
"reflect"
)
func fileFD(f *os.File) int {
file := reflect.ValueOf(f).Elem().FieldByName("file").Elem()
pfdVal := file.FieldByName("pfd")
return int(pfdVal.FieldByName("Sysfd").Int())
}
func main() {
fileName := os.Args[1]
f, err := os.Open(fileName)
if err != nil {
panic(err)
}
defer f.Close()
fmt.Printf("file descriptor is %d\n", f.Fd())
fmt.Printf("file descriptor in reflect is %d\n", fileFD(f))
}
```


执行上述示例：

```
$go build file_fd.go
$./file_fd file_fd.go
file descriptor is 3
file descriptor in reflect is 3
```


我们看到通过reflect获取到的fd值与通过Fd方法得到的值是一致的。

下面我们可以基于上面对读写基本类型和复合类型变量的理解来简单分析一下fileFD函数的实现：

os.File的定义如下：

```
// $GOROOT/src/os/types.go
type File struct {
*file // os specific
}
```


为了通过反射获取到未导出指针变量file，我们使用下面反射语句：

```
file := reflect.ValueOf(f).Elem().FieldByName("file").Elem()
```


有了上面的Value实例file，我们就可以继续反射os.file结构了。os.file结构是因os而异的，以linux/mac的unix为例，os.file的结构如下：

```
// $GOROOT/src/os/file_unix.go
type file struct {
pfd poll.FD
name string
dirinfo *dirInfo // nil unless directory being read
nonblock bool // whether we set nonblocking mode
stdoutOrErr bool // whether this is stdout or stderr
appendMode bool // whether file is opened for appending
}
```


于是我们继续反射：

```
pfdVal := file.FieldByName("pfd")
```


而poll.FD的结构如下：

```
// $GOROOT/src/internal/poll/fd_unix.go
// field of a larger type representing a network connection or OS file.
type FD struct {
// Lock sysfd and serialize access to Read and Write methods.
fdmu fdMutex
// System file descriptor. Immutable until Close.
Sysfd int
// I/O poller.
pd pollDesc
// Writev cache.
iovecs *[]syscall.Iovec
// Semaphore signaled when file is closed.
csema uint32
// Non-zero if this file has been set to blocking mode.
isBlocking uint32
// Whether this is a streaming descriptor, as opposed to a
// packet-based descriptor like a UDP socket. Immutable.
IsStream bool
// Whether a zero byte read indicates EOF. This is false for a
// message based socket connection.
ZeroReadIsEOF bool
// Whether this is a file rather than a network socket.
isFile bool
}
```


这其中的Sysfd记录的就是系统的文件描述符的值，于是通过下面语句即可得到该文件描述符的值：

```
return int(pfdVal.FieldByName("Sysfd").Int())
```


#### b) socket描述符

unix下一切皆文件！socket描述符也是一个文件描述符，并且Go并没有在标准库中直接提供获取socket文件描述符的API。我们只能通过反射获取。看下面示例：

```
// github.com/bigwhite/experiments/blob/master/vars-in-reflect/system-resource/socket_fd.go
package main
import (
"fmt"
"log"
"net"
"reflect"
)
func socketFD(conn net.Conn) int {
tcpConn := reflect.ValueOf(conn).Elem().FieldByName("conn")
fdVal := tcpConn.FieldByName("fd")
pfdVal := fdVal.Elem().FieldByName("pfd")
return int(pfdVal.FieldByName("Sysfd").Int())
}
func main() {
ln, err := net.Listen("tcp", ":8080")
if err != nil {
panic(err)
}
for {
conn, err := ln.Accept()
if err != nil {
if ne, ok := err.(net.Error); ok && ne.Temporary() {
log.Printf("accept temp err: %v", ne)
continue
}
log.Printf("accept err: %v", err)
return
}
fmt.Printf("conn fd is [%d]\n", socketFD(conn))
}
}
```


我们看到socketFD的实现与fileFD的实现有些类似，我们从net.Conn一步步反射得到底层的Sysfd。

传给socketFD的实参实质是一个TCPConn实例，通过reflect.ValueOf(conn).Elem()我们可以获取到该实例在反射世界的Value

```
// $GOROOT/src/net/tcpsock.go
type TCPConn struct {
conn
}
```


然后再通过FieldByName(“conn”)得到TCPConn结构中字段conn在反射世界中的Value。net.conn结构如下：

```
// $GOROOT/src/net/net.go
type conn struct {
fd *netFD
}
```


起哄的netFD是一个os相关的结构，以linux/mac为例，其结构如下：

```
// $GOROOT/src/net/fd_posix.go
// Network file descriptor.
type netFD struct {
pfd poll.FD
// immutable until Close
family int
sotype int
isConnected bool // handshake completed or use of association with peer
net string
laddr Addr
raddr Addr
}
```


我们又看到了poll.FD类型字段pfd，再往下的反射就和fileFD一致了。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/vars-in-reflect)下载：https://github.com/bigwhite/experiments/blob/master/vars-in-reflect

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

Related posts:

## 评论