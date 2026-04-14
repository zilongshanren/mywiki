---
tags: [source, 渲染, 移动gpu, tbdr, 翻译]
date: 2026-04-14
sources: 1
---

# Tile-Based 架构下的性能调校（Bruce Merry / gameKnife 译）

[[people/gameknife]] 于 2014 年 2 月发布的 _OpenGL Insights_ 章节翻译，原文作者 Bruce Merry。这是中文世界较早系统讲解 [[tbdr-vs-imr|Tile-Based Deferred Rendering]] 性能模型与调优实践的文章之一。

## 摘要

本文面向有 OpenGL ES 移动平台开发经验的工程师，系统介绍 Tile-Based GPU 的工作原理以及一套实用调优建议。作者先解释为什么移动 GPU 选择 Tile-Based 架构——核心原因是内存带宽比计算更贵电，把 framebuffer / depth-stencil / MSAA 全部搬到极小但高速的 on-chip tile buffer 上，只在 tile 完成后写回主存。接着讨论 frame data（多边形列表 / 参数缓存）的概念，以及由此衍生的一整套反直觉优化规则：**必须 glClear 或 discard framebuffer**、一帧每个 FBO 只绑定一次、谨慎使用 glReadPixels / 遮挡查询以避免迟滞、理解 Power VR 的 HSR（隐面剔除）、在 TBDR 上 MSAA 几乎免费、颜色混合几乎免费。译者在多处加入注释，记录"踩坑"经验，例如 PVR 硬件上不归位 ColorMask 的 glClear 会静默失败。

## 关键要点

- **frame data 的增长** 是 TBDR 的隐藏成本：提交越多三角形越涨，必须每帧正确 terminate。
- **glClear / glDiscardFramebufferEXT** 在 TBDR 上是**零代价甚至加速**——因为它们直接释放 frame data。
- **scissor / colormask / stencilmask 阻碍 frame data 清空**，移动端是性能灾难。
- 每个 framebuffer object **一帧内只绑定一次**，在解绑前确保所有渲染提交完毕；典型例子：渲染前一次性烘焙所有环境贴图，而不是逐个物体 bind→draw→unbind。
- **glReadPixels / render-to-texture 读取 / 遮挡查询** 都会强制开启新的像素着色流程，代价极高。
- PowerVR 的逐像素 HSR 在使用 discard / alphaTest / alphaToCoverage / 颜色混合时**失效**；此时用 depth-only-pass 是备用手段。depth-only-pass 在 IMR 上增加 depth 带宽，在 TBDR 上几乎免费。
- **MSAA 在 TBDR 上几乎免费**：采样只住 tile buffer，resolve 后才写回。代价主要是 tile 变小与边缘像素变多。
- 颜色混合在 TBDR 上也几乎免费，因为读-改-写循环全发生在 on-chip 存储器上。
- **性能和三角面数量不是线性的**：frame data 溢出会触发 16 倍带宽的强制 flush；不能简单用小场景外推。
- 移动平台必须在性能和电量消耗之间取平衡；达到目标帧率之后继续优化，换来的是更长的休眠时间。

## 链接到的概念

- [[tbdr-vs-imr]]
- [[hsr-tbdr]]
- [[early-z-late-z]]
- [[msaa-ssaa]]
- [[overdraw]]
- [[draw-call]]

## 原文

- 原文作者：Bruce Merry（_OpenGL Insights_ Chapter 23）
- 译者链接：<http://gameknife.github.io/tech/2014/02/28/opengl-insight/>
- 本地：`raw/articles/gameknife.github.io/2014-02-28_tile-basedjia-gou-xia-de-xing-neng-diao-xiao.md`
