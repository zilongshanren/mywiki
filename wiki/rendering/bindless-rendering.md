---
tags: [渲染, gpu, api, 架构]
date: 2026-04-14
sources: 1
---

# Bindless Rendering

Bindless 是现代 GPU 把"资源访问自由化"的关键一步。传统渲染管线里，每个 drawcall 都要走一套"逐 drawcall 寄存器绑定"：CPU 反复告诉 GPU"这是这次要用的 CB、SRV、纹理"。这层绑定既是 [[draw-call]] 开销的主要来源，也限制了着色器内部任意访问资源的能力。

## Bindless 的本质

Bindless 依赖 **现代 GPU 的 address 访问机制**：CPU 只需要把所有可能用到的资源组织成一张大表，把表的地址告诉 GPU；着色器在运行时直接用 `instanceId`、`triangleId`、material index 等数据索引到具体的顶点缓冲、材质参数、纹理上。资源访问 **几乎完全发生在 GPU 内部**，CPU 只负责"组织"而不负责"绑定"。

## 为什么光追和 VB 管线是 Bindless 的天然受益者

光追场景下，GPU 根据 hit 结果需要自由访问任意三角面的顶点、任意材质的属性、任意纹理的采样；显然没法提前 per-drawcall 绑好。**Bindless 本就是光追的前提条件之一**。

同样，[[visibility-buffer|Visibility Buffer]] 管线靠像素上的 `instanceId + triangleId` 反查资源，也天然需要 bindless：任意像素对应的材质/纹理都要能即时索引。

## 工业界观察

[[people/gameknife|gameknife]] 在用 RenderDoc 观察 R 星的《荒野大镖客》、Decima（《地平线》系列）时发现，它们的 shader 代码 **异常精简**——因为 bindless 已经把"一层一层的寄存器绑定样板"清洗掉了。这是现代 AAA 渲染器把复杂度从 CPU API 驱动侧转移到 GPU 数据结构侧的典型结果。

## 兼容性

Bindless 的硬件/驱动兼容性在 2024 年已经相当成熟：gkNextRenderer 在骁龙 865 这种 2020 年的移动 SoC 上都能完整跑起来，只有硬件光追本身仍需要 8 Gen 2 级别的设备。

## 相关

- [[visibility-buffer]]
- [[draw-call]]
- [[d3d12-resource-binding]]
- [[gpu-hazard-tracking]]
- [[rendering-api-depth]]

## Sources

- [[sources/gameknife-gknextrenderer-yearone]]
