---
title: JSON包新提案：用“omitzero”解决编码中的空值困局
url: https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero/
published: '2024-09-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# JSON包新提案：用“omitzero”解决编码中的空值困局

![](../../assets/1c24e6ba47467988.png)


[本文永久链接](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero) – https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero

Go标准库是Go号称“开箱即用”的重要因素，而标准库中的encoding/json包又是标准库最常用的Go包。虽然其性能不是最好的，但好在由Go团队维护，对JSON规范兼容性好，且质量很高。但json包也不是没有“瑕疵”的，Go官方继[math/rand/v2](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)之后，也[开启了encoding/json/v2的讨论](https://github.com/golang/go/discussions/63397)，v2包含了对功能的增强，其中就包含了对空值编码的改进的考量，以及性能方面的优化。但json/v2毕竟还属于“长远”规划，当前版本的json包的问题也要修正和完善。

一个[提出于2021年的issue](https://github.com/golang/go/issues/45669)近期被即将[“功成身退”的Russ Cox](https://mp.weixin.qq.com/s/2Sy6K_dU1j3tZZiyyfCTDQ)[接受(accept)](https://github.com/golang/go/issues/33502#issuecomment-2329756576)，该issue就当前json包对空值编码的“瑕疵”做了描述并提出了修正方案。本文就将针对这一问题以及其方案进行探讨，希望能帮助大家更好地理解该issue以及其对应的方案。

## 1. 问题溯源：omitempty的局限性

在encoding/json包中，omitempty标签是开发者控制JSON序列化行为的重要工具。它的设计初衷是允许开发者指定：当某个字段值为“空”时，在JSON编码过程中应该被忽略。然而，omitempty的空值定义存在一些固有的局限性。下面是json包中对omitempty的说明：

The “omitempty” option specifies that the field should be omitted from the encoding if the field has an empty value, defined as false, 0, a nil pointer, a nil interface value, and any empty array, slice, map, or string.


总结一下，omitempty标签的判断逻辑如下：

- 对于布尔类型：false被视为空
- 对于数值类型：0被视为空
- 对于字符串：”"（空字符串）被视为空
- 对于指针、接口：nil被视为空
- 对于数组、切片、map：长度为0被视为空

下面是一个完整的Go示例，展示了omitempty标签在不同类型上的应用：

```
package main
import (
"encoding/json"
"fmt"
)
type Example struct {
BoolField bool `json:"bool_field,omitempty"`
IntField int `json:"int_field,omitempty"`
StringField string `json:"string_field,omitempty"`
PointerField *string `json:"pointer_field,omitempty"`
InterfaceField interface{} `json:"interface_field,omitempty"`
ArrayField [0]int `json:"array_field,omitempty"` // 空数组
SliceField []string `json:"slice_field,omitempty"` // 空切片
MapField map[string]int `json:"map_field,omitempty"` // 空地图
}
func main() {
var nilString *string = nil
example := Example{
BoolField: false, // 布尔类型
IntField: 0, // 数值类型
StringField: "", // 空字符串
PointerField: nilString, // nil 指针
InterfaceField: nil, // nil 接口
ArrayField: [0]int{}, // 空数组
SliceField: []string{}, // 空切片
MapField: map[string]int{}, // 空地图
}
jsonData, err := json.Marshal(example)
if err != nil {
fmt.Println("Error marshalling example:", err)
}
fmt.Println(string(jsonData)) // 输出：{}
}
```


然而，这种预定义的”空”值判断逻辑并不能满足所有实际场景的需求。让我们来看几个具体的例子：

- 空结构体问题

```
package main
import (
"encoding/json"
"fmt"
)
type Config struct {
EmptyStruct struct{} `json:",omitempty"`
}
func main() {
cfg := Config{}
data, _ := json.Marshal(cfg)
fmt.Println(string(data)) // 输出：{"EmptyStruct":{}}
}
```


我们看到：在这个例子中，尽管Config中的EmptyStruct字段是一个空结构体类型，且添加了omitempty标签，但它仍然出现在JSON输出中。

- 零值结构体

除了空结构体，零值结构体也是目前omitempty标签语义覆盖不到的类型：

```
package main
import (
"encoding/json"
"fmt"
)
type ZeroStruct struct {
A int
B string
C float64
}
type Config struct {
ZeroStruct ZeroStruct `json:",omitempty"`
}
func main() {
cfg := Config{}
data, _ := json.Marshal(cfg)
fmt.Println(string(data)) // 输出：{"ZeroStruct":{"A":0,"B":"","C":0}}
}
```


我们看到：即便ZeroStruct中各个类型的值都为零，且有了omitempty标签，json.Marshal依然输出了Config中的ZeroStruct字段。

- time.Time类型的处理

在开发实践中，我们发现json对time.Time类型在omitempty下的处理也与“常理”不符，比如下面这个示例：

```
package main
import (
"encoding/json"
"fmt"
"time"
)
type Event struct {
Time time.Time `json:",omitempty"`
}
func main() {
evt := Event{Time: time.Time{}} // 零值时间
data, _ := json.Marshal(evt)
fmt.Println(string(data)) // 输出：{"Time":"0001-01-01T00:00:00Z"}
}
```


我们看到：time.Time类型的零值依然被输出了。并且输出的是公元1年1月1日UTC时间。对于很多应用来说，这个时间并不具有实际意义，更合理的零值是”January 01, 1970 00:00:00 UTC”。

很显然，Gopher们希望json包能更好的处理上述情形。

## 2. 社区讨论与omitzero标签方案的确认

关于上述问题的解决方法，在Go社区引发了广泛讨论。不过大家普遍认为不要改变现有omitempty语义，那样会导致破坏性的change，无法向后兼容。

在讨论过程中，社区成员提出了一些其他的解决方案：

- 允许MarshalJSON()方法返回nil来完全忽略某个字段

这个方案的优点是利用了已有的接口，不需要引入新的标签。但缺点是需要为每个支持零值的类型都实现MarshalJSON()方法。

- 添加OmitJSONField方法

这个方案提议为每个类型添加一个OmitJSONField() bool方法，由开发者自己控制字段的忽略逻辑，该方案提供了很大的灵活性，但可能会导致JSON序列化逻辑过于分散。

最终，”omitzero”方案最终被认为是一个相对平衡的解决方案，因为它可以与现有的标签系统兼容，开发者可以很容易地将omitempty替换为omitzero，或者在需要的地方同时使用两者。此外，omitzero也保持了简洁性，相比其他需要大量代码修改的方案，omitzero只需要添加标签或实现一个方法(可选项)即可。

“omitzero”标签提案的核心内容是：在序列化时，”omitzero”选项指定如果字段值为零，则该结构体字段应被省略。如果该类型定义了IsZero bool方法，那么这个零值就通过IsZero方法来判断；否则是根据字段是否是零值（通过reflect.Value.IsZero判断）来判断。该omitzero选项在反序列化(unmarshal)时没有效果。如果同时指定了”omitempty”和”omitzero”，则字段是否被省略基于两者的**逻辑或关系**。 这将意味着，在省略切片时，omitzero会省略空指针切片，但对于长度为零的非空切片，则不会。对于time.Time类型，会省略time.Time{}。

此外，omitzero不强制你实现IsZero方法，但开发者可以利用IsZero方法来自由控制自定义类型在omitzero标签下是否会被省略。

一旦有了omitzero，我们就可以用它解决上面提到的问题（omitzero尚未实现，下面是伪代码）：

- 解决空结构体问题

```
type Config struct {
EmptyStruct struct{} `json:",omitzero"`
}
cfg := Config{}
data, _ := json.Marshal(cfg)
fmt.Println(string(data)) // 输出：{}
```


- 更好地处理time.Time类型

```
type Event struct {
Time time.Time `json:",omitzero"`
}
evt := Event{Time: time.Time{}} // 零值时间
data, _ := json.Marshal(evt)
fmt.Println(string(data)) // 输出：{}
```


- 自定义类型的”零值”判断

```
type CustomInt int
func (ci CustomInt) IsZero() bool {
return ci <= 0 // 自定义零值判断逻辑
}
type Data struct {
Value CustomInt `json:",omitzero"`
}
d := Data{Value: CustomInt(-1)}
data, _ := json.Marshal(d)
fmt.Println(string(data)) // 输出：{}
```


## 3. 小结

通过引入”omitzero”标签，Go语言在解决JSON编码中”空”值处理的痛点上迈出了重要一步。这个方案不仅满足了开发者对更灵活的”空”值定义的需求，还保持了与现有系统的兼容性。目前该omitzero的落地时间尚未确定，最早也要等到Go 1.24版本。此外，encoding/xml等也会效仿json包，增加omitzero标签。

此外，伴随着omitzero提案被接受，另外一个在2021年由Josh Bleecher Snyder提出的相关提案：[proposal: cmd/vet: warn about structs marked json omitempty](https://github.com/golang/go/issues/51261)也被重新“唤醒”，针对该提案，目前社区在active discussions。

随着后续encoding/json/v2的到来，我们可以期待Go语言在数据序列化领域会有更出色的表现。这不仅将提升json编解码效率，还将为构建更加健壮和灵活的基于json的Go应用程序铺平了道路。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

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

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论