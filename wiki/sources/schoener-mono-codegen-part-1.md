---
tags: [source, unity, mono, 编译器, 值类型, simd]
date: 2026-04-19
sources: 1
---

# What I learned from improving Unity's Mono codegen, part 1（Sebastian Schöner）

[[sebastian-schoener]] 2026 年 4 月初的技术深潜第一篇，手把手演示一段 `dot4` 是如何在 Mono JIT 管线中被折磨成 400 行汇编的。

## 摘要

文章沿着 Mono 的 JIT 流水线跟踪 `dot4(xs,ys,zs,mx,my,mz) = xs*mx + ys*my + zs*mz` 这样一个再普通不过的 `float4` 乘加：**IL（栈式）→ 高层 IR（寄存器式）→ lowering 展开 → 最终 x64**。IL 才 10 行，而最终汇编有 400 多行。罪魁有几层——Mono 内部全用 `double` 做数学，到处插 `cvtss2sd` / `cvtsd2ss` 往返（可关）；`float4` 按值传进来被当作 valuetype，`vmove` 在 lowering 时展开成 4 次 `loadi4/storei4` 的栈拷贝；每个内联乘法都生成一个零初始化的临时 `float4`、逐分量写入再拷到下一个临时；完全没有向量化。作者新加的 pass 在 IR 层就消除多余 `vmove` 和临时，搭配「告诉 Mono `float4` 是 SIMD 向量」，最终能收敛到 3 条 `mulps`/`addps`。遗留问题是 Windows x64 ABI 仍要求 16 字节值按引用传，真正正路是把 `dot4` 直接内联。

## 关键要点

- Mono IR 是「寄存器中心」但寄存器是虚拟的；`float4` 默认被当作 16 字节栈对象，不知道能住 XMM
- `vmove` 在 lowering 里展开成 4 条 4 字节 load/store，是值类型代码爆炸的核心机制
- 每次内联乘法会新建一个 vzero 的临时 + 按分量 store + 全量 `vmove` 到下一个局部
- `cvtss2sd` 往返是 Mono 特有的，IL2CPP / Burst 都不这样
- 作者的新优化 pass **在 IR 层** 改写，而非到 x64 层再补救
- Windows x64 ABI 的「大值按引用传」导致就算看穿 SIMD 也得走一次 `movups xmm, [rax]`；解决靠 `vectorcall` 或真正内联

## 链接到的概念

- [[mono-jit-pipeline]]
- [[calling-conventions-x86]]

## 原文

- 链接：https://blog.s-schoener.com/2026-04-07-mono-codegen-1/
- 本地：`raw/articles/blog.s-schoener.com/2026-04-07_what-i-learned-from-improving-unity-s-mono-codegen-part-1-se.md`
