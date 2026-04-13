---
title: Go究竟是否为空切片分配了底层数组
url: https://tonybai.com/2022/02/15/whether-go-allocate-underlying-array-for-empty-slice/
published: '2022-02-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go究竟是否为空切片分配了底层数组

![](../../assets/416ad46f1e76d25f.png)


[本文永久链接](https://tonybai.com/2022/02/15/whether-go-allocate-underlying-array-for-empty-slice) – https://tonybai.com/2022/02/15/whether-go-allocate-underlying-array-for-empty-slice

这周在[“Go语言第一课”](http://gk.link/a/10AVZ)的留言区看到一位同学的这样一个问题：

![](../../assets/28160a935a09fae3.png)


切片是Go语言中的一个重要的语法元素，也是日常Go开发中使用最为频繁的语法元素。有过Go语言开发经验的童鞋估计大多都知道空切片(empty slice)与nil切片(nil slice)比较的梗，这也是Go面试中的一道高频题。

```
var sl1 = []int{} // sl1是空切片
var sl2 []int // sl2是nil切片
```


要真正理解切片，离不开运行时的切片表示。在我的[专栏](http://gk.link/a/10AVZ)和[《Go语言精进之路》](https://book.douban.com/subject/35720728/)一书中都有对切片在运行时表示的细致讲解。

切片在运行时由三个字段构成，[reflect包](https://mp.weixin.qq.com/s/KgUZGVF08yEO2oARryOLcg)中有切片在类型系统中表示的对应的定义：

```
// $GOROOT/src/reflect/value.go
type SliceHeader struct {
Data uintptr
Len int
Cap int
}
```


基于这个定义我们来理解空切片和nil切片就容易多了。我们用一段代码来看看这两种切片的差别：

```
// dumpslice.go
package main
import (
"fmt"
"reflect"
"unsafe"
)
func main() {
var sl1 = []int{}
ph1 := (*reflect.SliceHeader)(unsafe.Pointer(&sl1))
fmt.Printf("empty slice's header is %#v\n", *ph1)
var sl2 []int
ph2 := (*reflect.SliceHeader)(unsafe.Pointer(&sl2))
fmt.Printf("nil slice's header is %#v\n", *ph2)
}
```


在这段代码中，我们通过unsafe包以及reflect.SliceHeader输出了空切片与nil切片在内存中的表示，即SliceHeader各个字段的值。我们在[Go 1.18beta2](https://mp.weixin.qq.com/s/Zthy6IAxGC10Q7q2N3gqMQ)下运行一下上述代码(使用-gcflags ‘-l -N’可关闭Go编译器的优化)：

```
$go run -gcflags '-l -N' dumpslice.go
empty slice's header is reflect.SliceHeader{Data:0xc000092eb0, Len:0, Cap:0}
nil slice's header is reflect.SliceHeader{Data:0x0, Len:0, Cap:0}
```


通过输出结果，我们看到nil切片在运行时表示的三个字段值都是0；而空切片的len、cap值为0，但**data值不为零**。

好了，此时我们再回到本文开始处那个童鞋提出的那个问题：**空切片到底分没分配底层数组**？

答案是肯定的：**没有分配**！那么上述代码中空切片在运行时表示中第一个字段data的值0xc000092eb0从何而来，难道不是底层数组的地址么？

要想回答这个问题，我们需要下沉到汇编层面去看。

Go使用plan9的汇编语法，目前市面上关于这种汇编的资料比较少，比较权威是

[Go官方的asm资料]和Rob Pike编写的[A Manual for the Plan 9 assembler]。此外IBM工程师的[Dropping down Go functions in assembly language]这份资料也十分不错。国内[《Go语言高级编程》]一书以及曹春辉的[plan9 assembly 完全解析]讲解的十分全面，值得大家参考。

我们以下面这段最简单的有关空切片的代码为例：

```
// layout6.go
1 package main
2
3 func main() {
4 var sl = []int{}
5 _ = sl
6 }
```


生成go源码对应汇编代码的主要方法有：go tool compile -S xxx.go和针对编译后的二进制文件使用go tool objdump -S exe_file。


我们看看这段代码对应的汇编代码，我们使用下面命令将上述go源码转换为汇编代码(Go 1.18beta2 on darwin amd64)：

```
$go tool compile -S -N -l layout6.go > layout6.s // -N -l两个命令行选项用于关闭Go编译器的优化，优化后的代码会掩盖实现细节
```


(在MacOS上)生成的layout6.s汇编代码如下（汇编代码中的FUNCDATA和PCDATA是Go编译器插入的、给GC使用的指示符，这里将其滤掉了）：

```
"".main STEXT nosplit size=48 args=0x0 locals=0x30 funcid=0x0 align=0x0
0x0000 00000 (layout6.go:3) TEXT "".main(SB), NOSPLIT|ABIInternal, $48-0 // 48是main函数的栈帧大小，0表示参数大小
0x0000 00000 (layout6.go:3) SUBQ $48, SP
0x0004 00004 (layout6.go:3) MOVQ BP, 40(SP)
0x0009 00009 (layout6.go:3) LEAQ 40(SP), BP
0x000e 00014 (layout6.go:4) LEAQ ""..autotmp_2(SP), AX
0x0012 00018 (layout6.go:4) MOVQ AX, ""..autotmp_1+8(SP)
0x0017 00023 (layout6.go:4) TESTB AL, (AX)
0x0019 00025 (layout6.go:4) JMP 27
0x001b 00027 (layout6.go:4) MOVQ AX, "".sl+16(SP)
0x0020 00032 (layout6.go:4) MOVUPS X15, "".sl+24(SP)
0x0026 00038 (layout6.go:6) MOVQ 40(SP), BP
0x002b 00043 (layout6.go:6) ADDQ $48, SP
0x002f 00047 (layout6.go:6) RET
0x0000 48 83 ec 30 48 89 6c 24 28 48 8d 6c 24 28 48 8d H..0H.l$(H.l$(H.
0x0010 04 24 48 89 44 24 08 84 00 eb 00 48 89 44 24 10 .$H.D$.....H.D$.
0x0020 44 0f 11 7c 24 18 48 8b 6c 24 28 48 83 c4 30 c3 D..|$.H.l$(H..0.
go.cuinfo.packagename. SDWARFCUINFO dupok size=0
0x0000 6d 61 69 6e main
""..inittask SNOPTRDATA size=24
0x0000 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
0x0010 00 00 00 00 00 00 00 00 ........
gclocals·33cdeccccebe80329f1fdbee7f5874cb SRODATA dupok size=8
0x0000 01 00 00 00 00 00 00 00 ........
gclocals·ff19ed39bdde8a01a800918ac3ef0ec7 SRODATA dupok size=9
0x0000 01 00 00 00 04 00 00 00 00 .........
```


关于汇编语法的问题，大家可以参考前面提供的参考资料，这里不赘述。我们这里最关注的是对应Go源码第4行Go代码的汇编源码，这里我把这段汇编源码单独提出来放在下面：

```
0x000e 00014 (layout6.go:4) LEAQ ""..autotmp_2(SP), AX
0x0012 00018 (layout6.go:4) MOVQ AX, ""..autotmp_1+8(SP)
0x0017 00023 (layout6.go:4) TESTB AL, (AX)
0x0019 00025 (layout6.go:4) JMP 27
0x001b 00027 (layout6.go:4) MOVQ AX, "".sl+16(SP)
0x0020 00032 (layout6.go:4) MOVUPS X15, "".sl+24(SP)
```


我们逐行看一下：

- 00014行：将SP寄存器指向的内存单元(该内存单元被命名为autotmp_2)的地址存入AX寄存器中；
- 00019行：将AX寄存器中存储的值写入地址为SP+8的内存单元中，这个内存单元被命名为autotmp_1；
- 00023行：将AL寄存器中的值与AX寄存器指向的内存单元的值做逻辑与操作，设置相关标志位；
- 00025行：无条件跳转至00027行执行；
- 00027行：将AX寄存器中存储的值写入sl切片变量运行时表示的第一个字段data中，该字段的地址为SP+16；
- 00032行：使用intel平台上的SIMD指令集SSE的MOVUPS指令通过X15代表的固定的零寄存器对起始地址为SP+24的连续128bit(16个字节）进行清零。即sl切片变量运行时的len和cap字段被清零。

关于X15寄存器的含义，在

[Go internal ABI specification]中有说明。

我这里用一幅图展示一下上面操作后的main函数栈情况：

![](../../assets/ff80f22ec7565570.png)


我们看到切片sl的指向底层数组的指针data的值实际上是一个栈上的内存单元的地址，Go编译器并没有在堆上额外分配新的内存空间作为切片sl的底层数组。只是上面汇编代码的第00019行、00023行的操作让人很迷，不知道这两部指令操作的意图为何。

我们再来看一个例子，以进一步证实我们上面的结论。这个例子的源码如下：

```
// layout7.go
1 package main
2
3 func main() {
4 var sl = []int{}
5 sl = append(sl, 1)
6 }
```


在这个例子中，我们先是声明了一个空切片sl，之后又通过append为sl追加了一个元素。append时，由于sl为空切片，Go势必会为sl新分配底层存储数组，我们通过对比一下第4行和第5行两个操作的异同来确认“空切片并未分配底层数组”的结论。我们同样通过go tool compile -S命令得到该源码对应的汇编代码：

```
$go tool compile -S -N -l layout7.go > layout7.s
```


layout7.s中main函数的汇编代码如下(过滤掉了PCDATA和FUNCDATA指示符行)：

```
"".main STEXT size=114 args=0x0 locals=0x70 funcid=0x0 align=0x0
0x0000 00000 (layout7.go:3) TEXT "".main(SB), ABIInternal, $112-0
0x0000 00000 (layout7.go:3) CMPQ SP, 16(R14)
0x0004 00004 (layout7.go:3) JLS 107
0x0006 00006 (layout7.go:3) SUBQ $112, SP
0x000a 00010 (layout7.go:3) MOVQ BP, 104(SP)
0x000f 00015 (layout7.go:3) LEAQ 104(SP), BP
0x0014 00020 (layout7.go:4) LEAQ ""..autotmp_2+64(SP), BX
0x0019 00025 (layout7.go:4) MOVQ BX, ""..autotmp_1+72(SP)
0x001e 00030 (layout7.go:4) TESTB AL, (BX)
0x0020 00032 (layout7.go:4) JMP 34
0x0022 00034 (layout7.go:4) MOVQ BX, "".sl+80(SP)
0x0027 00039 (layout7.go:4) MOVUPS X15, "".sl+88(SP)
0x002d 00045 (layout7.go:5) JMP 47
0x002f 00047 (layout7.go:5) LEAQ type.int(SB), AX
0x0036 00054 (layout7.go:5) XORL CX, CX
0x0038 00056 (layout7.go:5) MOVQ CX, DI
0x003b 00059 (layout7.go:5) MOVL $1, SI
0x0040 00064 (layout7.go:5) CALL runtime.growslice(SB)
0x0045 00069 (layout7.go:5) LEAQ 1(BX), DX
0x0049 00073 (layout7.go:5) JMP 75
0x004b 00075 (layout7.go:5) MOVQ $1, (AX)
0x0052 00082 (layout7.go:5) MOVQ AX, "".sl+80(SP)
0x0057 00087 (layout7.go:5) MOVQ DX, "".sl+88(SP)
0x005c 00092 (layout7.go:5) MOVQ CX, "".sl+96(SP)
0x0061 00097 (layout7.go:6) MOVQ 104(SP), BP
0x0066 00102 (layout7.go:6) ADDQ $112, SP
0x006a 00106 (layout7.go:6) RET
0x006b 00107 (layout7.go:6) NOP
0x006b 00107 (layout7.go:3) CALL runtime.morestack_noctxt(SB)
0x0070 00112 (layout7.go:3) JMP 0
... ...
```


有了对layout6.s的汇编的分析的基础，再来看这段汇编似乎就好很多了。首先layout7.s中对应var sl = []int{}代码的第00020到00039的原理与layout6.s一致。sl的data字段被赋值为一个栈上内存单元(SP+64)的地址。

从第00047到00073实际上是为调用runtime.growslice函数做准备以及调用runtime.growslice函数。runtime.growslice函数负责在堆上分配新的底层数组用于存储切片sl的元素。runtime.growslice返回后，我们看到，第00075行，Go将一个立即数1写入AX寄存器指向的内存单元，即growslice新分配的底层数组的第一个元素的内存单元。

之后，sl的三个字段被重新做了赋值：

```
0x0052 00082 (layout7.go:5) MOVQ AX, "".sl+80(SP)
0x0057 00087 (layout7.go:5) MOVQ DX, "".sl+88(SP)
0x005c 00092 (layout7.go:5) MOVQ CX, "".sl+96(SP)
```


我们看到：00082行，sl的data字段(SP+80)被赋值为AX寄存器中的值，即堆上分配新的底层数组的地址。而后的len和cap字段也分配用DX和CX寄存器的值做了赋值，这两个寄存器分配存储了切片的len和cap。

我这里同样用一幅示意图展示append后main函数栈的情况：

![](../../assets/432d27d349674450.png)


通过这个例子，我们可以看到，如果Go在堆上为切片分配底层数组，我们会在汇编代码中看到growslice或newobject这样的调用。

如果一个非空切片没有逃逸到堆上，那么Go也可能在栈上为该切片分配底层数组空间，比如下面这段代码：

```
// layout10.go
package main
func main() {
var sl = []int{11, 12, 13}
_ = sl
}
```


它对应的汇编如下：

```
"".main STEXT nosplit size=103 args=0x0 locals=0x40 funcid=0x0 align=0x0
0x0000 00000 (layout10.go:3) TEXT "".main(SB), NOSPLIT|ABIInternal, $64-0
0x0000 00000 (layout10.go:3) SUBQ $64, SP
0x0004 00004 (layout10.go:3) MOVQ BP, 56(SP)
0x0009 00009 (layout10.go:3) LEAQ 56(SP), BP
0x000e 00014 (layout10.go:4) MOVUPS X15, ""..autotmp_2(SP)
0x0013 00019 (layout10.go:4) MOVUPS X15, ""..autotmp_2+8(SP)
0x0019 00025 (layout10.go:4) LEAQ ""..autotmp_2(SP), AX
0x001d 00029 (layout10.go:4) MOVQ AX, ""..autotmp_1+24(SP)
0x0022 00034 (layout10.go:4) TESTB AL, (AX)
0x0024 00036 (layout10.go:4) MOVQ $11, ""..autotmp_2(SP)
0x002c 00044 (layout10.go:4) TESTB AL, (AX)
0x002e 00046 (layout10.go:4) MOVQ $12, ""..autotmp_2+8(SP)
0x0037 00055 (layout10.go:4) TESTB AL, (AX)
0x0039 00057 (layout10.go:4) MOVQ $13, ""..autotmp_2+16(SP)
0x0042 00066 (layout10.go:4) TESTB AL, (AX)
0x0044 00068 (layout10.go:4) JMP 70
0x0046 00070 (layout10.go:4) MOVQ AX, "".sl+32(SP)
0x004b 00075 (layout10.go:4) MOVQ $3, "".sl+40(SP)
0x0054 00084 (layout10.go:4) MOVQ $3, "".sl+48(SP)
0x005d 00093 (layout10.go:6) MOVQ 56(SP), BP
0x0062 00098 (layout10.go:6) ADDQ $64, SP
0x0066 00102 (layout10.go:6) RET
```


这段汇编代码就留给大家自己阅读分析吧。

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

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论