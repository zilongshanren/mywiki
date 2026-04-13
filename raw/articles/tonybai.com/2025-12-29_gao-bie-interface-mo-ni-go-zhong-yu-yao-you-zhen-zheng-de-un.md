---
title: 告别 interface{} 模拟，Go 终于要有真正的 Union 类型了？
url: https://tonybai.com/2025/12/29/go-community-new-sum-type-end-interface-union-types/
published: '2025-12-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 告别 interface{} 模拟，Go 终于要有真正的 Union 类型了？

![](../../assets/0a3e56b6d1ff6ec4.png)


[本文永久链接](https://tonybai.com/2025/12/29/go-community-new-sum-type-end-interface-union-types) – https://tonybai.com/2025/12/29/go-community-new-sum-type-end-interface-union-types

大家好，我是Tony Bai。

“Go 什么时候支持枚举？”


“Go 什么时候有真正的联合类型？”

这可能是 Go 语言诞生以来，被问得最多的问题之一。现有的解决方案——无论是用 const 模拟枚举，还是用 interface{} 配合类型断言模拟联合类型——在类型安全、表达力和穷尽性检查上，都总让人感觉“差了那么一点意思”。

近日，Go 核心团队成员 [neild](https://github.com/neild) 在 GitHub 上发起了一个[非正式的讨论 (#76920)](https://github.com/golang/go/issues/76920)，抛出了一种全新的、**非接口 (non-interface)** 的联合类型设计构想。这个构想虽然只是一个“思想实验”，却迅速引爆了社区的热情，成为了近期最热门的话题之一。

本文将带你深入这场讨论的核心，看看这个名为 union 的新类型，究竟有何魔力。

![](../../assets/9363dc5447a22f65.png)


## 核心痛点：为什么我们需要 Sum Types？

在深入设计之前，让我们先回顾一下，为什么我们如此渴望这个特性。neild 列举了三个极具代表性的场景：

**Direction 类型 (Enum)**：一个类型只能是 North, South, East, West 四者之一。**Option/Maybe (Sum Type)**：一个类型要么包含一个值 T，要么什么都没有（None）。**IP 地址 (Variant)**：一个类型要么是 IPv4 ([4]byte)，要么是 IPv6 ([16]byte)。

目前，我们通常使用 interface 来模拟这些场景。但 neild 指出，**接口并不是最佳方案**：

**零值问题**：接口的零值是 nil。这迫使我们必须处理一个额外的、可能毫无意义的 nil 状态，这在很多时候（如 Direction）是不合理的。**定义繁琐**：你需要为每一个变体定义一个单独的类型，这在变体较多时显得非常啰嗦。**语义混淆**：接口本质上是关于**行为**的抽象，而和类型本质上是关于**数据结构**的定义。强行用接口来表达数据结构，是一种概念上的错位。

## 大胆构想：像定义 Struct 一样定义 Union

neild 提出的方案，不仅巧妙，而且极具 Go 风格。他的核心洞察是：**Struct 是“积类型” (Product Type)，Union 是“和类型” (Sum Type)。既然它们是对偶的，为何不使用相似的语法呢？**

```
// 积类型 (Struct): 同时包含所有字段
type Point struct {
X int
Y int
}
// 和类型 (Union): 包含且仅包含其中一个变体
type Direction union {
North, South, East, West atom
}
type Maybe[T any] union {
Unset atom
Set T
}
type IP union {
IPv4 [4]byte
IPv6 [16]byte
}
```


这里引入了一个新概念：**atom**（也可以叫 unit 或其他名字）。它本质上是 struct{} 的别名，用于表示那些**不携带数据、只代表某种状态**的变体（如 North 或 Unset）。

这种设计的美妙之处在于：

**语法一致性**：它看起来就像我们熟悉的结构体，只是关键字变成了 union。**明确的零值**：Union 的零值就是其**第一个变体**的零值。例如 Direction 的零值就是 North，IP 的零值就是 IPv4{0,0,0,0}。没有额外的 nil 状态！**内聚性**：所有变体都定义在同一个类型内部，不需要像接口那样定义一堆散落的类型。

## 使用体验：类型安全与穷尽性检查

这个设计不仅在定义上优雅，在使用上也力求符合 Go 的直觉。

### 构造与赋值

你可以像使用结构体字面量一样构造 Union，但**只能指定一个键**：

```
d := Direction{North: atom{}} // 或者简化为 d := Direction.North
m := Maybe[int]{Set: 42}
```


### 访问与判断

对于 atom 类型的变体，访问它返回一个布尔值；对于携带数据的变体，访问它返回数据和布尔值（类似 map 的查找）：

```
if d.North {
fmt.Println("Heading North")
}
if v, ok := m.Set; ok {
fmt.Println("Value is:", v)
}
```


### Union Switch：杀手级特性

这是 Sum Types 最强大的地方——**穷尽性检查**。

```
switch d.(union) {
case North:
// ...
case South:
// ...
// 如果漏掉了 East 或 West，编译器会报错！
}
```


这种编译期的保障，彻底消除了“忘记处理某种情况”的 Bug 来源，是构建健壮系统的基石。

## 社区激辩：细节中的魔鬼

虽然大方向得到了广泛认可，但在具体细节上，社区展开了激烈的讨论。

### struct{} 的特殊待遇

neild 提议对 atom (即 struct{}) 进行特殊处理，使其可以直接作为值使用（如 Direction.North）。但这引起了 ianlancetaylor 等人的担忧：这种特殊规则是否会增加语言的复杂性和不一致性？如果不特殊处理，写 Direction{North: struct{}{}} 又实在太啰嗦了。

### 命名之争：atom vs unit vs iota

atom 这个名字是否合适？有人建议使用 null，有人建议复用 iota，还有人建议直接允许 union { North, South } 这种省略类型的语法。这再次证明了，“命名”永远是计算机科学中最难的问题之一。

### 与泛型的纠葛

如果 Union 是泛型的，如何处理？Maybe[T] 是一个完美的例子。但如果 T 本身也是一个 Union 呢？嵌套的 Union 及其 Switch 语句该如何设计？这些都是需要深思熟虑的边缘情况。

## 小结：Go 语言演进的新曙光？

尽管 #76920 目前只是一个“讨论”，并非正式提案，但它释放了一个强烈的信号：**Go 团队也许正在认真思考如何以一种“地道”的方式引入和类型(Sum Type)。**

这个设计方案，在保持 Go 语言简单性的同时，极大地增强了其表达力和安全性。它避开了接口的动态性陷阱，提供了一种静态的、高效的、内存布局可控的数据结构。

如果这个构想最终能成真，它将填补 Go 语言类型系统中最后一块重要的拼图，让我们彻底告别用 iota 和 interface{} 拼凑枚举与联合类型的日子。

资料链接：https://github.com/golang/go/issues/76920

**你的态度是？**

对于这个打破常规的 union 语法设计，你是感到**兴奋**，觉得它终于填补了 Go 的拼图？还是感到**担忧**，觉得它让 Go 变复杂了？

**如果给你一张选票，你会支持这个提案落地吗？**

**欢迎在评论区投出你的一票，并分享你的理由！** 让我们一起见证 Go 语言的演进。

**如果这篇文章让你对 Go 的未来有了新的期待，别忘了点个【赞】和【在看】，并分享给身边的 Gopher 朋友！**

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论