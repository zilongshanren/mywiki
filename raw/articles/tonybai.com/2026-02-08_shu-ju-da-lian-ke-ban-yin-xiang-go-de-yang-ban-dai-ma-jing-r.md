---
title: 数据打脸刻板印象：Go 的“样板代码”竟然和 Rust 一样多？
url: https://tonybai.com/2026/02/08/go-boilerplate-code-vs-rust-data-refutes-stereotypes/
published: '2026-02-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 数据打脸刻板印象：Go 的“样板代码”竟然和 Rust 一样多？

![](../../assets/593b4798ea254eb1.png)


[本文永久链接](https://tonybai.com/2026/02/08/go-boilerplate-code-vs-rust-data-refutes-stereotypes) – https://tonybai.com/2026/02/08/go-boilerplate-code-vs-rust-data-refutes-stereotypes

大家好，我是Tony Bai。

在编程语言的鄙视链中，Go 语言常常因为其“繁琐”而饱受诟病。

“if err != nil 写断手”、“缺乏语法糖”、“到处都是重复的样板代码”…… 这些似乎已经成为了 Go 的标签。

相比之下，Rust 往往被视为“表达力”的代表，拥有强大的宏、模式匹配和类型系统，能够用更少的代码做更多的事。

然而，[Ben Boyter 最近的一项硬核研究](https://boyter.org/posts/boilerplate-tax-ranking-popular-languages-by-density/)，通过分析 GitHub 上各语言 Top 100 仓库（总计约 4 亿行代码），得出了一个令编程语言社区大跌眼镜的结论：

**在代码重复率和“样板代码”密度上，Go 和 Rust 几乎处于同一水平线。**

![](../../assets/9363dc5447a22f65.png)


## 不仅是行数：ULOC 指标

传统的 SLOC（源代码行数）往往无法真实反映项目的复杂度和冗余度。Ben Boyter 使用了他开发的工具 [scc](https://github.com/boyter/scc) 中的一个特殊指标：[ULOC (Unique Lines of Code，唯一代码行数)](https://boyter.org/posts/sloc-cloc-code-new-metic-uloc/)。

ULOC 指标并非简单的“全量去重”，而是通过剥离“结构性噪音”来更精准地衡量系统的真实复杂度。其计算逻辑如下：

- 剔除结构化冗余：不仅排除了空行，还排除了单纯的闭合大括号行（}）以及在不同文件中大量重复出现的公共引用代码（如 include 或 import）。
- 过滤文件级模板：有效识别并扣除在项目中每个文件顶部几乎完全相同的 License（许可证）声明头，避免这些非逻辑性的“样板文字”虚增代码总量。
- 计入注释成本：与传统 SLOC 不同，ULOC 会保留注释统计。作者认为，注释与代码一样需要同等的维护精力，反映了开发者的思考过程，因此属于“有效工作量”。

通过这种方式计算出的 Dryness（干度），代表了剔除“语法支架”和“版权模板”后，真正的业务逻辑与注释在代码中的占比。百分比越高，说明重复代码越少，信息密度越高；百分比越低，说明“样板代码”或重复结构越多。

## 令人震惊的对比：Go vs Rust

让我们直接看数据（数据来源：[GitHub Top 100 仓库](https://github.com/EvanLi/Github-Ranking/)分析，2026年2月）：

![](../../assets/188e029b622f0000.png)


**发现了吗？Rust (60.5%) 和 Go (58.78%) 的差距微乎其微，甚至可以说在统计学上是等价的。**

Ben Boyter 在文章中坦言，他之前也持有“Go 的样板代码比 Rust 多得多”的刻板印象。但数据表明，虽然两者的“啰嗦”方式不同，但结果是一样的：

- Go 的啰嗦：体现在显式的错误处理、显式的循环结构，以及为了简单性而不得不写的重复逻辑。
- Rust 的啰嗦：体现在复杂的类型系统设置、Trait 的实现（impl blocks）、以及为了满足借用检查器而编写的“仪式性”代码。

正如作者所总结的：

Go 狂热者：“Go 很简单！” -> “是的，简单到你需要把同一件事写很多遍。”


Rust 狂热者：“Rust 完美表达！” -> “是的，但你花了 40% 的时间在写 setup 代码和 trait 实现。”

## 其他颠覆性的发现

除了 Go 和 Rust 的“握手言和”，这份报告还有几个极具冲击力的发现：

### 1. Lisp 家族是“干度之王”

Clojure 以 77.91% 的惊人密度位居榜首。Haskell 紧随其后。

这验证了一个古老的观点：如果你想要最高的“人类思想 vs 击键次数”比率，Lisp 和函数式语言依然是王者。它们几乎每一行代码都是纯粹的业务逻辑。

### 2. Java 居然比 Go 和 Rust 都“干”？

Java 的得分为 65.72%，显著高于 Go、Rust 和 C#。

这听起来反直觉，毕竟 Java 以 PublicStaticVoidMain 这种冗长著称。但这可能说明：

- 现代 Java 及其生态（Spring 等）通过注解等方式极大地消除了样板代码。
- 或者，Top 100 的 Java 项目多为成熟的业务系统，核心逻辑占比大，而 Go/Rust 项目中系统级代码（通常包含更多底层重复逻辑）较多。

### 3. 脚本语言的特异性

Shell Script 的密度极高（72.24%），但这主要是因为 Shell 脚本通常很短且高度定制化（Bespoke），很难复用，因此“唯一性”很高。

## 小结：复杂度的守恒

这个研究告诉我们一个道理：语言特性（Features）并不一定能消除复杂度，它往往只是转移了复杂度。

Go 选择了少量的特性，导致逻辑必须通过显式的重复代码来表达；Rust 选择了丰富的特性（宏、泛型、Trait），导致开发者必须编写大量的结构性代码来支撑这些特性。

对于 Gopher 来说，这或许是一种宽慰：别再为 if err != nil 感到羞愧了。隔壁写 Rust 的兄弟，虽然代码看起来很酷，但他们为了让编译器开心而敲击键盘的次数，并不比你少。

**毕竟，软件工程没有银弹，只有取舍。**

资料链接：https://boyter.org/posts/boilerplate-tax-ranking-popular-languages-by-density/

**聊聊你的“啰嗦”体验**

看完这个数据，你是感到“意料之中”还是“大吃一惊”？在你的实际开发中，你觉得 Go 的 if err != nil 更磨人，还是 Rust 的类型体操和 Trait 实现更让你头大？你认同“复杂度守恒”这个观点吗？

欢迎在评论区留下你的看法，让我们来一场理性的“语言之争”！

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


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论