---
tags: [source, unity, draw-call, rendering, tutorial]
date: 2026-04-19
sources: 1
---

# Draw Call 初步理解（Ted Sie / 阿祥的开发日常）

[[ted-sie]] 于 2016 年 7 月发表，作为 NGUI 系列里的延伸一篇，用 Unity 编辑器里的 DrawCall 计数器演示了**材质/渲染路径如何决定 Draw Call 数**。

## 摘要

文章把 Draw Call 定义为"一次从 Shader 到显示的转换"，Draw Call 越高越吃 CPU 性能。作者用三个场景对照说明：两个共用 `Material_1` 的平面 → DrawCall = 2（即便 Material 相同，两个独立对象各自一次渲染路径）；把其中一个材质换成 `Material_2`（Shader 相同，Material 不同）→ DrawCall = 3，说明**Material 实例就是批的边界**；而 NGUI 场景里多张 UISprite 仍能维持 DrawCall = 2——因为 [[ngui-legacy-ui-system|NGUI]] 的 UIPanel 把同一 Atlas 的 Sprite 合成一次提交。文章偏入门，但提供了一份好用的最小反例集合，正好把 [[draw-call]] 的理论落到 Unity 的表现上。

## 关键要点

- Draw Call 高 = CPU 压力大，降 DrawCall 是 2D UI 与移动端的核心优化。
- **相同 Material 实例**才能合批，"Shader 相同 Material 不同"仍然拆批。
- Atlas（共享 Material）是 NGUI 能合批的前提。
- 作者自承"只是个人理解"，未涉及 SRP Batcher / GPU Instancing 等后续方案——这篇是 2016 年的入门视角。

## 链接到的概念

- [[draw-call]]
- [[ngui-legacy-ui-system]]
- [[ted-sie]]

## 原文

- 链接：<https://tedsieblog.wordpress.com/2016/07/10/basic-knowledge-of-draw-call/>
- 本地：`raw/articles/tedsieblog.wordpress.com/2016-07-10_basic-knowledge-of-draw-call-draw-call-chu-bu-li-jie.md`
