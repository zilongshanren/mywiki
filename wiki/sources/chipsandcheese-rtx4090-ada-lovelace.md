---
tags: [source, chipsandcheese, nvidia, gpu, ray-tracing, dlss, rtx4000]
date: 2026-04-27
sources: 1
---

# Nvidia's RTX 4090 Launch: A Strong Ray-Tracing Focus（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 9 月的文章，分析 Nvidia Ada Lovelace 架构（RTX 4000 系列）发布时的技术重点。

## 摘要

Ada Lovelace 的战略重心在于光线追踪+AI 超采样的深度绑定：三角形求交速率翻倍（已连续三代提升）、Shader Execution Reordering（SER）改善 RT 负载并行度、以及 DLSS 3 引入帧生成能力。文章详细分析了 BVH 胖/瘦结构与 GPU 特性的匹配关系，解释了为何增加三角形吞吐量可以让 BVH 做得更胖从而规避缓存延迟。DLSS 3 帧生成需要极高张量算力（FP16 tensor 与 FP32 向量比值提升至 16:1），绑定 Lovelace 专属。光栅化方面，4090 在 AC Valhalla 测试中提升约 50%（理论 FP32 翻倍），符合实际应用非全程计算绑定的预期；AD102 引入约 96 MB L2 缓存弥补内存带宽增速差距。同期预告了 AMD RDNA 3 的双发射 VOPD 指令和 LDS 加速 BVH 遍历。

## 关键要点

- Ada Lovelace 三角形求交速率第三次翻倍，BVH 可做得更胖
- SER 对 RT 工作的重排序机制，Nvidia 类比为 CPU 乱序执行（但原理更接近 warp 组织优化）
- DLSS 3 帧生成：tensor:vector = 16:1，仅限 Lovelace
- AD102 96 MB L2 缓存缓解带宽压力
- RDNA 3 预计引入 VOPD 双发射和 LDS BVH 栈指令

## 链接到的概念

- [[ada-lovelace-architecture]]
- [[gpu-latency-hiding]]
- [[gcn-wave-occupancy]]

## 原文

- 链接：https://chipsandcheese.com/p/nvidias-rtx-4090-launch-a-strong-ray-tracing-focus
- 本地：`raw/articles/chipsandcheese.com/2022-09-22_nvidias-rtx-4090-launch-a-strong-ray-tracing-focus.md`
