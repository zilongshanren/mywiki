---
tags: [source, 渲染, mipmap, cpu优化, morton, srgb, 缓存]
date: 2026-04-19
sources: 1
---

# Simultaneous Mipmap Level Generation（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2016 年 5 月在 X-Plane PNG 纹理上传链路上做的一个非递归 CPU mipmap 算法探索：按 Morton 序遍历源图，一次循环产出整个金字塔，每个源像素只读一次。

## 摘要

传统 mipmap 的 recursive downsample 最省读样（≈ 1.33× 原图总像素），但每一层都是上一层的平均——**第 7 级 mip 的每个像素等价于原图经过 7 次重采样**，在 [[pbr-roughness-prefilter|roughness-aware prefilter]] 等非线性 filter 下误差累积严重。Supnik 想在**单次遍历**里同时构建所有 level，且每个 mip 都**直接从原图采样**。关键 trick 是把像素编号按二进制**奇偶位拆**成 X/Y——即 Morton / Z-order——这样「连续访问 k 个像素恰好填满某层 mip 的一个 bucket」的递归性质自动成立。代价：这种遍历顺序对行主序内存布局**极度 cache 不友好**。benchmark：纯整数 raw filter 下 recursive 18.4、sequential 72.1、parallel 124.9——recursive 完胜，parallel 被 cache miss 拖死；但在 sRGB filter 下（u8 → linear float → pow(·, 2.4)），解码成本主导，sequential 爆到 2732、recursive 374、**parallel 392**——几乎追平 recursive 而质量更好。评论区指出一个更优雅的路线：按行扫描也能在「每行结束时填满对应 mip 的 bucket」，同样做到「每源像素一次」且保持线性访问。Supnik 承认。X-Plane 不用 GPU mipgen 的理由来自驱动 residency 管理与未来迁低级 API 的统一路径。

## 关键要点

- Morton / Z-order 地址交错是「一次遍历生成所有 mip」的前置约束
- novel 不是 Morton 本身，而是**把它用来做 mipmap**
- recursive 在 data-movement bound 任务上不可战胜
- parallel 只在 per-pixel 解码成本 >> cache miss 成本时有用（sRGB 是个甜点）
- 评论区的行扫描方案做到同样「每源像素一次」且 cache-friendly——更好
- X-Plane 不用 GPU mipgen：统一 DDS/PNG 路径、避免驱动 residency 抖动

## 链接到的概念

- [[morton-order-parallel-mipmap]]
- [[mipmap-generation-sampling]]
- [[color-space]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/05/simultaneous-mipmap-level-generation.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-05-07_simultaneous-mipmap-level-generation.md`
