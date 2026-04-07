---
tags: [游戏引擎, gea]
date: 2026-04-05
sources: 1
---

# 软实时（Soft Real-Time）

**必须在时间约束内完成，但偶尔违反是可接受的**。

## 硬实时 vs 软实时

| | 硬实时 | 软实时 |
|---|---|---|
| 例子 | 起搏器、导弹控制、ABS 刹车 | 视频游戏、流媒体 |
| 违反时限 | 系统失败 / 人命危险 | 体验降级 |
| 设计重点 | 最坏情况延迟 | 大部分情况的平均延迟 |

## 游戏的时间约束

- 60 fps → **16.67ms 帧预算**
- 120 fps → 8.33ms
- VR 90 fps → 11.11ms（且必须**稳定**，卡帧引起眩晕）

## 软实时的含义

- 偶尔掉帧不会让游戏崩溃，只是卡顿。
- 不需要追求硬实时的最坏情况保证。
- 但"偶尔"不能太频繁——30 秒卡一次玩家可以忍，每秒卡一次不可以。

## 引擎设计后果

- **帧率是核心约束**，超过预算必须剪裁：降 LOD、关粒子、降分辨率。
- **Dynamic Scaling**：UE5 Variable Rate Shading、Unity DLSS/FSR。
- **Performance Budget**：不是一次性的"跑多快"，是"每帧必须稳定在 X ms 以内"。

## 和实时渲染的关系

实时渲染是软实时的**GPU 层面**体现：帧预算驱动所有 [[rendering-pipeline|渲染管线]]的优化决策。

## 相关

- [[game-engine]]
- [[rendering-pipeline]]
- [[latency-vs-throughput]]

## Sources

- [[sources/gea-day01]]
