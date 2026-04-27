---
tags: [source, game-development, art-pipeline, dcc, studio-management]
date: 2026-04-27
sources: 1
---

# Why Big Game Studios Use Single Main 3D Software Environment（Bart Wronski）

[[people/bartosz-wronski]] 发表于 2014 年 2 月的文章，回答「为何大型 AAA 工作室强制规定统一 DCC 工具」这一管理问题。

## 摘要

这篇文章从管理与技术两个维度分析了大型工作室统一使用单一三维软件（3ds Max / Maya / Blender）的原因。核心答案是**生产力**——不是指单个美术师的个人效率，而是整个工作室大规模协作的综合效率。文章列举了 11 个论点：资产跨人员共享与版本管理、批量授权成本、中间文件的来源管理复杂性、软件与引擎的 live-connection 开发成本、文件格式标准（smoothing groups / 坐标系）的可预测性、PSD 层级的 PBR 材质打包工作流、技术美术的脚本与插件维护成本、自动化导入管线的单一支持路径、LOD/Rigging/Skinning 的工具链、材质在 DCC 内预览与引擎的同步等。作者还提到 Guerrilla Games 直接用 Maya 作为关卡编辑器的极端做法。结论是艺术指导选软件并非偏好问题，而是工业规模生产组织决策。

## 关键要点

- 资产共享需求（成员离职/请假时接手）要求所有人用同一格式；不同软件之间格式转换会丢失元数据
- Live-connection（DCC 与引擎实时同步）极大压缩迭代时间，但开发成本高，只能为单一 DCC 维护
- PSD 多图层工作流解决 PBR 贴图打包/通道切换的复杂性，这是纯通用格式无法提供的
- 技术美术插件（顶点绘制自动化、LOD 工具等）绑定特定软件，迁移成本极高
- Guerrilla Games 将 Maya 用作全体人员（LD/Light Artist/Env Art）的关卡编辑器，是将这一逻辑推到极端的案例
- 结论对求职者的建议：学会多种 DCC，保持工具灵活性

## 链接到的概念

- [[studio-dcc-standardization]]

## 原文

- 链接：https://bartwronski.com/2014/02/25/why-big-game-studios-usually-use-single-main-3d-software-environment/
- 本地：`raw/articles/bartwronski.com/2014-02-25_why-big-game-studios-usually-use-single-main-3d-software-env.md`
