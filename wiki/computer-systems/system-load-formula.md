---
tags: [公式, UI, 度量, 数值]
date: 2026-04-19
sources: 1
---

# 综合系统负载的数学公式

给你 N 个子系统，每个有 0…1 的负载（CPU 忙率、GPU 忙率、内存占用、飞船引擎温度……），怎么合成一个"整体负载"数字？[[adam-sawicki|Adam Sawicki]] 2026 年初整理的 math puzzle，继承了他 2022 年[内存碎片度量](https://asawicki.info/news_1757_a_metric_for_memory_fragmentation)的同一套玩法：列需求、试公式、配交互 demo。

## 三条需求

1. **单调**：任一输入增加，输出不减（或至少不减）
2. **饱和即饱和**：只要有一个输入达到 1，整体就到 1
3. **全部可见**：每个输入的变化都应该影响输出（不是只看最大那个）

## 四个候选

1. `AVERAGE(input[i])`——满足 1、3；但要所有输入都 =1 才能到 1，违反 2
2. `MAX(input[i])`——满足 1、2；但只看最大的那个，违反 3
3. **Inverse product**："headroom 相乘"：`output = 1 − ∏(1 − input[i])`
   - 三条全满足；几何解释：把"剩余余量"相乘再反过来
   - **缺点**：对低输入过于悲观——多个 0.3 相乘出来已经接近 1，用户会觉得面板一直在报警
4. **混合**：`(AVERAGE + output1) * 0.5`
   - 把 inverse product 与 average 50/50 混，压低低输入时的视觉噪声
   - 仍满足三条需求

## 关键经验

- 几乎所有"多通道合成一个指标"的 UI 问题都能套这个框架——风险仪表盘、团队健康度、飞船 HUD、CI pipeline 整体健康度
- **先把需求写成数学条件**再挑公式，而不是反过来
- 数值公式要配**可拖动的交互 demo**：拖滑块比看图表更能暴露公式在极端情况下的怪异行为

## 相关

- [[adam-sawicki]]
- [[cpu-performance-formula]]
- [[amdahls-law]]

## Sources

- [[sources/asawicki-system-load-formula]]
