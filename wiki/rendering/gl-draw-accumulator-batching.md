---
tags: [渲染, opengl, batching, draw-call, 性能]
date: 2026-04-19
sources: 1
---

# GL 绘制累加器（Accumulator）与重排合批

**累加器**是 Ben Supnik 在 X-Plane 10 Mobile 上反复使用的中间层：当上层代码已经写成「一次一个三角形」的 naive API（`draw_colored_triangle_2d(...)` / `draw_textured_triangle_3d(...)` 之类的便利函数），已经无法短期内改成「一次一批」时，在 GL 调用之前插入一个 CPU 侧缓冲，把三角形**先存后发**，用批处理换吞吐。

## 为什么 naive-一三角形-一调用 必死

每个 [[draw-call]] 的大头不在 GPU 执行，而在 CPU 侧的**状态同步**（见 [[opengl-state-change-deferral]]）。一张 profile 会把时间算在 `glDrawArrays` 上，其实是 draw 前驱动在补齐所有 glVertex*Pointer / glBindBuffer 的延迟工作。硬件的代价结构是「建立贵、每三角形便宜」，naive API 恰好**最大化 setup、最小化吞吐**——Ben 直接把它叫「correct drawing and truly awful performance」。

## 累加器做两件事

1. **合批**：相同状态（shader / texture / blend）的连续三角形**不发**，先塞到内存；下一次 draw 之前，一次性发整个 run。原文举例：200 个同色三角形合成一次 state setup + 一次 200-tri draw，**吞吐涨 200×**。
2. **省状态切换**：累加器记得「上一批画的是什么」；同一张贴图、同一个 shader 接着来就免掉对应 glUniform / glBind 调用——哪怕相邻 run 之间只有部分 state 改变，也能省掉共享那部分。

副产品：累加器是天然的**usage 统计点**——在 debug 模式里记录每次 flush 的 run 长度，一眼就能看出「平均 batch size=2」这类不效率排序问题。

## 「平均 batch=2」怎么解

累加器已经 on，但 run 长度还是 2？多半是上层在**交替**两类 state：*UI 背景（贴图 shader）→ 文字（字体 shader）→ UI 背景→ 文字*。每块都是两次 shader 切换。两条武器：

### 1. Draw reordering（分层）

给累加器一个**层号**，让它先画所有 layer 0、再画所有 layer 1。X-Plane 10 Mobile 的 UI 正好是这个情形——每个控件是背景 + 文字两趟、两个 shader。给文字一个独立 layer，让累加器把「先所有背景、再所有文字」重排过来，UI 内部 shader 切换从 *每控件两次* 降到 *整个窗口两次*。碰到必须先显示的地方（例如跨窗口的 z-order）就插 **barrier**，强制先把已缓存的文字 flush 出来。

### 2. 合并状态（State merging）

重排破坏语义的场合（比如 alpha blend 次序重要），就反过来**让不同的 state 看起来一样**：
- 用 1×1 纯白贴图当「无贴图」，整条 pipeline 都能走同一个 sample-texture shader。
- 不走 color application 时把颜色写成纯白不透明，shader 照样过。
- 预乘 alpha（见 [[srgb-premultiplied-alpha-compression]]）允许 additive 和 non-additive 在同一套 blend 状态下共存——只要美术资源按预乘形式准备。

合并 state 是**量准再合**——一次合并可能省了 shader 切换，也可能因为让整条管线跑得更重而亏，依赖具体模型先 profile。[[batching]] 以及 [[texture-encoded-state]] 的思路都是这条路的变体。

## 与批量几何生成的关系

累加器是**退让**方案——能直接生成大 VBO 的代码（terrain、粒子、静态 mesh）永远都应该走批量路径：`void draw_lots(color_t, int count, float xyz[])`，never a for-loop 外层发单三角形。累加器的存在是为了给已经长成单三角形 API 的上层代码**一条渐进式升级通道**，不是终极答案。

## 相关
- [[batching]]
- [[draw-call]]
- [[opengl-state-change-deferral]]
- [[opengl-draw-call-batching-sweet-spot]]
- [[sprite-batch-instance-draw]]
- [[streaming-quads-drawing-strategies]]
- [[iphone-4-opengl-es-perf-gap]]

## Sources
- [[sources/supnik-accumulation-small-batch]]
