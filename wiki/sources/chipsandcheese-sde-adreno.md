---
tags: [source, gpu, qualcomm, adreno, snapdragon, igpu, laptop, mobile]
date: 2026-04-27
sources: 1
---

# The Snapdragon X Elite's Adreno iGPU（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 7 月的文章，通过微基准测试与游戏实测，对 Snapdragon X Elite 搭载的 Adreno X1（内部型号 Adreno 741）iGPU 进行横向评测，竞品为 Intel Meteor Lake Xe-LPG 与 AMD Phoenix RDNA 3 iGPU。

## 摘要

Adreno X1 在浮点算力（FP32/FP16）上与 Meteor Lake 接近，借助 LPDDR5X 128-bit 宽内存总线在 DRAM 带宽上小幅领先竞品。独特的 GMEM 可灵活复用为 Tile Buffer、局部内存或颜色缓存，延迟表现接近 AMD/Intel。然而多项弱点明显：L1 纹理缓存仅 2 KB（最小）、缓存带宽远落后竞品、wave64/128 宽向量对寄存器占用形成压力、INT64 性能极差、FP64 不支持。在 Cyberpunk 2077 游戏测试中，1080p 仅 24 FPS，落后 AMD Phoenix 与 Intel Meteor Lake。驱动成熟度是另一大软肋：部分游戏无法启动，更新驱动后稳定性反而下降；驱动包无统一安装器，用户体验粗糙。整体结论：硬件潜力可见，但软件生态仍需大量投入。

## 关键要点

- Adreno X1 = Adreno 741，是 Adreno 730（Snapdragon 8+ Gen 1）的扩展版
- 每个 uSPTP 拥有 192 KB 寄存器文件（较 Adreno 730 的 64 KB 提升 50%）
- 新增三个 128 KB 集群缓存（Cluster Cache），形成四级缓存层次
- GMEM 扩展至 3 MB，可多用途复用，是 TBDR 架构的核心优势
- 不支持 DirectX 12 Ultimate，光线追踪仅限 Vulkan API

## 链接到的概念

- [[adreno-x1-igpu-architecture]]
- [[adreno-640-architecture]]
- [[qualcomm-kryo-microarchitecture]]
- [[xe-lpg-igpu-architecture]]
- [[hsr-tbdr]]

## 原文

- 链接：https://chipsandcheese.com/p/the-snapdragon-x-elites-adreno-igpu
- 本地：`raw/articles/chipsandcheese.com/2024-07-04_the-snapdragon-x-elites-adreno-igpu.md`
