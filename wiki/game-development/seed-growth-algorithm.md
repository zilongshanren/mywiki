---
tags: [game-development, procedural-generation, dungeon-generation, algorithm]
date: 2026-04-27
sources: 1
---

# 种子扩张算法（Seed Growth）

种子扩张（Seed Growth）是一种程序化区域生长算法，Boris The Brave 在分析 Watabou 的 Cave/Glade 生成器时对其进行了归纳。该算法在[[game-development/dungeon-generation-algorithm]]中也有所涉及（Boris 在 Binding of Isaac 地牢分析中称其为"随机洪水填充"），但缺乏一个广为接受的统一命名。

## 算法核心

1. 随机选取一个起始格子（种子）。
2. 维护一个"待扩张边界"集合，初始只含起始格。
3. 重复从边界集合中按权重随机选取一格，将其加入当前区域，并把它的未访问邻居加入边界集合。
4. 达到预设面积阈值后停止，开始下一个区域的种子扩张，且区域之间不允许接触。

## 通过权重控制形状

扩张格的选取权重决定了区域的形状风格：

- 权重 ∝ `pow(c, gamma)`，其中 c 是该格已有多少邻居在当前区域内、gamma 是全局参数：
  - 高 gamma → 区域倾向于聚团，轮廓圆润。
  - gamma ≈ 0 → 近似均匀随机，形状不规则。
  - 负 gamma（`coral` 模式）→ 偏好仅有一个邻居的孤立格，形成细长触须状轮廓。
  - 固定 gamma=6（`cavities` 模式）→ 非常紧密的团状腔室。

这种参数化使同一算法可以生成从紧密腔室到珊瑚礁状触须的各种形态，只需在初始化时随机化 gamma。

## 连通性修复

生成多个独立区域后，需要挑选"通道格"连通它们。Cave Generator 的做法：

1. 找到所有边界相邻的区域对。
2. 按连通性策略剪枝（生成树 / 允许少量环路 / 全连通）。
3. 对每对区域，从共享边界随机选一格作为门。
4. 部分区域随机"收缩为走廊"——反复删除非必要格子，同时用洪水填充确保所有门仍然连通（参考 Boris 的 Chiseled Paths 算法）。

## Cave/Glade Generator 中的完整流程

Watabou 的生成器将种子扩张置于一条完整的处理管线中：

1. 在六边形网格上生长区域（内部以 DCEL 数据结构表示）。
2. 连通区域、生成门、收缩走廊。
3. 对六边形边界做多步细分与随机偏移，隐藏底层网格。
4. 应用 Chaikin 曲线平滑、Dyson 阴影线等风格化后处理。
5. 用 Tracery 语法生成地图名称。

Boris 的核心观察是：出色的程序化结果不来自高级算法，而来自**将若干简单规则有效组合，并以目标风格为导向**。

## Sources

- [[sources/boris-cave-glade-generator]]
