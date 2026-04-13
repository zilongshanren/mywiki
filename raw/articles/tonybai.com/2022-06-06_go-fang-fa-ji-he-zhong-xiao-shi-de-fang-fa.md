---
title: Go：方法集合中“消失的方法”
url: https://tonybai.com/2022/06/06/the-disappeared-method-in-method-set/
published: '2022-06-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go：方法集合中“消失的方法”

![](../../assets/d1d895215bafdf38.png)


[本文永久链接](https://tonybai.com/2022/06/06/the-disappeared-method-in-method-set) – https://tonybai.com/2022/06/06/the-disappeared-method-in-method-set

在[《Go语言第一课》](http://gk.link/a/10AVZ)中，我花了三节课对Go方法做了全面细致的讲解，而类型的方法集合是其中的一个重点，因为[ 方法集合决定接口实现](https://tonybai.com/2022/05/17/understand-the-nature-of-go-method-and-how-to-choose-the-correct-receiver-type)，并且课程还分门别类地对各种使用类型嵌入(type embedding)机制定义的类型进行了说明，讲解了这些类型的

**方法集合的组成规则**。我还提供了一个可以输出某类型的方法集合的辅助函数，便于大家很直观地查看特定类型的方法集合。

学员们在Go方法集合方面也投入了极大的学习热情，提出了不少好问题。这不，前两天有一位学员Aeins就[提出了一个很好的问题](https://time.geekbang.org/discuss/detail/347295)，其问题如下(略做润色)：

```
Aeins：
下面示例中的结构体类型使用两种不同方式嵌入接口类型。
由于接口类型嵌入允许重名方法，因此I接口有三个方法。类型SI嵌入了接口类型I，因此，SI也有三个方法；
SI12嵌入了接口类型I1和I2, 但SI12却只有两个方法。难道是结构体类型嵌入不允许重名，M 方法被自动隐藏了？，
package main
import (
"fmt"
"reflect"
)
type I1 interface {
M()
M1()
}
type I2 interface {
M()
M2()
}
type I interface {
I1
I2
}
type SI struct {
I
}
type SI12 struct {
I1
I2
}
func main() {
var si SI
var si12 SI12
DumpMethodSet(si)
DumpMethodSet(si12)
}
func DumpMethodSet(i interface{}) {
dynTyp := reflect.TypeOf(i)
if dynTyp == nil {
fmt.Printf("there is no dynamic type\n")
return
}
n := dynTyp.NumMethod()
if n == 0 {
fmt.Printf("%s's method set is empty!\n", dynTyp)
return
}
fmt.Printf("%s's method set:\n", dynTyp)
for j := 0; j < n; j++ {
fmt.Println("-", dynTyp.Method(j).Name)
}
fmt.Printf("\n")
}
============
main.SI's method set:
- M
- M1
- M2
main.SI12's method set:
- M1
- M2
```


从这个问题的示例代码中我们看到Aeins这位学员的疑问：通过嵌入组合了I1和I2的接口类型I的类型SI的方法集合中包含了方法M，而通过直接嵌入接口类型I1和I2的类型SI2的方法集合中的**方法M却“消失”了，这是为什么呢**？

好了，下面我们就来分析一下。

我们知道：一个类型的方法集合中的方法应该都是可以被这个类型实例所合法调用的。比如：

```
// https://go.dev/play/p/gGkgsGRJpHv
package main
type I interface {
M1()
M2()
}
type T struct {
}
func (T) M1() {
}
func (T) M2() {
}
type S struct {
I
}
func (S) M3() {}
func main() {
var s = S{
I: T{},
}
s.M1()
s.M2()
s.M3()
}
```


结构体类型S的方法集合中有三个方法，其中M1、M2来自于对接口类型I的类型嵌入，M3则是S自定义的方法。不过**无论是哪个方法，一旦进入S的方法集合，它就可以被S实例合法调用**。

反过来说：**只有能被类型实例直接调用的方法才能进入其方法集合**。那么我们分别看看问题示例中的SI和SI12。

先来分析一下SI。SI嵌入了接口类型I，而接口类型I则是由I1和I2两个接口类型组合而成。这种通过嵌入其他接口类型来创建新接口类型的方式，在[Go 1.14版本](https://tonybai.com/2020/03/08/some-changes-in-go-1-14)之前是有约束的：如果新接口类型嵌入了多个接口类型，这些嵌入的接口类型的方法集合不能有交集，同时嵌入的接口类型的方法集合中的方法名字，也不能与新接口中的其他方法同名。但自Go 1.14版本开始，Go语言去除了这些约束，这也是I1和I2的方法集合有交集，但仍可以同时嵌入到SI中的原因。这样接口类型SI的方法集合就包含了M、M1和M2。

当SI通过嵌入I进行定义时，SI的方法集合“继承”了接口类型I的方法集合，通过合理初始化后的SI的实例，我们可以合法调用M、M1和M2：

```
type S3 struct {
}
func (S3) M() {
}
func (S3) M1() {
}
func (S3) M2() {
}
func main() {
var s = SI{
I : S3{},
}
s.M() //ok
s.M1() //ok
s.M2() //ok
}
```


我们再来看SI12。在问题示例中，SI12没有嵌入整合了I1和I2的接口类型I，而是直接嵌入了I1和I2。那么是否I1和I2的方法集合中的方法都会变成SI12类型的方法集合中的方法呢？那要看SI12类型的实例是否可以合法调用I1和I2的方法？我们看下面例子：

```
type S1 struct {
}
func (S1) M() {
}
func (S1) M1() {
}
type S2 struct {
}
func (S2) M() {
}
func (S2) M2() {
}
func main() {
var si12 = SI12{
I1: S1{},
I2: S2{},
}
DumpMethodSet(si12)
si12.M1() // ok
si12.M2() // ok
si12.M() // ambiguous selector si12.M
}
```


我们看到通过SI12类型的实例可以成功调用M1和M2方法，但在调用M方法时出现了“歧义”，Go编译器无法确定究竟该调用si12.I1.M方法还是si12.I2.M方法，即Go编译器无法合法调用M方法，因此M方法因未决的歧义性不能被列入SI12的方法集合中。

这就是SI12类型方法集合中方法M“消失”的原因，你get到了么！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论