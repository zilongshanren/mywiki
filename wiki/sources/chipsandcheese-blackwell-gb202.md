---
tags: [source, gpu, nvidia, blackwell, 微架构]
date: 2026-04-27
sources: 1
---

# Blackwell: Nvidia's Massive GPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 6 月的文章，系统深挖 GB202 die 的微架构细节，并与 AMD RX 9070（RDNA4）进行逐层对比。

## 摘要

文章以 RTX PRO 6000 Blackwell（188 SM 启用，600 W TDP）为测试平台，访问由 Will Killian 提供。从工作分发机制出发，分析了 GPC:SM = 1:16 的设计权衡、SM 前端的两级指令缓存、执行单元重组为单路 32-wide pipe、SM 内 128 KB L1/Shared Memory 的带宽路径、以及 GPU 级 L2 与 VRAM 的延迟回退问题。文章最终以 FluidX3D 实测作为综合性能佐证，结论是 Blackwell 以规模取胜——188 SM 对 28 WGP，弥补了单核效率差距。

## 关键要点

- GB202 面积 750 mm²，921 亿晶体管，192 SM（RTX PRO 6000 启用 188）
- GPC:SM = 1:16，比 Ada Lovelace 的 1:12 更激进，牺牲短 wave 效率换 SM 数量
- Blackwell 新增同队列图形/compute 重叠执行，消除 subchannel switch 强制等待
- L1i 约 128 KB，L0i 32 KB/partition；AMD 的 32 KB WGP-wide L1i 在多 wave 场景下带宽更均衡
- 主执行管道重组为 32-wide 单路，与 Pascal/RDNA 类似，INT32 × FP32 交替流不再停顿
- SM 内 L1/Shared Memory 128 KB 保持 Ampere 以来不变，单路 128 B/cycle 到执行单元
- GB202 L2 延迟约 130 ns（Ada 为 107 ns），64 个 bank，8.7 TB/s
- VRAM 延迟约 329 ns，高于 RDNA4 的 254 ns
- 512-bit GDDR7，VRAM 带宽大幅领先 AMD 256-bit GDDR6

## 链接到的概念

- [[rendering/blackwell-gb202-architecture]]
- [[rendering/rdna4-architecture]]
- [[rendering/gb10-gpu-blackwell-igpu]]
- [[rendering/ada-lovelace-architecture]]
- [[computer-systems/gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/blackwell-nvidias-massive-gpu
- 本地：`raw/articles/chipsandcheese.com/2025-06-29_blackwell-nvidias-massive-gpu.md`
