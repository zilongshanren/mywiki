---
tags: [source, cpu, intel, sapphire-rapids, golden-cove, avx512, amx, server, emib]
date: 2026-04-27
sources: 1
---

# Sapphire Rapids: Golden Cove Hits Servers（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 3 月的文章，通过 Intel Developer Cloud 和 Google Cloud Platform 对 Xeon Platinum 8480（Sapphire Rapids）进行微基准测试，评估其相对于 Golden Cove 客户端版本和 AMD EPYC 的变化。

## 摘要

Sapphire Rapids（SPR）在 Golden Cove 核心基础上增加了 AVX-512 支持（两个 512-bit FMA 单元）、AMX 矩阵加速以及加密/压缩加速器。文章的核心发现是：SPR 为了在单片设计内塞入 56 核，付出了沉重的缓存性能代价——L3 延迟比 Ice Lake SP 退步约 33%（约 33 ns），跨 die 的 EMIB 互联使 mesh 流量复杂度大幅上升。作为对比，AMD EPYC 的"分而治之"策略（每 CCD 独立 L3）规避了巨型互联问题，V-Cache 方案更在保持低延迟的同时提供超高容量。SPR 在 AVX-512 重度工作负载（向量带宽、矩阵运算）和统一 L3 的灵活性上有优势，但在通用服务器场景中难以撼动 AMD 的地位。

## 关键要点

- L2 缓存从 Golden Cove 客户端 1280 KB 升至 2 MB，但 L2 延迟从 15 周期增至 16 周期
- SPR L3 延迟约 33 ns，比 Ice Lake SP 退步 33%；4 KB 页面下有效 L3 延迟最高达 48.5 ns
- 两个 512-bit FMA 单元：一个由 port 0/1 的两个 256-bit 单元融合而成，另一个独立位于 port 5
- AMX 加速矩阵乘法，对 AI 推理/训练工作负载有针对性优势
- 向量寄存器文件：约 240 个 512-bit 宽重命名槽，与 Golden Cove 客户端略低（确认官方幻灯片数据）
- 前端带宽在代码 footprint 超出 L2 后急剧下降，L3 取指性能明显弱于 Golden Cove 和 Zen 3
- Minecraft 服务器测试：启动时间优秀，chunk 生成落后（受限于低云端时钟 3 GHz）

## 链接到的概念

- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/avx512-cache-efficiency]]
- [[computer-systems/numa-multi-socket-design]]
- [[computer-systems/mcm-gpu-design]]

## 原文

- 链接：https://chipsandcheese.com/p/a-peek-at-sapphire-rapids
- 本地：`raw/articles/chipsandcheese.com/2023-03-12_sapphire-rapids-golden-cove-hits-servers.md`
