---
tags: [渲染, 路径追踪, GPU, 历史, 非偏置渲染]
date: 2026-04-19
sources: 1
---

# GPU 非偏置渲染器大爆发（2010）

2010 年是消费级 GPU 上**非偏置（unbiased）路径追踪**产品化的元年。在此之前，Octane、iray、V-Ray RT 之类的名字要么还是 CPU 离线渲染器，要么还停留在演示 demo。[[sam-lapere|Sam Lapere]] 在 2010-01 的博客上把当时这场"tsunami"列成了一张清单，今天回看是难得的一手史料。

## 2010 年初同时出现的 GPU 渲染器

- **V-Ray RT GPU**（Chaos Group, CUDA）：2009 Siggraph 公布
- **iray**（mental images / NVIDIA）：2009 GTC 上演示，当时跑在 **15 张 Tesla** 上
- **LuxRender OpenCL / smallLuxGPU**（David Bucciarelli）：2009 年 12 月放出
- **Octane Render**（Refractive Software）：2010 年 1 月出现，由前 LuxRender 主程开发，单张 **GTX 260** 上演示
- **Arion**（RandomControl / Fryrender）：hybrid GPU/CPU unbiased
- **Brigade** / OTOY 的 raytraced Ruby demo：把 GPU 路径追踪推到实时游戏演示

Lapere 还按压力传导预测，Bunkspeed、Indigo Renderer、Maxwell Render、Kerkythea/Thea 很快会跟进。

## 为什么是 2010？Larrabee 的真空

2009 年 12 月 Intel 宣布 [[larrabee-cancellation|Larrabee 消费 GPU 推迟/取消]]，对渲染器公司是一次关键分叉：

- 之前业内普遍在等 Larrabee——"多核 x86 的 GPU"听起来比把渲染器硬塞进 NVIDIA GPU 的 SIMT 与受限显存容易得多；
- Larrabee 死后，继续**只做 CPU 版本**就意味着交出市场。于是原本观望的厂商集体公布 GPU 加速计划。
- 这一轮觉醒靠的是几个存在证明：**OptiX（NVIRT）**、V-Ray GPU、iray 和 OTOY 的 Ruby demo，它们让"没做过 GPGPU 的程序员"相信 ray casting 与 path tracing 在 GPU 上确实快。

## 非偏置 vs 有偏置

术语 *unbiased* 在当时的市场语言里几乎等价于"Monte Carlo 路径追踪 + 不做 cache / irradiance map / photon map 近似"。卖点是**同一个 render core 同时负责 preview 和最终出片**——Arion 和 Octane 都特别强调这一点。这是与传统 offline 渲染（preview 是光栅化，final 是 photon mapping）的最大区别。

## 后来的延伸

这条线最终长成两条脉络：
- 商业产品线：Octane → OTOY 生态 → NVIDIA 的 [[nvidia-omniverse|Omniverse]]
- 独立研究线：Brigade → Brigade 2 → [[lighthouse-2-optix|Lighthouse 2]]（Jacco Bikker）

2010 的一众 GPU 渲染器与 [[path-tracing-basics|路径追踪基础]]和 [[path-tracing-monte-carlo|蒙特卡洛采样]]一起，是 RTX 时代"实时全局光照"工业化的起点。

## 相关

- [[sam-lapere]]
- [[lighthouse-2-optix]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[otoy-cloud-rendering]]
- [[nvidia-omniverse]]

## Sources
- [[sources/raytracey-2010-gpu-renderer-landscape]]
- [[sources/raytracey-fermi-optix-benchmark]]
