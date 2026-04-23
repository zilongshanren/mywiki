---
tags: [source, game-development, 热重载, 工具链, 调研]
date: 2026-04-19
sources: 1
---

# Live-editing poll results（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 5 月公布的博客投票结果：**你（或你的游戏 / 引擎）用哪种 live-editing？** 75 人参与，结果被整理成 8 档分类，每一档都带 Pesce 自己的吐槽注释。

## 摘要

结果分布：None 16% / File swap 41% / Script swap 41% / External tools 29% / Tool + RPC live-update 21% / Engine-in-tool DLL 18% / Tool ↔ Game 反射 RPC 9% / In-game editor 10% / Code hot-swap 9%。多选项导致合计超过 100%，评论区有人反驳，Pesce 回应 overlapping ≠ mutually exclusive。

Pesce 的核心判断：**文件热换最普遍**（最好写）；**外部工具很多**，但常常变成「平行的好用世界」而不解决原问题；**真正关心代码迭代的人极少**（仅 9%），而他认为这是整张表里最重要的一档——「有了它其他都不重要」。评论里 Nicolas 追问代码热换怎么做，Pesce 给出一份短短的工程清单，重点是**立项时就把热重载当目标、模块接口清晰、序列化状态、不跨模块共享非 POD 对象**。另一位读者指出 Mono 在主机上是可选项，Pesce 回应是授权和实现限制让 C# 推广缓慢，但已有项目在用。

整篇帖子实质上是一份**「工具链迭代速度」工业现状的小型快照**——以 2010 年为时点，但分类学在 2026 年仍然成立。

## 关键要点

- 八档分类从 None 到 Code hot-swap，每档都有对应的现实痛点（见 [[live-editing-taxonomy-2010]]）。
- **C++ = pain** 的原话含义不是吐槽 C++，而是：**「如果你的方案没照顾到 code iteration，那 C++ 这一层的痛就无法被任何数据 live-edit 工具遮蔽」**。
- Code hot-swap 的设计约束：目标前置 + 接口清晰 + 可序列化状态 + 不共享非 POD 跨模块对象。
- Mono / C# 在主机上的可行性：技术上可以，但授权 + 实现限制让推广缓慢。
- Pesce 对 partial tools（独立 shader editor / anim editor）的犀利评价：**「它不解决原问题，它创造一个新的、好用但不是游戏的环境」**——与 [[tools-first-iteration-loop|Evan Todd 2011]] 的论点一脉相承。

## 链接到的概念

- [[live-editing-taxonomy-2010]]
- [[runtime-editor-console-connection]]
- [[tools-first-iteration-loop]]
- [[binary-hot-reload]]
- [[decoupled-tool-engine-json-rpc]]
- [[dependencies]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/05/poll-results.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-05-10_poll-results.md`
