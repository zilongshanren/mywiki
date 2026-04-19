---
tags: [编译器, 优化, 死代码消除, jit]
date: 2026-04-19
sources: 1
---

# 死代码消除（Dead Store Elimination）

DSE 的目标：如果一次内存写入之后，没人再从这块内存读，就删掉这次写。在 [[mono-jit-pipeline|Mono 的 JIT]] 里，大量「写到栈上的临时 struct」本该就此消失。但 [[sebastian-schoener]] 在实现 Mono 优化 pass 时发现：**DSE 是整个管线里最脆弱的一步，必须集中到单一 pass 里做，绝不可以让每个 pass 都顺手做一点**。

## 为什么脆弱：本质非局部

大多数优化可以是「看一小段代码就能决定」的局部操作。DSE 不行：要确信一次 store 可以删，必须证明 **整个函数、每条可能的执行路径上** 都不会再读这块内存。证据面是全局的、和 [[pointer-alias-analysis|别名分析]] 深度耦合——任何走潜在别名指针的 load 都会推翻结论。

## 信息要预计算，不要顺手重建

作者的第一版做法是「每个 pass 都尽量就近做多一点事」。这种「maximal pass」策略看似简单，实则两头出事：

- **效率**：每个 pass 都得临时重建一遍「这点存过什么、那点存的是谁的地址 + 偏移多少」这类信息，最坏情况是来回反向遍历指令流。正确姿势是**一次性前向传播所有信息，后面所有 pass 直接消费**。
- **硬的部分会乘法式膨胀**：如果十处代码都在局部判断「这次 store 应该能删」，就有十处各自错漏的风险。集中到一个点后，其它 pass 可以大胆留下潜在的 dead store，让 DSE 来总清。

「**Don't multiply the hard parts**」——识别出哪一步是全局难题，把它孤立在一个专门 pass 里，其它模块保持局部简单。这是从多个 pass 相互纠缠里抽出来的方法论。

## 与冗余 load 消除的分工

「冗余 load 消除」（上一次存进去的值直接从寄存器拿）反而是**局部且简单**的：只看一段连续代码就能决定。它会顺带把一些 store 变成「没人读」——但是否真的能删，仍留给 DSE 裁决。

## 相关

- [[pointer-alias-analysis]]
- [[mono-jit-pipeline]]
- [[compilation-pipeline]]
- [[sebastian-schoener]]

## Sources

- [[sources/schoener-mono-codegen-part-2]]
