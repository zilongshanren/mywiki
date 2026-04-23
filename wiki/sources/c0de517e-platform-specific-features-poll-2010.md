---
tags: [source, 调研, 平台特性, 360, ps3, dx10, dx11]
date: 2026-04-19
sources: 1
---

# Platform specific features - poll results（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 9 月公布的一份 70 人投票结果：**你的引擎 / 游戏用到了哪些平台特定特性？** 多选题，合计超 100%。

## 摘要

**Xbox 360 top 3**：vertex shader 纹理采样 **30%**、custom vfetch **28%**、command buffer predication **20%**——都是**扩展图形管线可编程性**的底层接口。Tessellator (11%)、shader memwrite (12%)、L2 → GPU (5%) 则使用率低。

**PS3 top 3**：half-precision shader **41%**（最广泛）、SPU → GPU fast path **30%**、主存 / 本地内存带宽优化 **27%**。**SPU 渲染仅 10%**——_Killzone 3_ / _LBP_ 之类的 SPU rasterization 还未普及。

**DX10/10.1**：合计约 40%，每项两位数出头，**没有集中爆点**。**DX11** 刚发布不足一年，API 15% 最高，multithreaded rendering 仅 7%。

**「完全不用任何平台特性」24% + 「仅主机」21%**——跨平台抽象和主机独占各占半壁。

Pesce 自评：样本偏渲染工程师，所以使用率偏高；选项设计不全，other 比例高。这篇本质是**社区信号采集**，不做分析。评论区读者问投票问题是什么、怎么解读百分比，Pesce 一一回答。

## 关键要点

- **360 = 挤管线可编程性**，**PS3 = 挤精度 + SPU 通路**——两个平台的「好糖」形状不同。
- **DX10 没有集中爆点**，暗示它在主机压力下推进缓慢。
- **DX11 multithreaded 7%**——跨平台新路线至少还要 2 年才普及。
- **约一半项目**要么不用平台特性、要么只做主机优化——跨平台抽象层在 2010 年仍占半壁。
- 工业界**特性采纳曲线滞后官方发布 2–3 年**是普遍规律。
- 数据不做分析，意义在**快照**而非**结论**。

## 链接到的概念

- [[platform-specific-features-poll-2010]]
- [[tbdr-vs-imr]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/09/platform-specific-features-poll-results.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-09-12_platform-specific-features-poll-results.md`
