---
tags: [编译器, 微架构, 性能, ai, top-down]
date: 2026-04-19
sources: 1
---

# LLM 写的 C 编译器与微架构暴露

这篇文章表层是 April Fools（讽刺 Anthropic 的 CCC "Claude's C Compiler"），但微架构分析本身是真的。把一个会生成极度低效冗余代码的编译器产物作为输入，反而成了压测 CPU 容错能力的好工具——**看哪种微架构特性在冗余指令洪水下还能救命**。

## CCC 生成的代码有多奇怪

对 `A[current]` 这种简单 pointer chasing：
- GCC：一条 indexed addressing load
- CCC：把 index 在几个寄存器之间来回搬、往栈里压一次再弹出，最终成 **9 条指令的依赖链**；arm 版本甚至在循环里 `mov` 寄存器到自己

## 哪些微架构特性是救生圈

把 CCC 的 9 条指令链喂进不同核：
- **Zen 5 / Lion Cove（强 move elimination + 零延迟 store forwarding）**：把 9 条链崩成 2 个额外 cycle，OoO 宽度吸收多余指令
- **Arm Cortex X925（move elimination 弱、无零延迟 store forwarding）**：同一段代码吃 6–7 cycle 惩罚
- **In-order 小核**：灾难，因为没有 OoO 吸收余量

结论清晰：move elimination + store forwarding 这两项在 GCC 正常输出下只是锦上添花（Ice Lake 关掉 move elimination 也只退 1–3%），但一旦代码变病态，它们是否存在就决定了是不是直接死掉。

## SPEC CPU2017 上的 top-down

CCC 编译的 SPEC 比 GCC 的慢 70%+，部分工作负载指令数膨胀 **10×**。但它的 IPC 经常更高（`525.x264` 上 Arrow Lake 平均 IPC 6.09，GCC 最好也就 5.5）——因为核心忙着跑一堆 bogus 指令。正好说明 **IPC 是诊断指标而非优化目标**：指令都是废话时，IPC 再高也没意义。

Top-down 视角：
- 三个 C-only FP workload 在 CCC 下变极度 core-bound（后端等 ALU 执行）
- 整数 workload 从 frontend bound 变成后端 bound
- Zen 5 `500.perlbench` 成 op cache 的少见反例——per-thread 4-wide decoder 不够喂 8-wide rename，op cache miss 一多就被 frontend 卡住
- X925 在 `519.lbm` 的 backend memory bound 飙升，根因是 CCC 生成的代码反复把 `x0` spill 到栈再几条指令后 reload，store forwarding 延迟直接进关键依赖链

## 架构取舍的镜子

这种极端实验像放大镜，把几项"平时不起眼但设计时花了硅面积"的特性暴露出来价值。作者的讽刺结尾（"只要 20–30 GHz 就能补回性能"）反向论证了：软件质量塌方的时候，硬件怎么堆都救不回来——"well optimized software performs well across a wide variety of hardware"。

## 相关

- [[cpu-performance-formula]]
- [[compilation-pipeline]]
- [[memory-hierarchy]]
- [[gb10-memory-subsystem]]

## Sources

- [[sources/chipsandcheese-ccc-april-fools]]
