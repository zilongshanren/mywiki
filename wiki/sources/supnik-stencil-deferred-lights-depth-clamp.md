---
tags: [source, deferred-rendering, stencil, depth-clamp, opengl, x-plane]
date: 2026-04-19
sources: 1
---

# Stencil Optimization for Deferred Lights Without Depth Clamp（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 12 月 13 日的博文，讲 X-Plane 10 在延迟渲染光源体积 + stencil 剔除管线里，面对「远剪裁面切掉光源体积背面」时的处理方案——尤其是没有 `GL_ARB_depth_clamp` 扩展时的 vertex-shader hack 与其代价。

## 摘要

延迟管线里用光源包围体 + 双面 stencil（背面 increment / 正面 decrement，depth-fail + wrap）标出被光源影响的屏幕像素，再只对这些像素跑光照 shader。问题：远剪裁面如果穿过包围体，背面被 clip 掉 → 光照覆盖缺失 + stencil 计数错乱，污染其他光源的 stencil。正解是 `GL_ARB_depth_clamp`（近远平面夹深度不 clip）。老驱动没这个扩展时 Supnik 给出 vertex-shader 替代：`gl_Position.z = clamp(gl_Position.z, gl_Position.w, -gl_Position.w)`，因为 clip space 是正交的，只改 Z 不改屏幕 XY。但 Z 被提前 clamp 会让插值后的片段 Z 偏移（类似 polygon offset），因此 Z 测试不再正确，不能与 stencil depth-fail 合用。X-Plane 10 据此分三档：大世界纯 stencil / 小世界有 depth_clamp 用 stencil+clamp / 小世界无 depth_clamp 用 VS-clamp 放弃 stencil。评论里有人提议 pixel shader 写 DEPTH，Supnik 反对：那会 kill early-Z，对 X-Plane 这种 bus 瓶颈场景不划算。

## 关键要点

- 双面 stencil 光源体积剔除的标准做法
- 近剪裁面穿体积 → 无影响（前面本无几何可照）
- 远剪裁面切背面 → 覆盖缺失 + stencil 污染其他光
- `GL_ARB_depth_clamp` 是首选方案
- 无 depth_clamp 时 vertex-shader `clamp(gl_Position.z, w, -w)` 保留屏幕覆盖
- clip space 正交性让只改 Z 不影响光栅位置
- VS clamp 的副作用：插值后 Z 错，不能与 stencil depth-fail 合用
- X-Plane 10 三档策略（大世界/有 clamp/无 clamp）
- PS 写 DEPTH 方案会 kill early-Z，bus 瓶颈场景更慢
- 真实瓶颈辨识：X-Plane 有时是 vertex bus 而非 shading

## 链接到的概念

- [[deferred-light-volume-stencil-depth-clamp-hack]]
- [[stencil-buffer]]
- [[deferred-rendering]]
- [[early-z-late-z]]
- [[agp-vs-vram-streaming]]
- [[xplane-gbuffer-format]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/12/stencil-optimization-for-deferred.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-12-13_stencil-optimization-for-deferred-lights-without-depth-clamp.md`
