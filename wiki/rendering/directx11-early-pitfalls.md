---
tags: [渲染, DirectX11, tessellation, compute-shader, HLSL, API设计]
date: 2026-04-14
sources: 1
---

# DirectX 11 早期开发踩坑笔记

DirectX 11 在 2009–2010 年刚铺开时，文档稀薄、debug layer 提示模糊、驱动也没磨光，开发者只能**靠 trial-and-error** 摸索 tessellation、compute shader、HLSL 这些新加入的特性。[[matthaeus-chajdas]] 在 2010 年初的一篇短笔记里整理了几个典型坑，至今仍然能反映**新硬件特性 + 验证层不充分**的混合体验：编译器报错信息含混、驱动在用户错误下直接死锁、API 设计的隐含约束散落在 SDK 各处。

## tessellation：domain shader 与 topology

[[rendering-pipeline]] 在 DX11 里多了 hull / tessellator / domain 三个阶段。两个常见报错对应两类被忽略的硬约束：

- **`error X4577: Not all elements of SV_Position were written`**——domain shader 必须写满 4 维 `SV_Position`，跟 vertex shader 一样不能偷懒只写 xyz。
- **`error X3502: tessfactor inputs missing`**——三角形与四边形 patch 都必须同时设置 `SV_TessFactor`（边细分数）与 `SV_InsideTessFactor`（内部细分数）。两者**幅度差距过大**会让边界顶点的 valence 爆炸，结果是沿边产生破洞或撕裂。

更阴险的是 topology 设置不对会**直接冻死整台机器**：tessellation 阶段必须用 `D3D11_PRIMITIVE_TOPOLOGY_<N>_CONTROL_POINT_PATCHLIST`，`<N>` 等于 hull shader 期待的控制点数量。如果误用 `TRIANGLELIST`，2010 年的 ATI 驱动会直接 hang，需要等待 Windows 7 的 TDR 重置。这是「驱动应当对用户错误防御」的反例。

## compute shader：资源绑定危险与 RW 纹理

compute shader 把 SRV 与 UAV 引入了 [[d3d12-resource-binding|资源绑定]] 模型，但 DX11 的状态机继承自传统图形管线，**资源绑定状态会跨 dispatch 残留**。典型现象是 debug layer 抱怨：

- `OMSetRenderTargets` 时旧的 SRV 还挂在某个 slot 上 → `DEVICE_OMSETRENDERTARGETS_HAZARD`；
- 后续 dispatch 时驱动被迫强制把 CS 资源 slot 置空 → `DEVICE_CSSETSHADERRESOURCES_HAZARD`。

唯一稳妥的解法是**在每次 `Dispatch` 后用 `CSSetShaderResources` 显式解绑**，传入一个全 nullptr 的数组。这是 [[gpu-hazard-tracking|GPU 资源 hazard]] 在用户层手动解决的一个具体案例。

可读写纹理的创建方式也不直观：`D3D11_TEXTURE2D_DESC` 的 BindFlags 必须同时打开 `SHADER_RESOURCE | UNORDERED_ACCESS`，再为它单独建一个 `UnorderedAccessView`。一旦缺少其中之一，绑定与采样都会失败。HLSL 里 register 也是有规矩的——`tN` 给纹理与 structured buffer，`uN` 给 UAV，`bN` 给 cbuffer，**顺序必须一致**才能跨 shader 复用绑定布局。

## HLSL 小招

要在 HLSL 里得到正无穷，直接写 `float i = 1.#INF`——比 `1.0/0.0` 这种依赖 IEEE 行为的写法稳。

## 为什么这篇笔记仍然有意义

笔记本身的具体坑随着 DX11 文档与 debug layer 完善已经过时，但它示范的几条**新 API 上线期的工程态度**是通用的：debug 信息含混时把每条警告记录下来当成 contract；驱动会因用户错误冻机时，把状态清理写成 invariant 而不是「记得就清」；API 默认值与隐含约束散落各处时，宁可在自己代码里包一层 wrapper。这些做法在后来 [[d3d12-resource-binding|D3D12 显式资源绑定]]、Vulkan 验证层、Metal 等更新的 API 演化里反复出现。

## 相关
- [[rendering-pipeline]]
- [[d3d12-resource-binding]]
- [[gpu-hazard-tracking]]
- [[shaderlab-hlsl-basics]]
- [[matthaeus-chajdas]]
- [[directx-sdk-to-windows-sdk-migration]] —— June 2010 SDK 迁到 Windows 8.x SDK 的三类隐形依赖

## Sources

- [[sources/anteru-directx11-hints]]
- [[sources/alain-raw-dx11]] — Alain Galvan DX11 Hello Triangle 完整流程
