---
tags: [source, 渲染, 调试, gpu]
date: 2026-04-14
sources: 1
---

# New debugging options in CSharpRenderer framework（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 9 月发布的 CSharpRenderer（他自己的 C#/.NET DX11 渲染框架）小更新公告。文章简短，但值得记录的是它示范了两条对小型图形项目都很有价值的调试工具实现路径。

## 摘要

更新主要做了两件事：

1. **Surface debug snapshots**：很多调试需求是「我想看 SSAO buffer 长什么样」，但中间 RT 会被后续 pass 覆盖，无法在帧末抓。框架提供 `SurfaceDebugManager.RegisterDebug(context, "name", surface)`，在用户请求时把当前快照拷到一个独立 debug buffer 显示，可显示 RGB / Alpha / 小数值（用于 depth / world position）。无需写额外 shader 代码，UI 自动注册。
2. **GPU printf via UAV append buffers**：用 append/consume buffer 实现一个简陋但好用的「printf from GPU」。在 shader 里只需 `if (DEBUG_FILTER_VPOS(...)) DebugInfo(...)`，框架在 CPU 侧回读 buffer 显示。提供按屏幕坐标过滤（pixel shader）和按 dispatch thread ID 过滤（compute shader）两种宏；过滤坐标可以通过 UI 覆盖，甚至在 viewport 上点击直接拾取。

文章还提到一些次要更新：基于 luma clamping 的简易 TAA（受 Brian Karis UE4 SIGGRAPH 演讲启发）、最终图像加 dithering、提取 global constant buffer、freeze time 选项。

## 关键要点

- **快照式 debug**：解决「中间 RT 被覆盖」问题的最简单方案——在感兴趣点显式注册一份拷贝。
- **UAV append buffer = GPU printf**：思路并不新（c0de517e 2013 年就写过 DX11 GPU printf），Wronski 的贡献是把它做成无需写 CPU 代码的小工具。
- **过滤宏配合 UI 拾取**：调试 NaN / 负值时，「屏幕上点一下」就能定位的体验比 RenderDoc 重抓一帧要轻得多。
- **设计视角**：两套机制都是典型「小接口、大功能」的深模块——调用者只写 1-2 行，框架处理状态管理 / 数据流 / UI 集成。

## 链接到的概念

- [[gpu-printf-debugging]]
- [[debug-visualization]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/09/14/new-debugging-options-in-csharprenderer-framework/
- 仓库：https://github.com/bartwronski/CSharpRenderer
- 本地：`raw/articles/bartwronski.com/2014-09-14_new-debugging-options-in-csharprenderer-framework.md`
