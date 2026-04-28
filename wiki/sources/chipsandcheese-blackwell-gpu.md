---
tags: [source, gpu, nvidia, blackwell, gb202, 微架构]
date: 2026-04-27
sources: 1
---

# Blackwell: Nvidia's Massive GPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 6 月的文章，以 RTX PRO 6000 Blackwell 为测试平台，对 GB202 die 的微架构逐层解剖，并与 AMD RX 9070（RDNA4）进行对比。

## 摘要

文章从工作分发机制出发，系统测量了 GPC:SM = 1:16 的规模代价、SM 前端两级指令缓存（L0i 32 KB + L1i 128 KB）、执行单元重组为单路 32-wide pipe、SM 内 128 KB L1/Shared Memory 的带宽路径、以及 GPU 级 L2 延迟回退（约 130 ns，Ada 为 107 ns）。最终以 FluidX3D 实测作为综合佐证，结论是 Blackwell 以数量取胜——188 SM 对比 AMD 的 28 WGP，弥补单核效率劣势，并在整机算力、缓存总量和 VRAM 带宽上全面碾压 RDNA4。文章还记录了 Blackwell 新增的同队列图形/compute 重叠执行能力，以及光线追踪三角形相交速率翻倍。

## 关键要点

- GB202 面积 750 mm²，921 亿晶体管，192 SM（RTX PRO 6000 启用 188 个，600 W TDP）
- GPC:SM = 1:16（Ada 为 1:12），短 wave 场景下分发速率成瓶颈
- 新增同队列图形/compute 重叠，消除 subchannel switch 强制等待
- L1i 约 128 KB（约 8K 条指令）；L0i 32 KB/partition，与 Ada 相同
- 主执行管道重组为 32-wide 单路，避免单一类型指令流导致停顿
- SM 内 128 KB L1/Shared Memory 不变（自 Ampere 以来），单路 128 B/cycle
- L2 约 64 bank，8.7 TB/s，延迟约 130 ns（较 Ada 的 107 ns 回退）
- VRAM 延迟约 329 ns，高于 RDNA4 的 254 ns；512-bit GDDR7 带宽大幅领先 AMD
- 光线三角形相交速率是 Ada 的两倍，支持 Opacity Micromaps

## 链接到的概念

- [[rendering/blackwell-gb202-architecture]]
- [[rendering/rdna4-architecture]]
- [[rendering/ada-lovelace-architecture]]
- [[computer-systems/gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/blackwell-nvidias-massive-gpu
- 本地：`raw/articles/chipsandcheese.com/2025-06-29_blackwell-nvidias-massive-gpu.md`
