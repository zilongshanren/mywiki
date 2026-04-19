---
tags: [计算机体系结构, 可靠性]
date: 2026-04-05
sources: 1
---

# MTTF 与可靠性

**可靠性的量化指标**：

- **MTTF（Mean Time To Failure）**：平均故障前运行时间。
- **MTTR（Mean Time To Repair）**：平均修复时间。
- **MTBF = MTTF + MTTR**。
- **Availability = MTTF / MTBF**。
- **AFR（Annual Failure Rate）= (1 / MTTF) × 8760**（小时/年）。

## 九的含义

| Availability | 年停机 |
|---|---|
| 99%（两个九） | 3.65 天 |
| 99.9%（三个九） | 8.76 小时 |
| 99.99%（四个九） | 52.56 分钟 |
| 99.999%（五个九） | 5.26 分钟 |

**每多一个九，停机时间缩短 10 倍**——工程成本呈指数上升。

## SSD 例子

NVMe SSD 标称 MTTF 1.5M 小时 → AFR ≈ 0.584%。运营 1000 盘一年平均坏 5-6 块。

## 游戏开发应用

- **存档冗余**：Dark Souls 的三重备份降低 MTTR（保留多版本）。
- **云存档**：多地域降低丢失概率。
- **热更新回滚**：MTTR 最短化的工程实践。

## 相关
- [[memory-hierarchy]]
- [[virtual-memory]]
- [[electromigration-voltage-degradation]] — 电压/电流密度如何把 MTTF 砍掉的物理模型

## Sources

- [[sources/caqa-day02]]
