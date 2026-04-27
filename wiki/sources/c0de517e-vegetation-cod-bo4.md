---
tags: [source, 渲染, 植被, 程序化生成, COD, 游戏引擎]
date: 2026-04-27
sources: 1
---

# Vegetation in COD: BO4 — 程序化植被放置系统（Angelo Pesce / c0de517e）

[[angelo-pesce]] 发表的"from the archive"系列，回顾他在 Activision 参与 Call of Duty: Black Ops 4 开发时负责的植被程序化散布系统 R&D 过程。

## 摘要

BO4 增加了"Blackout"大地图战术竞技模式，Treyarch 需要在原本为走廊关卡设计的 COD 引擎上快速支持宽阔地形与大量植被。Pesce 和 Central Tech 团队负责解决三个核心问题：编辑器原型加载植被数据时内存溢出（仅是位置数据就超出控制台预算）、程序化生成性能太差无法实时交互、以及散布模式单调缺乏变化感。

**关键设计决策**：放弃实时 GPU 生成（参考 Horizon Zero Dawn 的方案后认为不适用），改为编辑时生成、运行时流式加载位图。每个植被层使用预计算的固定点集，通过 Mitchell 最佳候选算法生成初始点集，再用松弛算法对点位置做均匀化，得到蓝噪声分布；然后对点集生成多套"排列顺序"（排列即风格），支持密度渐变、簇状聚集、绳状分布等不同外观。多个图层之间通过影响半径做相互遮蔽/吸引/排斥的逻辑，实现"大树层排斥石头层"等自然共生关系。最终存储只需要图层参数加上每瓦片的位图（bit mask），配合空间局部性排序后进行游程编码，体积极小。

## 关键要点

- 植被系统被拆分为编辑时生成（艺术家可交互调整）+ 运行时流式加载，不需要实时 GPU 生成
- 多图层架构：每层有独立的点集和大小比例，层间可相互抑制/吸引
- 点集基于 Mitchell 最佳候选算法 + 松弛（避免六边形过于规则），产生分级蓝噪声分布
- 不同"排列顺序"产生不同视觉风格（均匀扩散 / 随机 / 簇状聚集 / 绳状）
- 密度地图通过点的激活阈值转换：每个点有唯一激活序号，密度采样决定激活多少点
- 存储为瓦片 bitmask + 游程编码，运行时性能与实例化系统对接
- 草地由单独的专用系统处理，使植被点集实例数量降低了数个数量级

## 链接到的概念

- [[vegetation-procedural-placement]]
- [[poisson-disk-sampling]]
- [[gpu-driven-grass-tiles]]
- [[batching]]

## 原文

- 链接：https://c0de517e.com/015_vegetation_system.htm
- 本地：`raw/articles/c0de517e.com/2014-03-10_from-the-archive-vegetation-in-cod-bo4-another-tale-of-twist.md`
