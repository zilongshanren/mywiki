---
title: Go 1.25规范大扫除：移除“Core Types”，为更灵活的泛型铺路
url: https://tonybai.com/2025/03/27/remove-coretypes-from-go-spec/
published: '2025-03-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.25规范大扫除：移除“Core Types”，为更灵活的泛型铺路

![](../../assets/9d3bdf29d7aec208.jpeg)


[本文永久链接](https://tonybai.com/2025/03/27/remove-coretypes-from-go-spec) – https://tonybai.com/2025/03/27/remove-coretypes-from-go-spec

[Go 1.18引入泛型](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)无疑是Go语言发展史上的一个里程碑，它带来了类型参数、类型约束等强大的新特性。伴随这些特性，一个名为“核心类型”（Core Type）的抽象概念也被引入，旨在简化泛型初期的规范定义和编译器实现。

然而，随着社区对泛型理解的深入和实践的积累，“核心类型”带来的复杂性和局限性也逐渐显现。近日，Go团队在[提案#70128](https://go.dev/issue/70128)中正式决定，并已在开发分支中实施：将在即将到来的[Go 1.25版本](https://github.com/golang/go/milestone/364)（预计2025年8月发布）中，从[Go语言规范](https://go.dev/ref/spec)中移除“核心类型”这一概念。这项看似底层的改动，实则对Go语言的简洁性、易学性以及未来发展具有深远意义。

## “核心类型”：泛型时代的权宜之计

在Go 1.18设计泛型时，为了快速有效地更新语言规范以适应类型参数，Go团队引入了“核心类型”。这里对当前版本Go规范中对Core Types的说明进行了截图如下：

![](../../assets/ef56db3ea595c9e8.png)


Core Types概念的理解还是有门槛的，但结合泛型类型参数一起，简单来说就是：

- 对于非类型参数的类型，其核心类型就是其
[底层类型](https://go.dev/ref/spec/#Underlying_types)。 - 对于类型参数，其核心类型是其类型集（Type Set）中所有类型共同拥有的**唯一*底层类型。如果类型集中类型的底层类型不唯一，则该类型参数没有核心类型。

例如，下面约束类型的核心类型是[]int：

```
interface{ ~[]int }
```


但对于下面约束类型Constraint：

```
type Constraint interface {
~[]byte | ~string
Hash() uint64
}
```


由于其包含[]byte和string两种不同的底层类型，它便没有核心类型。

这种设计在当时起到了“快捷方式”的作用，许多原先依赖“底层类型”的规范规则被直接替换为依赖“核心类型”。这在一定程度上简化了泛型引入初期的工作量。

## “权宜之计”带来的困扰

然而，“核心类型”作为一个抽象且有特定规则（尤其对channel、append、copy等有复杂调整）的概念，逐渐暴露出一些问题：

**过度限制:**基于核心类型的规则往往比基于类型集的规则更严格。例如，根据[Go 1.24的规范](https://tonybai.com/2025/02/16/some-changes-in-go-1-24/)，对类型参数为P Constraint (上文定义的Constraint) 的变量进行切片操作 (s[i:j]) 是不允许的，因为Constraint没有核心类型，即使切片操作对[]byte和string本身都是合法的。**增加认知负担:**开发者，尤其是初学者，在理解某些非泛型代码相关的规范（如切片表达式）时，也不得不去理解“核心类型”这个泛型相关的概念，增加了学习曲线。**规则不一致感:**像索引(a[x])、len、cap等操作的规则是基于类型集设计的（检查操作对类型集中所有类型是否有效），这使得它们看起来像是语言规则中的“特例”，而基于核心类型的规则反倒成了“常态”。**阻碍未来发展:**“核心类型”的存在，使得一些本可以自然推广到泛型的特性难以落地。例如，提案[#48522](https://go.dev/issue/48522)设想允许访问类型集中所有结构体都共享的字段 (x.f)，但在核心类型的框架下显得格格不入。类似的，它也限制了更灵活的切片操作和[类型推断改进](https://go.dev/issue/69153)的可能性。

## Go 1.25的变革：回归清晰，拥抱未来

为了解决上述问题，Go 1.25选择了“移除核心类型”这条路径。具体的做法并非引入破坏性变更，而是：

- 重写规范描述

将语言规范中所有依赖“核心类型”的地方，改用更明确、独立的语言来描述：对于涉及**非泛型**操作数的规则，回归到Go 1.18之前的、基于具体类型（如数组、切片、字符串、通道等）的描述方式。而对于涉及**泛型**操作数（类型为类型参数）的规则，添加专门的段落，清晰地阐述该操作在这种情况下需要满足的条件（通常是基于类型集的要求）。

- 移除核心类型章节

从规范中彻底删除关于核心类型的定义和解释。

例如，内置函数close的规范描述，在Go 1.18后是：

For an argument ch with

core typethat is a channel…

而在 Go 1.25 中将回归到更简洁直观的形式（类似 Go 1.18 之前），并为泛型情况添加说明：

For a channel ch, the built-in function close(ch)…

If the type of the argument to close is a type parameter all types in its type set must be channels with the same element type. It is an error if any of those channels is a receive-only channel.


关键在于，这次变更旨在清理和简化规范，本身并不改变任何现有Go代码的行为，保证了100%的向后兼容性。同时，编译器输出的错误信息也将更新，不再提及令人困惑的“核心类型”，并有望在某些场景下提供更具体、指向性更强的错误提示。

## 对开发者的意义与未来展望

移除“核心类型”对 Go 开发者而言，短期和长期都带来了积极影响：

- 更简洁的规范: Go 语言规范变得更加清晰、易于理解和学习，降低了心智负担。
- 清晰的边界: 非泛型代码的行为可以独立于泛型概念来理解，逻辑更自洽。
- 铺平道路: 这是最重要的一点。通过移除核心类型这个历史包袱和限制性框架，为未来Go语言在泛型领域引入更灵活、更强大的特性打开了大门。这包括：更灵活的泛型操作（如
[#48522](https://go.dev/issue/48522)提到的共享字段访问）、更强大的切片操作能力以及改进类型推断（如解决[#69153](https://go.dev/issue/69153)中的某些场景）。

值得注意的是，最初的讨论中曾考虑过伴随此次变更放宽一些语言规则（例如range对某些混合类型集的支持），但考虑到对现有工具链（如x/tools/ssa, vet分析器）的潜在影响以及某些场景下语义的复杂性（如range对[]byte和string的不同行为），Go团队最终决定本次Go 1.25的变更仅限于规范文本的清理和概念移除。这意味着，那些令人期待的语言灵活性提升，将作为独立的提案在未来版本中逐步引入。

## 小结

Go 1.25移除“核心类型”是一次重要的“技术债务”清理，它简化了语言规范，降低了开发者的学习成本，并且最关键的是，为Go 泛型的未来演进扫清了障碍。虽然它不直接改变现有代码的行为，但其长远影响值得每一位 Go 开发者关注。让我们期待一个规范更清晰、未来可能性更广阔的Go语言！

## 参考资料

[Go语言规范](https://go.dev/ref/spec)– https://go.dev/ref/spec[Goodbye core types – Hello Go as we know and love it!](https://go.dev/blog/coretypes)– https://go.dev/blog/coretypes[spec: remove notion of core types](https://github.com/golang/go/issues/70128)– https://github.com/golang/go/issues/70128

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

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