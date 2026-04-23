---
tags: [source, opengl-es, 2d, instancing, mobile]
date: 2026-04-19
sources: 1
---

# There Must Be 50 Ways to Draw Your Streaming Quads（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2013-04-20 的菜谱式小结：画一堆位置每帧都变的 2D 四边形（UI / text / 粒子 / 2D 游戏），有哪些画法，哪条路各有什么代价。立场鲜明：**移动端（iPhone GLES 2.0）才真正需要这场讨论**，桌面端 profile 先于优化。

## 摘要

所有路线的前提：全部几何放进一个 VBO、指向同一张 atlas——切 VBO 或 texture 的 CPU 代价远高于画单个 quad。路线 A 用 OpenGL 矩阵栈（uniform 矩阵） per-quad push：每次 uniform 改变都让驱动重建整块 uniform buffer，一次 draw call 只画一个 quad，CPU 巨贵。路线 B **CPU 预变换、每帧推流式 VBO**：一次 draw 一个 VBO，驱动压力最小；不依赖 GL 3.x 扩展；代价是每帧推整份顶点，桌面占带宽 / 移动占 CPU——**GLES 2.0 iOS 的最佳路径**。路线 C 桌面的聪明版：`glVertexAttribDivisor` + 压缩的 instance 数据（仅 translate+2D rotate 可压到 2D offset + sin/cos + UV 变换）+ 静态 4 顶点 mesh，attribute instancing 走 HW。Supnik 留免责：他没实测过，因为 X-Plane 桌面上 B 够用。反路线（不推荐）：geometry shader blow-up（"um, don't"）、UBO/TBO 替代 divisor（YMMV）、immediate mode 每 quad push（救急可以）。评论区贡献：interleaved 顶点布局优于分开布局以最大化 cache line 利用；Instruments 下 `glDrawXXX` call stack 里冒出"吓人名字"是路径走错的最强信号；CPU vs GPU transform 的归属权要看哪一边空闲。

## 关键要点

- 前提：single VBO + single atlas 是所有优化的基础
- uniform 矩阵路径天然 1 quad / draw call，不能用
- CPU transform + 每帧推 VBO = GLES 2.0 iOS 最佳路径
- 桌面 HW instancing 用压缩 instance（2D offset + sin/cos）是理论最优，Supnik 没测
- GS blow-up 只在 vertex stride 极小时赢，否则输给直接 4 顶点 quad
- interleaved vertex 布局（pos0,col0,nrm0,pos1,...）cache 最优
- Instruments 看 CPU stack 的"吓人名字"验证是否踩坑

## 链接到的概念

- [[streaming-quads-drawing-strategies]]
- [[bricksmith-instancing-pipeline]]
- [[vbo-double-buffering-orphaning]]
- [[sprite-batch-instance-draw]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2013/04/there-must-be-50-ways-to-draw-your.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-04-20_there-must-be-50-ways-to-draw-your-streaming-quads.md`
