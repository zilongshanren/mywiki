---
tags: [source, 渲染, GPU, shader, ISA, 性能]
date: 2026-04-14
sources: 1
---

# The hidden cost of shader instructions（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou]] 发表于 2025 年 1 月的文章，起因是他发了一张单条 `atan2()` 生成的 AMD RDNA ISA 截图，引起大量"原来这条指令这么贵"的惊讶——于是写了这篇完整分类。

## 摘要

文章用 RGA 在 GCN/RDNA 上的 ISA 输出为证据，把 shader 指令的"隐藏成本"归为三类：**(1) 硬件无原生实现**——acos/asin/atan/atan2、tan、normalize、length、integer div、cubemap sampling、动态 VGPR 数组索引等；单个 `atan2()` 展开成约 60 条 vop 并包含两次 `v_div_scale_f32`、 rcp、六次 Horner fma，以及大量 execute mask 和分支。**(2) 原生指令不等价**——GCN/RDNA 上 rcp/cos/sin/sqrt/rsq 和整数乘法都是 **16 cycles**，是普通 FMA 的 4×；scalar float 不被支持，会被强制搬到 vector unit，抬高 VGPR 占用。**(3) 外部资源依赖**——纹理 cache miss 走 VRAM 几百 cycle；单通道 sampler 路径 16 cycles vs `Load()` 的 4 cycles；`NonUniformResourceIndex` 触发 **waterfall loop** 最坏情况要 32 圈；groupshared LDS 的 bank conflict 能把单次访问放大 32×。作者强调"实际影响取决于 bottleneck"——ALU 富余的 shader 里 atan2 可能无感，关键 loop 里一个 bank conflict 能把 dispatch 拖垮。对策一侧给出了 Sébastien Lagarde 的反三角近似、Inigo Quilez 的"无 acos 技巧"，以及"看 ISA 别猜"。

## 关键要点

- **`atan2()` 在 RDNA 上展开约 60 条 vop**——包含除法、Horner 多项式、execute mask 变换
- **`tan`/`normalize`/`length` 都没原生实现**，被拆成 sin+cos+rcp / mul+fma+rsq 套路
- **整数 div**: vector 约 35 条指令，scalar 约 42 条（scalar 更糟）
- **cubemap 采样多出 face-select 开销**：`v_cubema/tc/sc/id` 全要跑一遍
- **动态 VGPR 索引**：uniform 下标走 `v_movrels_b32` 便宜；thread-variant 下标编译器只能做 N 遍 cmp+cndmask
- **transcendentals 和 integer mul 是 quarter-rate**（16 cycle vs 4 cycle FMA）
- **scalar float 在 GCN 不存在**，编译器把 scalar register 的 float 运算强制搬到 VGPR
- **LDS 32 banks**：`data[GTid.y*32 + GTid.x]` 无冲突，`data[GTid.x*32 + GTid.y]` **放大 32×**
- **`NonUniformResourceIndex` waterfall loop**：用 `v_readfirstlane_b32` 分批处理，最坏情况吞吐 1/32
- 规则："**看 ISA，不要猜**"

## 链接到的概念

- [[shader-instruction-cost]]
- [[register-spilling-avoidance]]
- [[gcn-wave-occupancy]]
- [[gpu-latency-hiding]]
- [[bottleneck-analysis]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/01/19/the-hidden-cost-of-shader-instructions/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-01-19_the-hidden-cost-of-shader-instructions.md`
