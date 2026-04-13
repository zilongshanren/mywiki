---
title: Go导出标识符：那些鲜为人知的细节
url: https://tonybai.com/2025/01/23/the-hidden-details-of-go-exported-identifiers/
published: '2025-01-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go导出标识符：那些鲜为人知的细节

![](../../assets/29a4522d808edea1.png)


[本文永久链接](https://tonybai.com/2025/01/23/the-hidden-details-of-go-exported-identifiers) – https://tonybai.com/2025/01/23/the-hidden-details-of-go-exported-identifiers

前不久，在“Go+用户组”微信群里看到有开发者向七牛云老板许式伟反馈[七牛云Go SDK中的某些类型没有导出，导致外部包无法使用的问题(如下图)](https://github.com/qiniu/go-sdk/blob/bb391c9d9ea2c115494df5c38d058cb3b673a29f/qvs/record.go#L41)：

![](../../assets/62830d7e48f65ec7.png)


七牛开发人员迅速对该问题做出了“更正”，将问题反馈中涉及的类型saveasArgs和saveasReply改为了导出类型，即首字母大写：

![](../../assets/db4e5f4fb965a012.png)


不过，这看似寻常的问题反馈与修正却引发了我的一些思考。

我们大胆臆想一下：如果saveasReply类型的开发者是故意将saveasReply类型设置为非导出的呢？看一下“更正”之前的saveasReply代码：

```
type saveasReply struct {
Fname string `json:"fname"`
PersistenId string `json:"persistentId,omitempty"`
Bucket string `json:"bucket"`
Duration int `json:"duration"` // ms
}
```


有读者可能会问：那为什么还将saveasReply结构体的字段设置为导出字段呢？请注意每个字段后面的结构体标签(struct tag)。这显然是为了进行JSON 编解码，因为目前Go的encoding/json包仅会对导出字段进行编解码处理。

除了这个原因，原开发者可能还希望包的使用者能够访问这些导出字段，而又不想完全暴露该类型。我在此不对这种设计的合理性进行评价，而是想探讨这种做法是否可行。

我们对Go导出标识符的传统理解是：导出标识符（以大写字母开头的标识符）可以在包外被访问和使用，而非导出标识符（以小写字母开头的标识符）只能在定义它们的包内访问。这种机制帮助开发者控制类型和函数的可见性，确保内部实现细节不会被随意访问，从而增强封装性。

但实际上，Go的导出标识符机制是否允许在某些情况下，即使类型本身是非导出的，其导出字段依然可以被包外的代码访问呢？该类型的导出方法呢？这些关于Go导出标识符的细节可能是鲜少人探讨的，在这篇博文中，我们将系统地了解这些机制，希望能为各位小伙伴带来更深入的理解。

## 1. Go对导出标识符的定义

我们先回顾一下[Go语言规范(go spec)对导出标识符的定义](https://go.dev/ref/spec#Exported_identifiers)：

![](../../assets/a7ca201af608b16e.png)


我们通常使用英文字母来命名标识符，因此可以将上述定义中的第一句理解为：以大写英文字母开头的标识符即为导出标识符。

注：Unicode字符类别Lu（Uppercase Letter）包含所有的大写字母。这一类别不仅包括英文大写字母，还涵盖多种语言的大写字符，例如希腊字母、阿拉伯字母、希伯来字母和西里尔字母等。然而，我非常

不建议大家使用非英文大写字母来表示导出标识符，因为这可能会挑战大家的认知习惯。

而第二句后半部分的描述往往被我们忽视或理解不够到位。一个类型的字段名和方法名可以是导出的，但**并没有明确要求其关联的类型本身也必须是导出的**。

这为我们提供了进一步探索Go导出标识符细节的机会。接下来，我们就用具体示例看看是否可以在包外访问非导出类型的导出字段以及导出方法。

## 2. 在包外访问非导出类型的导出字段

我们首先定义一个带有导出字段的非导出类型myStruct，并将它放在mypackage里：

```
// go-exported-identifiers/field/mypackage/mypackage.go
package mypackage
type myStruct struct {
Field string // 导出的字段
}
// NewMyStruct1是一个导出的函数，返回myStruct的指针
func NewMyStruct1(value string) *myStruct {
return &myStruct{Field: value}
}
// NewMyStruct1是一个导出的函数，返回myStruct类型变量
func NewMyStruct2(value string) myStruct {
return myStruct{Field: value}
}
```


然后我们在包外尝试访问myStruct类型的导出字段：

```
// go-exported-identifiers/field/main.go
package main
import (
"demo/mypackage"
"fmt"
)
func main() {
// 通过导出的函数获取myStruct的指针
ms1 := mypackage.NewMyStruct1("Hello1")
// 尝试访问Field字段
fmt.Println(ms1.Field) // Hello1
// 通过导出的函数获取myStruct类型变量
ms2 := mypackage.NewMyStruct1("Hello2")
// 尝试访问Field字段
fmt.Println(ms2.Field) // Hello2
}
```


在go-exported-identifiers/field目录下编译运行该示例：

```
$go run main.go
Hello1
Hello2
```


我们看到，无论是通过myStruct的指针还是实例副本，都可以成功访问其导出变量Field。这个示例的关键就是：我们**使用了短变量声明**直接通过调用myStruct的两个“构造函数(NewXXX)”得到了其指针(ms1)以及实例副本(ms2)。在这个过程中，我们没有在main包中显式使用mypackage.myStruct这个非导出类型。

采用类似的方案，我们接下来再看看是否可以在包外访问非导出类型的导出方法。

## 3. 在包外访问非导出类型的导出方法

我们为非导出类型添加两个导出方法M1和M2：

```
// go-exported-identifiers/method/mypackage/mypackage.go
package mypackage
import "fmt"
type myStruct struct {
Field string // 导出的字段
}
// NewMyStruct1是一个导出的函数，返回myStruct的指针
func NewMyStruct1(value string) *myStruct {
return &myStruct{Field: value}
}
// NewMyStruct1是一个导出的函数，返回myStruct类型变量
func NewMyStruct2(value string) myStruct {
return myStruct{Field: value}
}
func (m *myStruct) M1() {
fmt.Println("invoke *myStruct's M1")
}
func (m myStruct) M2() {
fmt.Println("invoke myStruct's M2")
}
```


然后，试着在外部包中调用M1和M2方法：

```
// go-exported-identifiers/method/main.go
package main
import (
"demo/mypackage"
)
func main() {
// 通过导出的函数获取myStruct的指针
ms1 := mypackage.NewMyStruct1("Hello1")
ms1.M1()
ms1.M2()
// 通过导出的函数获取myStruct类型变量
ms2 := mypackage.NewMyStruct2("Hello2")
ms2.M1()
ms2.M2()
}
```


在go-exported-identifiers/method目录下编译运行这个示例：

```
$go run main.go
invoke *myStruct's M1
invoke myStruct's M2
invoke *myStruct's M1
invoke myStruct's M2
```


我们看到，无论是通过非导出类型的指针，还是通过非导出类型的变量复本都可以成功调用非导出类型的导出方法。

提及方法，我们会顺带想到接口，非导出类型是否可以实现某个外部包定义的接口呢？我们继续往下看。

## 4. 非导出类型实现某个外部包的接口

在Go中，如果某个类型T实现了某个接口类型I的方法集合中的所有方法，我们就说T实现了I，T的实例可以赋值给I类型的接口变量。

在下面示例中，我们看看非导出类型是否可以实现某个外部包的接口。

在这个示例中mypackage包中的内容与上面示例一致，主要改动的是main.go，我们来看一下：

```
// go-exported-identifiers/interface/main.go
package main
import (
"demo/mypackage"
)
// 定义一个导出的接口
type MyInterface interface {
M1()
M2()
}
func main() {
var mi MyInterface
// 通过导出的函数获取myStruct的指针
ms1 := mypackage.NewMyStruct1("Hello1")
mi = ms1
mi.M1()
mi.M2()
// 通过导出的函数获取myStruct类型变量
// ms2 := mypackage.NewMyStruct2("Hello2")
// mi = ms2 // compile error: mypackage.myStruct does not implement MyInterface
// ms2.M1()
// ms2.M2()
}
```


在这个main.go中，我们定义了一个接口MyInterface，它的方法集合中有两个方法M1和M2。根据类型方法集合的判定规则，*myStruct类型实现了MyInterface的所有方法，而myStruct类型则不满足，没有实现M1方法，我们在go-exported-identifiers/interface目录下编译运行这个示例，看看是否与我们预期的一致：

```
$go run main.go
invoke *myStruct's M1
invoke myStruct's M2
```


如果我们去掉上面代码中对ms2的注释，那么将得到Compiler error: mypackage.myStruct does not implement MyInterface。

接下来，我们再来考虑一个场景，即非导出类型用作嵌入字段的情况，我们要看看该非导出类型的导出方法和导出字段是否会promote到外部类型中。

## 5. 非导出类型用作嵌入字段

我们改造一下示例，新版的带有嵌入字段的结构见下面mypackage包的代码：

```
// go-exported-identifiers/embedded_field/mypackage/mypackage.go
package mypackage
import "fmt"
type nonExported struct {
Field string // 导出的字段
}
// Exported 是导出的结构体，嵌入了nonExported
type Exported struct {
nonExported // 嵌入非导出结构体
}
func NewExported(value string) *Exported {
return &Exported{
nonExported: nonExported{
Field: value,
},
}
}
// M1是导出的函数
func (n *nonExported) M1() {
fmt.Println("invoke nonExported's M1")
}
// M2是导出的函数
func (e *Exported) M2() {
fmt.Println("invoke Exported's M2")
}
```


这里新增一个导出类型Exported，它嵌入了一个非导出类型nonExported，后者拥有导出字段Field，以及两个导出方法M1。我们也Exported类型定义了一个方法M2。

下面我们再来看看main.go中是如何使用Exported的：

```
// go-exported-identifiers/embedded_field/main.go
package main
import (
"demo/mypackage"
"fmt"
)
// 定义一个导出的接口
type MyInterface interface {
M1()
M2()
}
func main() {
ms := mypackage.NewExported("Hello")
fmt.Println(ms.Field) // 访问嵌入的非导出结构体的导出字段
ms.M1() // 访问嵌入的非导出结构体的导出方法
var mi MyInterface = ms
mi.M1()
mi.M2()
}
```


在go-exported-identifiers/embedded_field目录下编译运行这个示例：

```
$go run main.go
Hello
invoke nonExported's M1
invoke nonExported's M1
invoke Exported's M2
```


我们看到，作为嵌入字段的非导出类型的导出字段与方法会被自动promote到外部类型中，通过外部类型的变量可以直接访问这些字段以及调用这些导出方法。这些方法还可以作为外部类型方法集中的一员，来作为满足特定接口类型(如上面代码中的MyInterface)的条件。

Go 1.18增加了泛型支持，那么非导出类型是否可以用作泛型函数和泛型类型的类型实参呢？最后我们来看看这个细节。

## 6. 非导出类型用作泛型函数和泛型类型的类型实参

和前面一样，我们先定义用于该示例的带有导出字段和导出方法的非导出类型：

```
// go-exported-identifiers/generics/mypackage/mypackage.go
package mypackage
import "fmt"
// 定义一个非导出的结构体
type nonExported struct {
Field string
}
// 导出的方法
func (n *nonExported) M1() {
fmt.Println("invoke nonExported's M1")
}
func (n *nonExported) M2() {
fmt.Println("invoke nonExported's M2")
}
// 导出的函数，用于创建非导出类型的实例
func NewNonExported(value string) *nonExported {
return &nonExported{Field: value}
}
```


现在我们将其用于泛型函数，下面定义了泛型函数UseNonExportedAsTypeArgument，它的类型参数使用MyInterface作为约束，而上面的nonExported显然满足该约束，我们通过构造函数NewNonExported获得非导出类型的实例，然后将其传递给UseNonExportedAsTypeArgument，Go会通过泛型的类型参数自动推导机制推断出类型实参的类型：

```
// go-exported-identifiers/generics/main.go
package main
import (
"demo/mypackage"
)
// 定义一个用作约束的接口
type MyInterface interface {
M1()
M2()
}
func UseNonExportedAsTypeArgument[T MyInterface](item T) {
item.M1()
item.M2()
}
// 定义一个带有泛型参数的新类型
type GenericType[T MyInterface] struct {
Item T
}
func NewGenericType[T MyInterface](item T) GenericType[T] {
return GenericType[T]{Item: item}
}
func main() {
// 创建非导出类型的实例
n := mypackage.NewNonExported("Hello")
// 调用泛型函数，传入实现了MyInterface的非导出类型
UseNonExportedAsTypeArgument(n) // ok
// g := GenericType{Item: n} // compiler error: cannot use generic type GenericType[T MyInterface] without instantiation
g := NewGenericType(n)
g.Item.M1()
}
```


但由于目前Go泛型还不支持对泛型类型的类型参数的自动推导，所以直接通过g := GenericType{Item: n}来初始化一个泛型类型变量将导致编译错误！我们需要借助泛型函数的推导机制将非导出类型与泛型类型进行结合，参见上述示例中的NewGenericType函数，通过泛型函数支持的类型参数的自动推导间接获得GenericType的类型实参。在go-exported-identifiers/generics目录下编译运行这个示例，便可得到我们预期的结果：

```
$go run main.go
invoke nonExported's M1
invoke nonExported's M2
invoke nonExported's M1
```


## 7. 非导出类型使用导出字段以及导出方法的用途

前面的诸多示例证明了：即使类型本身是非导出的，但其内部的导出字段以及它的导出方法依然可以在外部包中使用，并且在实现接口、嵌入字段、泛型等使用场景下均有效。

到这里，你可能会提出这样一个问题：**会有Go开发者使用非导出类型结合导出字段或方法的设计吗**？

其实这种还是很常见的，在Go标准库中就有不少，只不过它们更多是包内使用，类似于非导出类型xxxImpl和它的Wrapper类型XXX的关系，或是xxxImpl或嵌入到XXX中，就像这样：

```
// 包内实现
type xxxImpl struct { // 非导出的实现类型
// 内部字段
}
// 导出的包装类型
type XXX struct {
impl *xxxImpl // 包含实现类型
// 其他字段
}
// 或者通过嵌入方式
type XXX struct {
*xxxImpl // 嵌入实现类型
// 其他字段
}
```


但也有一些可以包外使用的，比如实现了某个接口，并通过接口值返回，提供给外部使用，例如下面的valueCtx，它实现了Context接口，并通过WithValue返回，供调用WithValue的外部包使用：

```
//$GOROOT/src/context/context.go
func WithValue(parent Context, key, val any) Context { // 构造函数，实现接口
if parent == nil {
panic("cannot create context from nil parent")
}
if key == nil {
panic("nil key")
}
if !reflectlite.TypeOf(key).Comparable() {
panic("key is not comparable")
}
return &valueCtx{parent, key, val}
}
// A valueCtx carries a key-value pair. It implements Value for that key and
// delegates all other calls to the embedded Context.
type valueCtx struct {
Context
key, val any
}
func (c *valueCtx) Value(key any) any {
if c.key == key {
return c.val
}
return value(c.Context, key)
}
```


这么做的目的是什么呢？大约有如下几点：

- 隐藏实现细节

非导出类型的主要作用是防止外部直接使用和依赖其内部实现细节。通过限制类型的直接使用，库作者可以保持实现的灵活性，随时调整或重构类型的内部逻辑，而无需担心破坏外部调用代码； 还可以避免暴露多余的API，使库的接口更加简洁。

- 控制实例的创建和管理

通过非导出类型，开发者还可以确保外部代码无法直接实例化类型，而必须通过导出的构造函数或工厂函数，就像前面举的示例那样。这种模式可以保证对象始终以特定的方式初始化，避免错误使用。同时，它还可以用来实现更复杂的初始化逻辑，如依赖注入或资源管理。

- 在接口实现中的作用

非导出类型可以用来实现导出的接口，从而将接口的实现细节完全隐藏。对于用户来说，只需要关心接口的定义，而无需关注其实现。

## 8. 小结

本文探讨了Go语言中的导出标识符及其相关细节，特别是非导出类型如何与其导出字段和导出方法结合使用。

尽管某些类型是非导出的，其内部的导出字段和方法依然可以在包外访问。此外，非导出类型在实现接口、嵌入字段和泛型中也展现出良好的应用。这种设计不仅促进了封装和接口实现的灵活性，还允许开发者通过构造函数返回非导出类型的实例，从而有效控制实例的创建与管理。这种方式帮助隐藏实现细节，简化外部接口，使得代码结构更加清晰。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go-exported-identifiers)下载。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾

。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论