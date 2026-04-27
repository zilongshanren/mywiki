---
tags: [source, cpu, arm, cortex-x925, microarchitecture, gb10, high-performance, spec-cpu2017]
date: 2026-04-27
sources: 1
---

# Arm's Cortex X925: Reaching Desktop Performance（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2026 年 3 月的文章，以 Nvidia GB10（Dell Pro Max）为测试台，深度分析 Cortex-X925 高性能核，并与 AMD Zen 5 和 Intel Lion Cove 全面对比。

## 摘要

X925 是 10-wide 乱序核，在 GB10 中以 3.9–4 GHz 运行，SPEC CPU2017 整数分数与 Zen 5 / Lion Cove 持平——这是 Arm 首次在高性能桌面段实现真正的竞争力。核心优势在于极大的乱序执行窗口（实测约 525 in-flight，高于 Zen 5 的 448）、顶尖的分支预测（BTB 容量接近 Zen 5，部分 workload 精度更优）以及充足的 FP 调度容量（三组各约 53-entry 调度队列 + 6 FP 管道）。主要短板是 128-bit 向量宽度：浮点密集型 workload（如 554.roms）需执行 Zen 5 两倍以上的指令，高 IPC 无法弥补。

## 关键要点

- 10-wide ROB ~525 in-flight（Zen 5: 448，Lion Cove: 576）
- BTB L1 约 2048 branches，支持 2 taken/cycle，远超 A725/X2
- 同样放弃 MOP Cache（与 A725 同理）
- Store forwarding 整数侧全面改善，但无零延迟 forwarding（Zen 5/Lion Cove 有）
- Move elimination 宽约束下易失效，链式 MOV 不支持——CCC 代码压测下暴露
- FP 浮点：整体输给 Zen 5（128-bit vs 256-bit 向量宽度）；SPEC FP 553/554 差距超过 2×
- 在 LPDDR5X 内存环境下整数分数仍与桌面平台 DDR5 持平，说明 IPC 优势弥补了内存延迟劣势

## 链接到的概念

- [[computer-systems/cortex-x925-microarchitecture]]
- [[computer-systems/cortex-x2-microarchitecture]]
- [[computer-systems/cortex-a725-microarchitecture]]
- [[computer-systems/zen5-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-x925-reaching-desktop
- 本地：`raw/articles/chipsandcheese.com/2026-03-03_arm-s-cortex-x925-reaching-desktop-performance.md`
