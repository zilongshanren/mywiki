---
tags: [source, rendering, ssao, gtao, webgpu, use-gpu]
date: 2026-04-19
sources: 1
---

# Occlusion with Bells On（Steven Wittens / acko.net）

[[steven-wittens]] 发表于 2025 年 3 月的 Use.GPU 0.14 release note，把 [[ground-truth-ambient-occlusion|GTAO]]、buffer history、render pass 编排、WGSL 结构体类型串成一个"现代 SSAO 落地实录"。

## 摘要

Use.GPU 0.14 的标志性更新是内建 GTAO，让 out-of-the-box 渲染终于不再像"2000 年代早期 OpenGL"。作者解释 GTAO 选型（算的是正确可见性积分，同时产出 bent normal 用于 IBL），以及上线所需的配套：half-res 采样 + IGN 噪声 + 2x2 quad 预过滤 + temporal reprojection 基于 3D motion vector + depth/normal bilateral filter + overscan 抑制屏幕边缘失效。这些需求反过来驱动了 render 管线重构：buffer history 作为 first-class（每个 render target 有 `history[i]` 槽位自动轮转）、`<Pass>` 接受 `ssao={...}` 这样的 flag 自动 lower 成 buffer + subpass 图、binding group layout 从 4 个中腾出一个给传统 sub-pipeline 风格使用。Shader linker 升级为能完整解析 WGSL 结构体（包括跨模块 `array<T>`），配合 `structType(...)` 在 run-time 生成 WGSL 结构体，使数据源格式可以写成 `T` 或 `array<T>`，其中 T 是一个 shader 模块。inspector 新增按 reconciler node 类型过滤，依 data dependency 高亮，让 Use.GPU 大树一屏可读。作者的总结：renderer 本来就想是 reactive run-time，"写不出 wiring 的 pass 就别让用户写"。

## 关键要点

- GTAO vs crease SSAO：前者算正确可见性积分 + bent normal，显著改善 IBL 外观
- Interleaved Gradient Noise (IGN) + 2x2 quad 预过滤：比 blue noise 更快收敛
- Temporal reprojection：复用历史 depth/normal/samples；摄像机平滑移动不清空
- 刻意不让 reprojection 模糊 bent normal（否则所有边被圆角化）→ 用 depth/normal bilateral + 3D motion vector
- Overscan：framebuffer 扩张固定像素 + projectionMatrix 同步扩张，resolve 时裁掉；多出来的像素在下一帧可被 reproject 进可见区域
- Buffer history 应作为 GPU API 的 first-class 概念
- `<Pass>` 自动 lower：资源（`use(NormalBuffer, opts)`...）和 pass（`use(NormalPass, opts)`...）两阶段声明，通过"well-known names"隐式接线
- WebGPU 4 个 bind group 的腾挪：0.14 把 View 并入 Pass，`#3` 空出来给传统 monomorphized sub-pipeline
- `@binding` + struct types 可被 shader linker 完整解析，自动算 minimum binding size
- `structType(...)` 在 run-time 生成 WGSL struct，让"T or array<T> 里 T 是 shader module"成立

## 链接到的概念

- [[ground-truth-ambient-occlusion]]
- [[use-gpu-reactive-runtime]]
- [[render-pass-orchestration]]
- [[steven-wittens]]
- [[webgpu-intro]]

## 原文

- 链接：https://acko.net/blog/occlusion-with-bells-on/
- 本地：`raw/articles/acko.net/2025-03-24_occlusion-with-bells-on.md`
