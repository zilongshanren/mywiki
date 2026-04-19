---
tags: [source, metal, 字体渲染, 矢量渲染, gpu]
date: 2026-04-19
sources: 1
---

# Slug: GPU 字体渲染算法在 Metal 的实现（Warren Moore / Metal by Example）

[[warren-moore|Warren Moore]] 发表于 2026 年 3 月 30 日。Eric Lengyel 2017 年发表的 **Slug 算法**（JCGT "GPU-Centered Font Rendering Directly from Glyph Outlines"）被申请了专利，原本要等 12 年（2029）才能写这类教程。**作者把算法捐到公共领域后**，Warren 立刻用 Core Text + Metal 做了最小样例（GitHub: metal-by-example/MetalSlug，Apache 2.0）。开篇第一句话："I expected to have to wait 12 more years to write this post."

## 摘要

背景：GPU 直接从 Bézier 轮廓光栅化字形（不走 atlas / SDF 中介）历来被**数值精度 + 视觉保真**两个问题拖住。Slug 用一套精心设计的数学解决了这两点，能在任意投影变换下做 pixel-perfect 字形渲染。本文不复述论文，只讲"如何在 Metal 上跑起来"。

### Inside / Outside：winding number

TrueType glyph 是一组**二次 Bézier 样条**闭合曲线（PostScript Type 1 / OpenType 可能是三次；本文只讲二次）。判断像素是否在字形内不简单：从该点射线出去，数相交次数不够——可能射线共线、可能碰端点、可能射线方向有歧义。

正确做法用 **winding number**（绕数）：给每条闭合曲线定方向（逆时针为正），每个交点贡献 ±1（局部左转 +1、右转 -1）。**nonzero rule**：绕数非零表示在内部。Slug 的一大创新是**数值稳健的二次方程根分类**（2018 I3D presentation 详述），解决浮点精度下的抖动和裂缝。

二值 in/out 判定会产生锯齿（jaggies）。Slug 走的是**分数覆盖（fractional coverage）**：每个 pixel 算出被 glyph 覆盖的比例。为了处理完全水平 / 完全垂直的线段这种退化情形，**水平和垂直两方向射线都算**，结果合并。

### Bands 加速

brute-force 每采样点对所有曲线段都算贡献太贵。Slug 预处理把每个 glyph 的曲线段分桶到**水平 bands + 垂直 bands**：一个 band 是矩形切片，射线不会穿出包围盒外的曲线。每采样只看所在 band 的曲线段，工作量大幅下降。完全水平的线段不算进水平 band（不影响 winding），完全垂直的不进垂直 band。

### 动态 Dilation

极小字号时窄特征可能因为采样不足消失。Slug 2019 加的 dynamic dilation 用 MVP 精确推出 glyph bounding rect，保证可能覆盖的 pixel 都被光栅化。Warren 实测没看出太大差别，可能自己数学写错了，细节看 [专利释放公告博客](https://terathon.com/blog/decade-slug.html)。

### Metal 实现结构

Text rendering context 维护每 typeface 一个 **font atlas**，两张纹理：

- **band texture**：每个 (水平 / 垂直) band 里的曲线索引
- **curve texture**：实际 Bézier 控制点

每个 glyph 记录 typographic metrics + 引用的曲线段索引。layout / shaping 交给 **Core Text**（等价于 Harfbuzz / Uniscribe / DirectWrite），处理 ligature / bidi / 连字脚本 / combining characters / hinting 等。

Shader 代码约 200 行 MSL，基本机械翻译自 Lengyel 的[reference shader](https://github.com/EricLengyel/Slug)（Apache 2.0 发布，版权归 Lengyel）。

### 不足

- 不支持 emoji
- 每个 text run 一次 draw call，有冗余资源绑定——正式版应合并同资源 run
- font atlas 目前一 typeface 一个，可合并成 atlas array

## 关键要点

- Slug 2026 年被捐到公共领域，提前 12 年解禁教程
- GPU 直接光栅 Bézier 轮廓的核心难点是数值稳健 + 视觉保真，Slug 用二次根稳健分类解决
- winding number + nonzero rule 判 inside/outside；水平+垂直双射线合并 coverage 消除锯齿
- Bands 预处理把曲线分矩形桶，每采样只看本 band 少量曲线
- Dynamic dilation 用 MVP 推边界保小字号采样完整
- Metal 实现核心是 band texture + curve texture 两张纹理 + Core Text layout
- Shader 约 200 行 MSL，Apache 2.0 开源
- 专利释放让 GPU 字体渲染走出 SDR atlas / multi-channel SDF 局限

## 链接到的概念

- [[slug-gpu-glyph-rendering]]
- [[bezier-curve-triangulation]]
- [[analytical-antialiasing]]
- [[metal-api-overview]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/slug/
- 本地：`raw/articles/metalbyexample.com/2026-03-30_slug.md`
