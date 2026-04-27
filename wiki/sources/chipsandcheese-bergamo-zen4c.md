---
tags: [source, computer-systems, amd, zen4c, bergamo, server, epyc]
date: 2026-04-27
sources: 1
---

# AMD Bergamo 测试：Zen 4c 海量核心（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 6 月，借助 Hot Aisle 提供的双路 Bergamo 系统进行两周实测，全面评估 AMD 密度优先服务器 CPU 策略。

## 摘要

Bergamo 是 AMD 面向密度优先服务器市场的 EPYC，单路最多 128 核，使用与标准 Zen 4 相同的 IO die 和 Genoa 平台，但将 CCD 换成 Zen 4c 版本：每个 Zen 4c CCD 含两个 CCX，每个 CCX 有 8 核但 L3 削减为 16 MB（标准 Zen 4 为 32 MB），整体核密度约为 2×。[[zen4c-microarchitecture|Zen 4c]] 保持与 Zen 4 完全相同的 ISA 和微架构，仅在物理实现上优化面积与低频效率，代价是峰值频率降低。测试显示：单 CCX 比较时 Zen 4c 比标准 Zen 4 慢 4–37%（工作负载不同差异很大），但两核心的 CCD 总吞吐在 libx264 等并行负载下领先 69%。双路配置可达 256 核，跨 socket 延迟约 200 ns，DRAM 带宽接近 360 GB/s。

## 关键要点

- Zen 4c：同架构同 ISA，仅物理实现优化面积，约 2× 核密度
- Bergamo 单路 128 核，复用 Genoa IO die 和 DDR5 平台
- Zen 4c CCX L3 削至 16 MB，L3 命中率从 64.3% 降至 57.6%（libx264 测试）
- 单核性能：vanilla Zen 4 比 Zen 4c 快 4–37%；VCache 变体最快
- 多线程吞吐：Zen 4c CCD 比单 Zen 4 CCX 快 ~69%（libx264）
- DRAM 带宽约 360 GB/s（768-bit DDR5-4800，效率 ~78%）
- 跨 socket 延迟 ~200 ns，优于 Milan-X，劣于 Intel Sapphire Rapids（<150 ns）
- AMD 同架构策略节省了 ISA 兼容性和验证成本，与 Intel 双架构（P+E Core）形成对比

## 链接到的概念

- [[zen4c-microarchitecture]]
- [[amdahls-law]]

## 原文

- 链接：https://chipsandcheese.com/p/testing-amds-bergamo-zen-4c-spam
- 本地：`raw/articles/chipsandcheese.com/2024-06-22_testing-amds-bergamo-zen-4c-spam.md`
