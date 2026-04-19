---
tags: [游戏引擎, 2d, sokol, sprite, cloudwu, soluna]
date: 2026-04-19
sources: 1
---

# Soluna（云风的 2D 游戏框架）

Soluna 是 [[cloudwu]] 于 2025 年 2 月在 GitHub 上起的新坑（`cloudwu/soluna`），目标是给自己的策略向独立游戏搭一个轻量 2D 框架。这不是一个再造 Ant Engine 的项目——他明确表示：之前几年做的 3D 移动端引擎对这个新需求来说太复杂，而且这次不主打移动平台，所以那些为移动平台妥协的决策也没意义。

## 定位

- **2D 专用**：策略向独立游戏不需要以画面取胜，2D 表现力够了
- **桌面优先**：不再为移动端续命设计，砍掉相应复杂度
- **亲自写底层**："我太久没写代码了，而做这个非常有趣"——自娱动机占比不小
- **sokol 做图形后端**：单线程 API，云风在上面再搭 batch 中间层适配多线程逻辑

## 设计切面

目前公开的第一刀切在 [[sprite-batch-instance-draw|sprite 批渲染管线]]：

- 顶点数据从朴素的 10 float 压到每 sprite 26 字节
- storage buffer 存 sprite 元信息（12 字节/条）和 SR 矩阵表
- instance draw 去掉 per-sprite 冗余
- CPU 侧引入 batch 中间层给 sokol 单线程 API 解耦
- sprite id 负数作非默认材质调度位

## 与早年 ejoy2d 的对照

云风当年在 [[draw-procedural-gpu|ejoy2d]] 用 CPU 算 2×3 定点数矩阵再把结果填入顶点流，那是为了在早期智能手机上跑得动。十多年后，GPU 能力宽裕，把矩阵搬上 GPU、用 storage buffer 去重成了更自然的选择。Soluna 的顶点压缩思路也是"观察几何约束（轴对齐、UV/offset 同形、int16 像素坐标足够）然后一步步砍冗余"。

## 相关

- [[cloudwu]]
- [[ant-engine]]
- [[sprite-batch-instance-draw]]
- [[draw-procedural-gpu]]
- [[batching]]
- [[indie-game-dev-rhythm]]
- [[main-thread-task-injection]]

## Sources

- [[sources/cloudwu-soluna-2d-pipeline]]
- [[sources/cloudwu-deepfuture-postmortem]]
- [[sources/cloudwu-main-thread-task-injection]]
