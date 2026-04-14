---
tags: [source, 工具链, 关卡编辑器, python, wxwidgets]
date: 2026-04-14
sources: 1
---

# WoF Scenario/Entity Editors（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 为《[[sources/elopezr-will-of-flame|Will of Flame]]》手写的配套**关卡编辑器**和**实体编辑器**的项目说明，用 Python + wxPython + PIL 实现，代表小团队自研游戏典型的"**先做引擎再做工具**"路径。

## 摘要

Scenario Editor 是一个图形化的关卡拼装器，把美术产出的 PNG 按层导入、支持**视差层（parallax layers）**结构、可以拖放/旋转/删除各种游戏实体、最终导出为 **XML** 给 Android 版游戏读取。特别的一点是它会把背景层按 tile 切分导出，配合 TexturePacker 一起完成打包管线。快捷键比较齐全：Ctrl+R 旋转、Delete 删除、Ctrl+Z 撤销、方向键微调位置，还有按类别统计实体数量的面板。Entity Builder 则是一个"**把多个部件组装成复合实体**"的工具——专为主角和 boss 设计，运行时整个复合体作为一个游戏实体对外表现。整篇没有给出架构细节，但两件工具都是独立引擎团队小而全工具链的微型样板。

## 关键要点

- 技术栈：Python + wxPython + PIL（Pillow 前身），纯 CPU 图像处理做缩放/旋转/切分；
- 导出目标是 **XML** 格式的 scenario 描述，被游戏运行时读取；
- 视差层是运行时表达的直接映射——编辑器里的层结构就是游戏里 parallax 的层；
- 背景被切成 tile 再交给 TexturePacker，这让"美术画一张超大长图 → 自动变成多张 POT atlas"的流程跑通；
- Entity Builder 把多部件复合实体作为第一类概念——这和后来商业引擎里的 prefab/blueprint 是同一个需求；
- 自研小引擎项目里**工具链的投入往往和引擎本身相当**——这是这份文章最重要的、没有明说的信息。

## 链接到的概念

- [[sources/elopezr-will-of-flame]]
- [[resource-system-design]]

## 原文

- 链接：https://www.elopezr.com/wof-scenarioentity-editors/
- 本地：`raw/articles/elopezr.com/2014-03-10_wof-scenario-entity-editors.md`
