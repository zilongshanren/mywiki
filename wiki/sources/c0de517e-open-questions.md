---
tags: [source, 渲染, 视觉感知, 艺术指导, 游戏开发]
date: 2026-04-27
sources: 1
---

# Open Questions（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2011 年 10 月的思考文章，探讨渲染质量与视觉感知之间的未解问题。

## 摘要

Pesce 以几个反直觉的游戏观察开篇：同一款游戏在 360 投影仪环境下令人震撼，在 PC 上却平庸；Mass Effect 2 在 PC 上反而比 360 更出色；Red Dead Redemption 技术指标弱于 Crysis 却在视觉冲击力上大幅胜出。这些现象促使他追问：决定渲染「好看」的究竟是什么？

他总结了自己观察到的几条经验模式，但坦承这些只是薄薄几行文字，整个行业对此知之甚少：混叠和高频噪声最快击碎沉浸感；30fps + 正确运动模糊比 60fps 裸跑更具电影感；帧率抖动在视觉繁忙的场景中比在安静场景中更被容忍；颜色、环境遮蔽和大气散射对体积感至关重要；高光/镜面叶瓣无处不在且必须有菲涅尔项；溢出暗边比亮晕更不显眼。

他的核心观点是：**渲染行业知道物理但不知道感知**。我们选择渲染技术的依据极其薄弱——更多靠艺术感觉而非感知科学。他呼吁从艺术驱动转向科学分析：可测量、可分享、可积累的视觉感知研究，而非依赖美术总监的主观判断。

## 关键要点

- 平台/播放环境（投影仪 vs 显示器）可以彻底改变感知质量，技术数字无法预测这一点。
- 低分辨率纹理在高分辨率下的负面效果被放大，反之高 AA + 艺术风格化在 PC 上效果更好（ME2 案例）。
- 延迟渲染可能损失了预计算光照对材质微妙表现的能力（Pesce 的质疑，非结论）。
- 感知驱动的 hack 比物理驱动的 hack 更有价值，但前者几乎没有文献。
- Holly Rushmeier 等人的感知渲染研究方向被点名为值得跟进。

## 链接到的概念

- [[rendering-perception-psychology]]
- [[deferred-rendering]]
- [[frequency-is-not-latency]]
- [[aliasing]]
- [[atmospheric-perspective]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/10/open-questions.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-10-26_open-questions.md`
