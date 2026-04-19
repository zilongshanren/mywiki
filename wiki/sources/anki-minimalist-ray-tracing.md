---
tags: [source, 渲染, 光线追踪, gpu, 移动]
date: 2026-04-19
sources: 1
---

# Minimalist ray-tracing leveraging only acceleration structures（Panagiotis Charitos）

[[people/panagiotis-charitos|Charitos]] 2025 年 12 月发表的 AnKi "potato RT" 方案。用 ray query + TLAS instanceCustomIndex + position fetch 三件套，彻底绕开 `VK_KHR_ray_tracing_pipeline` / DXR 1.0，为移动和低端 GPU 提供一个能用的 indirect RT fallback。

## 摘要

AnKi 原本用 `VK_KHR_ray_tracing_pipeline` 做 RT shadows/indirect diffuse/indirect specular。indirect RT 的 hit shader 已经很薄——只写 thin G-Buffer（diffuseColor + worldNormal + emission + rayT），光照放在 ray-gen 里。但移动端要么不支持 RT pipeline、要么性能很差。Charitos 提出彻底绕开的"potato"实现：（1）材质的平均 diffuse 色在 asset baking 时算好、塞进 TLAS 的 `instanceCustomIndex`（24 位，RGB888 正好）；（2）法线用 `VK_KHR_ray_tracing_position_fetch` 在 shader 里从三个顶点位置现算面法线——DXC 未绑定该扩展，用 `[[vk::ext_instruction]]` + SPIR-V 魔法数字手动声明；（3）完全不用 SBT 和 hit shader。在 Sponza 上 indirect diffuse 看不出差别，Bistro 4K/RTX 4080 上速度略快。emission 暂未解决，设想用 instanceCustomIndex 的一个 bit 做 diffuse/emission 开关。文章结尾评论区有读者指出 normal 变换应该用 inverse transpose 而非直接用 object→world，作者承认。

## 关键要点

- **TLAS `instanceCustomIndex` 有 24 bits**——能塞 RGB888 或其他 per-instance 数据；shader 里用 `CommittedInstanceID()` 读。
- **`VK_KHR_ray_tracing_position_fetch`** 直接吐 ray 命中三角形的三个顶点位置，叉乘即面法线——省掉顶点 buffer 间接访问。DX12 **没有等价物**。
- DXC 未对该扩展做原生绑定，需要 `[[vk::ext_capability]]` + `[[vk::ext_extension]]` + `[[vk::ext_instruction]]` 手动外挂 SPIR-V 指令。和 [[mesh-shader-vulkan-hlsl-per-primitive]] 是同一类技巧。
- **不用 SBT**：因为 hit shading 完全移除——CPU 或 GPU 的 SBT 构建成本省掉。AnKi 的 SBT 构建在 GPU 端。
- **视觉近似**：indirect diffuse 低频，SSR 弥补反射细节——最坏情况（roughness=0，无 normal map）也勉强可看。
- **已知局限**：emission 尚未实现；AMD 驱动有 bug 导致 position_fetch + ray query 组合跑不起来；normal 变换应该用 inverse transpose（评论区指出）。
- **性能差距不大**：RTX 4080 / Bistro / 4K native，potato 比 RT pipeline 快但不夸张——说明 pipeline 版本开销本身就已被 AnKi 压得很薄。

## 链接到的概念

- [[minimalist-rt-acceleration-structures]]
- [[hybrid-raytracing-pipeline]]
- [[hybrid-raytraced-shadows-reflections]]
- [[bindless-rendering]]
- [[mesh-shader-vulkan-hlsl-per-primitive]]

## 原文

- 链接：https://anki3d.org/minimalist-ray-tracing-leveraging-only-acceleration-structures/
- 本地：`raw/articles/anki3d.org/2025-12-04_minimalist-ray-tracing-leveraging-only-acceleration-structur.md`
