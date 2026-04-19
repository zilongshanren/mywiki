---
tags: [source, ui, ux, game-design, benui]
date: 2026-04-19
sources: 1
---

# UI as Communication（Ben UI）

[[ben-ui]] 的一篇博客，把游戏 UI 作为"把想法从游戏搬进玩家脑袋"的通道来拆解，列出可用的传达媒介与其优缺点。

## 摘要

文章提出一个设计视角：先想"如何传达"，再想"传达什么"。作者按"理解速度"和"信息容量"这两个维度列出十种传达媒介——尺寸、位置、形状、图标、亮度/颜色、纹理、声音、运动、震动、文字——每种都有适用场景与可达性盲点：颜色对 8% 色盲用户失效，声音对失聪/静音玩家失效，震动对不支持设备的玩家失效，因此关键信息不能只压一个通道。反面示例是菜单里把"退出"和"开始游戏"做成同尺寸，违反"相对尺寸传达相对重要性"的基本约定。要传达的内容则分为重要性、可交互性、顺序、设定与主题、世界观价值几类。

## 关键要点

- UI 先是传达工具，再是视觉设计对象。
- 媒介有优先级：尺寸/位置 > 形状/颜色 > 纹理/运动 > 文字。
- 大小承载相对重要性；位置承载顺序（跟玩家母语阅读方向走）；形状能承载世界观（Splatoon vs Mario）。
- 文字信息量最大但阅读最慢、对语言/年龄/学习能力敏感，属于"最后一公里"而不是主通道。
- 关键信息必须冗余：颜色 + 形状，声音 + 字幕，震动 + 视觉。
- 引用 Zach Gage《Building games that can be understood at a glance》、Steph Chow 关于太平洋岛屿 UI 形状的 GDC 演讲。

## 链接到的概念

- [[ui-as-communication]]
- [[ux-opinions-checklist]]
- [[ben-ui]]

## 原文

- 链接：https://benui.ca/blog/ui-as-communication/
- 本地：`raw/articles/benui.ca/2026-01-01_ui-as-communication.md`
