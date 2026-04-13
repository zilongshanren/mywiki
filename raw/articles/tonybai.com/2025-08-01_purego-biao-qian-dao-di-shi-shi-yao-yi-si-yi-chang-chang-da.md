---
title: purego 标签到底是什么意思？一场长达六年的社区辩论终于有了定论
url: https://tonybai.com/2025/08/01/proposal-purego/
published: '2025-08-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# purego 标签到底是什么意思？一场长达六年的社区辩论终于有了定论

![](../../assets/26c3ef63e0890a62.png)


[本文永久链接](https://tonybai.com/2025/08/01/proposal-purego) – https://tonybai.com/2025/08/01/proposal-purego

大家好，我是Tony Bai。

对于许多 Go 开发者来说，purego 构建标签一直是一个模糊的存在。它到底意味着“没有 Cgo”、“没有 unsafe”，还是“没有汇编”？这个问题的答案在社区中众说纷纭，甚至连标准库中的使用也不尽统一。最近，一项历时六年、编号为[#23172](https://github.com/golang/go/issues/23172) 的提案终于尘埃落定，Go 团队正式**接受 (accepted)** 了关于 purego 含义的共识。本文将带大家一起回顾这场漫长而精彩的社区辩论，深入探讨其背后的技术权衡，并阐明这个小小的标签对于 Go 的跨实现（如 TinyGo）和可移植性生态的深远意义。

## 背景：一个模糊的约定

purego 标签的诞生，源于 Go 生态系统日益增长的多样性。除了官方的 gc 编译器，还涌现出了 GopherJS、TinyGo、gccgo 等多种 Go 实现。在这些非标准环境中，对 unsafe 包的指针操作、Cgo 的支持以及 Go 汇编的兼容性各不相同。

最初，protobuf 等库为了兼容Google App Engine 等不允许 unsafe 的环境，开始使用 safe 标签。这个概念逐渐演变为 purego，但其确切含义从未被正式定义。这导致了混乱：

- 有人认为 purego 意味着
**完全的内存安全**，即禁止 unsafe 包。 - 有人认为它意味着
**纯粹的 Go 代码**，即禁止 cgo 和汇编。 - 还有人认为它应该是一个
**包罗万象的标签**，同时禁止 unsafe、cgo 和汇编。

这种模糊性给库作者和不同 Go 实现的维护者带来了困扰。

## 辩论的焦点：一个标签，多重含义的冲突

提案的讨论过程充满了精彩的技术思辨，核心矛盾在于试图用一个标签来承载多个正交（orthogonal）的概念：

-
**noasm vs. nounsafe vs. nocgo**：来自 TinyGo 团队的开发者明确指出，TinyGo**支持 unsafe 和 cgo，但不支持 Go 汇编**。如果 purego 同时禁止这三者，那么 TinyGo 将被迫禁用它本可以支持的功能。!cgo 标签已经很好地解决了 Cgo 的问题，因此将 cgo 捆绑进来显得多余。 -
**unsafe 的多重“不安全”**：Go 安全负责人 Filippo Valsorda (@FiloSottile) 进一步指出，unsafe 包本身也包含了不同层次的“不安全”：**类型转换**（如 unsafe.String）：通常是可移植的。**linkname**：与运行时实现紧密耦合。**指针运算**：依赖内存布局，是真正的不可移植性的主要来源。

用一个 nounsafe 标签一概而论，过于粗暴，可能会“误伤”许多可移植的 unsafe 用法。

-
**生态现状**：seankhliao 通过 GitHub 搜索发现，社区中 //go:build !purego 与 import “unsafe” 的组合（表示非 purego 版本才使用 unsafe）远多于 //go:build purego 与 import “unsafe” 的组合。这表明，社区的主流用法倾向于将 purego 视为**不使用 unsafe 和汇编**的版本。

## 达成共识：“完美是优秀的敌人”

在长达数年的讨论后，Filippo Valsorda 的一段评论为这场辩论指明了方向，他主张“**不要让完美成为优秀的敌人**”：

**核心用例**：当前最主要的需求来自**TinyGo**和**标准库加密包的通用后备代码测试**，这两者本质上都需要一个“**禁用汇编**”的开关。**现有约定**：purego 已经是社区和标准库中广泛用于禁用汇编的**事实标准**。虽然名字不够理想（noasm 会更清晰），但改变一个已广泛使用的约定的成本太高。**重新界定**：我们应该停止扩大 purego 的定义，回归其最核心、最被需要的用途。

最终，在 aclements 等核心成员的推动下，社区达成了清晰的共识。

## 最终决议：purego 意为“无汇编”

Go 团队最终**接受 (accepted)** 了该提案，并明确了其最终方向：将在 go help buildconstraint 中正式文档化 purego 构建标签的**约定**：

- purego
**主要用于禁用汇编代码**，从而启用纯 Go 的实现作为后备。 - purego 与 cgo
**是正交的**。是否使用 Cgo 应由 cgo 标签控制。 - purego
**不常规地影响 unsafe 包的使用**。可移植的 unsafe 用法是被允许的。

## 对 Go 开发者的影响

这个决议对于 Go 生态系统意义重大：

**为库作者提供了清晰的指导**：当你的库同时包含汇编优化版本和纯 Go 实现版本时，purego 是官方推荐的、用于在两者之间切换的标签。**为 Go 的替代实现铺平了道路**：像 TinyGo 这样的编译器现在可以自信地默认设置 purego 标签，从而无缝地使用标准库和第三方库中提供的纯 Go 后备代码，而不用担心会意外地禁用它们所支持的 unsafe 或 cgo 功能。**提升了测试的便利性**：开发者可以在拥有汇编优化的平台（如 amd64）上，通过 -tags purego 来方便地测试和调试纯 Go 的实现版本。

## 结论

purego 标签的标准化之路，是 Go 社区在实践中不断探索、辩论并最终达成务实共识的又一个经典案例。它表明，一个健康的语言生态不仅需要顶层设计，更需要在真实世界的需求碰撞中，不断澄清和完善其约定。通过为 purego 赋予一个清晰、专注的定义，Go 语言再次为其跨平台、跨实现的承诺，奠定了一块坚实的基石。

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