---
tags: [source, memory-allocation, fragmentation, algorithms]
date: 2026-04-19
sources: 1
---

# A Metric for Memory Fragmentation（Adam Sawicki）

[[adam-sawicki]] 发表于 2022 年 4 月的文章，提出一个给单块内存"碎片程度打分"的简洁公式——`F = 1 - (√Σf² / Σf)²`，用 L2/L1 范数比衡量空闲区间大小的分布均衡性。

## 摘要

Sub-allocator 经常要决定"现在值不值得做一次 defragmentation"，所以需要一个能量化碎片度的指标。Adam 先列出期望性质（归一到 0..1、与单位/碎片总量/分配个数无关、单个空闲区间给 0、均匀分散接近 1），然后否掉两个 naive 方案：只看最大空闲区会忽略剩下结构；只数空闲段数又对小洞过度敏感。他的公式取所有空闲区间大小的平方，加起来开方，除以总空闲量，再 `1 - x²` 翻面：`Quality = Σf²; QualityPercent = √Quality / Σf; F = 1 - QualityPercent²`。数值上 `[1000]→0`，`[500,500]→0.5`，20 个等大段 `→0.95`；小洞对大主结构影响极小（`[200,800]→0.32`，加四个 1 元素只升到 0.3254）。局限是：n 个等大段最多到 `(n-1)/n` 永不到 1，且只度量单块，跨 heap 的"把几乎空的块搬空还给系统"是另一个问题。公式作者自述是独立推导，后来 google 发现 `umm_malloc` 早有人提过。

## 关键要点

- 碎片度量应与"碎片绝对量"和"分配个数"解耦。
- `sqrt(Σx²) / Σx` 本质是 L2/L1 范数比，衡量分布集中度。
- 与只看最大空闲区或只数空闲段数比，该公式兼顾"主结构"与"小洞"。
- 单块度量 ≠ 全 allocator 策略；跨块时"清空某个 heap 还系统"是不同目标函数。
- Adam 在 VMA / D3D12MA 中以此类指标判断 defrag 时机。

## 链接到的概念

- [[a-metric-for-memory-fragmentation]]
- [[vulkan-memory-allocation]]
- [[d3d12-memory-allocator]]

## 原文

- 链接：https://asawicki.info/news_1757_a_metric_for_memory_fragmentation
- 本地：`raw/articles/asawicki.info/2022-04-06_a-metric-for-memory-fragmentation.md`
