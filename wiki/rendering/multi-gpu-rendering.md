---
tags: [渲染, multi-gpu, 延迟渲染, 游戏引擎, 性能]
date: 2026-04-27
sources: 1
---

# 多 GPU 渲染

多 GPU 渲染（Multi-GPU Rendering）是指将渲染管线的不同阶段或不同帧分配给多颗 GPU 并行执行，以突破单卡性能上限。在高端战场仿真、科研可视化和极分辨率（4K/8K）实时渲染场景中，单张消费级 GPU 往往无法在帧时间预算内完成 G-Buffer 填充、光照、后处理和粒子的全部工作，多 GPU 因此成为一条可行路线。

## 管线切分策略

[[people/wolfgang-engel|Wolfgang Engel]] 2015 年提出的一种参考布局将 [[deferred-rendering|延迟渲染管线]] 按阶段切分给 4 颗 GPU：

- **GPU 0**：Z prepass + G-Buffer 填充
- **GPU 1**：延迟光照与阴影（消费 GPU 0 的 G-Buffer）
- **GPU 2**：粒子系统与植被（消费 GPU 1 的光照结果）
- **GPU 3**：屏幕空间材质（皮肤等）+ 后处理（PostFX）
- **GPU 4+**：物理模拟、AI 计算

各 GPU 形成流水线，下一颗等待上一颗输出。可以并行执行，但会引入 2–3 帧渲染延迟。在 60 fps / 120 fps 目标帧率下，这个延迟通常低于 17–25 ms，视觉上不可感知。

G-Buffer 本身也可以在多颗 GPU 之间横向拆分：一颗负责 Z prepass，一颗填 diffuse/normal，另一颗填地形几何数据，植被专属一颗。

## 工程资源规则

- **CPU 核心数**：每颗 GPU 约需 2–4 个 CPU 核心来喂给它足够的 draw call；4 GPU 系统建议 8–16 CPU 核心。
- **系统内存**：建议至少是 GPU 显存总量的 2 倍（每 GPU 2 GB → 系统需 ≥ 16 GB）。

## 带宽约束与 G-Buffer 的局限

4K 分辨率（3840×2160）下，四张 32-bit 渲染目标占约 127 MB；含 MSAA 后 G-Buffer 可轻松膨胀到 500 MB–1 GB。高端 GPU 在 8–16 ms 内填满这样一个 G-Buffer 已相当吃力。Engel 事后承认，G-Buffer 在高分辨率下因内存带宽成为瓶颈而逐渐不再适合，建议改用 [[visibility-buffer|Visibility Buffer]]——仅需两张 32-bit 渲染目标，带宽压力随分辨率提升差距愈发显著。

## API 支持

DirectX 12 和 Vulkan 提供显式多适配器（Multi-Adapter）接口，允许应用程序直接控制跨 GPU 的资源创建、命令队列和内存传输。相比 DirectX 11 的隐式 SLI/CrossFire 黑盒，显式 API 让管线拆分方案更容易实现和调试。

## 相关

- [[deferred-rendering]] — 多 GPU 布局最常见的宿主管线
- [[visibility-buffer]] — 高分辨率下 G-Buffer 的替代方案，带宽更优
- [[async-compute]] — 单 GPU 内 compute 与光栅化的并行，是多 GPU 管线的"单卡版"
- [[the-forge-renderer]] — Confetti 的跨平台渲染框架，承载了多 GPU 相关实验
- [[people/wolfgang-engel]]

## Sources

- [[sources/humus-multi-gpu-engine]]
