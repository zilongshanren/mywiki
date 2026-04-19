---
tags: [渲染, gpu, mesh-shader, vulkan, hlsl, 坑]
date: 2026-04-19
sources: 1
---

# Mesh Shader + Vulkan + HLSL 的 per-primitive 坑

[[meshlets-and-mesh-shaders|Mesh shader]] 管线里，输出变量可以是 **per-vertex**（和老 vertex shader 一样）或 **per-primitive**（mesh shader 新增）。per-primitive 变量用 `primitives` 关键字声明：

```hlsl
[numthreads(64,1,1)] [outputtopology("triangle")]
void meshMain(
    out vertices PerVertOut myVerts[XXX],
    out primitives PerPrimitiveOut myPrimitives[XXX],
    out indices uint3 indices[XXX])
{
    ...
}
```

## 问题在 fragment shader

DXC 会把 mesh shader 里的 `myPrimitives` 自动加上 **PerPrimitiveEXT** decoration——这是 mesh shader 专属的 SPIR-V decoration。但 Vulkan 规范要求：**fragment shader 的对应入参也必须带 PerPrimitiveEXT**，否则 SPIR-V 链接信息不对。问题在于 HLSL 的 fragment shader 里根本没有 `primitives` 这个关键字，DXC 也不会主动给 fragment 入参加 decoration。于是写出来的 HLSL 是"合法"的，但编出来的 SPIR-V 是错的。

这个 bug 极其难排查：

- HLSL 代码 **合法**，编译通过；
- D3D12 里 **正常运行**（DX 在 PSO 创建时才做 semantic 链接，能兜住）；
- nVidia + Vulkan **正常运行**（驱动习惯性兜底用户错误）；
- Vulkan validation layer **不报错**；
- 在 AMD 上 **失败**，且没人知道为什么。

典型的"三份硬件里两份能跑"型地雷。

## 绕法：SPIR-V inline intrinsic

DXC 支持用 `[[vk::ext_decorate]]`、`[[vk::ext_extension]]`、`[[vk::ext_capability]]` 把任意 SPIR-V decoration/capability 直接写进 HLSL。所以手动补一份：

```hlsl
struct PerPrimitiveOut {
    [[vk::ext_decorate(5271 /*PerPrimitiveEXT*/)]] float4 someMember;
    [[vk::ext_decorate(5271 /*PerPrimitiveEXT*/)]] float4 someOtherMember;
};

FragOut psMain(
    in PerVertOut myVerts,
    [[vk::ext_extension("SPV_EXT_mesh_shader")]]
    [[vk::ext_capability(5283 /*MeshShadingEXT*/)]]
    PerPrimitiveOut myPrimitives)
{
    ...
}
```

数字 `5271` 是 `PerPrimitiveEXT` 的 SPIR-V 枚举值，`5283` 是 `MeshShadingEXT` capability。丑但有效——AMD 上立刻跑通。

## 经验教训

- **"nVidia 能跑"不等于"写对了"**——nVidia 驱动对不合规 shader 的容错比 AMD/Arm 高一个量级，跨厂商移植时必须反过来用 AMD/Arm 做真理机。
- **Vulkan validation 不覆盖 inter-stage decoration 不匹配**——至少 2024 年那一版还没有。AnKi 作者同时提了 issue 到 DXC、Vulkan-ValidationLayers 和 SPIRV-Cross 希望补上。
- **DXC 的 `[[vk::ext_*]]` 系列**是 HLSL 写 Vulkan 专属 SPIR-V 的逃生舱。类似的技术也用在 [[minimalist-rt-acceleration-structures]] 里手工调用 `VK_KHR_ray_tracing_position_fetch`。

## 相关

- [[meshlets-and-mesh-shaders]] —— mesh shader 管线总览
- [[spirv-parsing-rewriting]] —— 同一作者另一条"手动碰 SPIR-V"的线索
- [[minimalist-rt-acceleration-structures]] —— 同样用 `[[vk::ext_instruction]]` 外挂 SPIR-V 指令

## Sources

- [[sources/anki-mesh-shader-vulkan-hlsl]]
