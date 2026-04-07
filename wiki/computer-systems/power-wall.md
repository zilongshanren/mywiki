---
tags: [计算机体系结构, 历史]
date: 2026-04-05
sources: 1
---

# 功耗墙（Power Wall）

**动态功耗公式**：

```
P_dynamic = α × C × V² × f
```

- α：activity factor（切换频率）
- C：电容
- V：电压
- f：时钟频率

**电压平方影响**——不能无限提高频率而不让芯片烧掉。

## 物理极限

CMOS 工艺下，频率 ~3-5 GHz 后再提就需要大幅拉高电压，V² 项爆炸，热密度超过硅的散热能力。

## [[dennard-scaling|Dennard Scaling]] 崩塌前后

- **崩塌前**：缩小晶体管 = 降电压 = 频率免费升。
- **崩塌后**：电压不能再降，频率被热封死。

## 对软件的影响

**免费午餐结束**——同代码不会因新 CPU 自然变快。必须：

- 并行化（多核）
- 向量化（SIMD）
- 专用化（GPU 等）
- 数据布局优化（SoA）
- 能效优化（移动端 TDP 紧张）

## 移动端的体现

手机 TDP 预算只有 4-8W。10 分钟后 thermal throttling 可把 120fps 压到 40fps。这就是为什么**移动端优化的核心是带宽/功耗**，而非 ALU。

## 相关

- [[dennard-scaling]]
- [[cpu-performance-formula]]
- [[amdahls-law]]
- [[tbdr-vs-imr]]——移动端 GPU 架构正是对功耗墙的回应

## Sources

- [[sources/caqa-day02]]
