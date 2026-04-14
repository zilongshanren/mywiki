---
tags: [source, 游戏开发, 工具链, 内容管线, 工程哲学]
date: 2026-04-14
sources: 1
---

# Tools are everything（Evan Todd / etodd.io）

[[people/evan-todd|Evan Todd]] 2011 年 11 月的一篇短文，对「不要造引擎，要造游戏」这句口号打补丁：**真正决定项目成败的是工具，不是引擎也不是游戏特性本身**。无论自研引擎还是用 Unity / UDK，工具应该排第一优先级。

## 摘要

Todd 的核心论点：评估工具好坏的问题不该是「能挂多少图形特效」，而该是「往里面塞一段新内容有多容易」。游戏的核心是内容——关卡、AI、动画、音效——任何让内容创建变难的环节都会让开发者下意识地「少做内容、多做有立竿见影成就感的特性」，但那些特性并不构成游戏。他举了两个亲身例子：（1）切换到微软 [XACT](http://msdn.microsoft.com/en-us/library/ee415964) 后，他突然开始大量地往游戏里塞声音、调参数、做变体——代码一行没改、API 没扩，纯粹是因为「不用编译就能调」；（2）他给关卡编辑器加了一个按钮，让自己能在编辑器和游戏之间瞬间切换、不用退出重启——关卡设计水平没变但做关卡这件事突然变得享受。Todd 把同一个原则推广到 API 层：他做 iPhone 游戏时一直懒得加 UI 转场，发现库自带 tween 系统后突然到处都在加动画。结论：**API 易用度等价于工具易用度**，门槛降低一个量级，使用率会涨好几个量级。

## 关键要点

- 「内容创建的便利度」应该是评估引擎的第一指标，不是特性表
- 工具改进的优先级要和「实现新游戏特性」放在同一张 backlog 上排
- 任何能去掉一次「重启游戏」的小改动都值得优先做（编辑器/游戏热切换）
- 一个易用的 API ≈ 一个内置工具，会驱动开发者真正去用某项能力
- Todd 列举了潜在工具改进方向：自动化测试、alpha 阶段统计采集工具、更好的 asset 系统

## 链接到的概念

- [[tools-first-iteration-loop]]
- [[binary-hot-reload]]
- [[csharp-runtime-script-compilation]]
- [[runtime-editor-console-connection]]

## 原文

- 链接：https://etodd.io/2011/11/25/tools-are-everything/
- 本地：`raw/articles/etodd.io/2011-11-25_tools-are-everything.md`
