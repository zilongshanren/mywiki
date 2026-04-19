---
tags: [source, mach, zig, 游戏引擎, webgpu, 音频]
date: 2026-04-19
sources: 1
---

# Mach v0.3 released - Zig game engine & graphics toolkit（Stephen Gutekanst）

[[stephen-gutekanst]] 2024 年 2 月的 Mach v0.3 release note，集中展示了 sysgpu 从"WebGPU 的一个实现"演变成"WebGPU 继任者"、Mach 引擎作为"一套模块"的定位，以及 libmach / sysaudio / ECS / mach.math / Sprite 等各模块的进展。

## 摘要

Mach 在 v0.3 里把自己从"又一个 game engine"重新包装成"一套可独立使用的 Zig 标准库风模块"。核心模块 mach-core 目标是替代 SDL+OpenGL / GLFW+Vulkan，当前仍借 GLFW+WebGPU 过渡；libmach 给 core 和引擎层加 C API。sysgpu 在半年内发展成功能近乎完整的 WebGPU 原生实现（D3D12/Vulkan/Metal/OpenGL + 自己的 WGSL 编译器），并开始有计划脱离 WebGPU 的 API 兼容——削减 pipeline 描述符样板、把 push constant 当一等特性、用 Zig 自身做 shading language 等。sysaudio 从 libsoundio 的 Zig 绑定独立成原生库，加入 SIMD 采样转换、修复 macOS CoreAudio 多通道麦克风 bug。ECS 拿到 query API，mach.math 引入基础向量/矩阵/四元数和 ray-triangle intersect，mach.gfx.Sprite 能用 ECS 每个 sprite 带独立变换压测数十万实体。v0.3 还正式化了 [[mach-nominated-zig-versions|Zig 提名版本]]。

## 关键要点

- Mach 的价值观：模块化标准库 vs 单体大引擎。
- sysgpu 脱离 WebGPU ABI 兼容是主动选择，不是意外。
- 作者继续明确"business job by day, Mach by night"，长期目标是靠 Mach+游戏为生。

## 链接到的概念

- [[mach-engine]]
- [[sysgpu-webgpu-successor]]
- [[mach-nominated-zig-versions]]
- [[stephen-gutekanst]]

## 原文

- 链接：<https://devlog.hexops.org/2024/mach-v0.3-released/>
- 本地：`raw/articles/devlog.hexops.org/2024-02-02_mach-v0-3-released-zig-game-engine-graphics-toolkit.md`
