---
title: 一文告诉你神奇的Go内建函数源码在哪里
url: https://tonybai.com/2020/12/17/where-is-the-source-of-builtin-functions/
published: '2020-12-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文告诉你神奇的Go内建函数源码在哪里

![img{512x368}](../../assets/bb8e871b41f7a883.png)


Go内建函数源码，我好像在哪里见过你。 – 佚名


### 1. 何为Go内建函数

众所周知，Go是最简单的主流编程语言之一，截至[Go 1.15版本](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)，Go语言的[关键字](https://tip.golang.org/ref/spec#Keywords)的规模依旧保持在25个：

![img{512x368}](../../assets/4ed9d0b0f5dc1603.png)


很多刚入门的gopher可能会问：像bool、byte、error、true、[iota](https://www.imooc.com/read/87/article/2380)甚至int都难道都不是关键字？没错！和其他语言不同，这些**标识符**并不是关键字，在Go中它们被称为[ 预定义标识符](https://tip.golang.org/ref/spec#Predeclared_identifiers)。这些标识符拥有

**universe block作用域**(关于go代码块作用域的详细解析，可参考我的技术专栏：“

[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”)，可以在任何源码位置使用。

![img{512x368}](../../assets/98e2e73474e63afe.png)


从上图我们看到：所谓的**Go内建函数**也包含在这个预定义标识符集合中，只是这些标识符被用作**函数名称标识符**罢了。

### 2. 预定义标识符可被override

Go语言的关键字是保留的，我们无法将其用于规范之外的其他场合，比如作为变量的标识符。但是预定义标识符不是关键字，我们可以override它们。下面就是一个对默认表示整型类型的预定义标识符**int**进行override的例子：

```
package main
import (
"fmt"
"unsafe"
)
type int int8
func main() {
var a int = 5
fmt.Printf("%T\n", a) // main.int，而不是int
fmt.Println(unsafe.Sizeof(a)) // 1，而不是8
}
```


在上述这个源文件中，预定义标识符int被override为一个自定义类型int，该类型的underlying type为int8，于是当我们输出该类型变量(代码中的变量a)的类型和长度时，我们得到的是main.int和1，而不是int和8。

### 3. 预定义标识符的声明源码在哪里

Go是开源的编程语言，这些预定义标识符想必也都有自己的“归宿”吧，的确是这样的。Go的每个发行版都带有一份源码，而预定义标识符就在这份源码中。

以[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)为例，我们可以在下面路径中找到预定义标识符的源码：

```
$GOROOT/src/builtin/builtin.go
```


以string、int、uint这几个代表原生类型的预定义标识符为例，它们的声明代码如下：

```
// $GOROOT/src/builtin/builtin.go
// string is the set of all strings of 8-bit bytes, conventionally but not
// necessarily representing UTF-8-encoded text. A string may be empty, but
// not nil. Values of string type are immutable.
type string string
// int is a signed integer type that is at least 32 bits in size. It is a
// distinct type, however, and not an alias for, say, int32.
type int int
// uint is an unsigned integer type that is at least 32 bits in size. It is a
// distinct type, however, and not an alias for, say, uint32.
type uint uint
```


同时，我们利用`go doc builtin.int`

也可以查看预定义标识符int的文档：

```
$go doc builtin.int
package builtin // import "builtin"
type int int
int is a signed integer type that is at least 32 bits in size. It is a
distinct type, however, and not an alias for, say, int32.
func cap(v Type) int
func copy(dst, src []Type) int
func len(v Type) int
```


### 4. 内建函数的源码在哪里？

作为预声明标识符子集的内建函数们在builtin.go中也都有自己的位置，比如：以append这个内建函数为例，我们可以在Go安装包的builtin.go中找到它的原型(Go 1.14)：

```
// The append built-in function appends elements to the end of a slice. If
// it has sufficient capacity, the destination is resliced to accommodate the
// new elements. If it does not, a new underlying array will be allocated.
// Append returns the updated slice. It is therefore necessary to store the
// result of append, often in the variable holding the slice itself:
// slice = append(slice, elem1, elem2)
// slice = append(slice, anotherSlice...)
// As a special case, it is legal to append a string to a byte slice, like this:
// slice = append([]byte("hello "), "world"...)
func append(slice []Type, elems ...Type) []Type
```


但我们惊奇的发现：**这里没有append函数的实现**。那么append内建函数实现的源码究竟在哪里呢？本质上讲append函数，包括其他内建函数其实并没有自己的实现源码。

内建函数仅仅是一个标识符，在Go源码编译期间，Go编译器遇到内建函数标识符时会将其替换为若干runtime的调用，我们还以append函数为例，我们输出下面代码的汇编代码(Go 1.14)：

```
// append.go
package main
import "fmt"
func main() {
var s = []int{5, 6}
s = append(s, 7,
```

fmt.Println(s)
}
$go tool compile -S append.go > append.s


汇编节选如下(append.s)：

```
"".main STEXT size=277 args=0x0 locals=0x58
0x0000 00000 (xxx.go:5) TEXT "".main(SB), ABIInternal, $88-0
0x0000 00000 (xxx.go:5) MOVQ (TLS), CX
0x0009 00009 (xxx.go:5) CMPQ SP, 16(CX)
0x000d 00013 (xxx.go:5) PCDATA $0, $-2
0x000d 00013 (xxx.go:5) JLS 267
0x0013 00019 (xxx.go:5) PCDATA $0, $-1
0x0013 00019 (xxx.go:5) SUBQ $88, SP
0x0017 00023 (xxx.go:5) MOVQ BP, 80(SP)
0x001c 00028 (xxx.go:5) LEAQ 80(SP), BP
0x0021 00033 (xxx.go:5) PCDATA $0, $-2
0x0021 00033 (xxx.go:5) PCDATA $1, $-2
0x0021 00033 (xxx.go:5) FUNCDATA $0, gclocals·69c1753bd5f81501d95132d08af04464(SB)
0x0021 00033 (xxx.go:5) FUNCDATA $1, gclocals·568470801006e5c0dc3947ea998fe279(SB)
0x0021 00033 (xxx.go:5) FUNCDATA $2, gclocals·bfec7e55b3f043d1941c093912808913(SB)
0x0021 00033 (xxx.go:5) FUNCDATA $3, "".main.stkobj(SB)
0x0021 00033 (xxx.go:6) PCDATA $0, $1
0x0021 00033 (xxx.go:6) PCDATA $1, $0
0x0021 00033 (xxx.go:6) LEAQ type.[2]int(SB), AX
0x0028 00040 (xxx.go:6) PCDATA $0, $0
0x0028 00040 (xxx.go:6) MOVQ AX, (SP)
0x002c 00044 (xxx.go:6) CALL runtime.newobject(SB)
0x0031 00049 (xxx.go:6) PCDATA $0, $1
0x0031 00049 (xxx.go:6) MOVQ 8(SP), AX
0x0036 00054 (xxx.go:6) MOVQ $5, (AX)
0x003d 00061 (xxx.go:6) MOVQ $6, 8(AX)
0x0045 00069 (xxx.go:7) PCDATA $0, $2
0x0045 00069 (xxx.go:7) LEAQ type.int(SB), CX
0x004c 00076 (xxx.go:7) PCDATA $0, $1
0x004c 00076 (xxx.go:7) MOVQ CX, (SP)
0x0050 00080 (xxx.go:7) PCDATA $0, $0
0x0050 00080 (xxx.go:7) MOVQ AX, 8(SP)
0x0055 00085 (xxx.go:7) MOVQ $2, 16(SP)
0x005e 00094 (xxx.go:7) MOVQ $2, 24(SP)
0x0067 00103 (xxx.go:7) MOVQ $4, 32(SP)
0x0070 00112 (xxx.go:7) CALL runtime.growslice(SB)
0x0075 00117 (xxx.go:7) PCDATA $0, $1
0x0075 00117 (xxx.go:7) MOVQ 40(SP), AX
0x007a 00122 (xxx.go:7) MOVQ 48(SP), CX
0x007f 00127 (xxx.go:7) MOVQ 56(SP), DX
0x0084 00132 (xxx.go:7) MOVQ $7, 16(AX)
0x008c 00140 (xxx.go:7) MOVQ $8, 24(AX)
0x0094 00148 (xxx.go:8) PCDATA $0, $0
0x0094 00148 (xxx.go:8) MOVQ AX, (SP)
0x0098 00152 (xxx.go:7) LEAQ 2(CX), AX
0x009c 00156 (xxx.go:8) MOVQ AX, 8(SP)
0x00a1 00161 (xxx.go:8) MOVQ DX, 16(SP)
0x00a6 00166 (xxx.go:8) CALL runtime.convTslice(SB)
... ...
```


我们可以看到：append并没有以独立的身份出现在CALL汇编指令的后面，而是被换成：runtime.growslice、runtime.convTslice以及相关汇编指令了。

**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


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

感谢感谢, 终于找到了源码

不客气。