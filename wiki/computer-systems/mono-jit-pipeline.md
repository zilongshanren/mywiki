---
tags: [编译器, jit, mono, unity, codegen, 值类型]
date: 2026-04-19
sources: 3
---

# Mono JIT codegen 流水线与值类型之痛

Unity 长期依赖 Mono 运行 Editor 与部分游戏。Mono 的 codegen 质量远不如 CoreCLR 或 IL2CPP——尤其在 C# 值类型（struct）密集的数学代码中，生成的 x64 汇编常常膨胀一个数量级。[[sebastian-schoener]] 做的改良工作揭示了 JIT 内部管线的全貌：**越晚清理垃圾，它越有时间破坏别的优化**。

## 五阶段流水线

从 C# 到机器码要经过五跳：

1. **C# → IL**。`.NET` 编译器离线一次性完成，产出栈式 IL。
2. **IL → 高层 IR**。JIT 启动时把栈式指令翻成寄存器式 IR，内联（inline）也在这一步发生。
3. **高层 IR → 低层 IR**。几轮 lowering：`vmove` 展开成 4 次 `loadi4/storei4`、`ldaddr` 取地址等。
4. **低层 IR → x64 前的伪汇编**。分配虚拟寄存器、分配栈槽。
5. **寄存器分配 + 机器码发射**。

Mono 的 IR 是「寄存器中心」的（不像 IL 的「栈中心」），但寄存器都是虚拟寄存器，一个 `float4` 默认住在 16 字节的栈槽上——Mono 不知道它可以住 XMM。

## `dot4` 之灾

一个 `xs * mx + ys * my + zs * mz` 的 `float4` 内联乘加，**未优化下 Mono 吐出 400 行汇编**：

- 全部 `float` 先 `cvtss2sd` 升为 `double` 再算再 `cvtsd2ss` 降回，因为 Mono 内部恒以 double 做数学（IL2CPP / Burst 都不做这事，可以直接关掉）
- 每个 `vmove`（value-type move）在 lowering 后变成 4 条 `loadi4/storei4`，把参数从栈复制到另一个栈槽，只为把「按值传进来的参数」忠实拷一份给内联后的 `op_Multiply`
- 每个乘法得到的临时 `float4` 零初始化 → 逐分量写入 → 整体 `vmove` 到下一个临时，每步都走栈
- 没有向量化：4 个分量手工标量 `mulss`

开启作者新写的 pass 后，IR 层直接塌缩到 12 行，再开启「告诉 Mono `float4` 是 SIMD 向量」后进一步变成 3 条 `mulps`/`addps`，汇编总共约 30 行——**比原版短一个数量级**。

## 值类型为什么是重灾区

`vmove R27 <- R17` 语义上是「复制一个 `float4` 从 R17 到 R27」。Mono 保守地翻成按字节拷贝的序列：

- 先 `ldaddr R231 <- R17` 取源地址、`ldaddr R232 <- R27` 取目的地址
- 再 4 次 `loadi4_membase` / `storei4_membase_reg` 逐 4 字节搬

对更大的结构体，Mono 会直接生成对 `memcpy` / `memset` 的调用——函数调用本身比要复制的几十字节还贵。整个 JIT 管线缺少「消除冗余 struct 拷贝」的 pass，是 Mono 在 [[ecs]] / `Vector3` / DOTS 代码上表现糟糕的根因。

## ABI 限制：Windows x64 vs vectorcall

哪怕 Mono 把 `float4` 认作 SIMD，标准 Windows x64 ABI 规定这类 16 字节值仍然按引用通过栈传递。所以 `mulps` 之前仍得做一次 `movups xmm, [rax]`。真正解法是两条：

- 让 Mono 懂 [vectorcall](https://learn.microsoft.com/en-us/cpp/cpp/vectorcall) 调用约定，XMM 直接传参
- 更正路：让 `dot4` 被完全内联，根本没有「调用」

## 何时值得优化

JIT 优化带来可观测的帧率提升的前提：**游戏至少有一段热代码是 CPU compute-bound**（不是完全在等内存）。Mono 默认 codegen 之糟糕让这个前提相对容易满足。Debug 构建一律关闭优化；Release 构建需要权衡 JIT 编译开销与运行期收益。

## 相关

- [[pointer-alias-analysis]] — 这些优化几乎都要用到的前置能力
- [[dead-store-elimination]] — 最脆弱的那一步，必须集中到单一 pass
- [[calling-conventions-x86]] — Windows x64 / vectorcall 背景
- [[aos-vs-soa]] — 值类型布局的相关视角
- [[sebastian-schoener]]
- [[cpp-multi-paradigm-discipline]]

## Sources

- [[sources/schoener-better-mono-codegen]]
- [[sources/schoener-mono-codegen-part-1]]
- [[sources/schoener-mono-codegen-part-2]]
