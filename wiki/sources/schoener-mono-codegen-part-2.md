---
tags: [source, unity, mono, 编译器, 别名分析, 死代码消除]
date: 2026-04-19
sources: 1
---

# What I learned from improving Unity's Mono codegen, part 2（Sebastian Schöner）

[[sebastian-schoener]] Mono codegen 系列的第二篇，讲三件事：**要不要上 LLVM**、**优化 pass 插在管线哪一段**、**为什么 DSE 是硬骨头**。

## 摘要

Unity 的 Mono 有个半成品的 LLVM 后端路径，作者考虑过走那条路，但最终选择自己写优化 pass——既为学习写优化编译器本身，也因为「没有依赖」是他一贯的品味（把烦人的构建管道问题换成愉快的实现问题）。他原计划把 pass 插在 x64 层（他更熟），最后却主要做在 Mono 的抽象 IR 层：**越晚清理，垃圾越有时间制造破坏；越抽象，事实越清晰**——局部变量在抽象层按定义不重叠，在 x64 层变成「字节区间是否重叠」的运行时谜题。别名分析在两层各写了一套，事后判断只留抽象层那套就够。作者对 `__restrict` / `[NoAlias]` 的心态也由「我比编译器懂」转为「帮可怜的编译器一把」。寄存器分配完后仍有局部 cleanup 值得做——比如两条看起来无关的 `pxor xmm0,xmm0` 在 RA 映射后其实是对同一个 xmm0 的重复清零，可以省一条。最后是 DSE：**它本质上非局部，且必须集中到单一 pass**，其它 pass 大胆留下潜在 dead store，让 DSE 总清——「不要让硬的步骤乘法式膨胀」是他最大的方法论收获。

## 关键要点

- **LLVM 不是银弹**：接 LLVM 的工作量是「水暖工」，手写 pass 是「你真正想做的活」
- **优化尽量早做**：抽象层的别名证明一句话，下游字节层要花命证
- 别名分析要预计算并前向传播，而不是每 pass 现算
- 寄存器分配后的小 cleanup（比如因为 vreg 映射到同一物理寄存器导致的重复清零）仍有价值
- DSE 必须独占一个 pass；别处可自由留 dead store 不碰
- 「Don't multiply the hard parts」——识别全局难题，集中处理

## 链接到的概念

- [[pointer-alias-analysis]]
- [[dead-store-elimination]]
- [[mono-jit-pipeline]]

## 原文

- 链接：https://blog.s-schoener.com/2026-04-13-mono-codegen-2/
- 本地：`raw/articles/blog.s-schoener.com/2026-04-13_what-i-learned-from-improving-unity-s-mono-codegen-part-2-se.md`
