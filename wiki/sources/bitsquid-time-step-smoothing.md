---
tags: [source, bitsquid, 游戏循环, 帧步长]
date: 2026-04-19
sources: 1
---

# Time Step Smoothing（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 10 月 Bitsquid Blog。谈变步长游戏循环里"用上一帧 `elapsed_time()` 直接推进下一帧"为什么不对，以及 Bitsquid 采用的滑动平均 + 离群值剔除策略。

## 摘要

变步长循环 `dt = elapsed_time(); update_game(dt);` 在概念上成立，但真正影响玩家观感的是 **帧被画到屏幕上的时刻**，不是 **模拟开始的时刻**——两者之间有抖动的 latency，而这段 latency 就是 `elapsed_time()` 波动的来源。如果能预测下一帧耗时就能抵消这段抖动，但完美预测不可能。Bitsquid 的默认策略：保留最近 11 帧 `dt` → 去掉两高两低的离群值 → 对剩 7 个取均值 → 再向上一帧 `dt` 做 lerp，叠加一层平滑。另外一个目标是**让步长本身不震荡**——因为 gameplay 代码（摄像机跟随、弹簧、插值）在剧烈振荡的步长下会自己开始抖。锯齿式的 zig-zag 帧率一般是引擎/驱动 bug，应该去修而不是去适应。需要与墙钟同步（网络）时，累积 **time debt** 慢慢还。引擎不规定 fixed/variable/smoothed 中任何一种，让游戏自己选 policy。作者在评论里老实承认这篇文章是**事后合理化**——他先发现加平滑手感更好，然后才坐下来想为什么。

## 关键要点

- 变步长的 `dt` 是前一帧从"开始模拟"到"开始模拟下一帧"的间隔，但 **玩家看到的是 frame 被送显的时刻**；两者间的 latency 抖动就是 `dt` 变化的主要来源。
- 滤波的目标之一：**更好地预测下一帧要花多长时间**。
- 滤波的目标之二：**让步长本身不震荡**——避免 gameplay 在震荡步长下产生二阶振荡。
- 默认算法：11 帧历史 → 丢两高两低 → 剩 7 帧取均值 → 对上一帧 `dt` 做 lerp。
- **不要为 zig-zag 帧率做特化**：通常是引擎/驱动 bug 的征兆，且震荡步长对 gameplay 有毒。
- **Time debt**：每帧 `debt += elapsed - taken`；还账 `take += f * debt`（f≈0.1）。
- 引擎不强制 policy：`set_time_step_policy()` 把选择权交给游戏代码。
- God of War 3 工程师在评论里给了反数据点：三缓冲 + VSync 下故意用**未滤波** CPU 时间推进反而手感更好——"平滑 vs 跳变"没有可量化最优，全靠玩着感觉。

## 链接到的概念

- [[variable-timestep-smoothing]]
- [[fixed-3000fps-gameplay-simplicity]]
- [[frames-in-flight]]
- [[soft-real-time]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/10/time-step-smoothing.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-10-18_time-step-smoothing.md`
