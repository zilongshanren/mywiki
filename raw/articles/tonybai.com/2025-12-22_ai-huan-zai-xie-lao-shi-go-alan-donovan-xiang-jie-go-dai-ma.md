---
title: AI 还在写“老式 Go”？Alan Donovan 详解 Go 代码的现代化
url: https://tonybai.com/2025/12/22/alan-donovan-go-code-modernization/
published: '2025-12-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# AI 还在写“老式 Go”？Alan Donovan 详解 Go 代码的现代化

![](../../assets/702d1738205004c1.png)


[本文永久链接](https://tonybai.com/2025/12/22/alan-donovan-go-code-modernization) – https://tonybai.com/2025/12/22/alan-donovan-go-code-modernization

大家好，我是Tony Bai。

“Go 承诺了兼容性，但这并不意味着我们应该永远停留在过去。”

在 GopherCon 2025 上，Go 团队核心成员、静态分析工具专家 Alan Donovan 带来了一场题为《[Analysis and Transformation Tools for Go Codebase Modernization](https://www.youtube.com/watch?v=_VePjjjV9JU)》的精彩演讲。

他的分享揭示了一个有趣的现象：**当我们还在为 AI 生成的代码欢呼时，Go 官方团队却发现 AI 正在固化过时的编程模式。** 为了应对这一挑战，官方正在构建一套强大的自动化工具链，帮助我们将代码库带入 Modern Go 的时代。

本文将带你深入这场演讲的核心，揭秘 Go 官方如何通过工具化手段，解决 AI 时代的“代码老化”问题。

![](../../assets/eea4f3d68dbb3fdb.png)


## 为什么要“现代化”？

Go 的兼容性承诺是其成功的基石，但这同时也带来了一个副作用：**旧的代码永远能跑，所以我们很少有动力去更新它。**

然而，随着 Go 版本的迭代，语言和标准库引入了大量旨在提升可读性、性能和安全性的新特性：

![](../../assets/09450b908de0c290.png)


Donovan 展示了一个经典案例：一段传统的、使用了 strings.Split 和三段式 for 循环的代码（如下图）：

![](../../assets/6ee6639dc2e43504.png)


通过引入新特性（迭代器、slices.Contains、range int），这段代码不仅减少了 6 行，还消除了不必要的内存分配，逻辑变得一目了然。新的现代Go代码如下图：

![](../../assets/d88e0114ae076ffb.png)


**现代化的意义，不仅在于代码质量的提升，更在于开发者能力的进化。** 通过工具自动应用这些新模式，开发者能在潜移默化中学习到“更地道”的 Go 写法。

## AI 的局限与工具的使命

Donovan 分享了一个令人深思的实验：他测试了当前最先进的“思考型”大模型，要求它们使用最新的 Go 特性编写代码。

结果令人大跌眼镜：**AI 顽固地坚持使用旧式的写法。**

![](../../assets/4d09370a006ce39a.png)


即使在被明确提示使用新特性后，AI 依然会编造出“这个特性在 1.22 中不可用”等谎言来为自己辩护，或者即使使用了新特性，也经常写出错误的代码。

“AI 是在旧代码的海洋中训练出来的。如果全世界的代码都是旧的，AI 就会永远说着一口‘老式 Go’的方言。”


这揭示了一个深刻的矛盾：**AI 正在固化过时的编程模式。** 打破这个循环的唯一方法，就是大规模地更新现有的代码库，让 AI 学习到新的语料。而这，正是 Go 官方工具链的使命。

## 第一条路径——定制化的 Modernizers

为了解决这个问题，Go 团队基于 go/analysis 框架（也就是 go vet 和 gopls 的底座），开发了一套名为 **Modernizers** 的分析器。

Modernizer 是一个特殊的 Linter，不仅能发现问题，还能提供**自动修复 (Fix)**，并且这个修复必须是**使用新特性**且**绝对安全**的。

![](../../assets/b38fc7a6169c704a.png)


Go 团队已经开发了[约 20 个 Modernizers](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize)，并在 gopls v0.18 中发布。你现在在编辑器中看到的很多“建议修改”，背后就是它在工作。

![](../../assets/930202ce6d7e4178.png)


然而，开发 Modernizer 的过程充满了艰辛。Donovan 以 range int 这个看似简单的重构为例，展示了它在处理变量作用域、副作用顺序时遇到的 4 个极其隐蔽的 Bug。比如下面这个：

![](../../assets/bf798c31101157f5.png)


“直接的语法树操作 (AST manipulation) 极其困难，即使是经验丰富的专家也容易出错。”


Modernizers 虽然好用，但开发成本极高，且只能针对特定特性进行定制，难以作为通用的解决方案。

注：要使用上述modernizer，需要单独运行命令go run golang.org/x/tools/go/analysis/passes/modernize/cmd/modernize@latest -fix ./…。


## 第二条路径——通用的 Auto-Inliner

为了解决 Modernizers 的局限性，赋能社区自己进行现代化改造，Go 团队探索出了一条更通用、更安全的路径：**基于内联 (Inlining) 的“自助式重构”**。

### 核心思想

如果我们想要废弃一个旧函数（如 oldmath.Sub），并引导用户使用新函数，库作者只需要做两件事：

**保留旧函数**，但将其实现修改为直接调用新函数。**添加魔法注释**：//go:fix inline。

![](../../assets/058be166e1bfc461.png)


### 工具的威力

当 gopls 或未来的 go fix 命令看到这个注释时，它会自动将所有调用 oldmath.Sub(a, b) 的地方，安全地替换为 newmath.Sub(b, a)。

注：由于newmath.Sub(b, a)是oldmath.Sub(a,b)的新实现，因此称为inline，而且是source-level inline。


实际的替换是这样的：

![](../../assets/4a7a427a25dd52fa.png)


这个机制的强大之处在于：

**安全性**：内联器 (Inliner) 是一个极其复杂的算法（约 7000 行代码），它已经系统性地处理了所有副作用顺序、变量遮蔽等边缘情况。基于它进行的重构，天然就是安全的。**自服务 (Self-Service)**：任何库的作者，都可以通过添加一行注释，来引导用户迁移到新的 API。这不再是 Go 官方的特权。

Google 内部的 C++ 团队已经利用类似的机制清理了 200 万处调用。Go 团队计划在 Go 1.26 或 1.27 中，将这一能力正式带入 go fix 命令。

## 小结：拥抱变化，拥抱工具

Alan Donovan 的演讲，为我们描绘了一个清晰的未来：

**Modernizers**将继续作为官方维护的精品工具，帮助我们采纳语言的新特性。**Auto-Inliner**将赋能所有库作者，以一种安全、自动化的方式推动生态系统的演进。

![](../../assets/a55bc7c7e330a57c.png)


作为 Gopher，我们需要做的，就是**及时更新我们的工具链**，关注 gopls 的提示，并乐于接受这些自动化的改进。因为在 AI 还在学习旧代码的时候，我们的工具已经准备好带领我们通向 Modern Go 的未来。

资料链接：https://www.youtube.com/watch?v=_VePjjjV9JU

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