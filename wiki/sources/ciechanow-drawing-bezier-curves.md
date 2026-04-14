---
tags: [source, 渲染, bezier, 描边, 2d-graphics]
date: 2026-04-14
sources: 1
---

# Drawing Bézier Curves（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2014 年 2 月发表的文章——这是他博客上**第一篇带交互 demo** 的作品，也是后来那种「在浏览器里拖参数」风格的雏形。主题是他的 iPad 应用 [Revolved](http://revolvedapp.com) 里怎么用 OpenGL 把三次 Bézier 曲线绘制成有宽度、无裂缝、自动适配 LOD 的描边。

## 摘要

Core Graphics 在 iPad Air 上连 60 条动画曲线都扛不住（CPU 光栅化 + 全屏重绘 + 315 MB 的每条曲线 layer），所以 Revolved 把曲线描边完全做成了 OpenGL 三角带。文章一步步推导了**曲线细分 → 线段扩宽 → 切线校正 → 自适应段数**四个阶段。关键洞察是：简单地把每段当独立矩形会在折角处产生裂缝；正确做法是在参数 *t* 上解析地求 dx/dt 和 dy/dt 得到切线，再取垂直方向作为宽度偏移，这样相邻段顶点自然对齐。段数则用控制多边形 |AB|+|BC|+|CD| 作为曲线长度上界，再套一个 hyperbola 形函数把小值提升——短曲线也有足够段数而不浪费三角形。OpenGL 原生的 `GL_LINES` 被直接拒掉，因为「实际画出来是平行四边形不是斜矩形」，线宽只能在 draw call 级别设定。

## 关键要点

- **参数化细分**：Bézier 的 *t* ∈ [0,1] 让曲率大的地方自动聚点，V 形尖角附近线段更密。
- **切线法线 = 解析导数**：对 B(t) 求 dB/dt 取垂向，是消除折角裂缝的正解——别在中点合并顶点凑合。
- **自适应段数公式**：控制多边形总长 → hyperbola 映射，短曲线被提升到合理下界。
- **Obj-C block 做 subdivider**：`SegmentSubdivision (^)(float t)` 把几何生成与具体曲线类型解耦，同一套 mesh 代码可给 2D 线段和 3D 旋转体共用。
- **为什么不用 Core Graphics**：CPU 光栅化、60 视图时 315 MB RAM、60× overdraw——高层 API 在大量动画场景下**抽象泄漏**。
- **为什么不用 `GL_LINES`**：OpenGL 画出的是平行四边形而非旋转矩形，线宽粒度是 draw call 级。

## 链接到的概念

- [[bezier-curve-triangulation]]
- [[sdf-2d-primitives]]
- [[rasterization]]
- [[triangle-primitives]]
- [[continuous-design]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/drawing-bezier-curves/
- 本地：`raw/articles/ciechanow.ski/2014-02-18_drawing-bezier-curves-bartosz-ciechanowski.md`
