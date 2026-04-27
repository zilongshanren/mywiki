---
tags: [procedural-generation, graph-rewriting, level-generation, tool]
date: 2026-04-27
sources: 1
---

# PhantomGrammar 与 Ludoscope

PhantomGrammar 是 Joris Dormans 开发的图改写引擎，Ludoscope 是其配套的图形化 IDE。两者共同构成了驱动 Unexplored 等游戏关卡生成的完整工具链，也是[[game-development/graph-rewriting-proc-gen|图改写]]从理论走向实践的代表性系统。

## 系统设计

PhantomGrammar 在基础图改写之上增加了若干工程级扩展：

**扩展图**：节点和边均可携带任意属性，节点内还可嵌套子图。匹配模式支持基于属性的条件表达式（例如统计入边数量、检查属性值范围），替换模式支持随机选择多个候选方案并内嵌代码钩子。

**多目标重写**：除图之外，PhantomGrammar 还可对字符串和切片地图执行改写，使得 L-System 字符串展开和元胞自动机均可用同一语言描述。

**三种迭代模式**：
- *Normal*：在所有匹配中随机选一个执行一次规则
- *LSystem*：按固定扫描顺序对所有匹配逐一应用，类似文本编辑器的"全部替换"
- *Cellular*：先收集所有匹配，再批量应用，模拟元胞自动机的同步更新语义

## 菜谱（Recipe）机制

规则本身只描述"如何改"，执行时序由菜谱控制。菜谱是一组顺序指令，指定哪批规则在什么模式下迭代、迭代多少次或直到无匹配为止。规则本身也可携带子菜谱，在替换成功时触发，形成调用栈。Unexplored 的 5000+ 条规则通过模块化菜谱分层管理，避免全量并行带来的混乱。

## 局限性

图改写本质上是局部模式的渐进替换，擅长把小编辑堆叠成复杂结构，但不擅长表达传统算法。典型瓶颈是**图布局（Graph Layout）**——系统无法从无坐标图推断 2D 平面上节点的合理位置，这是 Unexplored 与 Enter the Gungeon 相比缺失的能力。此外，缺乏函数抽象导致重复性几何操作（如计算最远节点）需要多步规则拼接完成。

## 与其他工具的关系

PhantomGrammar / Ludoscope 目前未公开发布，仅在学术论文和 GDC 演讲中有展示。Boris 的文章系列将其定位为理解[[game-development/dungeon-generation-algorithm|Unexplored 地牢生成]]的前置知识。Enter the Gungeon 和 Dungeon Architect 各自以更有限的图替换语言实现了类似思路的子集。

## Sources

- [[sources/boris-phantomgrammar-ludoscope]]
