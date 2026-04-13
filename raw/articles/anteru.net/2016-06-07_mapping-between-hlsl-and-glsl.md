---
title: Mapping between HLSL and GLSL
url: https://anteru.net/blog/2016/mapping-between-HLSL-and-GLSL
published: '2016-06-07'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

It’s 2016 and we’re still stuck with various shading languages - the current contenders being HLSL for Direct3D, and GLSL for OpenGL and as the “default” front-end language to generate SPIR-V for Vulkan. SPIR-V may become eventually the IL of choice for everything, but that will take a while, so right now, you need to convert HLSL to GLSL or vice versa if you want to target both APIs.

I won’t dig into the various cross-compilers today - that’s a huge topic - and focus on the language similarities instead. Did you ever ask yourself how your `SV_Position`

input is called in GLSL? Then this post is for you!

Note

This is by no means complete. It’s meant as a starting point when you’re looking to port some shaders between GLSL to HLSL. I’m omitting functions which are the same for instance.

## System values & built-in inputs

Direct3D specifies a couple of system values, GLSL has the concept of built-in variables. The mapping is as following:

| HLSL | GLSL |
|---|---|
`SV_ClipDistance` |
`gl_ClipDistance` |
`SV_CullDistance` |
`gl_CullDistance` if
|
`SV_Coverage` |
`gl_SampleMaskIn` & `gl_SampleMask` |
`SV_Depth` |
`gl_FragDepth` |
`SV_DepthGreaterEqual` |
`layout (depth_greater)` `out float gl_FragDepth;` |
`SV_DepthLessEqual` |
`layout (depth_less)` `out float gl_FragDepth;` |
`SV_DispatchThreadID` |
`gl_GlobalInvocationID` |
`SV_DomainLocation` |
`gl_TessCord` |
`SV_GroupID` |
`gl_WorkGroupID` |
`SV_GroupIndex` |
`gl_LocalInvocationIndex` |
`SV_GroupThreadID` |
`gl_LocalInvocationID` |
`SV_GSInstanceID` |
`gl_InvocationID` |
`SV_InsideTessFactor` |
`gl_TessLevelInner` |
`SV_InstanceID` |
`gl_InstanceID` & `gl_InstanceIndex` (latter in Vulkan with different semantics) |
`SV_IsFrontFace` |
`gl_FrontFacing` |
`SV_OutputControlPointID` |
`gl_InvocationID` |
| N/A | `gl_PatchVerticesIn` |
`SV_Position` |
`gl_Position` in a vertex shader, `gl_FragCoord` in a fragment shader |
`SV_PrimitiveID` |
`gl_PrimitiveID` |
`SV_RenderTargetArrayIndex` |
`gl_Layer` |
`SV_SampleIndex` |
`gl_SampleID` |
The equivalent functionality is available through `EvaluateAttributeAtSample` |
`gl_SamplePosition` |
`SV_StencilRef` |
`gl_FragStencilRef` if
|
`SV_Target` |
`layout(location=N) out` `your_var_name;` |
`SV_TessFactor` |
`gl_TessLevelOuter` |
`SV_VertexID` |
`gl_VertexID` & `gl_VertexIndex` (latter Vulkan with different semantics) |
`SV_ViewportArrayIndex` |
`gl_ViewportIndex` |

This table is sourced from the [OpenGL wiki](https://www.opengl.org/wiki/Built-in_Variable_%28GLSL%29), the [HLSL semantic documentation](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509647%28v=vs.85%29.aspx) and the [GL_KHR_vulkan_glsl](https://www.khronos.org/registry/vulkan/specs/misc/GL_KHR_vulkan_glsl.txt) extension specification.

## Atomic operations

These map fairly easily. `Interlocked`

becomes `atomic`

. So `InterlockedAdd`

becomes `atomicAdd`

, and so on. The only difference is `InterlockedCompareExchange`

which turns into `atomicCompSwap`

.

## Shared/local memory

`groupshared`

memory in HLSL is `shared`

memory in GLSL. That’s it.

## Barriers

| HLSL | GLSL |
|---|---|
`GroupMemoryBarrierWithGroupSync` |
`groupMemoryBarrier` and `barrier` |
`GroupMemoryBarrier` |
`groupMemoryBarrier` |
`DeviceMemoryBarrierWithGroupSync` |
`memoryBarrier` , `memoryBarrierImage` , `memoryBarrierImage` and `barrier` |
`DeviceMemoryBarrier` |
`memoryBarrier` , `memoryBarrierImage` , `memoryBarrierImage` |
`AllMemoryBarrierWithGroupSync` |
All of the barriers above and `barrier` |
`AllMemoryBarrier` |
All of the barriers above |
`N/A` |
`memoryBarrierShared` |

## Texture access

Before Vulkan, this is bundled and [not trivial to emulate](https://anteru.net/blog/2013/05/02/2119/). Fortunately, this changes with Vulkan, where the semantics are the same as in HLSL. The main difference is that in HLSL, the access method is part of the “texture object”, while in GLSL, they are free functions. In HLSL, you’ll sample a texture called `Texture`

with a sampler called `Sampler`

like this:

```
Texture.Sample (Sampler, coordinate)
```


In GLSL, you need to specify the type of the texture and the sampler, but otherwise, it’s similar:

```
texture (sampler2D(Texture, Sampler), coordinate)
```


| HLSL | GLSL |
|---|---|
`CalculateLevelOfDetail` & `CalculateLevelOfDetailUnclamped` |
`textureQueryLod` |
`Load` |
`texelFetch` and `texelFetchOffset` |
`GetDimensions` |
`textureSize` , `textureQueryLevels` and `textureSamples` |
`Gather` |
`textureGather` , `textureGatherOffset` , `textureGatherOffsets` |
`Sample` , `SampleBias` |
`texture` , `textureOffset` |
`SampleCmp` |
`samplerShadow` |
`SampleGrad` |
`textureGrad` , `textureGradOffset` |
`SampleLevel` |
`textureLod` , `textureLodOffset` |
| N/A | `textureProj` |

## General math

GLSL and HLSL differ in their default matrix interpretation. GLSL assumes column-major, and multiplication on the right (that is, you apply \(M * v\)) and HLSL assumes multiplication from left (\(v * M\)) While you can usually ignore that - you can override the order, and multiply from whatever side you want in both - it does change the meaning of `m[0]`

with `m`

being a matrix. In HLSL, this will return the first row, in GLSL, the first column. That also extends to the constructors, which initialize the members in the “natural” order.

## Various functions

| HLSL | GLSL |
|---|---|
`atan2(y,x)` |
`atan` |
`ddx` |
`dFdx` |
`ddx_coarse` |
`dFdxCoarse` |
`ddx_fine` |
`dFdxFine` |
`ddy` |
`dFdy` |
`ddy_coarse` |
`dFdyCoarse` |
`ddy_fine` |
`dFdyFine` |
`EvaluateAttributeAtCentroid` |
`interpolateAtCentroid` |
`EvaluateAttributeAtSample` |
`interpolateAtSample` |
`EvaluateAttributeSnapped` |
`interpolateAtOffset` |
`frac` |
`fract` |
`lerp` |
`mix` |
`mad` |
`fma` |
`saturate` |
`clamp(x, 0.0, 1.0)` |

Anything else I’m missing? Please add a comment and I’ll update this post!