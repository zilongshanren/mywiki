---
tags: [source, playcanvas, engine, webgl, webgpu, semver]
date: 2026-04-19
sources: 1
---

# PlayCanvas Engine Hits 2.0.0（Will Eastcott / PlayCanvas）

[[will-eastcott]] 在 2024 年 8 月发表的版本公告，宣布 PlayCanvas Engine 从 1.x 跨到 2.0.0——距离 1.0.0 已经过去 6 年、跨过 73 个 minor 版本。

## 摘要

PlayCanvas 团队借 2.0.0 这次 **major bump** 做了一次有意识的"春季大扫除"：按 semver 的语义，major 版本号的唯一合法用途就是引入 breaking change。自 2018 年 1.0.0 之后代码库里堆了不少 cruft——"设计糟糕、过度复杂或无用的代码"——到了影响引擎向前演进的程度，尤其是在推动 [[webgpu-intro|WebGPU]] 支持时被老分支拖累。这次清理砍掉了三类包袱：**WebGL 1** 支持（市场占有率已不足 2%）、**Scripts 1.0**（已废弃 8 年）、**AudioSourceComponent**（被 SoundComponent 取代多年）。Eastcott 强调策略上的审慎：Engine-only 用户可按需升级，Editor 用户在后续几周内按 opt-in 迁移，Engine 1.x 会在 Editor 里额外维持至少一年；新项目默认 2.0。同时宣布了基于 ESM 的新脚本系统即将推出。

## 关键要点

- Semver 的 major bump 的真正价值：**给团队一次"允许破坏"的窗口期**，把长期 deprecated 的代码一次性清掉。
- 支撑 breaking change 的数据基础：WebGL 1 份额 <2% 且单调下降。
- **cruft 的定义**（引用 Informal Computing 辞典）被作为决策依据：代码库健康不是空话，是拦路石多到挡住下一代 API 落地时才会被正视。
- Editor 用户的迁移路径提供了"商业引擎 major 升级"的模板：Engine-only 先行、Editor 长期兼容、新项目默认新版。
- Engine 2.0 同时推出若干新示例：cross-hatching 自定义 shader、SSAO、hardware instancing（含 glTF EXT_mesh_gpu_instancing）。

## 链接到的概念

- [[playcanvas-engine-2-breaking-changes]]
- [[playcanvas-webgpu-editor]]
- [[webgpu-intro]]
- [[will-eastcott]]

## 原文

- 链接：<https://blog.playcanvas.com/playcanvas-engine-hits-2-0-0>
- 本地：`raw/articles/blog.playcanvas.com/2024-08-22_playcanvas-engine-hits-2-0-0-playcanvas-blog.md`
