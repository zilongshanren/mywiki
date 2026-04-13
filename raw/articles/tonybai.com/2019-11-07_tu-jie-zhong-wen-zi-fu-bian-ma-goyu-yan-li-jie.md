---
title: 图解中文字符编码-Go语言例解
url: https://tonybai.com/2019/11/07/non-ascii-character-encoding-illustrated/
published: '2019-11-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 图解中文字符编码-Go语言例解

今天几个同事在处理一个有关中文字符编码的问题，感觉他们对[字符编码](https://tonybai.com/2007/11/03/also-talk-about-char-encoding/)这件事依然理解不够透彻。这里用图文方式对中文字符编码做一个简要的解释，例子使用[Go语言](https://tonybai.com/tag/go)。

我们知道每个英文字母和数字在计算机中都会对应一个字节，或者说用一个字节来表示，这就是最初的[ASCII码](https://www.asciitable.com/)。但是随着计算机在全球范围内的广泛使用，非英语国家也要在计算机使用自己的字符，于是出现了字符集“百花齐放”的情况，我国在早期也颁布了自己的中文字符集标准。字符集一多，难免出现字符集编码不兼容的情况，比如：A字符集中某字符X的编码值是Y，但是在B字符集中Y这个值所表示的字符却是Z，这种不兼容的情况在一段时间内长期存在，导致因字符集导致的传输、处理、呈现、存储等问题常常发生，非常恼人。直到[Unicode(万国码/统一码)](https://home.unicode.org/)在1994年发布，人类终于有了以统一人类所有字符为目的的统一字符集。Unicode的普及也是花费了不少的时间。但在2019年的今天，世界上绝大多数系统都支持了Unicode。

Unicode究竟是啥？Unicode就是一个表，如下图：

![img{512x368}](../../assets/8384864a1a71600b.png)


图：unicode是什么

我们看到这个表中有两列：序号和字符。其中**序号**就是为全世界所有国家的所有语言文字的符号做的编码，每个字符分配一个序号，序号的范围从0×000000到0x10FFFF，一共110多万个字符，这个序号也被称为Unicode码点(code point)。第二列的字符就称为“Unicode字符”。注意：同样一个“中”字，在Unicode表中的”中”称为Unicode字符“中”；在GB18030码表中的“中”称为GB18030字符“中”。计算机中的字符是有**字符集属性**的，因此虽然字符外形相同（都是“中”），但在计算机内部的存储表示是不同的。

![img{512x368}](../../assets/4509d6cdc936d7b5.png)


图：拉丁字符对应的unicode表段

试想一下如果全世界的计算机系统都将Unicode序号作为Unicode字符的编码方案进行编解码，那么字符集问题便会从地球上彻底消失。但这个“理想的情况”并未发生。原因是什么呢？原因就是如果按照”理想方案”编码，那么无论是世界上最常用的26个字母a-z还是亚马逊森林中某个尚处于原始社会形态的某个部落的一个符号都要用一个”三字节”的存储单元表示，这意味着现实世界中所有数字资料的存储空间要变为原先的三倍（注：世界上大部分资料是用英语的26个字母编写的，原先每个字母仅需一个字节存储）、在传输相同信息的情况下，传输压力增加为原来的三倍，这是世界所无法接受的。Unicode组织其实也没有要求大家使用这种“**理想的编码方案**”对Unicode字符进行编码。于是就出现了UTF-8、UTF-16等变长的Unicode字符的编码方案，专门用于在**存储和传输Unicode字符时使用**。其中UTF-8经过实践，已经成为如今世界的Unicode字符的编码方案事实标准。

![img{512x368}](../../assets/fac2322f5637aaba.png)


图：凤凰网默认采用utf-8编码方案

UTF-8这种Unicode字符的编码方案有几个特点：

-
使用变长字节对Unicode字符进行编码。采用什么编码与Unicode字符的序号有关，序号小的使用的字节就少，序号大的使用的字节就多。使用的字节个数从 1 到 4 个不等。

-
兼容ASCII字符集编码。这点非常重要，这意味着采用Unicode字符集时，已有的ASCII字符存储和传输方式无需改变，依然兼容可用。

-
UTF-8 的编码单元为一个字节（也就是一次编解码一个字节），所以在处理UTF8字符的时候就不需要考虑这一个字节的存储是在高位还是在低位。


下面我们结合图、代码示例来更清晰地了解一下Unicode字符、UTF-8编码、[GB18030编码](http://www.gb18030.com/)的区别。

![img{512x368}](../../assets/a631614556a94160.png)


图: “中国人”三个字对应Unicode字符、字符对应的码点（序号）、UTF-8编码与GB18030编码

从上图中，我们看到三个Unicode字符：中、国、人对应的在Unicode表中的序号(码点）分别是：U+4E2D、U+56FD和U+4EBA。我们可以通过一段Go代码来输出Unicode字符的码点。

```
package main
import "fmt"
func main() {
var s = "中国人"
for _, v := range s {
fmt.Printf("%s => 码点：%X\n", string(v), v)
}
}
```


运行该程序的输出结果：

```
中 => 码点：4E2D
国 => 码点：56FD
人 => 码点：4EBA
```


我们知道在Go语言中，rune这种builtin类型被用来表示一个**“Unicode字符”**，因此一个rune的值就是其对应Unicode字符的序号，即码点。通过for range语句对字符串进行迭代访问是，range会依次返回Unicode字符对应的rune，即码点。这里可以看到Unicode字符“中”对应的rune（码点）为0x4E2D。

前面我们说过，Unicode字符在存储和传输时采用的并非“理想编码方案”，而多维UTF-8编码，也就是说在上面的例子中“中国人”这三个Unicode字符在内存中并不是以码点值存储的，而是以UTF-8编码后的值存储的。还以Unicode字符“中”为例，在上图中，我们看到其对应的UTF-8编码为0xE4B8AD这三个字节，我们用Go代码来验证一下：

```
package main
import "fmt"
func main() {
var s = "中"
fmt.Printf("%s => UTF8编码: ", s)
for _, v := range []byte(s) {
fmt.Printf("%X", v)
}
fmt.Printf("\n")
}
```


运行该程序得到如下结果：

```
中 => UTF8编码: E4B8AD
```


我们将字符串转换为对应的切片元素，然后按字节逐一输出便得到了Unicode字符“中”所对应的UTF-8编码，即存储“中”这个字符时，内存所使用的字节(三个)和对应的值。

“中”这个字符也存在于我们的国标GB18030编码表中，那么GB18030表中是如何对GB18030字符“中”进行编码的呢？我们来看一个全面些的例子：

```
// github.com/bigwhite/experiments/non-ascii-char-encoding/demo1.go
package main
import (
"fmt"
utils "github.com/bigwhite/gocmpp/utils"
)
func main() {
var stringLiteral = "中国人"
var stringUsingRuneLiteral = "\u4E2D\u56FD\u4EBA"
if stringLiteral != stringUsingRuneLiteral {
fmt.Println("stringLiteral is not equal to stringUsingRuneLiteral")
return
}
fmt.Println("stringLiteral is equal to stringUsingRuneLiteral")
for i, v := range stringLiteral {
fmt.Printf("中文字符: %s <=> Unicode码点(rune): %X <=> UTF8编码(内存值): ", string(v), v)
s := stringLiteral[i : i+3]
for _, v := range []byte(s) {
fmt.Printf("0x%X ", v)
}
s1, _ := utils.Utf8ToGB18030(s)
fmt.Printf("<=> GB18030编码(内存值): ")
for _, v := range []byte(s1) {
fmt.Printf("0x%X ", v)
}
fmt.Printf("\n")
}
}
```


运行该程序，得到如下结果：

```
$go run demo1.go
stringLiteral is equal to stringUsingRuneLiteral
中文字符: 中 <=> Unicode码点(rune): 4E2D <=> UTF8编码(内存值): 0xE4 0xB8 0xAD <=> GB18030编码(内存值): 0xD6 0xD0
中文字符: 国 <=> Unicode码点(rune): 56FD <=> UTF8编码(内存值): 0xE5 0x9B 0xBD <=> GB18030编码(内存值): 0xB9 0xFA
中文字符: 人 <=> Unicode码点(rune): 4EBA <=> UTF8编码(内存值): 0xE4 0xBA 0xBA <=> GB18030编码(内存值): 0xC8 0xCB
```


我们看到，如果使用[GB18030编码](https://www.qqxiuzi.cn/zh/hanzi-gb18030-bianma.php)，中文字符“中”字仅需要在内存中使用两个字节0xD6和0xD0表示。

综上，关于中文字符编码，需记住以下要点：

-
Unicode是目前被支持最为广泛的

**字符集**； -
Utf-8是目前被支持最为广泛的

**Unicode字符的编码方式**(还有其他方式，比如UTF-16、UTF-32等)； -
针对同一个字符，比如：“中”，如果该字符存在于两个字符集编码方案A（比如：utf8)和B(比如gb18030)中，那么我们可以通过转换，将该字符在A中的编码(如：”中”的E4B8AD)转换为在B中的编码(如“中”的D6D0)。


## >本文涉及的例子源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/non-ascii-char-encoding)下载。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

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

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

UTF8编码: E4B8AD 三个字节

GB18030编码(内存值): 0xD6 0xD0 两个字节

博主，请教个小白问题，编码串的长度是怎么看出是几个字节的呀？

E4 B8 AD这些都是十六进制数啊。每个十六进制数用4个bit（从0000，即0×0 到1111,即0xF)表示，比如：0xE。两个十六进制数就是一个字节，比如：0xE4。这样清晰了吧:)