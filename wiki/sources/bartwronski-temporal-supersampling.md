---
tags: [source, 渲染, taa, temporal, 抗锯齿]
date: 2026-04-14
sources: 1
---

# Temporal supersampling and antialiasing（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 3 月发表的基础教学文，同时也是 **Assassin's Creed 4: Black Flag** 在 Xbox One / PS4 上使用 SMAA 1TX + temporal 分量的实战复盘。这篇早于当前 wiki 上基于 elopezr 的现代 [[temporal-antialiasing|TAA]] 综述，属于这条技术线的「一手祖师文」之一。

## 摘要

文章从信号论的 aliasing 定义讲起，指出三角形光栅化的 step-edge 本质上是无限频谱，经典的解法是超采样——但成本 N 倍。**temporal supersampling 的洞察**是：相邻帧大部分像素对应同一些表面，只要知道它们在上一帧的位置（[[motion-vectors|motion vectors]]），就可以把 N 个子采样分摊到 N 帧里，成本趋近于零。Tiago Sousa 在 Siggraph 2011 提出对 MVP 矩阵做逐帧 subpixel 抖动 + post-process 式累积，是 Bart 落地的起点。文章诚实地写出 AC4 的踩坑：动机是 FXAA + 深度边缘检测在绳索/栅栏/树叶等亚像素几何上噪声爆炸；第一步先用 SMAA 1x 替代 FXAA；第二步挂上 temporal 分量后立刻美如画——但这只是静态。真正的工程痛是把所有物体的 motion vectors 做对：布料/软体物理物体矩阵是 identity，海洋不写 G-buffer，程序化植被动画没进 vertex history，骨骼 teleport 没被标记。每一类都单独修，前后两三周。Crytek / SMAA 的 motion-magnitude 作为 rejection 指标阈值难调，shadow/particle 之类纹理动画没有 motion 会 ghost，Bart 改成「任一帧位移超过 ~2 像素直接不混」。最后顺带讲 SSAO 的 temporal 分量（3 个空间图案旋转、用深度做 rejection），一天就接完，收益巨大。

## 关键要点

- **temporal = supersampling 分摊到帧**：理论很简单，实现是两三个月的 bug 大冒险。
- **jitter 投影矩阵**：把 `(j_x/w, j_y/h)` 写到投影矩阵的 `[2][0]/[2][1]` 位置，等同于在 clip space 做 `(x + tx·w, y + ty·w)`，perspective divide 后正好是 NDC 平移——读者问到这里作者亲自解释。
- **motion vectors 必须像素精准覆盖所有物体**：布料、海洋、植被、teleport 骨骼、粒子，缺一就 ghost；per-object motion blur 的精度远不够。
- **motion-magnitude rejection 不够用**：阴影、贴花、爆炸、粒子没有 motion，会被当作静止并累积拖影；Bart 的兜底是「位移 > ~2 像素直接不混」。
- **edge cases 吃掉额外 1–2 周**：菜单弹出、暂停、返回仪表板、post-effect 切换，每一种都要单独关掉 jitter 和 accumulation。
- **temporal SSAO 几乎免费**：3 个采样图案轮换、深度 rejection、额外两张 history，效果和成本都极好。
- **作者已经预告 Tiago Sousa 2013 的 color-based metric**——这就是现代 TAA color clamping 的前身，顺接到 [[taa-history-rectification]]。

## 链接到的概念

- [[temporal-supersampling]]
- [[temporal-antialiasing]]
- [[taa-history-rectification]]
- [[motion-vectors]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[hbao-interleaved-sampling]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/
- 本地：`raw/articles/bartwronski.com/2014-03-15_temporal-supersampling-and-antialiasing.md`
