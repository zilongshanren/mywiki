---
tags: [source, cpu, amd, vcache, 9800x3d, zen5, packaging]
date: 2026-04-27
sources: 1
---

# AMD's 9800X3D: 2nd Generation V-Cache（George Cozma / Chips and Cheese）

[[people/george-cozma]] 发表于 2024 年 11 月的评测，重点分析第二代 V-Cache 封装改变及其性能影响。

## 摘要

第一代 V-Cache（Zen 3/4）将 SRAM die 叠放于 CCD 上方，需要两枚支撑 silicon die。第二代（9800X3D）将 SRAM die 翻转到 CCD 下方，消除了支撑 die，SRAM die 同时承担 CPU 核心的额外电源分配网络。关键收益是热阻大幅降低：散热器直接面对 CCD（不再隔着 SRAM die），9800X3D 在 95°C 下仍可维持 4.7 GHz 基础频率。电压耐受性也从第一代的 1.2V 提升至 1.4V（与标准 9700X 相同），核心间频率抖动从 ~70 MHz 收窄至 ~10 MHz。然而 300 MHz 的 boost 时钟差距（9700X vs 9800X3D）仍然存在，部分游戏仍可能偏好频率而非缓存容量。L3 延迟额外 4 cycle 惩罚与第一代相同，带宽几乎与非 V-Cache 版本持平。SPEC INT 测试中 9800X3D 反超 9950X（+500 MHz），FP 测试基本持平，两者差异主要由工作负载的内存绑定程度决定。

## 关键要点

- 封装颠倒（SRAM 置于 CCD 下方）：去除支撑 die，热阻显著降低，散热器直触 CCD
- 电压耐受上限 1.4V（与非 X3D 版本相同），核心频率一致性大幅提升（delta ~10 MHz）
- L3 命中额外 4 cycle 延迟（与第一代相同）；L3 带宽几乎与 9950X 持平
- SPEC INT 9800X3D 领先 9950X；FP 测试 503.bwaves（计算密集）9950X 领先，549.fotonik3d（内存密集）9800X3D 领先 7.5%
- 剩余痛点：boost 时钟较 9700X 仍低 300 MHz，对计算绑定游戏有负面影响

## 链接到的概念

- [[computer-systems/vcache-3d-die-stacking]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-9800x3d-2nd-generation-v-cache
- 本地：`raw/articles/chipsandcheese.com/2024-11-06_amd-s-9800x3d-2nd-generation-v-cache.md`
