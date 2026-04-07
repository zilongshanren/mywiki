---
tags: [source, 计算机体系结构, caqa]
date: 2026-04-05
sources: 1
---

# Computer Architecture Day 2 —— 存储层次与可靠性

CAQA 学习推送第 2 天。

## 摘要

**存储层次**：Registers → L1/L2/L3 → DRAM → SSD，延迟跨越 5 个数量级。**局部性原理**（时间+空间）。**AoS vs SoA** 对 cache 的影响。**MTTF/MTTR/AFR**、**可用性**。**动态功耗公式**与 **Dennard Scaling 崩塌**（~2004）导致**功耗墙**。

## 关键要点

- 存储延迟：Register 0c → L1 1-4c → L2 10-25c → L3 30-60c → DRAM 200-300c → SSD ~100kc。
- **局部性原理**：时间局部性 + 空间局部性。
- **AoS**（传统 OOP）cache 利用率 ~18.75%（含 padding）。**SoA**（ECS/DOTS）接近 100%。
- 一次 DRAM miss ≈ 100 次 L1 hit。
- **可用性 = MTTF / (MTTF + MTTR)**；三个九 vs 五个九差 100× downtime。
- **P_dynamic = α × C × V² × f**——电压平方影响。
- **Dennard Scaling 崩塌（2004）**：漏电流超越电压缩放收益，频率停滞 3-5 GHz。
- **功耗墙**：物理限制阻止进一步提频；逼出多核范式。
- Apple M1 GPU 173 GFLOPS/W vs RTX 3090 102 GFLOPS/W——能效优先。
- 移动游戏 TDP 4-8W，10 分钟 thermal throttling 可将 120fps 压到 40fps。

## 链接到的概念

- [[memory-hierarchy]]
- [[locality-principle]]
- [[aos-vs-soa]]
- [[dennard-scaling]]
- [[power-wall]]
- [[mttf-reliability]]

## 原文

- 链接到：[[raw/articles/computer architexture a quantitative approach/day02]]
