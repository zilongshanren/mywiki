---
tags: [source, ecs, svelto, 数据结构]
date: 2026-04-19
sources: 1
---

# Svelto.ECS 3.3 and the new Filters API（Sebastiano Mandalà / Seba's Lab）

[[sebastiano-mandala]] 2022 年 4 月发布的 Svelto.ECS 3.3 版本说明，重点介绍 Filters API 的第二次重写。

## 摘要

Svelto 的 entity 存储以 group 为单位、一个 entity 只能在一个 group 里，这种设计让状态表达清晰但也容易产生 group 组合爆炸。Filter API 的作用是给"跨 group 的 entity 子集"一个独立索引——不改变 entity 的存放位置，只记录 `(filterID, group) → indices`。新版 API 的主要突破是**用户不再需要知道 entity 在哪些 group**：iterate 时 filter 是一等公民，group 跟在它下面。filter 分 transient（每次 submission 自动清空）和 persistent（框架长期持有、entity 删除时自动摘除）两种；用户可以自定义 filter ID，再加上 `context` 做命名空间。文中用 Stride Doofuses demo 演示：entity 的 group 表示游戏状态（饿 / 吃），mesh 用哪个 prefab 则用 persistent filter 以 stride entityID 为 ID 索引；iterate filter 时遍历每个 filter 的 `(indices, group)` 对，拷贝 matrix 给 Stride 做实例化。

## 关键要点

- Filter 是跨 group 的 entity 子集索引，不改变内存位置，仅记录引用
- transient filter：submission 后自动清空；persistent filter：entity 删除时自动更新
- 必须用 `indices[i]` **二级索引**，不能直接用 `i` 读 component 数组
- filter ID 可自定义 + context 分命名空间，方便语义化
- 比 event / publisher-consumer 更 ECS：等价于"一批处于某状态的 entity"

## 链接到的概念

- [[svelto-filters-api]]
- [[svelto-ecs]]
- [[sebastiano-mandala]]

## 原文

- 链接：https://www.sebaslab.com/svelto-ecs-3-3-and-the-new-filters-api/
- 本地：`raw/articles/sebaslab.com/2022-04-12_svelto-ecs-3-3-and-the-new-filters-api-seba-s-lab.md`
