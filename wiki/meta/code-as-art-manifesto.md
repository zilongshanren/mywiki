---
tags: [工具链, 热重载, 引擎架构, manifesto, 迭代速度]
date: 2026-04-19
sources: 1
---

# 代码平权宣言（Pesce 2010）

2010 年 9 月 [[angelo-pesce|Pesce]] 在 C0DE517E 上贴了一篇半正经半吐槽的「International movement for code rights」——主张**代码和数据应当享有同等基础设施投资**。十五年后回头看，这是一份清晰的工业痛点清单，也是他后续多篇博文（[[live-editing-taxonomy-2010]]、[[pesce-2010-engine-layer-sketch]] 等）的纲领。

## 五项诉求

- **Ease of change**：美术换一张贴图、换一个占位模型是零摩擦的；代码为什么要忍「[code rot](https://en.wikipedia.org/wiki/Software_rot)」「[prototry pattern](http://www.lsd.ic.unicamp.br/~oliva/fun/prog/resign-patterns)」？代码应当同样便于替换。
- **Ease of scale**：每代主机都砸钱做**数据规模**（streaming、terabyte 资产管线），却没人同等投资**代码规模**——编译、链接、可执行体积在同代数量级下仍然喘。
- **Ease of iteration**：美术有 live-edit、hot-reload、工具 ↔ 游戏直连；代码只有 shader live-reload 和「script 语言」两种特权通道，C++ 本体几乎没有热重载投资。「为什么要被迫用脚本语言？**代码应当享有同等迭代速度**。」
- **Tools**：像 schema / 静态检查 / 可视化那样审视代码。能在游戏里点一个模型看它用了哪些贴图——为什么不能点一个对象看驱动它的代码、它的输入输出状态、它跑到了哪里？「为什么还要用 debugger 这种原始手段去解剖代码？」
- **Equal dignity**：数据是艺术、数据是独一无二的；为什么代码只能是「框架」「基础设施」，不能是独一无二的艺术？一个主角美术能做几周，一段驱动主角的 ad-hoc 代码为什么不能？

## 核心提案

- **Fuck OOP**：Pesce 明确反对把角色 / 对象塞进 mesh ← 3dobject 的继承树。他的替代是：**角色是一组行为代码的复合**（load / update / render 函数），跟它的美术组件（mesh / material / texture）一样**独一份、不强求复用**。
- **轻量框架、厚重应用**：框架应专注于**编码人体工学**——热交换、live-edit、数据流可视化——而不是提供越来越深的抽象树。
- **接口 + 合约**：用模块接口 / 函数契约声明输入、输出、持久状态，静态检查 + 推断保证正确性；运行时前/后条件 + 默认降级处理错误而不崩溃。
- **反射 + 可视化**：运行时看清每个对象挂了哪些代码、各模块的输入输出状态、各个 hook 跑到了哪里。

## 结尾的 MW2 比喻

文章尾段 Pesce 拿 _Modern Warfare 2_ 的战役模式作佐证：它最打动他的不是美术，而是**机制密度**——几乎每个场景都有独一份的玩法逻辑，不在反复套用同一个骨架。他承认不知道这些独一份的行为是靠脚本、数据驱动还是额外 C++ 实现的；但他明确了一件事：**我们应当是艺术家，造 GAMES，而不是造 frameworks / tools**。

## 和其他 Pesce 想法的串联

- **Live-editing 诉求**：直接承接 2010 年 5 月的 [[live-editing-taxonomy-2010]] poll——那里分出了 code hot-swap 是「有了它其他都不重要」的终极档位，这里把它上升为一份政治诉求。
- **Tools 诉求**：延续 [[c0de517e-pix-is-great-but|PIX is great but]] 的结论——真正省时间的是**渲染内置的 debug view**，不是切工具。
- **反 OOP 诉求**：对应 [[scene-graph-unnecessary-in-engine|scene graph 不该是引擎核心]]——不要为复用构造深继承树。
- **Ease of change 诉求**：和 [[pesce-2010-engine-layer-sketch]] 里把 DevOps / 构建放首层是同一个思想——**先让代码容易动**，再谈架构。

## 历史位置

这份 manifesto 放在 2010 年是**挑衅式预测**；放在 2026 年回看，行业已经部分兑现：

- Live-edit：ImGui、runtime reflection、数据驱动、Unreal Blueprint、[[binary-hot-reload|binary hot-reload]] 框架（RCR、Live++）都部分实现了「代码热换」。
- Tools for code：现代 IDE 有反射、调用图、profiler overlay；语言层有 Rust / Zig 等强合约静态检查。
- Unique code：独立游戏圈早已抛弃「万能引擎框架」思想；但 3A 仍然是「巨型引擎 + 少量独特脚本」结构。

Pesce 自己后来在 [[pesce-2010-engine-layer-sketch]] 里用「六层引擎架构草图」回应了这份诉求——**把 code iteration 基础设施当作引擎的一层，而不是附属工具**。

## 相关

- [[live-editing-taxonomy-2010]]
- [[pesce-2010-engine-layer-sketch]]
- [[scene-graph-unnecessary-in-engine]]
- [[binary-hot-reload]]
- [[tools-first-iteration-loop]]
- [[experience-as-noise-filter]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-code-rights]]
