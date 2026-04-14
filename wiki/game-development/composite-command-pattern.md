---
tags: [设计模式, 命令模式, 游戏架构, ecs]
date: 2026-04-14
sources: 1
---

# 复合命令模式（Composite Command）

**命令模式（Command Pattern）**是把「要做的事」打包成对象——每个命令暴露一个 `execute()` 和一个完成信号 `onComplete`。单命令已经有用——可撤销、可序列化、可被 AI 规划器生成——但真正的威力在于把命令再嵌套起来：一个命令内部可以包含一组子命令，由一个**复合命令（composite command）**统一调度。

## Serial / Parallel 两种基元

Allen Chou 在他 2011 年的 Rusher 2 框架里给出了最小实现：

- **`SerialCommand`**：一串子命令**顺序执行**，前一个触发 `onComplete` 之后下一个才开始。实现只需要监听每个子命令的完成信号，在回调里启动下一个，最后一个完成后再触发自身的 `onComplete`。
- **`ParallelCommand`**：一组子命令**同时启动**，全部触发 `onComplete` 之后父命令才算完成。常见用法是引用计数：每个子命令完成时 `--pending`，归零触发父命令的完成。

这两个类都继承自一个通用 `CompositeCommand`，后者提供 `append(cmd)` 方法动态加子命令，也可以通过构造函数一次传入命令列表。子命令也可以是复合命令——所以一个「5 只小球追随鼠标」的逻辑可以拆成 `SerialCommand(Tween1, Tween2, ..., Tween5)`，而每个 Tween 本身又是一个命令对象。

## 为什么要完成信号，而不是直接返回

命令模式的**隐藏假设**是：命令的执行可能跨多个帧——一个 Tween 命令要持续 0.5 秒插值位置，不可能在一个函数调用里「做完」。这就迫使框架必须把「完成」从「函数返回」里剥离出来，用显式信号表达。这也是命令模式和同步函数调用的根本区别：**命令是时间上分布的工作单元，函数是瞬时的计算**。一旦你接受这件事，很多游戏系统（AI 行为树、技能系统、过场动画脚本、UI 状态迁移）都可以建模成命令树。

## 在 ECS 里的位置

在一个 [[ecs|ECS]] 游戏框架里，命令通常由一个 `CommandManager` 系统持有和调度，通过依赖注入拿到 `EntityManager`、`Clock`、`Mouse` 等其它系统引用。command 本身不持有复杂状态——只持有指向目标 component 的引用（例如 `Position` 组件），执行时直接改这些 component 的数据。这和 ECS「数据在 component、逻辑在 system」的教条稍有张力：命令既是数据又是逻辑。大多数框架的做法是把命令视作 system 的扩展——一种可组合、可延迟执行的 system 调用，而不是 component。

命令模式与行为树、状态机之间有深度重合：状态机的每个 transition 可以是命令，行为树的每个 leaf 节点也常被建模成命令；Serial / Parallel 复合命令对应行为树的 Sequence / Parallel 节点，是设计模式在不同抽象层级的同构表达。

## Sources

- [[sources/allenchou-rusher-2-composite-commands]]
