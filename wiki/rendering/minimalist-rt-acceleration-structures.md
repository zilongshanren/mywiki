---
tags: [渲染, 光线追踪, gpu, 移动, 优化]
date: 2026-04-19
sources: 1
---

# 只用加速结构的"土豆级"光追

[[people/panagiotis-charitos|Charitos]] 在 AnKi 里为移动和低端 GPU 做的"勉强能看"的 RT 实现。目标是**彻底绕开 `VK_KHR_ray_tracing_pipeline` / DXR 1.0**——不用 ray-gen/hit/miss 三段式，不用 shader binding table，甚至不用采样任何纹理——只靠 ray query（inline RT）加顶层加速结构里塞的几个数据位就把间接漫反射和间接镜面反射糊出来。

## 为什么要这么抠

`ray_tracing_pipeline` 在移动端要么不支持，要么跑起来巨慢；它还强制使用 shader binding table，这在 TLAS 动态重建的场景里成本不低。对 indirect diffuse / specular 这种**本来就是低频 + 大量近似**的需求来说，一个能跑就行的"potato"版本反而比高保真 pipeline 更实用。

## 基线：`ray_tracing_pipeline` 怎么用

AnKi 的 indirect RT 已经做得很精简：hit shader 只写回一个 "thin G-Buffer"——`diffuseColor + worldNormal + emission + rayT`——真正的光照在 ray-gen 里完成。即便如此仍需管理多个 RT library（RT shadows、indirect RT）、多份 hit shader、完整的 SBT，和材质加载时的 hit shader 选择逻辑。

## Potato 版本的三板斧

### 1. 把 diffuse 塞进 TLAS instanceCustomIndex

`VkAccelerationStructureInstanceKHR` 里的 `instanceCustomIndex` 有 24 位空位，正好塞一个 RGB888 的"平均 diffuse 颜色"。离线 baking 时对每张 diffuse 贴图算一个平均色，材质烘焙时写进 TLAS instance。shader 里用 `CommittedInstanceID()` 读回：

```hlsl
RayQuery<...> q;
...
U32 id = q.CommittedInstanceID();
UVec3 coloru = (UVec3)id >> UVec3(16, 8, 0);
coloru &= 0xFF;
Vec3 color = Vec3(coloru) / 255.0;
```

**副产品**：完全不用采样任何 diffuse 贴图——省掉了 bindless 访问和 cache miss。

### 2. 法线从 `VK_KHR_ray_tracing_position_fetch` 现算

扩展 `VK_KHR_ray_tracing_position_fetch` 让 ray query 直接吐出命中三角形的三个顶点位置。DX12 没有等价品。拿到三点之后叉乘得面法线，再用 TLAS 的 object→world 矩阵变换到世界空间。HLSL 里因为 DXC 不直接绑定该扩展，需要用 `[[vk::ext_instruction]]` 手动声明 SPIR-V 指令：

```hlsl
[[vk::ext_capability(SpvRayQueryPositionFetchKHR)]]
[[vk::ext_extension("SPV_KHR_ray_tracing_position_fetch")]]
[[vk::ext_instruction(SpvOpRayQueryGetIntersectionTriangleVertexPositionsKHR)]]
float3 spvRayQueryGetIntersectionTriangleVertexPositionsKHR(
    [[vk::ext_reference]] RayQuery<RAY_FLAG_FORCE_OPAQUE> query, int committed)[3];

// ...
Vec3 positions[3] = spvRayQueryGetIntersectionTriangleVertexPositionsKHR(q, 1);
Vec3 vertNormal = normalize(cross(positions[1] - positions[0], positions[2] - positions[1]));
Vec3 worldNormal = normalize(mul(q.CommittedObjectToWorld3x4(), Vec4(vertNormal, 0.0)));
```

（文章评论区有人指出：严格来说 normal 变换应该用 `CommittedWorldToObject` 的**逆转置**，否则带非均匀缩放或 skew 的 mesh 会出错。作者已承认。）

这是和 [[mesh-shader-vulkan-hlsl-per-primitive]] 同源的技巧——用 DXC 的 `[[vk::ext_*]]` 拼装 Vulkan 专属 SPIR-V。

### 3. 扔掉 SBT

因为 hit shading 完全不发生了（`CommittedInstanceID` 和 position fetch 都在 ray-gen 侧跑），可以完全关掉 shader binding table 和 hit group 的构造——CPU 或 GPU 侧（AnKi 的 SBT 在 GPU build）都省一截。

### 未解决：emission

尚未实现。可选方案是把 `instanceCustomIndex` 拆一位做 flag：0 表示后 23 位是 diffuse RGB，1 表示是 tone-mapped emission。不完美但可行。

## 效果

- **Sponza 上 indirect diffuse**：和 pipeline 版基本看不出差距（indirect diffuse 本来就是低频信号）。
- **反射**：作者刻意把 roughness 全拉到 0、法线贴图全关掉，做最坏情况；结果仍接近——主要是因为 AnKi 同时用 SSR 补了细节。
- **性能**：4080 跑 Bistro 4K native，potato 比 pipeline 快，但不夸张。AMD 因为 `VK_KHR_ray_tracing_position_fetch` + ray queries 有驱动 bug 没法测。

## 启示

- 当一个特性**语义上就是低频/近似**（indirect diffuse、AO、间接 GI 的 fallback），高保真的硬件管线是过度设计。TLAS instance 里塞数据 + ray query 就能顶很多事。
- DXR 的"完整 pipeline"在移动和低端场景里是累赘。**只要加速结构构建可用**，就能做出很便宜的混合方案——和 [[hybrid-raytracing-pipeline]] 的思路同源，但更极端。
- 这套技术对 SSR/probe/ambient cube 等现有缓存有强协同——在 SSR 能覆盖的范围内，RT 只要糊出远场就够。

## 相关

- [[hybrid-raytracing-pipeline]] —— 另一种对"昂贵 RT"的回避策略
- [[hybrid-raytraced-shadows-reflections]] —— Kostas 2018 年 compute shader 手写 BVH 的先驱
- [[bindless-rendering]] —— pipeline RT 依赖 bindless 访问材质，potato RT 彻底绕过
- [[mesh-shader-vulkan-hlsl-per-primitive]] —— 同样借助 DXC `[[vk::ext_*]]` 外挂 SPIR-V
- [[spirv-parsing-rewriting]] —— 作者另一条"手动碰 SPIR-V"的线索

## Sources

- [[sources/anki-minimalist-ray-tracing]]
