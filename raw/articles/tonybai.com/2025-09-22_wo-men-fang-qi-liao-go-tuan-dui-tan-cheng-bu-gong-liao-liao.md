---
title: “我们放弃了”——Go 团队坦诚布公，聊聊那些可能永远不会加入 Go 的功能
url: https://tonybai.com/2025/09/22/go-team-gave-up-on-features/
published: '2025-09-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “我们放弃了”——Go 团队坦诚布公，聊聊那些可能永远不会加入 Go 的功能

![](../../assets/2561def889d3daa6.png)


[本文永久链接](https://tonybai.com/2025/09/22/go-team-gave-up-on-features) – https://tonybai.com/2025/09/22/go-team-gave-up-on-features

大家好，我是Tony Bai。

在 GopherCon Europe 2025 的 Go 团队座谈会上，[Michael Stapelberg(负责go protobuf)](https://github.com/stapelberg)、[Damien Neil(负责Go安全相关)](https://github.com/neild)、[Michael Pratt(负责Go运行时和Go性能相关)](https://github.com/prattmic) 和 [Jonathan Amsterdam(log/slog作者，负责Go工具相关)](https://github.com/jba) 四位核心成员与社区进行了[一场坦诚的对话](https://www.youtube.com/watch?v=etl1Z8T4B9g)。他们不仅分享了诸如[官方 MCP SDK](https://tonybai.com/2025/07/10/mcp-official-go-sdk)、[“裸金属”Go](https://tonybai.com/2025/05/13/goos-none-proposal) 等激动人心的进展，更以一种罕见的坦率，正面回应了社区长期以来关心的多个“老大难”问题——包括不可变类型、泛型错误处理和非 nil 指针。其中最引人注目的一句“我们放弃了”，几乎为 Go 语言在某些方向上的演进画上了句号。

![](../BlogImages/2025/go-team-gave-up-on-features-2.png)


本文将带你深入这场座谈会的核心内容，一探 Go 语言的现在与未来。

![](../../assets/f3973191ef9d6abe.png)


## 语言设计的哲学——“不做什么”比“做什么”更重要

座谈会最精彩的部分，莫过于对多个长期存在的语言功能提案的讨论。Go 团队的态度清晰而一致：**为了维护 Go 的核心价值——简洁性和易读性，他们愿意对许多看似“美好”的功能说“不”。**

### 不可变数据类型 (immutable)

**社区的期待**：为 Go 增加类似 immut和const(修饰变量的) 的关键字，以增强代码的安全性和可预测性。**团队的困境**：Michael Pratt 承认，这是“**可能做的最好的事情之一**”，但他紧接着说，“**我们不知道该如何实现它**”。内部曾有多个提案，但都未成功。核心问题在于，任何这类功能都会像病毒一样在代码库中蔓延，迫使所有 API 都需要考虑 const 和非 const 两种版本，这与 Go 的设计哲学背道而驰。**结论**：在社区提出一个绝佳的、能保持语言简洁性的提案之前，官方不会主动推进。

### 泛型错误处理 (减少 if err != nil)

**社区的期待**：引入 try/check 等机制，减少错误处理的冗余代码。**团队的“投降”**：在经过长达数年的思考和无数次讨论后，Go团队给出了一个[爆炸性的结论](https://tonybai.com/2025/06/04/error-syntax)：“**我们放弃了 (we give up)。**” 团队承认，他们找不到任何一种能让所有人都满意的、既能减少冗余又不损失清晰性的方法。**新的焦点**：这一“投降”反而让团队感到“极度兴奋”。因为它意味着可以停止在“冗余”这个问题上内耗，转而思考其他更重要的错误处理问题。Damien 明确指出，**如何在错误中加入堆栈跟踪**才是当前错误处理最大的痛点，也是团队更愿意投入精力去探索的方向。

### 非 Nil 指针 (non-nil)

**社区的期待**：通过语言机制在编译期防止 nil 指针解引用。**团队的权衡**：Jonathan Amsterdam 解释道，虽然非 nil 指针很好，但它会引入两种指针类型，让一切都变成两倍。或者需要引入复杂的流式类型分析，这会使代码更难阅读和理解。**一个反直觉的洞见**：“**Nil 指针错误是最好的运行时错误**”，因为它有确定性的堆栈跟踪，易于定位。团队更关心那些非确定性的、只在生产环境中出现的并发 bug，比如 goroutine 泄漏。

### 枚举 (enum)

**社区的期待**：提供比 iota 更强大、更类型安全的枚举支持。**团队的困惑**：Damien 指出，社区对 enum 的需求至少有两种截然不同的解读：一种是“整数的枚举”，另一种是“类型的枚举”（即代数数据类型），两者差异巨大。在社区就“到底想要什么”达成共识之前，团队很难推进。

## 标准库的“新陈代谢”——演进、维护与“瘦身”

标准库是 Go 生态的基石，但随着时间的推移，一些包也显现出历史的痕迹。

### 哪些包应该被“移除”？

团队成员们“点名”了一些他们认为设计不佳或已不再主流的包：

- text/tabwriter: Damien 认为其设计不佳，如果现在重来，会做一个 v2 版本。
**运行时的诊断(diagnostic) API**: Michael Pratt 认为现有的 API “有点陈旧，难以使用”，希望能有更好的 API，但不确定是否值得为此做一个 v2。- net/rpc: 被 gRPC 全面超越。
- expvar: 非常小众，很少有人使用。
- syscall: 正在被 golang.org/x/sys 逐步取代，以实现更灵活的更新。
- net/mail, syslog: 社区已经有了功能更强大、更受青睐的替代方案，标准库的实现已沦为“鸡肋”。

虽然因为 Go 1 的兼容性承诺无法真正移除它们，但团队的态度表明，未来的发展重心将不会在这些包上。

### 拥抱 v2，但极其审慎

[json/v2](https://tonybai.com/2025/05/15/go-json-v2/) 和 math/rand/v2 的出现，标志着 Go 团队愿意为那些存在根本性设计缺陷的包创建 v2 版本。但团队强调，这是一个**极为例外**的手段，只有在“**现有 API 框架内无法做出改进**”时才会考虑，因为 v2 会带来生态的分裂和迁移成本。

## Go 在新时代的定位与机遇

面对 AI、裸金属(bare metal)等新兴领域，Go 将如何定位自己？

### Go 在 AI 与数据科学领域的角色

**清晰的边界**：Go 团队不会去开发一个与 LangChain 或 Genkit 竞争的官方 AI 框架，也不会深入数值计算（社区的 gonum 已经很出色）。**专注“生产化” (Productionization)**：团队认为，Go 的核心优势在于将 Python 中训练和设计的模型，**部署到高性能、高并发的生产环境中**。这是 Go 想要“拥有”的领域。Jonathan Amsterdam 更是直言：“你用 numpy 把东西搭起来，但你不会想用 Python 把它部署到生产环境。这时候你就该用 Go 了。”**提供核心 SDK 支持**：团队将致力于为重要的 AI 规范和平台（如 MCP, Gemini, Genkit）提供[高质量的官方 Go SDK](https://tonybai.com/2025/07/10/mcp-official-go-sdk/)。

### “裸金属” Go (Bare metal Go)

**进展**：Michael Pratt 确认，[一项由 Tamago 项目推动的新提案正在讨论中](https://tonybai.com/2025/05/13/goos-none-proposal)，旨在为 Go 运行时提供一个更稳定的内部 API，使其能更好地与底层系统交互。**价值**：这将使 Go 在嵌入式、unikernel 等领域的应用变得更加容易，并且其设计是通用的，不局限于特定 CPU 架构。

## 激动人心的地平线——运行时与工具链的前沿探索

座谈会也透露了几个正在进行中的、令人兴奋的底层项目：

**官方 MCP SDK**：Jonathan Amsterdam 确认，官方的[Go MCP SDK](https://github.com/modelcontextprotocol/go-sdk)随时可能发布正式版，它吸取了社区现有实现的经验，设计更清晰，旨在成为官方标准。**Green Tea GC**：Michael Pratt 提到，Michael Knyszek 正在进行一项名为“Green Tea”的 GC 改进提案，旨在提升 GC 在超多核（如 256 核）机器上的**可扩展性和局部性 (locality)**，以应对现代服务器硬件的发展。**Goroutine 泄漏检测**：团队正在与 Uber 的工程师合作，计划将一项[利用 GC 来动态检测部分死锁（即 goroutine 泄漏）的技术](https://tonybai.com/2025/07/24/deadlock-detection-by-gc)引入 Go。这项技术能找出那些“永远等待”在一个无人能触及的 channel 上的 goroutine，并将其报告出来。**WASM 的原生 GC 集成**：团队希望未来能让 Go 编译的 WebAssembly 使用宿主环境（如浏览器）的原生 GC，但这面临着 Go 严重依赖“内部指针”（interior pointers）而 WASM GC 不支持的巨大技术挑战。**结构体对齐优化**：David Chase 正在推动一个“个人激情项目”，目标是让编译器**自动优化结构体字段的顺序**，以减少内存空洞和提高空间效率。未来开发者将不再需要手动调整字段顺序。相关的提示功能已在 gopls 中提供。

## 开发者的日常——工具、协作与社区

座谈会的最后，团队成员分享了他们作为开发者的工作日常和对社区的看法。

**AI 工具的使用**：团队成员普遍开始使用 LLM。Jonathan Amsterdam 发现它是学习 OAUTH2 这类复杂规范的“极有耐心的老师”；Michael Stapelberg 则用它来学习 NixOS。Damien 更是认为 LLM 在处理 Go 代码时表现出色，因为 Go 的简洁性和向后兼容性为模型提供了高质量的训练数据。**编辑器之争**：Michael Stapelberg 坦诚自己已从 Vim 叛逃至 Emacs，引发了现场的善意哄笑。**对 Go 社区的信心**：当被问及“如果 Google 不再支持 Go，社区能否接手”时，团队成员们毫不犹豫地表示肯定。他们认为 Go 社区非常强大且自给自足，拥有大量非 Google 的核心贡献者（并以 Filippo Valsorda 为例），社区的繁荣并不完全依赖于 Google。

## 拾遗——关于性能、安全与其他语言的思考

除了上述重大议题，座谈会还触及了许多开发者关心的具体问题，这些简短的问答同样充满了来自 Go 团队的深刻洞见。

### Go 与 Rust：灵感的源泉

当被问及对 Rust 等其他语言的看法时，团队表现出开放和欣赏的态度。

**并发安全**：Jonathan Amsterdam 坦言，Rust 提供的并发安全模型是他们“都希望在 Go 中拥有”的东西，因为它能极大地提升程序的可靠性。但他同时指出，在不让 Go 变得像 Rust 一样复杂的前提下，目前还没有找到实现路径。**不同的演进道路**：团队也关注 OCaml 在并发安全上的探索。Jane Street 采用了一种与 Rust 完全不同的方法来实现并发安全，这表明解决同一问题可以有多条路径，Go 也在持续观察和学习。

### 性能：一个“双峰分布”的社区

Michael Pratt 对 Go 的性能有一个有趣的观察，他认为社区对此的感受呈现“双峰分布”：

**一端是极其满意的用户**：他们可能从 Python 等动态语言迁移而来，享受到了数十倍的性能提升，对现状非常满意。**另一端是要求极致性能的用户**：大厂在海量部署下，对性能的渴求永无止境，任何微小的优化都能带来巨大的成本节约。

Go 团队的性能优化工作，主要聚焦于服务后一类用户，例如 json/v2、[新的 map 实现](https://tonybai.com/2024/11/14/go-map-use-swiss-table)以及 [Green Tea GC](https://tonybai.com/2025/05/03/go-green-tea-garbage-collector/)。

### 安全：API 优于“模式开关”

对于“能否为 Go 增加一个‘高安全模式’开关”的问题，团队更倾向于通过**改进 API** 来解决安全问题。

- **Damien ** 提到，一个可能的方向是为 net/http 包增加一个“高安全服务器”标志，该标志将启用一系列更安全的默认配置（例如，更严格的超时），以修正十年前设定的一些已过时的默认值。
**Michael Stapelberg**补充道，Go 已经提供了像 os.ReadDirFS 这样更安全的路径遍历 API，并且 Go 程序与 Seccomp、Landlock 等 Linux 沙箱技术能很好地集成。从 API 和系统层面入手，是比引入一个全局的、模糊的“安全模式”更精细、更合理的做法。

### io_uring：令人兴奋但为时过早

对于 Linux 下备受瞩的 io_uring，Michael Stapelberg 表达了谨慎的乐观。他承认 io_uring 性能惊人，但其复杂的 API 和过去暴露出的**严重安全问题**，使得 Google 内部服务器完全禁用了该功能。他认为，在它变得更成熟、更安全之前，[考虑将其大规模引入 Go 还为时过早](https://tonybai.com/2025/08/11/why-go-not-embrace-iouring)。此外，Michael Pratt 补充说，Go 的运行时和调度器已经通过 goroutine 隐藏了大部分 I/O 异步的复杂性，因此 io_uring 能带来的部分核心优势，Go 已经通过不同的方式实现了。

### Go 作为 DevOps 脚本语言

当被问及 Go 能否取代 Python 成为 DevOps 脚本语言时，团队成员们几乎异口同声地表示：**“在 Google 内部，这已经发生了。”** Michael Stapelberg 分享说，他自己现在会避免编写任何中等复杂度的 shell 脚本，而是直接从 Go 开始，因为 Go 的强类型和工程化能力，能避免脚本在变复杂后迅速变得难以维护。

## 小结：一个务实、专注且充满活力的 Go

这场座谈会向我们展示了一个成熟、务实的 Go 团队。他们不再试图让 Go 成为解决所有问题的“瑞士军刀”，而是更加专注于其核心优势：**简洁性、高性能、以及在构建大规模、高可靠性生产系统方面的卓越能力。**

他们愿意为了保持语言的长期健康而对一些“美好”的功能说“不”，也乐于承认在某些领域的探索（如错误处理冗余）已经走到了尽头。但与此同时，他们也在积极地拥抱新的机遇（如 AI 生产化），并从底层（GC、运行时）不断地进行着深刻的、影响深远的优化。

正如 Michael Stapelberg 所言，Go 社区是如此强大和自给自足，以至于团队的参与有时并非决定性的。这或许是对 Go 这门语言及其社区生态成熟度的最高赞誉。

视频链接：https://www.youtube.com/watch?v=etl1Z8T4B9g

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