---
tags: [source, game-development, procedural-generation, wfc, model-synthesis]
date: 2026-04-27
sources: 1
---

# Model Synthesis and Modifying in Blocks（Boris The Brave）

[[boris-the-brave]] 发表于 2021 年 10 月的文章，介绍 WFC 的前身 Model Synthesis（Merrell 2007 博士论文）及其分块修改（Modifying in Blocks）技术。

## 摘要

文章梳理了 [[model-synthesis]] 与 [[wave-function-collapse]] 的联系与区别：两者本质上是同一约束传播生成框架，WFC 在选格策略（最小熵启发）、Overlapped 模型以及工程易用性上有所提升。Model Synthesis 长期被忽视的原因主要是 3D 瓦片门槛高、官网曾下线多年，以及"WFC"名字更具传播力。

文章重点介绍 Modifying in Blocks：大规模生成时矛盾不可避免，简单重启和回溯均不能扩展到大面积输出。分块技术将生成区域划分为互相重叠的小块，每块独立求解，失败时只重启该块而非全局。关键在于每块的所有边界都被约束——已生成邻块提供相邻边约束，开放边固定为一组预定义的合法背景瓦片，保证每次求解"至少存在一个已知解"。

## 关键要点

- Model Synthesis 是 WFC 的学术前身，使用 AC-4 约束传播，核心洞察是"约束求解器 + 随机选择 = 约束生成器"
- WFC 在 MS 基础上增加了最小熵启发和 Overlapped 模型；两者能力相当，但 WFC 入门门槛低
- 分块修改通过"已知合法背景"使每块求解有退路，从而在大面积输出下保持可靠性
- 重叠块设计使固定背景最终被后续块覆盖，不影响最终视觉效果
- 参数调优（块大小、重叠度、重启阈值）仍较繁琐，限制了通用化

## 链接到的概念

- [[model-synthesis]]
- [[modifying-in-blocks]]
- [[wave-function-collapse]]
- [[arc-consistency]]

## 原文

- 链接：https://www.boristhebrave.com/2021/10/26/model-synthesis-and-modifying-in-blocks/
- 本地：`raw/articles/boristhebrave.com/2021-10-26_model-synthesis-and-modifying-in-blocks.md`
