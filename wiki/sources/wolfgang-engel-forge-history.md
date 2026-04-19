---
tags: [source, graphics, forge, gpu-zen, 光线追踪, 行业观察]
date: 2026-04-19
sources: 1
---

# Catching Up / History of The Forge / GPU Zen / Ray Tracing / Holiday Dinner（Wolfgang Engel）

[[people/wolfgang-engel|Wolfgang Engel]] 2020 年 11 月的一篇混合随笔——公司管理 + [[the-forge-renderer|The Forge]] 的回顾 + GPU Zen 的定位调整 + 对 DXR 之争的 2020 年回望 + 居家办公时代的 Holiday 晚餐安排。文章风格很松弛，但对 Confetti 这条线的**技术线程演化**给出了权威注脚。

## 摘要

Engel 先解释自己 2018 之后为什么几乎不发博客——Confetti 规模扩张意味着他在处理 H1B / O1 签证、401k、房东、税务、IP / 普通律师、员工面试、Holiday 晚餐安排等事务；COVID 还让他多练两种武术（Gum Do 和太极）。剩下给技术的时间都流向了 The Forge 的 release notes。他把 release notes 本身定位成"博客替代品"——每次 release 都会写技术成败回顾，某种程度上比博客更有价值因为附带全量源码。

The Forge 的历史：Confetti 从成立第一天就有内部框架，作为公司"蜂巢意识"——每个被邀请贡献的人扩展它，然后所有人受益。2017 年决定推倒重写以拥抱新一代显式 API，2018 年初开源，命名为 *The Forge*。迄今已经在 AAA 定制引擎、编辑器 / 教育 app、商业框架底座里出货，还给 Supergiant 写了跑 *Hades* 的引擎（PC / macOS / Switch）。

关于 **GPU Zen**：Engel 直接点明立场转变——**「我现在认为 The Forge 比新一版 GPU Zen 更有用」**，因为它提供可跑、在出货游戏上验证过的代码，而不是「一段伪代码 + 一个公式」那种 presentation 式知识。GitHub 上的 The Forge 就是"下一代 GPU Zen"。将来会不会再出 GPU Zen 要看书本能提供 The Forge 提供不了的什么价值。

**Ray tracing**：他承认 2018 年的 DXR 博文在业内掀起了波澜，后来自己没时间继续推动这个议题；但在 advisory board / IP 项目中反复被提起，**行业"作为一个整体"最终成功让 RT 接口变得更开放**。Confetti 后来做过一次跨平台 RT 的 talk：把 macOS / iOS ray tracing runtime 扩展到和 DXR / RTX 功能对等，代码放在 GitHub——主要用于工具开发，也是跨平台游戏引擎的 RT 蓝图。

结尾一段写他组织**第一次 Skype 假日晚餐**的尝试——用 DoorDash 送餐、公司报销，按时区分批开几场，顺便看一下各家狗狗的近况。

## 关键要点

- **The Forge 的定位**：Confetti 内部 framework 的开源 / 重写版，2018 年推出；跨 DX12 / Vulkan / Metal / Linux / 主机
- **出货实战**：Supergiant *Hades* 的引擎在其上；AAA 定制引擎、编辑器、教育应用
- **"The Forge = 下一代 GPU Zen"**：Engel 明确把 source code 视为比 book chapter / talk slides 更有知识价值的媒介
- **Release notes 是他现在的博客替代品**——每次 release 都有长篇技术回顾
- **DXR 之争的 2020 年回望**：行业整体推动了更开放的 RT 接口；Confetti 写了一版能和 DXR/RTX 对等的 macOS/iOS runtime
- 对「公司规模扩大 → 个人输出下降」的**诚实记录**——这点对理解 2018-2020 行业信息流变化有参考价值

## 链接到的概念

- [[the-forge-renderer]]
- [[ray-tracing-api-debate]]
- [[hybrid-raytraced-shadows-reflections]]
- [[visibility-buffer]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2020/11/catching-up-history-of-forge-gpu-zen.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2020-11-20_catching-up-history-of-the-forge-gpu-zen-ray-tracing-holiday.md`
