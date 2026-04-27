---
tags: [source, cpu, qualcomm, arm, 服务器, 微架构, aarch64]
date: 2026-04-27
sources: 1
---

# Qualcomm's Centriq 2400 and the Falkor Architecture（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 5 月 29 日的文章，对 Qualcomm Centriq 2452 系统中的 Falkor AArch64 服务器核进行了完整的微基准测试分析，由 Corellium 提供测试系统。

## 摘要

文章系统性地分析了 Falkor 的双级指令缓存（24 KB L0 + 64 KB L1，共 88 KB，BTIC 零泡沫跳转）、多历史长度方向预测器（类 TAGE）、受限的 3+1 宽度重命名器、写穿 L1D 加 WCC 写合并侧缓、双级 TLB（含 non-final 和 stage-2 TLB 用于虚拟化）、512 KB L2 + 60 MB L3 + 分段环形总线。SPEC CPU2017 对比显示 Falkor 领先 Cortex A72 21.6%（INT）和 53.4%（FP）。文章最后评估了 Centriq 商业失败的原因（ARM 生态不成熟 + 缺乏 Linux 生态承诺 + 面对 Skylake-X 的性能差距），并提及 Qualcomm 2025 年重返服务器市场的计划。

## 关键要点

- Falkor：4-wide（实际约 3+1）AArch64，5th in-house Qualcomm core
- 88 KB 双级指令缓存，当时领先行业（被 Apple M1 超越前）
- 写穿 L1D + WCC 侧边写合并，parity 而非 ECC 保护 L1D
- L2 512 KB，15-17 周期；L3 60 MB，>40 ns 延迟，6 DDR4 通道 128 GB/s
- 分段环形总线（双方向 ×2），24 duplex + 12 L3 slice
- SPEC INT 领先 A72 22%，落后 Skylake 明显；向量能力弱（128-bit 拆 2 micro-op）
- 不支持多路 NUMA，仅 32 PCIe lanes，定位 mainstream cloud

## 链接到的概念

- [[qualcomm-falkor-centriq-microarchitecture]]
- [[qualcomm-kryo-microarchitecture]]
- [[neoverse-n1-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/qualcomms-centriq-2400-and-the-falkor
- 本地：`raw/articles/chipsandcheese.com/2025-05-29_qualcomm-s-centriq-2400-and-the-falkor-architecture.md`
