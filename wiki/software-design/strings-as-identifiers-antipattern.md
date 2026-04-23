---
tags: [标识符设计, 反模式, 软件设计, bitsquid]
date: 2026-04-19
sources: 1
---

# 字符串作标识符的反模式

[[niklas-frykholm|Niklas Frykholm]] 在重写 Bitsquid 的 **Flow**（可视化脚本系统，见 [[flow-graph-data-oriented-runtime]]）时回看第一版代码，总结出一条纪律："**字符串只有一种好用途——存给用户看或用户键入的文本，其它一切用法都应保持怀疑**"。

字符串之所以危险，是因为它同时**多义又强大**：`"a/b.txt"` 和 `"A//b.txt"` 算不算同一路径？你能用大小写转换、正则替换给出一个"基本对"的答案，但这意味着**每个需要字符串含义的地方都要重跑一遍规范化规则**——而任何一次漏掉就是 bug。所谓 "stringly typed" 数据（把日期存成 `"2012-12-09"` 这种）是最显眼的症状；更隐蔽的是把字符串当**标识符**。

## Flow 的那次被坑

Flow 第一版用 connector name 同时充当**外部显示名**和**内部连线 ID**。结果：

- 一个节点里不允许有两个同名 connector，哪怕它们在不同的"连线语义"上。
- 任何一次改名（哪怕只是把 `Out` 改成 `Output` 以让美术看得舒服）都会把存档里所有历史连线打断。
- 折叠（fold）多节点为子图时，如果内部节点有重名 connector，必须维护一张 rename 映射表，代码因此堆出一堆 hairy code。

正确做法是**拆成两个字段**：`Id`（稳定 GUID，只用于代码内部连线匹配）和 `DisplayName`（可本地化、可随意改、给人看）。

## 另一个容易踩的陷阱：临时重名

Niklas 在另一个系统里也吃过亏：他以为 "script 里按 name 访问对象，name 必然全局唯一" 就可以把 name 当 id 用。没考虑的是**输入过程**：用户先有一个 `rock`，再想创建 `rock_small`，在她敲到一半（字符串还是 `rock`）时，系统里**暂时存在两个 name 为 `rock` 的对象**——这个"短暂违反唯一性"的窗口足以让任何依赖"name 唯一"的代码崩溃。

结论：**"name 在稳定态唯一" 不等于 "任何时刻都能当 id 用"**。id 必须独立于 name，且在对象诞生时就固定。

## 评论区的反驳与精调

不少读者指出两种"合理使用字符串"的场景：

1. **枚举风常量**：像 `"bold"` 这种有限、预定义、面向存档可读性的选项，落盘时写字符串无妨。但 Niklas 坚持：**落盘后马上转 enum**，内存里用 `Styles.Bold` 而不是 `"bold"`，否则代码到处散落魔数字符串。
2. **用户不可改的稳定 id**：如果字符串 id 保证一旦分配就不能改，也确实能工作。但 GUID 更"自明"（一眼看出它是内部 id），更难被错用。

## 关联

这条反模式和 wiki 里若干概念互为旁证：

- [[no-magic-principle]]：字符串操作里有大量"约定大于显式"的隐含语义，是典型的魔法。
- [[intent-vs-state]]：display name 是 state（随时可变的展现层），id 是 intent（系统认同的身份）——混用就是混淆了 intent/state。
- [[static-hash-value-debug-assert]]：Bitsquid 落盘还是用字符串（如事件名 `"jump_start"`），但在 runtime 一律转成 32-bit hash；id 和 display 的分离在这里演化成 hash 和 source string 的分离。
- [[guid-object-database-schema]]：另一种彻底方案——内容管线全用 GUID，display name 仅挂在 asset 元数据里。

## Sources

- [[sources/bitsquid-four-meditations-bad-design]]
