---
tags: [source, 渲染, mesh-shader, vulkan, hlsl, 坑]
date: 2026-04-19
sources: 1
---

# Workarounds for issues with mesh shaders + Vulkan + HLSL（Panagiotis Charitos）

[[people/panagiotis-charitos|Charitos]] 2024 年 8 月的一篇短博客，专门曝光一个"nVidia 能跑、AMD 崩、validation 不报错"的恶性地雷：mesh shader 输出变量里的 `PerPrimitiveEXT` decoration 在 HLSL+Vulkan 组合下必须手动补。

## 摘要

Mesh shader 的输出可以是 per-vertex 或 per-primitive，后者通过 `out primitives` 关键字声明。DXC 会给 mesh shader 的 primitive 变量加 `PerPrimitiveEXT` decoration，但 Vulkan 要求 **fragment shader 的对应入参也必须加上同一个 decoration**——而 HLSL 语法不允许 `primitives` 出现在 fragment 入口。结果：HLSL 合法、D3D12 正常、nVidia+Vulkan 正常、validation 无警告，只有 AMD+Vulkan 崩溃。作者给出的绕法是利用 DXC 的 `[[vk::ext_decorate]]` / `[[vk::ext_extension]]` / `[[vk::ext_capability]]` 属性手动在 struct member 和 fragment 入参上声明 decoration（魔法数字 `5271` = PerPrimitiveEXT, `5283` = MeshShadingEXT capability）。

## 关键要点

- per-primitive 变量在 VS→PS 链接层面需要两端都有 PerPrimitiveEXT decoration。
- DXC 补 mesh shader 侧，不补 fragment shader 侧。
- nVidia 驱动的高容错掩盖了大量这类 SPIR-V 不合规。跨厂商测试时 AMD/Arm 是更可靠的"真理机"。
- Vulkan validation layer 没覆盖这种 inter-stage decoration 不匹配。
- `[[vk::ext_*]]` 是 HLSL→SPIR-V 的通用逃生舱，可以塞任意 SPIR-V decoration/capability/extension/instruction。

## 链接到的概念

- [[mesh-shader-vulkan-hlsl-per-primitive]]
- [[meshlets-and-mesh-shaders]]
- [[spirv-parsing-rewriting]]

## 原文

- 链接：https://anki3d.org/workarounds-for-issues-with-mesh-shaders-vulkan-hlsl/
- 本地：`raw/articles/anki3d.org/2024-08-19_workarounds-for-issues-with-mesh-shaders-vulkan-hlsl.md`
