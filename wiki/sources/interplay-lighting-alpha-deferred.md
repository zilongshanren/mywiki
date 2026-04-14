---
tags: [source, 渲染, 延迟渲染, 透明, 光照]
date: 2026-04-14
sources: 1
---

# Lighting alpha objects in deferred rendering environments（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 9 月的调研笔记：在 Hieroglyph [[tiled-light-prepass|light prepass]] 渲染器里尝试多种方案给透明物体打上和 deferred 场景一致的多灯光照。

## 摘要

标准 [[deferred-rendering|deferred shading]] 天然不支持 alpha blending：G-Buffer 的每屏幕像素只能存一份材质，透明物必须另走 forward。Kostas 梳理了四条路：（1）**Deep G-Buffer / per-pixel linked list**——多层或可变层，强但吃内存；（2）**Stencil 多 pass**——对每个透明物跑一整遍 G-Buffer + 光照累加，O(#物 × #灯) 开销；（3）**屏幕门 / Dithered / Stochastic transparency**——用点阵把透明物混进 G-Buffer，Inferred Rendering 的路线，换视觉噪声；（4）**UV unwrap + off-screen lightmap**（Creative Assembly, Develop 2012）——把所有透明物体 UV 展开打到共享纹理、每个 texel 写入世界位置，交给光照 pass 生成一张 alpha lightmap，最后 forward 渲染时采样。他亲自实现了第四条：用一个气泡模型演示展开 → 写位置 → 光照 pass → 采样的流程，评述了三条限制——没法做镜面（只存位置）、纹理容量有限、光照 pass 需要适配非 screen-space 输入。

## 关键要点

- Deferred 的 G-Buffer 无法存多层 alpha 材质，是透明物的根本矛盾
- 路线 1：深 G-Buffer 或 per-pixel linked list——最强，但显存和 DX11 atomic 依赖
- 路线 2：Stencil 多 pass——O(#透明物 × #灯) 开销线性涨爆
- 路线 3：Inferred / Stochastic transparency——屏幕门伪透明，换视觉噪声换正确性
- 路线 4：UV 展开进纹理、存世界位置、光照 pass 做 alpha lightmap、最后 forward 采样
- 路线 4 把光照目标从屏幕像素改成物体表面，绕开了 depth sort
- 限制：只存位置 → 无 specular；纹理容量 → 有限透明物数量；光照 pass → 需要改写 light culling
- Kostas 在 Hieroglyph light prepass 上验证了路线 4 的可行性

## 链接到的概念

- [[deferred-alpha-lighting]]
- [[deferred-rendering]]
- [[alpha-blending]]
- [[tiled-light-prepass]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/09/24/lighting-alpha-objects-in-deferred-rendering-contexts/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-09-24_lighting-alpha-objects-in-deferred-rendering-environments.md`
