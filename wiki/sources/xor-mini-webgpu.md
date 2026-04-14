---
tags: [source, 渲染, gpu, api, webgpu, wgsl, compute]
date: 2026-04-14
sources: 1
---

# WebGPU（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 2 月 10 日的短文，从 GameMaker 用户视角解释 WebGPU 是什么、为什么 web 之外的引擎也要关心它，附带一份 WGSL 的极简入门。

## 摘要

WebGPU 是 W3C 推动的新一代 web 图形与计算 API，设计目标是**取代 WebGL** 并对齐 Vulkan / D3D12 / Metal 这代现代 GPU 编程范式。三个核心卖点：跨平台一套 API、低层级资源管理、**原生 compute shader**。Xor 强调这对 GameMaker 用户意义重大——GM 长期卡在 GLSL 1.00，连 `texelFetch` 都没有，而 WebGPU 随 GM 新 runtime 落地后会解锁 compute shader、storage buffer、bind group 等现代特性。配套语言 WGSL 的语法更接近 Rust / Swift：严格类型、`var` / `let`、`fn` 定义、`vec3f` 是 `vec3<f32>` 的别名、资源绑定用 `@group(x) @binding(y)`、主入口用 `@vertex / @fragment / @compute` 注解标记。GLSL 是驱动时编译的、跨硬件易出差异；WGSL 则设计为离线编译 + 前置验证，跨设备一致性强。作者坦言 WGSL 比 GLSL 啰嗦很多但这是必要的代价。

在开头有一大段**作者关于订阅商业模式的自白**：每周一天写教程、全年从 paid subscribers 赚 $655，决定改成「隔篇免费、间篇订阅」的新机制，并列出后续计划（Gamma Correction、Generalized Blur、Volume Shadows、One Pass Shaders、Xor Lang）。评论区有读者给出详细反馈（曝光度、免费/付费平衡、营销难度）。这部分是社区运营史料，非技术内容但反映 shader 独立作者的真实处境。

## 关键要点

- **WebGPU = Vulkan/D3D12/Metal 在 web 端的统一抽象**：走 D3D12 / Vulkan / Metal 三套后端，用户写一套。
- **最大解锁是 compute shader**：不依附 vertex/fragment 阶段，可做粒子 / 流体 / 图像滤波 / ML 等非 raster 任务。
- **显式 pipeline state + bind group**：资源用 `@group(x) @binding(y)` 显式绑，告别按名查 uniform location。
- **storage buffer**：大块、可读写、跨 kernel 共享，是 CPU-GPU 大量数据交换的现代答案。
- **WGSL ≈ Rust 味的 shader 语言**：`var` / `let`、强类型、`fn` 定义、`->` 返回类型、`@vertex` 标记入口、只支持 32 位标量类型。
- **跨设备一致性**：WGSL 离线编译 + 前置验证，避开 GLSL 驱动差异的历史顽疾。
- **GameMaker 的过渡**：runtime 级 GLSL → WGSL 自动翻译，存量 shader 不必立刻改写但终于能用 compute。
- **作者运营现状**：全年 $655 订阅收入，改成隔篇付费的新机制。

## 链接到的概念

- [[webgpu-intro]]
- [[rendering-api-depth]]
- [[fragment-shader]]
- [[compute-vs-raster-points]]
- [[gpgpu-json-parsing]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/webgpu
- 本地：`raw/articles/mini.gmshaders.com/2024-02-10_webgpu.md`
