---
tags: [software-design, ui, architecture, reactive]
date: 2026-04-19
sources: 1
---

# Intent 与 State 的分离

[[steven-wittens]] 在 *I is for Intent* 中提出：传统 MVC / React 教条里流行的 `View = f(State)` 并不够，真正符合用户直觉的应用需要在 `State` 之前再留一层 `Intent`。Intent 是用户操作原封不动记录下来的 source of truth（可能非法、不一致、越界），State 是把 Intent 经过 `validate(Intent)` 解析后得到的、可以用于渲染和业务逻辑的合法子集。

## 为什么必须分两层

文本编辑器的光标列号是最小的示范。用户在第 6 列按方向键向下跳到只有 2 列的短行，光标被强制挤到第 1 列；再按向下返回长行时，光标必须回到第 6 列。这个"记住的列号"不是 State，因为它在中间那一行上无效；但它必须作为 Intent 被持续保留，否则体验会很糟糕。更广泛的例子：树视图折叠时仍要记住被隐藏行的展开状态；属性面板要记住被禁用 tab 的选择；A/B/C 三态控件要保留互斥的全部三份配置；电子表格的循环引用必须允许临时进入非法状态，因为修复需要多步。

Wittens 将此总结为"validation 不是一次性的归一化动作，而是持续、非破坏地从 Intent 派生 State"。旧的 Intent 应保留原样（即使已非法），新的 Intent 应经过约束后写入；输入不允许越界被限制，但既有越界数据不能被丢弃。这与 Stanley 式（强类型/强事务/拒一切脏数据）后端思维根本不兼容——UI 这一侧必须容许脏 Intent 流动。

## Patch 作为一等公民

Intent 若随代码到处传递，会稀释类型系统提供的约束保证。Wittens 的经验方案是把"变更"本身作为一等值：`Update<T>` 描述"新 value 的稀疏差分"，通过 `patch(value, update)` 应用（递归、不可变 merge，数组按值处理，也支持 lambda-based update 表达 "append to list" 这类不带完整列表的变更）。这样只有一个函数需要接触原始 Intent，其他代码只需要 `updateIntent(update)`，Update 的形状在 Intent 和 State 间完全对称，可 100% 从 State 派生。WYSIWYG 预览则是 `patch(committed, ephemeral)`：临时 Intent 叠加，撤销等于清空 ephemeral 层。

Patch 的补集是 `diff(A, B)`，形状与 update 一致——于是撤销/重做、OT 风格的合并都统一在一张表里。Wittens 强调这不是 OT/[[crdt-as-resolution-strategy|CRDT]] 的替代，而是在大多数结构化编辑场景下的合理下限；CRDT 只有在真正需要"部分有序的 Intent 合并为单一 State"时才不可替代，例如协同富文本。

## Schema 即数据流

Intent/State 的分离最终会倒逼 schema 设计：哪些字段必须独立才能被 patch 精确更新？`column` 和 `line` 应拆成两个 field 还是打包成 `XY` 元组？要看读写路径。"ordered list of items" 应当拆成 `order: List<Id>` 加 `values: Map<Id, T>`，让重排和编辑成为正交操作——这也顺便规避了协同编辑里"索引随编辑漂移"的问题，用 ID 取代位置索引，只对 `order` 单独跑一个 fractional-index 风格的 list CRDT 即可。

更深的含义是：后端与前端的硬切分是大多数 SaaS 复杂度爆炸的真正源头。Wittens 主张前端应坐在后端*旁边*，而非前端*之前*，两者共享 patch 协议而不是通过 REST/GraphQL 来 "负半个问题"。GraphQL 被点名批判为"getter 反复拼装、setter 沦为千层面+意大利面"；SQL 用于建模交互式工作空间是"为行政流程设计的工具错配场景"。

## 与 reconciler 的共鸣

Wittens 把 React/tree-sitter/Use.GPU 归为同一类"结构保留的增量变换器"——它们在 Intent 与 State 间来回搬运，数据与代码有相同的形状。一个函数的 state 可能就是下一个函数的 intent，reconciler 帮你把派生关系自动维护好。这是他把 [[use-gpu-reactive-runtime]] 作为 render 层的同时也用来驱动 CPU canvas 的底层动机。

## Sources

- [[sources/acko-i-is-for-intent]]
