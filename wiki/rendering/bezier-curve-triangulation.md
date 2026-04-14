---
tags: [2d, bezier, 描边, 三角形, rendering]
date: 2026-04-14
sources: 1
---

# Bézier 曲线描边三角化

把一条有宽度的 Bézier 曲线交给 GPU 画的经典做法——不走 `GL_LINES`（OpenGL 的画线 API 线宽只能在 draw call 级别设定，而且实现通常把斜线处理成平行四边形而不是旋转矩形），也不走 Core Graphics（CPU 光栅化 + 全屏重绘，60 条动画曲线时直接炸）。正确做法是把曲线细分成短线段，每段扩成一个矩形，用两个三角形画。

## 四个步骤

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 在为 iPad 应用 Revolved 写这套线渲染时总结出的流程：

1. **参数化细分**：三次 Bézier 按 *t* ∈ [0,1] 均匀采样 N+1 个点得到 N 段。参数化的好处是曲率大的地方点会自然堆叠——V 形尖角附近段更密，而不是等弧长。
2. **扩宽**：每个采样点沿**垂直曲线方向**向两侧偏 `lineWidth/2` 得到四个顶点。
3. **切线校正**：这里是关键。不能把每段当独立矩形偏移——相邻段法线不同会产生裂缝。正确做法是对 B(t) 解析求导（直接对控制点做差分得到 dB/dt），把**曲线在该点的切线**取垂直得到真实法线，这样两段共享的顶点自然重合。
4. **自适应段数**：控制多边形 |AB|+|BC|+|CD| 是曲线真实长度的上界；把这个估计长度过一个 **hyperbola** 映射（小值往上提、大值渐近线性）得到段数，短曲线也有足够段不会看起来像折线。

## 为什么不直接合并端点

如果两段矩形之间只是把顶点「凑在中点」，得到的描边在拐角处会有可见的细缝或者法线方向突变——仅仅是 C⁰ 连续。用**曲线自身的切线**求法线，得到的其实是曲线的 offset curve 在该点的离散近似，在段数足够时既没有裂缝也没有法线跳跃。

## 工程小技巧

- **subdivider 作为 block**：Revolved 用了 `typedef SegmentSubdivision (^SegmentDivider)(float t)`，让同一套 mesh 生成代码既能喂 2D 描边也能喂 3D 旋转体，核心几何与具体曲线类型解耦。
- **数量规划**：Revolved 限制 60 条曲线，绘制区 448×768 points。作者算过如果用 Core Graphics `drawRect:` 加 per-curve CALayer 要 60×896×1536×4 ≈ **315 MB**，加上 60× overdraw，根本跑不动。这是典型的**抽象泄漏**案例：Quartz 的 API 足够简单但性能包线无法满足，只能下沉到 GL 三角形。

## 局限与更好的方法

文章末尾作者承认这不是 state of the art——Anti-Grain Geometry 和后来的 Loop-Blinn「直接在 fragment shader 里解三次方程」都能给出更鲁棒的结果。但对一个有固定屏幕上界、需要大量动画和实时交互的应用，**均匀细分 + 切线法线 + hyperbola 段数** 的组合在工程上已经够用了。

类似"几何上近似复杂曲线"的思路也见 [[sdf-2d-primitives]]——只不过 SDF 是把形状放到 fragment shader 里算距离场，而这里是显式把形状变成三角形。

## Sources

- [[sources/ciechanow-drawing-bezier-curves]]
