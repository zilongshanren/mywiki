---
tags: [source, 渲染, 剔除, 空间划分, ryg]
date: 2026-04-14
sources: 1
---

# Some more frustum culling notes（ryg / The ryg blog）

[[fabian-giesen]] 在 2010 年 10 月发表的一篇短文，是上一篇 [[ryg-view-frustum-culling]] 的续集，回应 Charles Bloom 在 cbloomrants 上的补充评论。主题从「单个 box 的最快测试」扩展到「一个场景里怎么组织 culling 层级」。

## 摘要

Charles 建议对便宜对象用 sphere vs. cone 做粗测。ryg 反对 cone 近似：几何上过于保守（16:9 视口下截面比外接矩形大 84%），而且**省下的那几十 cycle 在整条渲染路径的几千 cycle 面前几乎看不见**——假阳性率 5% 就能把收益吃光。他建议直接用 sphere vs. **frustum**。文章的更大主题是**层级感知的测试设计**：内节点和叶节点的假阳性代价不同（内节点浪费几次子节点测试，叶节点浪费一次 GPU 提交），应该用不同的 bounding volume 或不同的测试精度。层级结构本身应避免 binary tree（分支预测差、cache 不友好，SPU 上尤其），应该走**大 fan-out、扁平、按代价函数切分**的路线。另外一个实用技巧：用 clip-space 2D bbox 同时服务于 LOD 选择、小于几像素时的 contribution 剔除、以及粗糙遮挡测试，**比远平面更有用**；删掉远平面剩 5 个面，再删掉不起作用的顶/底面剩 4 个，正好喂 4-way SIMD。评论区 Charles 的反驳是球体的杀手锏：**1 个 float 的半径就能储存，不需要 model-to-world 变换**——在层级顶端这是巨大的收益。ryg 部分同意，但坚持「有主轴的物体」（角色、柱子、旗杆、武器、树）球体配合不好，AABB 一旋转也差，要精确就得 OBB，或者用 object-space bound 避开主轴退化。

## 关键要点

- **Cone vs. frustum 近似太粗**：16:9 下截面大 84%；节省的 50 cycle 在几千 cycle 的 draw 路径前几乎无意义
- **GPU cycle 比 CPU cycle 贵**——假阳性的主要代价在 GPU，不在你的测试指令数
- **层级不同层用不同测试**：内节点廉价（sphere-frustum），叶节点精确（p/n-vertex AABB 或 OBB）
- **层级形状**：大 fan-out、扁平；避免 binary tree；按简单代价函数选切分
- **clip-space 2D bbox** 比远平面更有用：同时服务 LOD、contribution 剔除、粗糙遮挡
- 删掉远平面 → 5 面；删掉非关键顶/底面 → 4 面；正好 4-way SIMD
- **球体的真正优势**：1 个 float 储存、不需要 model-to-world 变换就能剔除；顶层 / 内节点首选
- **球体的弱点**：有主轴的物体（角色、长武器、柱子、树）配合差——世界空间下一旋转就膨胀，要紧的话用 object-space bound 或 OBB

## 链接到的概念

- [[view-frustum-culling-ryg]]
- [[culling]]
- [[collision-detection-gjk-epa]] —— 同一族「沿轴中心 / 沿轴半径」原语
- [[hierarchical-z-buffer]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/20/some-more-frustum-culling-notes/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-20_some-more-frustum-culling-notes.md`
