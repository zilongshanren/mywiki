---
title: Go 1.15中值得关注的几个变化
url: https://tonybai.com/2020/10/11/some-changes-in-go-1-15/
published: '2020-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.15中值得关注的几个变化

![img{512x368}](../../assets/bcc7f089d01df22a.png)


[Go 1.15版本](https://tip.golang.org/doc/go1.15)在8月12日就正式发布了，给我的感觉就是发布的挺痛快^_^。这种感觉来自与之前版本发布时间的对比：[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)发布于当年的9月4日，更早的[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)发布于当年的8月25日。

不过这个时间恰与我家[二宝出生](https://tonybai.com/2020/07/29/my-second-daughter-was-born/)和老婆月子时期有重叠，每天照顾孩子团团转的我实在抽不出时间研究Go 1.15的变化:(。如今，我逐渐从照顾二宝的工作中脱离出来^_^，于是“Go x.xx版本值得关注的几个变化”系列将继续下去。关注Go语言的演变对掌握和精通Go语言大有裨益，凡是致力于成为一名高级Gopher的读者都应该密切关注Go的演进。

截至写稿时，Go 1.15最新版是Go 1.15.2。Go 1.15一如既往的遵循[Go1兼容性承诺](https://tip.golang.org/doc/go1compat.html)。[语言规范](https://tip.golang.org/ref/spec)方面没有任何变化。可以说这是一个“面子”上变化较小的一个版本，但“里子”的变化还是不少的，在本文中我就和各位读者一起就重要变化逐一了解一下。

### 一. 平台移植性

Go 1.15版本不再对darwin/386和darwin/arm两个32位平台提供支持了。Go 1.15及以后版本仅对darwin/amd64和darwin/arm64版本提供支持。并且不再对macOS 10.12版本之前的版本提供支持。

[Go 1.14版本](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)中，Go编译器在被传入-race和-msan的情况下，默认会执行**-d=checkptr**，即对unsafe.Pointer的使用进行[合法性检查](https://github.com/golang/go/issues/34964)。**-d=checkptr**主要检查两项内容：

-
当将unsafe.Pointer转型为*T时，T的内存对齐系数不能高于原地址的；

-
做完指针算术后，转换后的unsafe.Pointer仍应指向原先Go堆对象


但在Go 1.14中，这个检查并不适用于Windows操作系统。Go 1.15中增加了对windows系统的支持。

对于[RISC-V](https://riscv.org)架构，Go社区展现出十分积极的姿态，早在[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)，Go就为RISC-V cpu架构预留了GOARCH值：riscv和riscv64。[Go 1.14版本](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)则为64bit RISC-V提供了在linux上的实验性支持(GOOS=linux, GOARCH=riscv64)。在Go 1.15版本中，Go在GOOS=linux, GOARCH=riscv64的环境下的稳定性和性能得到持续提升，并且已经可以支持goroutine异步抢占式调度了。

### 二. 工具链

#### 1. GOPROXY新增以管道符为分隔符的代理列表值

在[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)中，[GOPROXY](https://tonybai.com/2018/11/26/hello-go-module-proxy/)支持设置为多个proxy的列表，多个proxy之间采用逗号分隔。Go工具链会按顺序尝试列表中的proxy以获取依赖包数据，但是当有proxy server服务不可达或者是返回的http状态码不是404也不是410时，go会终止数据获取。但是当列表中的proxy server返回其他错误时，Go命令不会向GOPROXY列表中的下一个值所代表的的proxy server发起请求，这种行为模式没能让所有gopher满意，**很多Gopher认为Go工具链应该向后面的proxy server请求，直到所有proxy server都返回失败**。Go 1.15版本满足了Go社区的需求，新增以管道符“|”为分隔符的代理列表值。如果GOPROXY配置的proxy server列表值以管道符分隔，则无论某个proxy server返回什么错误码，Go命令都会向列表中的下一个proxy server发起新的尝试请求。

注：Go 1.15版本中GOPROXY环境变量的默认值依旧为

https://proxy.golang.org,direct。

#### 2. module cache的存储路径可设置

[Go module机制](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)自打在[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)中以试验特性的方式引入时就将module的本地缓存默认放在了**\$GOPATH/pkg/mod**下（如果没有显式设置GOPATH，那么默认值将是**~/go**；如果GOPATH下面配置了多个路径，那么选择第一个路径），一直到Go 1.14版本，这个位置都是无法配置的。

Go module的引入为去除GOPATH提供了前提，于是module cache的位置也要尽量与GOPATH“脱钩”：Go 1.15提供了GOMODCACHE环境变量用于自定义module cache的存放位置。如果没有显式设置GOMODCACHE，那么module cache的默认存储路径依然是**\$GOPATH/pkg/mod**。

### 三. 运行时、编译器和链接器

#### 1. panic展现形式变化

在Go 1.15之前，如果传给panic的值是bool, complex64, complex128, float32, float64, int, int8, int16, int32, int64, string, uint, uint8, uint16, uint32, uint64, uintptr等原生类型的值，那么panic在触发时会输出具体的值，比如：

```
// go1.15-examples/runtime/panic.go
package main
func foo() {
var i uint32 = 17
panic(i)
}
func main() {
foo()
}
```


使用Go 1.14运行上述代码，得到如下结果：

```
$go run panic.go
panic: 17
goroutine 1 [running]:
main.foo(...)
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:5
main.main()
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:9 +0x39
exit status 2
```


Go 1.15版本亦是如此。但是对于派生于上述原生类型的自定义类型而言，Go 1.14只是输出变量地址：

```
// go1.15-examples/runtime/panic.go
package main
type myint uint32
func bar() {
var i myint = 27
panic(i)
}
func main() {
bar()
}
```


使用Go 1.14运行上述代码：

```
$go run panic.go
panic: (main.myint) (0x105fca0,0xc00008e000)
goroutine 1 [running]:
main.bar(...)
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:12
main.main()
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:17 +0x39
exit status 2
```


Go 1.15针对此情况作了展示优化，即便是派生于这些原生类型的自定义类型变量，panic也可以输出其值。使用Go 1.15运行上述代码的结果如下：

```
$go run panic.go
panic: main.myint(27)
goroutine 1 [running]:
main.bar(...)
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:12
main.main()
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.15-examples/runtime/panic.go:17 +0x39
exit status 2
```


#### 2. 将小整数([0,255])转换为interface类型值时将不会额外分配内存

Go 1.15在runtime/iface.go中做了一些优化改动：增加一个名为staticuint64s的数组，预先为[0,255]这256个数分配了内存。然后在convT16、convT32等运行时转换函数中判断要转换的整型值是否小于256(len(staticuint64s))，如果小于，则返回staticuint64s数组中对应的值的地址；否则调用mallocgc分配新内存。

```
$GOROOT/src/runtime/iface.go
// staticuint64s is used to avoid allocating in convTx for small integer values.
var staticuint64s = [...]uint64{
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
... ...
0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7,
0xf8, 0xf9, 0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff,
}
func convT16(val uint16) (x unsafe.Pointer) {
if val < uint16(len(staticuint64s)) {
x = unsafe.Pointer(&staticuint64s[val])
if sys.BigEndian {
x = add(x, 6)
}
} else {
x = mallocgc(2, uint16Type, false)
*(*uint16)(x) = val
}
return
}
func convT32(val uint32) (x unsafe.Pointer) {
if val < uint32(len(staticuint64s)) {
x = unsafe.Pointer(&staticuint64s[val])
if sys.BigEndian {
x = add(x, 4)
}
} else {
x = mallocgc(4, uint32Type, false)
*(*uint32)(x) = val
}
return
}
```


我们可以用下面例子来验证一下：

```
// go1.15-examples/runtime/tinyint2interface.go
package main
import (
"math/rand"
)
func convertSmallInteger() interface{} {
i := rand.Intn(256)
var j interface{} = i
return j
}
func main() {
for i := 0; i < 100000000; i++ {
convertSmallInteger()
}
}
```


我们分别用go 1.14和go 1.15.2编译这个源文件（注意关闭内联等优化，否则很可能看不出效果）：

```
// go 1.14
go build -gcflags="-N -l" -o tinyint2interface-go14 tinyint2interface.go
// go 1.15.2
go build -gcflags="-N -l" -o tinyint2interface-go15 tinyint2interface.go
```


我们使用下面命令输出程序执行时每次GC的信息：

```
$env GODEBUG=gctrace=1 ./tinyint2interface-go14
gc 1 @0.025s 0%: 0.009+0.18+0.021 ms clock, 0.079+0.079/0/0.20+0.17 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 2 @0.047s 0%: 0.003+0.14+0.013 ms clock, 0.031+0.099/0.064/0.037+0.10 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 3 @0.064s 0%: 0.008+0.20+0.016 ms clock, 0.071+0.071/0.018/0.081+0.13 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 4 @0.081s 0%: 0.005+0.14+0.013 ms clock, 0.047+0.059/0.023/0.032+0.10 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 5 @0.098s 0%: 0.005+0.10+0.017 ms clock, 0.042+0.073/0.027/0.080+0.13 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
... ...
gc 192 @3.264s 0%: 0.003+0.11+0.013 ms clock, 0.024+0.060/0.005/0.035+0.11 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 193 @3.281s 0%: 0.005+0.13+0.032 ms clock, 0.042+0.075/0.041/0.050+0.25 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 194 @3.298s 0%: 0.004+0.12+0.013 ms clock, 0.033+0.072/0.030/0.033+0.10 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 195 @3.315s 0%: 0.003+0.17+0.023 ms clock, 0.029+0.062/0.055/0.024+0.18 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
$env GODEBUG=gctrace=1 ./tinyint2interface-go15
```


我们看到和go 1.14编译的程序不断分配内存，不断导致GC相比，go1.15.2没有输出GC信息，间接证实了小整数转interface变量值时不会触发内存分配。

#### 3. 加入更现代化的链接器(linker)

一个新版的[现代化linker](https://golang.org/s/better-linker)正在逐渐加入到Go中，Go 1.15是新版linker的起点。后续若干版本，linker优化会逐步加入进来。在Go 1.15中，对于大型项目，新链接器的性能要提高20%，内存占用减少30%。

#### 4. objdump支持输出GNU汇编语法

go 1.15为objdump工具增加了-gnu选项，**以在Go汇编的后面，辅助输出GNU汇编，便于对照**：

```
// go 1.14：
$go tool objdump -S tinyint2interface-go15|more
TEXT go.buildid(SB)
0x1001000 ff20 JMP 0(AX)
0x1001002 476f OUTSD DS:0(SI), DX
0x1001004 206275 ANDB AH, 0x75(DX)
0x1001007 696c642049443a20 IMULL $0x203a4449, 0x20(SP), BP
... ...
//go 1.15.2：
$go tool objdump -S -gnu tinyint2interface-go15|more
TEXT go.buildid(SB)
0x1001000 ff20 JMP 0(AX) // jmpq *(%rax)
0x1001002 476f OUTSD DS:0(SI), DX // rex.RXB outsl %ds:(%rsi),(%dx)
0x1001004 206275 ANDB AH, 0x75(DX) // and %ah,0x75(%rdx)
0x1001007 696c642049443a20 IMULL $0x203a4449, 0x20(SP), BP // imul $0x203a4449,0x20(%rsp,%riz,2),%ebp
... ...
```


### 四. 标准库

和以往发布的版本一样，标准库有大量小改动，这里挑出几个笔者感兴趣的和大家一起看一下。

#### 1. 增加tzdata包

Go time包中很多方法依赖时区数据，但不是所有平台上都自带时区数据。Go time包会以下面顺序搜寻时区数据：

```
- ZONEINFO环境变量指示的路径中
- 在类Unix系统中一些常见的存放时区数据的路径（zoneinfo_unix.go中的zoneSources数组变量中存放这些常见路径）：
"/usr/share/zoneinfo/",
"/usr/share/lib/zoneinfo/",
"/usr/lib/locale/TZ/"
- 如果平台没有，则尝试使用$GOROOT/lib/time/zoneinfo.zip这个随着go发布包一起发布的时区数据。但在应用部署的环境中，很大可能不会进行go安装。
```


如果go应用找不到时区数据，那么go应用运行将会受到影响，就如下面这个例子：

```
// go1.15-examples/stdlib/tzdata.go
package main
import (
"fmt"
"time"
)
func main() {
loc, err := time.LoadLocation("America/New_York")
if err != nil {
fmt.Println("LoadLocation error:", err)
return
}
fmt.Println("LoadLocation is:", loc)
}
```


我们移除系统的时区数据(比如将/usr/share/zoneinfo改名)和Go安装包自带的zoneinfo.zip(改个名)后，在Go 1.15.2下运行该示例：

```
$ go run tzdata.go
LoadLocation error: unknown time zone America/New_York
```


为此，Go 1.15提供了一个将时区数据嵌入到Go应用二进制文件中的方法：**导入time/tzdata包**：

```
// go1.15-examples/stdlib/tzdata.go
package main
import (
"fmt"
"time"
_ "time/tzdata"
)
func main() {
loc, err := time.LoadLocation("America/New_York")
if err != nil {
fmt.Println("LoadLocation error:", err)
return
}
fmt.Println("LoadLocation is:", loc)
}
```


我们再用go 1.15.2运行一下上述导入tzdata包的例子：

```
$go run testtimezone.go
LoadLocation is: America/New_York
```


不过由于附带tzdata数据，应用二进制文件的size会增大大约800k，下面是在ubuntu下的实测值：

```
-rwxr-xr-x 1 root root 2.0M Oct 11 02:42 tzdata-withouttzdata*
-rwxr-xr-x 1 root root 2.8M Oct 11 02:42 tzdata-withtzdata*
```


#### 2. 增加json解码限制

json包是日常使用最多的go标准库包之一，在Go 1.15中，go按照json规范的要求，为json的解码增加了一层限制：

```
// json规范要求
//https://tools.ietf.org/html/rfc7159#section-9
A JSON parser transforms a JSON text into another representation. A
JSON parser MUST accept all texts that conform to the JSON grammar.
A JSON parser MAY accept non-JSON forms or extensions.
An implementation may set limits on the size of texts that it
accepts. An implementation may set limits on the maximum depth of
nesting. An implementation may set limits on the range and precision
of numbers. An implementation may set limits on the length and
character contents of strings.
```


这个限制就是增加了一个对json文本最大缩进深度值：

```
// $GOROOT/src/encoding/json/scanner.go
// This limits the max nesting depth to prevent stack overflow.
// This is permitted by https://tools.ietf.org/html/rfc7159#section-9
const maxNestingDepth = 10000
```


如果一旦传入的json文本数据缩进深度超过maxNestingDepth，那json包就会panic。当然，绝大多数情况下，我们是碰不到缩进10000层的超大json文本的。因此，该limit对于99.9999%的gopher都没啥影响。

#### 3. reflect包

Go 1.15版本之前reflect包[存在一处行为不一致的问题](https://github.com/golang/go/issues/38521)，我们看下面例子(例子来源于https://play.golang.org/p/Jnga2_6Rmdf)：

```
// go1.15-examples/stdlib/reflect.go
package main
import "reflect"
type u struct{}
func (u) M() { println("M") }
type t struct {
u
u2 u
}
func call(v reflect.Value) {
defer func() {
if err := recover(); err != nil {
println(err.(string))
}
}()
v.Method(0).Call(nil)
}
func main() {
v := reflect.ValueOf(t{}) // v := t{}
call(v) // v.M()
call(v.Field(0)) // v.u.M()
call(v.Field(1)) // v.u2.M()
}
```


我们使用Go 1.14版本运行该示例：

```
$go run reflect.go
M
M
reflect: reflect.flag.mustBeExported using value obtained using unexported field
```


我们看到同为类型t中的非导出字段(field)的u和u2(u是以嵌入类型方式称为类型t的字段的)，通过reflect包可以调用字段u的导出方法(如输出中的第二行的M)，却无法调用非导出字段u2的导出方法（如输出中的第三行的panic信息）。

这种不一致在Go 1.15版本中被修复，我们使用Go 1.15.2运行上述示例：

```
$go run reflect.go
M
reflect: reflect.Value.Call using value obtained using unexported field
reflect: reflect.Value.Call using value obtained using unexported field
```


我们看到reflect无法调用非导出字段u和u2的导出方法了。但是reflect依然可以通过提升到类型t的方法来间接使用u的导出方法，正如运行结果中的第一行输出。

**这一改动可能会影响到遗留代码中使用reflect调用以类型嵌入形式存在的非导出字段方法的代码**，如果你的代码中存在这样的问题，可以直接通过提升(promote)到包裹类型(如例子中的t)中的方法（如例子中的call(v)）来替代之前的方式。

### 五. 小结

由于Go 1.15删除了一些GC元数据和一些无用的类型元数据，Go 1.15编译出的二进制文件size会减少5%左右。我用一个中等规模的go项目实测了一下：

```
-rwxr-xr-x 1 tonybai staff 23M 10 10 16:54 yunxind*
-rwxr-xr-x 1 tonybai staff 24M 9 30 11:20 yunxind-go14*
```


二进制文件size的确有变小，大约4%-5%。

**如果你还没有升级到Go 1.15，那么现在正是时候**。

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.15-examples)下载。https://github.com/bigwhite/experiments/tree/master/go1.15-examples

我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论