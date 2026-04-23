---
tags: [source, 帧率, 延迟, 运动模糊, 玩家感知, 工程传播]
date: 2026-04-19
sources: 1
---

# Tell the Internet That You're Not a Moron（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 3 月——借 EA《Fight Night Champion》从 60fps 降到 30fps gameplay 引发的舆论反弹，讲一条很工业的观察：**Frequency is NOT latency**，并顺带主张工程做了取舍应当大方解释、而不是抛个数字给网民乱吵。

## 摘要

前作《Fight Night Round 4》本就 60fps，画面已被高度评价。Champion 降到 30fps 被媒体读作「为了画面牺牲手感」。Pesce 揭示内部实情：

- 项目从 pre-production 就开始做 **30fps + 正确运动模糊** 的 AE 原型，再做引擎内原型，再做盲测。
- 物理仍然 120Hz、游戏逻辑 60Hz，只有渲染是 30Hz——**各层频率按各自需要设定**，不是一个统一数字。
- 运动模糊是 **skinned-silhouette-aware** 的光流模糊；早期用 Photoshop 模拟的截图还不如真机效果。
- 盲测结果：多数测试者更偏好 30fps 版本——「出拳更有力、更电影感」。
- 但公布帧率数字后，网民立刻反对——**不看东西，只看数字**。

Pesce 在评论区跟网友反复强调一句：**FPS 只给出延迟的下界，现代 AAA 游戏几乎都在 CPU / GPU / 输入 / 合成上叠几帧缓冲，所以 60fps 游戏完全可能比另一个 30fps 游戏响应更慢**。要找一个真·无缓冲的 60fps AAA 几乎不可能。

结尾是一条工程传播观：**做了取舍就负责解释**；否则互联网默认你是白痴。

## 关键要点

- **FPS != 延迟**：端到端延迟 = 输入 + 逻辑 + 渲染 + 提交 + GPU + 显示 + 手柄——每一段都可能有 buffer。
- **各子系统频率可以独立设**——Fight Night 用了三种频率：120 / 60 / 30。
- **运动模糊正确写就能补偿帧率感知**——配合光流、配合 skinned 轮廓保护；soap opera effect 反而是廉价 temporal resample 带来的（另一个问题）。
- **盲测 > 数字**——工程决策应由盲测驱动，但对外沟通会输给数字党。
- 对照 [[frame-pipeline-latency]] —— 那篇讲「引擎内部到底堆了几层 buffer」；本文讲「为什么大众视角的帧率崇拜是错位的」。

## 链接到的概念

- [[frequency-is-not-latency]]
- [[frame-pipeline-latency]]
- [[cpu-gpu-pipelining-input-lag]]
- [[stable-fps]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/03/tell-internet-that-youre-not-moron.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-03-07_tell-the-internet-that-you-re-not-a-moron.md`
