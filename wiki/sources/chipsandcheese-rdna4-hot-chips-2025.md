---
tags: [source, gpu, amd, rdna4, hot-chips-2025, 微架构]
date: 2026-04-27
sources: 1
---

# AMD's RDNA4 GPU Architecture at Hot Chips 2025（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 9 月的文章，报道 AMD 在 Hot Chips 2025 上的 RDNA4 官方架构演讲，并结合独立测试（媒体引擎质量评测、多显示器功耗实测、RGP 帧捕获对比）加以验证和补充。

## 摘要

文章覆盖 RDNA4 的媒体引擎改进（H.264/H.265/AV1 低延迟编码质量和速度）、Display Engine 的多显示器空闲功耗优化（FreeSync 动态刷新率降频）、计算侧的标量 FP 指令和 Split Barrier 新特性、内存子系统（L2 扩至 8 MB，去除 L1 中间层，Infinity Cache 透明压缩改进）、SoC RAS 特性，以及 AMD 在 RDNA4 中如何通过 Infinity Fabric 延续 CPU 侧设计经验。文章结尾强调 RDNA4 在效率而非规模上的取舍——放弃顶端竞争，以较小 die 和适度带宽实现接近上代高端的性能。

## 关键要点

- RDNA4 最大 L2 为 8 MB（RDNA3：6 MB，RDNA2：4 MB），有利于光线追踪 BVH 遍历
- 去除 L1 中间缓存层，Chester 推测是因为 L1 命中率长期偏低（RDNA1 常 <50%），面积不如用于 L2
- 标量 FP 指令（add/mul/FMA/min-max/convert），延迟 4 cycle（向量为 5 cycle）
- Split Barriers：s_barrier_signal + s_barrier_wait 分离，减少屏障空转
- Infinity Cache：16 个 CS 模块，每个 4 MB，合计 64 MB；支持 DVFS，IF 带宽约 2.5 TB/s
- 媒体引擎：低延迟 VBR 下 VMAF 分数提升，H.264 文字保留更佳，编码速度 ~200 FPS
- Display Engine：支持 FreeSync 动态降频空闲，RDNA4 多屏场景待机功耗显著低于 RDNA2
- RIS（Radeon Image Sharpening）在 Display Engine 中硬件实现，不消耗 GPU 算力
- 单片（monolithic）设计：AMD 评估后认为 RDNA4 规模不需要 chiplet

## 链接到的概念

- [[rendering/rdna4-architecture]]
- [[rendering/infinity-cache-efficacy]]
- [[rendering/rdna3-architecture]]
- [[computer-systems/infinity-fabric-loaded-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-rdna4-gpu-architecture-at-hot
- 本地：`raw/articles/chipsandcheese.com/2025-09-13_amds-rdna4-gpu-architecture-at-hot-chips-2025.md`
