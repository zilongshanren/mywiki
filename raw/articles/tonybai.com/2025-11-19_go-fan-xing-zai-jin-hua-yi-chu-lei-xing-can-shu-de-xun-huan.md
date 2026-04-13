---
title: Go 泛型再进化：移除类型参数的循环引用限制
url: https://tonybai.com/2025/11/19/proposal-remove-cycle-restriction-for-type-parameters/
published: '2025-11-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 泛型再进化：移除类型参数的循环引用限制

![](../../assets/64d0002441e53af1.png)


[本文永久链接](https://tonybai.com/2025/11/19/proposal-remove-cycle-restriction-for-type-parameters) – https://tonybai.com/2025/11/19/proposal-remove-cycle-restriction-for-type-parameters

大家好，我是Tony Bai。

自 Go 1.18 引入泛型以来，Gopher 们一直在探索其能力的边界。然而，在这片新大陆上，一直存在着一个由语言规范施加的限制，它禁止了一种强大而富有表达力的泛型模式的实现。

这个限制就是：“**在一个泛型类型 T 的类型参数列表中，其约束不能直接或间接地引用 T 自身。**”

![](../../assets/78f4f1a8e96b8444.png)


近日，由 Go 核心团队的 Robert Griesemer 亲自发起的一个关联提案（[NO.75883](https://github.com/golang/go/issues/75883)），旨在移除这个约束。在经过一系列的编译器修复和深度讨论后，最终被标记为 **likely accept**。这意味着，Go 语言规范中关于泛型“类型参数循环引用”的这条限制，即将在未来的版本中(最早Go 1.26)被正式**移除**。

这次微小的语法调整，将为 Go 社区解锁一种被称为“奇异递归模板模式” (Curiously Recurring Template Pattern, CRTP) 的强大能力，并对我们如何设计类型安全的泛型 API 产生深远影响。

在这篇文章中，我们将深入探讨这一重要变化，剖析其背后的技术原理、核心应用场景等。

![](../../assets/15cd5c3c070e1425.png)


## 被束缚的表达力——这条限制是什么？

让我们从一个 Griesemer 提出的、看似合理的代码开始，它在当前版本(比如Go 1.25.4)的 Go 中是**非法**的：

```
// 目标：定义一个“可比较”的元素接口
// E 应该是一个实现了 Element[E] 接口的类型
type Element[E Element[E]] interface {
Less(other E) bool
}
// 编译器报错：invalid recursive type: Element refers to itself
// (无效的递归类型)
```


这段代码的**意图**非常清晰：我们想定义一个 Element 接口，它有一个 Less 方法，该方法接收的参数 other，其类型 E 必须和实现这个接口的类型**是同一个类型**。这是一种“自引用”或“递归”的类型约束。

例如，如果我们有一个 Int 类型：

```
type Int int
// 我们希望 Less 的参数是 Int，而不是其他实现了 Element 接口的类型
func (i Int) Less(other Int) bool {
return i < other
}
```


Element[E Element[E]] 这种约束，正是为了在编译期强制执行这种“同类型比较”的保证。

然而，由于 Go 1.18 规范中的明确限制，这种优雅的、类型安全的表达方式，在过去几年中一直是一条死路。

## 为何需要它？—— CRTP 模式的威力

社区的讨论为我们揭示了这种“循环类型约束”的几个核心应用场景。它们都与 C++ 中的 CRTP(Curiously Recurring Template Pattern) 模式异曲同工。

Robert Griesemer 在提案中给出了一个经典的例子：如何用泛型来模拟一个数学上的“环”(Ring)。

```
// 未来将合法的代码
type Ring[T Ring[T]] interface {
Zero() T
One() T
Add(y T) T
Mul(y T) T
}
```


Ring[T Ring[T]] 这个约束，确保了 Add 和 Mul 等方法的参数和返回值，永远是实现该接口的具体类型 T，而不是某个其他也实现了 Ring 接口的无关类型。**它在编译期就锁定了操作的类型闭环**。

Prometheus 的开发者 Bryan Boreham 在 GopherCon 2023 的演讲中，也遇到了同样的问题。在实现一个通用的 K-路归并树时，他希望定义一个通用的 Value 接口，让放入树的元素**自带**类型安全的 Less 方法，而不是依赖外部传入的闭包。这不仅能让 API 更简洁，更重要的是，直接的方法调用比闭包调用**更容易被编译器内联**，从而带来显著的性能提升。

## 从“不可能”到“可能”——幕后的编译器修复

这个看似简单的语法限制，为何在 Go 1.18 中被加入，又为何现在可以被移除了？

答案隐藏在编译器的**类型检查**和**循环检测**机制中。在早期，Go 的类型检查器为了防止无限递归（例如 type T T），采用了一套相对保守的循环检测算法。当它遇到 type T[P T[P]] 这种通过类型参数列表形成的“循环依赖”时，会直接将其误判为非法的无限递归。

在 [NO.68162 issue](https://github.com/golang/go/issues/68162)的修复中，Go 团队改进了类型检查器的算法。新的算法能够更智能地区分**有害的无限递归**（如 type T *T）和**无害的、可以在实例化时“展开”的泛型递归约束**。

## 深度剖析——Griesemer 的“两步实例化”解释

在 #75883 提案的讨论中，一个极其深刻的问题被提出：type T[P T[P]] int 这样的定义，是否会导致无法解决的循环？Robert Griesemer 对此给出了一个权威的、清晰的解释，揭示了 Go 泛型实例化的核心机制。

他指出，Go 的泛型实例化，严格遵循**两个步骤**：

-
**第一步：类型替换 (Substitution)**

编译器首先会简单地、机械地将调用方提供的**类型实参 (type argument)**（例如 int），替换掉泛型定义中的**类型形参 (type parameter)**（例如 P）。`// 原始定义 type T[P T[P]] int // 假设我们尝试实例化 T[int] // 第一步替换后，我们得到一个临时的、假想的定义： type T[int T[int]] int`

-
**第二步：约束校验 (Verification)**

在替换完成后，编译器才会去检查：**被替换的类型实参 (int)，是否满足它所对应的类型形参的约束 (T[int])？**在这个例子中，约束 T[int] 是一个

**具名非接口类型**。根据 Go 的类型规则，只有 T[int] 自身才满足这个约束。而我们传入的 int 显然不是 T[int]。因此，**约束校验失败**，T[int] 是一次非法的实例化。

这个“两步走”的过程，清晰地证明了**这种递归约束并不会导致无限循环**，因为类型检查总能在有限的步骤内终止。正是基于这个坚实的理论基础，Go 团队才有信心去移除最初的限制。

## 一个完整的带有循环引用的类型参数的示例

让我们将 Griesemer 提出的 Ring 示例，扩展为一个完整的、在未来版本的 Go 中将可以运行的程序：

```
package main
import "fmt"
// 1. 定义一个递归约束的泛型接口
type Ring[T Ring[T]] interface {
Zero() T
One() T
Add(y T) T
Mul(y T) T
}
// 2. 实现该接口的具体类型
type MyInt int
func (x MyInt) Zero() MyInt { return 0 }
func (x MyInt) One() MyInt { return 1 }
func (x MyInt) Add(y MyInt) MyInt { return x + y }
func (x MyInt) Mul(y MyInt) MyInt { return x * y }
// 3. 编写一个操作该泛型接口的通用算法
// scale computes x + y*s
func scale[R Ring[R]](x, y, s R) R {
return x.Add(y.Mul(s))
}
func main() {
var a, b, c MyInt = 2, 3, 5
// 4. 调用通用算法，编译器会检查 MyInt 是否满足 Ring[MyInt] 约束
result := scale(a, b, c)
fmt.Printf("scale(2, 3, 5) = %d\n", result) // 预期输出: scale(2, 3, 5) = 17
}
```


让我们剖析一下scale 调用时的实例化过程：

main 函数中对 scale(a, b, c) 的调用，完美地展示了“两步实例化”机制是如何工作的：

-
**第一步：类型推断与替换 (Type Inference & Substitution)**- 编译器观察到 scale 函数的调用参数 a, b, c 的类型都是 MyInt。
- 通过类型推断，编译器确定类型实参 (type argument) 就是 MyInt。
- 它将 MyInt 替换掉 scale 函数签名中的类型形参 (type parameter) R。
- 此时，scale 函数的约束被临时实例化为 Ring[MyInt]。

-
**第二步：约束校验 (Verification)**- 现在，编译器需要校验：
**类型实参 MyInt 是否满足其约束 Ring[MyInt]？** - 要满足 Ring[MyInt]，MyInt 必须实现 Ring[MyInt] 接口中定义的所有方法。让我们来逐一检查：
- Zero() MyInt：MyInt 实现了 Zero() MyInt。
**满足。** - One() MyInt：MyInt 实现了 One() MyInt。
**满足。** - Add(y MyInt) MyInt：MyInt 实现了 Add(y MyInt) MyInt。
**满足。** - Mul(y MyInt) MyInt：MyInt 实现了 Mul(y MyInt) MyInt。
**满足。**

- Zero() MyInt：MyInt 实现了 Zero() MyInt。
- 由于 MyInt 完整地实现了 Ring[MyInt] 接口，约束校验
**通过**。 - 编译器确认此次泛型函数调用是合法的，并生成相应的代码。

- 现在，编译器需要校验：

这个过程与我们在第四章中看到的那个**非法**的 T[P T[P]] int 示例形成了鲜明对比。在这里，MyInt 是一个接口实现者，它能够满足由其自身参与定义的接口约束，从而构成了一个**有效的、有穷的递归**。

## 小结：Go 泛型的一次重要进化

移除泛型类型参数的循环引用限制，对于 Go 语言而言，远不止是修复了一个编译器 bug 或减少了一条规则。

**对开发者而言**：它解锁了一种全新的、更强大、更类型安全的泛型编程模式。我们将能够构建出表达力更强、性能更高、API 更简洁的通用库和数据结构。**对语言本身而言**：这是 Go 泛型走向成熟的一次重要进化。它表明 Go 团队正在持续地、审慎地打磨泛型这一新特性，使其在保持 Go 哲学的基础上，逐步释放其全部潜能。

不过，CRTP 模式对于不熟悉的开发者来说，**也确实存在一定的认知门槛**。

目前，该cl已经合并到主线，大家可以在go playground的go dev branch版本下体验。

资料链接：https://github.com/golang/go/issues/75883

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论