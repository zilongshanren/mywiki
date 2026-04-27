---
tags: [source, chipsandcheese, cpu, intel, raptor-lake, cache, l2]
date: 2026-04-27
sources: 1
---

# A Preview of Raptor Lake's Improved L2 Caches（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 8 月的文章，基于 Raptor Lake 工程样品的实测数据，分析其 L2 缓存改进对 P-Core 和 E-Core 的影响。

## 摘要

Raptor Lake 将 P-Core（[[golden-cove-microarchitecture|Golden Cove]]）的 L2 从 1.25 MB 扩大到 2 MB，延迟增加 1 周期；将 [[gracemont-microarchitecture|Gracemont]] E-Core 的 L2 从 2 MB 加倍到 4 MB 且延迟不变（20 周期）。ChampSim 模拟显示 L2 miss 率分别下降约 14-16%，固定频率 IPC 提升不足 1%，但功耗节省可转化为更高的频率余量，整体收益因此大于 IPC 数字所示。E-Core 的受益尤其突出，因为其乱序深度不足以吸收 60+ 周期的 L3 延迟。

## 关键要点

- L1 无变化；L3 延迟对比 Alder Lake 略有改善但工程样品不做最终结论
- 更大 L2 减少环形总线流量，缓解 Intel 高频下 uncore 跟不上 core clock 的瓶颈
- 4 MB E-Core L2 在历史上相当于整台移动 Zen 2 设备的完整 L3
- 工程样品测试：P-Core 约 4.9 GHz，E-Core 约 3.72 GHz（非最终频率）

## 链接到的概念

- [[raptor-lake-l2-cache]]
- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[cache-power-efficiency]]

## 原文

- 链接：https://chipsandcheese.com/p/a-preview-of-raptor-lakes-improved-l2-caches
- 本地：`raw/articles/chipsandcheese.com/2022-08-23_a-preview-of-raptor-lakes-improved-l2-caches.md`
