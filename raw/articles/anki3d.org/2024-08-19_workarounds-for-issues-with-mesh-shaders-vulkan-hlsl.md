---
title: Workarounds for issues with mesh shaders + Vulkan + HLSL
url: https://anki3d.org/workarounds-for-issues-with-mesh-shaders-vulkan-hlsl/
author: Panagiotis Christopoulos Charitos
published: '2024-08-19'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

**TL;DR: If using per-primitive in/out in mesh shaders in Vulkan and in HLSL/DXC you need to manually decorate variables and struct members using SPIR-V intrinsics. See how at the bottom.**

This is going to be a quick post to raise awareness to a difficult to track bug with mesh shaders in Vulkan when using HLSL. Hopefully this will save some time to the next poor soul that bumps into this.

With mesh shaders you have two options when it comes to output variables. Your output can be **per-vertex** (just like in vertex shaders) or it can be **per-primitive** which is a new addition with mesh shaders. This is how a mesh shader entry point could look like:

```
[numthreads(64, 1, 1)] [outputtopology("triangle")]
void meshMain(
out vertices PerVertOut myVerts[XXX],
out primitives PerPrimitiveOut myPrimitives[XXX],
out indices uint3 indices[XXX])
{
...
}
```

The **“vertices”** keyword denotes that the output will be per-vertex and the **“primitives”** keyword that it’s per-primitive. DirectX compiler will decorate the myPrimitives with the **PerPrimitiveEXT** decoration which is special to mesh shaders. That’s all fine but the real problem lies in the fragment shader. Vulkan mandates that myPrimitives should be decorated with PerPrimitiveEXT in the fragment shader as well. But in HLSL there is no way to do that. The “primitives” keyword is not allowed in fragment shaders.

```
FragOut psMain(in PerVertOut myVerts, PerPrimitiveOut myPrimitives)
{
...
}
```

In other words, if someone tries to use HLSL to write mesh shaders that use per-primitive input/output variables they will end with incorrect SPIR-V. The problems continue because **at the moment** this is a very hard to diagnose error.

- The HLSL is valid
- It works in D3D12 (because D3D12 does semantics linking at PSO creation time)
- It works on nVidia + Vulkan (because nVidia has a tendency to workaround user errors)
- Vulkan validation doesn’t complain

… but it fails on AMD and nobody can understand why.

How to workaround this issue then? We can use SPIR-V inline intrinsics! It’s a little bit cumbersome but it can be done. This is how we should change our fragment shader:

```
struct PerPrimitiveOut {
[[vk::ext_decorate(5271 /*PerPrimitiveEXT*/)]] float4 someMember;
[[vk::ext_decorate(5271 /*PerPrimitiveEXT*/)]] float4 someOtherMember;
};
FragOut psMain(
in PerVertOut myVerts,
[[vk::ext_extension("SPV_EXT_mesh_shader")]] [[vk::ext_capability(5283 /*MeshShadingEXT*/)]] PerPrimitiveOut myPrimitives)
{
...
}
```

And voila! It works on AMD.

For reference I’ve create a couple of github issues that will help avoiding this issue: