---
title: 关于xml包在Unmarshal时将\r\n重写为\n的问题
url: https://tonybai.com/2020/06/04/the-issue-of-go-xml-package-rewrite-carriage-return/
published: '2020-06-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于xml包在Unmarshal时将\r\n重写为\n的问题

今年4月份，中国移动、中国电信、中国联通三大运营商联合举行线上发布会，发布了[《5G消息白皮书》](http://finance.sina.com.cn/stock/stockzmt/2020-04-08/doc-iircuyvh6639036.shtml)。所谓5G消息，即传统短信消息（仅能进行文本展示）的升级版，是由[GSMA](https://www.gsma.com/)组织制定的[RCS(Rich Communication Suite)](https://www.gsma.com/futurenetworks/rcs/)消息规范所定义。2019年RCS UP（unified profile)更新到2.4版本，并成为了5G终端标准的一部分，该版本也是第一个具备商用能力的版本，为5G消息商用奠定了基础。中国移动计划2020.6月末正式实现5G消息的商用，目前已经在浙江和广东建立了两个5G消息的支撑节点（分别由中兴和华为承建）。作为电信移动增值领域的厂商，我方也参与了与浙江节点进行行业5G消息平台([MaaP](https://www.gsma.com/futurenetworks/resources/messaging-as-a-platform))联调与应用开发。

这引子有些长，本文重点不在5G消息，而在于与行业5G消息平台对接时遇到的一个Go xml包的问题，这是记录一下，以供自己备忘，同时也供广大gopher们参考。

## 1. 问题现象

行业5G消息使用的通信协议本质上就是[xml](https://www.w3.org/TR/REC-xml) over [http(s)](https://tonybai.com/2015/04/30/go-and-https/)。在http Body的xml中，有一个字段**bodyText**承载了真正到达5G智能终端上的有效信息载荷，且这个字段是一个[CDATA包裹的字段](https://www.w3.org/TR/REC-xml/#sec-cdata-sect)。在我们系统的某个转发流程中，我们解析了从Chatbot(5G行业消息机器人)下发的行业5G消息，但我们发现解析后的**bodyText**字段中的“\r\n”都被转换为“\n”了。我们用一个例子来直观描述一下该问题：

```
// xml-rewrite-carriage-return/test2.go
package main
import (
"encoding/hex"
"encoding/xml"
"fmt"
)
type DescCDATA struct {
Desc string `xml:",cdata"`
}
type Person struct {
Name string `xml:"name"`
Age int `xml:"age"`
Desc DescCDATA `xml:"desc"`
}
var profileFmt = `<person>
<name>"tony bai"</name>
<age>33</age>
<desc><![CDATA[%s]]></desc>
</person>`
func main() {
c := fmt.Sprintf(profileFmt, "hello\r\nxml")
var p Person
err := xml.Unmarshal([]byte(c), &p)
if err != nil {
fmt.Println("unmarshal error:", err)
return
}
fmt.Println("unmarshal ok")
fmt.Println(hex.Dump([]byte("hello\r\nxml")))
fmt.Println(hex.Dump([]byte(p.Desc.Desc)))
}
```


运行该例子：

```
$go run test2.go
unmarshal ok
00000000 68 65 6c 6c 6f 0d 0a 78 6d 6c |hello..xml|
00000000 68 65 6c 6c 6f 0a 78 6d 6c |hello.xml|
```


这是一个非常简单的xml unmarshal(反序列化)的例子。我们看到反序列化后，结构体desc字段中的内容相比于原始的xml中desc的内容少了一个字符：0x0d，即“\r”(carriage-return)。我们一直以为针对原xml中CDATA包裹的数据内容，xml包在unmarshal时会**原封不动**的拷贝下来。为什么”\r”字符会被删除掉呢？我们接下来找找原因。

## 2. 问题原因

Go是开源的编程语言，它最大的优势就是遇到问题后可以直接看Go标准库源码，当然也可以通过调试工具跟踪到标准库源码中。xml包并不复杂，我选择了直接看xml unmarshal代码的方式。在$GOROOT/src/encoding/xml/xml.go([go 1.14版本](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/))中，我们在Decoder的**text**方法中找到如下几行代码：

```
// $GOROOT/src/encoding/xml/xml.go
... ...
func (d *Decoder) text(quote int, cdata bool) []byte {
... ...
// We must rewrite unescaped \r and \r\n into \n.
if b == '\r' {
d.buf.WriteByte('\n')
} else if b1 == '\r' && b == '\n' {
// Skip \r\n--we already wrote \n.
} else {
d.buf.WriteByte(b)
}
... ...
}
```


Decoder的**text**方法是xml unmarshal在解析如下面name字段的值(xxxx)时被调用的：

```
<name>xxxx</name>
```


这段代码的逻辑是：将xxxx中的\r重写为\n，如果存在\r\n，则将其重写为\n。并且无论是否是CDATA字段，这块的逻辑均是生效的。比如我们将上面例子中的desc字段改为非CDATA类型：

```
// xml-rewrite-carriage-return/test1.go
type Person struct {
Name string `xml:"name"`
Age int `xml:"age"`
Desc string `xml:"desc"`
}
var profileFmt = `<person>
<name>"tony bai"</name>
<age>33</age>
<desc>%s</desc>
</person>`
func main() {
c := fmt.Sprintf(profileFmt, "hello\r\nxml")
var p Person
err := xml.Unmarshal([]byte(c), &p)
if err != nil {
fmt.Println("unmarshal error:", err)
return
}
fmt.Println("unmarshal ok")
fmt.Println(hex.Dump([]byte("hello\r\nxml")))
fmt.Println(hex.Dump([]byte(p.Desc)))
}
```


该例子的输出：

```
$go run test1.go
unmarshal ok
00000000 68 65 6c 6c 6f 0d 0a 78 6d 6c |hello..xml|
00000000 68 65 6c 6c 6f 0a 78 6d 6c |hello.xml|
```


我们看到：非CDATA包裹的数据，其中的”\r\n”也被重写为“\n”了。

关于这个问题，在Go项目issue中也有人提及：https://github.com/golang/go/issues/24426 。从该issue的讨论中看，Go标准库xml包的实现应该还是参考了xml规范中关于[line end](https://www.w3.org/TR/REC-xml/#sec-line-ends)的描述的：

```
XML parsed entities are often stored in computer files which, for editing convenience, are organized into lines. These lines are typically separated by some combination of the characters CARRIAGE RETURN (#xD) and LINE FEED (#xA).
To simplify the tasks of applications, the XML processor must behave as if it normalized all line breaks in external parsed entities (including the document entity) on input, before parsing, by translating both the two-character sequence #xD #xA and any #xD that is not followed by #xA to a single #xA character.
```


上面的英文规范翻译过来大致是：

```
XML解析的实体通常存储在计算机文件中，为了便于编辑，这些文件被组织成多行。 这些行通常由字符回车（#xD）和换行（#xA）的某种组合分隔。
为了简化应用程序的任务（解析回车和换行的组合），在解析之前，XML处理器必须对输入的外部解析实体（包括文档实体）进行转换使其规范化，转换规则是：将两字符序列#xD #xA以及后面未紧跟#xA字符的#xD字符转换为单个的#xA字符。
```


## 3. 解决方法

我们的述求就是对CDATA包裹的文本数据中的”\r\n”不做“重写”处理。我们采用了下面的方案：**clone一份标准库中的xml包，将clone版本放入我们自己的项目路径下，然后在clone版本基础上修改Decoder的text方法的实现**：

```
// xml-rewrite-carriage-return/xml/xml.go
... ...
func (d *Decoder) text(quote int, cdata bool) []byte {
... ...
// We must rewrite unescaped \r and \r\n into \n.
//
// tonybai change: only rewrite when text is not in CDATA section
// (https://github.com/golang/go/issues/24426)
if !cdata && b == '\r' {
d.buf.WriteByte('\n')
} else if !cdata && b1 == '\r' && b == '\n' {
// Skip \r\n--we already wrote \n.
} else {
d.buf.WriteByte(b)
}
....
}
```


改造后的代码仅对非CDATA数据进行\r\n的重写，而对于CDATA类型数据，则原封不动的解析出来。我们将test2.go改造成使用我们的clone版本的xml包的示例代码：**test3.go**：

```
// xml-rewrite-carriage-return/test3.go
package main
import (
"encoding/hex"
"github.com/bigwhite/xmltest/xml"
"fmt"
)
type DescCDATA struct {
Desc string `xml:",cdata"`
}
type Person struct {
Name string `xml:"name"`
Age int `xml:"age"`
Desc DescCDATA `xml:"desc"`
}
var profileFmt = `<person>
<name>"tony bai"</name>
<age>33</age>
<desc><![CDATA[%s]]></desc>
</person>`
func main() {
c := fmt.Sprintf(profileFmt, "hello\r\nxml")
var p Person
err := xml.Unmarshal([]byte(c), &p)
if err != nil {
fmt.Println("unmarshal error:", err)
return
}
fmt.Println("unmarshal ok")
fmt.Println(hex.Dump([]byte("hello\r\nxml")))
fmt.Println(hex.Dump([]byte(p.Desc.Desc)))
}
```


运行该示例：

```
$go run test3.go
unmarshal ok
00000000 68 65 6c 6c 6f 0d 0a 78 6d 6c |hello..xml|
00000000 68 65 6c 6c 6f 0d 0a 78 6d 6c |hello..xml|
```


我们看到这次包裹在CDATA中的\r\n没有被重写，我们对xml包的修改是有效的。

## 4. 小结

XML作为上一代被设计用来传输和存储数据的标记语言格式，在Go中的支持并不完善，关于标准库xml包的issue[还有好多处于open状态](https://github.com/golang/go/issues?q=encoding%2Fxml+is%3Aopen)。在标准库xml包更新较慢的情况下，clone一份xml包并进行定制不失为一种好的折中方法。

本文所涉及源码在[这里](https://github.com/bigwhite/experiments/tree/master/xml-rewrite-carriage-return)可以下载。

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