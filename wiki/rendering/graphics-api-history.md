---
tags: [图形API, DirectX, OpenGL, Vulkan, 历史]
date: 2026-04-19
sources: 1
---

# 图形 API 演进史（DirectX / OpenGL / Vulkan）

[[adam-sawicki|Adam Sawicki]] 2025 年底为波兰《Programista》杂志写的科普长文《Graphics APIs – Yesterday, Today, and Tomorrow》2026 年开放免费阅读，走一遍图形 API 的历史——固定管线 → 可编程管线 → "现代"低层 API——搭配 GPU 硬件与商业游戏的双线。

## 主线

- **固定管线时代**：DirectX 5–7、OpenGL 1.x，状态机 + 一串 `glBegin/End`，渲染全靠驱动改 `glTexEnv`、`glLightModel` 之类巨量开关
- **可编程管线**：DX9 + GLSL 1.x 引入顶点/像素 shader，渲染流水线开始"写出来"；这时 API 从"状态机 + 图元"退化成"给 shader 喂数据"
- **AAA 时代的 DX10/11**：unified shader、compute shader、tessellation。API 还很高层——驱动替你管内存、管命令缓冲、管同步
- **现代低层 API**：Vulkan（2016）、D3D12（2015）、Metal（2014）。把内存分配、barrier、descriptor、命令录制全部甩给应用。换来的是 CPU 多核扩展 + 可预测的帧时间——但学习曲线指数级上升
- **未来**：[[hlsl-cooperative-vectors-tensor-cores|HLSL Cooperative Vectors / Linear Algebra Matrix]]、[[d3d12-work-graphs|Work Graphs]]、[[dxr-tier-2-clas-ptlas|DXR Tier 2]]、[[advanced-shader-delivery|Advanced Shader Delivery]]——重点从"画三角形"滑向"把 GPU 当通用流水线/ML 引擎用"

## 为什么值得一读

这篇文章不是教学（作者明说"不会教你怎么写代码"），而是写给**玩过上世纪/本世纪初游戏的普通玩家**的背景知识——解释为什么今天 DX12 不像 DX9 那样"`Device->DrawIndexed` 就出三角形"。

同一作者还在 [[pix-api-and-dxdmp]]、[[dxr-tier-2-clas-ptlas]]、[[advanced-shader-delivery]] 等文里持续追踪 D3D12 的"今天与明天"。

## 相关
- [[hlsl-cooperative-vectors-tensor-cores]]
- [[d3d12-work-graphs]]
- [[d3d12-resource-binding]]
- [[dxr-tier-2-clas-ptlas]]
- [[advanced-shader-delivery]]
- [[adam-sawicki]]
- [[vulkan-explicit-performance]] —— Supnik 2015 年 Vulkan 公布当日的立场帖：三大卖点与未解的资源管理问题
- [[mantle-api]] — AMD 2013 年低层 API，DX12/Vulkan 的先驱与倒逼者
- [[dx11-driver-overhead]] — DX11 驱动 CPU 开销的三个结构性根因（延迟状态/资源生命周期/deferred context）

## Sources

- [[sources/asawicki-graphics-apis-yesterday-today]]
- [[sources/c0de517e-on-mantle]]
- [[sources/alain-modern-graphics-apis]]
