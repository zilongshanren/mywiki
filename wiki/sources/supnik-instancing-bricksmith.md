---
tags: [source, opengl, instancing, ldraw, renderer]
date: 2026-04-19
sources: 1
---

# Instancing for BrickSmith（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2013-01-30 的实现笔记：给开源 LDraw 编辑器 **BrickSmith** 重写 OpenGL 渲染底层，从 `glPushMatrix` 朴素路径一路推到 HW instancing + 三桶分流派遣。

## 摘要

LDraw 模型的特点是顶点极多（一块基础板就 180k 顶点，没有 LOD），但每帧 17,000 个砖只是一个稍大的模型——朴素 uniform 矩阵栈每个 draw call 触发整块 uniform buffer 重传，5,000 draw call 就是上限，跑不通。Supnik 把 modelview 矩阵塞进 vertex attribute（廉价的 per-vertex default），一次 immediate-mode attribute instancing 就快 2x；再进一步用 `glVertexAttribDivisor` 攒批做 HW instancing，单次 `glDrawArraysInstanced` 画一整组同款砖——相比朴素路径约 10x。BrickSmith 的 instance 是 24 float（4x4 矩阵 + RGBA current color + RGBA complement color），打包到一条 giant STREAM_DRAW buffer 里，mesh 本身是 STATIC_DRAW。派遣分三桶：半透明 back-to-front 排序、复杂（texturing）按 part 分组、简单合并做 HW instancing。新管线大多数模型 ≈2x 更快，CPU 从 100% 降到 30-35%——说明瓶颈从驱动转到 GPU 顶点吞吐。Datsville 极端模型（125M 顶点）上两者都是 5 fps，因为 ATI 4870 约 500M vertices/sec 已吃满，**没有 LOD 再优化也救不回来**。

## 关键要点

- LDraw "current color" 在 shader 里通过 `A=0` 特殊 RGBA 编码完成代换——一个砖一个 VBO，不按颜色切
- 朴素 uniform 矩阵 → attribute instancing 约 2x → HW instancing 再 10x
- 24-float instance：modelview matrix + current color + complement color
- Instance VBO 合到一个 giant stream buffer，避免一堆小 VBO 给驱动添堵（小于一页的 VBO 尤其不好）
- 三桶分流派遣：透明 / 复杂纹理 / 简单 instance
- 39,000 砖 × 125M 顶点撞到 vertex bound 天花板——下一步要做 LOD

## 链接到的概念

- [[bricksmith-instancing-pipeline]]
- [[xplane-instancing-2011-numbers]]
- [[vbo-double-buffering-orphaning]]
- [[alpha-blending-front-to-back]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2013/01/instancing-for-bricksmith.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-01-30_instancing-for-bricksmith.md`
