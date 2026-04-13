---
title: Resource uniformity & bindless access in Vulkan
url: https://anki3d.org/resource-uniformity-bindless-access-in-vulkan/
author: Panagiotis Christopoulos Charitos
published: '2020-11-10'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

This is going to be a short post around bindless descriptor access in Vulkan. There were other posts that touched this topic in the past but in this one I’ll focus more on the Vulkan spec and the terminology in general. The concepts described here also apply to DX12 so I’ll try to cover both terminologies when possible.

In SPIR-V/GLSL/HLSL you can have arrays of values or arrays of descriptors or whatever. These arrays can be sized, unsized, runtime sized etc, doesn’t matter. There are a few ways to index into those arrays:

- Constant integral index
- Dynamically uniform index
- Non-dynamically uniform index
- Subgroup uniform index

**Constant integral** index is a very typical access pattern. Nothing special:

```
const int idx = 10;
... = myArray[idx];
```

**Dynamically uniform** access is uniform across an **invocation group**. The Vulkan spec is a bit vague (on purpose) on defining what the invocation group is but to be 100% covered we can view it as a whole drawcall or a whole compute dispatch. So dynamically uniform access doesn’t diverge inside a drawcall at all. All invocations (threads in DX12) of a drawcall (or dispatch) access the same thing.

```
layout(...) uniform MyConstantBuffer
{
bool dynamicallUniformBool;
int dynamicallUniformIndex;
};
...
if(dynamicallUniformBool)
{
... = myArray[dynamicallUniformIndex];
}
```

In the above example *myArray* is accessed using a dynamically uniform index and it’s inside a dynamically uniform control flow. All invocations of that drawcall will access the same array element.

**Non-dynamically uniform** access is when there is divergence between invocations of an invocation group (aka drawcall or dispatch).

```
int idx = rand() % 100;
... = myArray[idx];
```

**Subgroup uniform** access is when something doesn’t diverge between the invocations that form a subgroup (wave in DX12). This is not explicitly exposed by the shading languages so we’ll leave that out for now.

We spoke about various access methods as a general concept but what we are really interested in is **access of arrays of descriptors**. This is what bindless really is. The Vulkan spec have added support for bindless in version 1.2 and as usual it also exposed a bunch of caps that define what’s allowed and what’s not.

**shaderUniformBufferArrayDynamicIndexing, shaderSampledImageArrayDynamicIndexing, shaderStorageBufferArrayDynamicIndexing and shaderStorageImageArrayDynamicIndexing** are caps since Vulkan 1.0. Having those false means that the arrays of the relevant resources can only be accessed using a constant index (or even better: any constant expression). Pretty much everyone has those set to true so let’s move on. Vulkan 1.2 added **shaderInputAttachmentArrayDynamicIndexing, shaderUniformTexelBufferArrayDynamicIndexing and shaderStorageTexelBufferArrayDynamicIndexing** and for most ISVs these are true as well. Note that sampler descriptors are absent from these caps.

Then there is the **XXXArrayNonUniformIndexing** family of caps. If these are false then the implementation doesn’t allow non-dynamically uniform access of descriptors. If that cap is true then you can do bindless on the specific type of descriptor. Most vendors have these set to true except Intel which doesn’t enable all of them.

An additional family of caps is the **XXXArrayNonUniformIndexingNative**. This feels like a performance warning more than anything else. If the XXXArrayNonUniformIndexingNative is false then the shader compiler will have to add additional instructions to work with non-dynamically uniform access. This varies between ISVs quite a bit.

One additional piece to the puzzle is the NonUniform SPIR-V decoration which is exposed via **nonuniformEXT** in GLSL and **NonUniformResourceIndex()** in HLSL. The default SPIR-V behavior mandates that descriptor accesses are dynamically uniform. When they are not, things might break. So when doing non-dynamically uniform accesses (when the implementation allows it ofcourse) you are required to use the NonUniform decoration. The NonUniform decoration is somewhat orthogonal to the caps discussed above. It doesn’t mean that if XXXArrayNonUniformIndexingNative is true you can omit the NonUniform decoration. The spec doesn’t really say when and if you can omit the NonUniform so the best thing to do is to always use it to decorate non-dynamically uniform accesses. If an implementation doesn’t care then it will simply ignore it.

Example of bindless in GLSL:

```
layout(...) uniform texture2D myBindlessHandles[]; // Runtime sized array
layout(...) uniform sampler mySampler;
...
vec4 color = texture(texture2D(myBindlessHandles[nonuniformEXT(nonUniformIndex)], mySampler), uvs);
...
```

So, putting all these together. AMD for example allows non-dynamically uniform access on sampled images (shaderSampledImageArrayNonUniformIndexing=true) but these accesses are not native (shaderSampledImageArrayNonUniformIndexingNative=false). By default AMD’s compiler will treat all descriptor accesses as dynamically uniform and use SGPR to store the descriptors. If the access is non-dynamically uniform then things might break. Then NonUniform comes into play. Since AMD’s HW doesn’t natively support non-dynamically uniform the NonUniform will instruct the compiler to add extra instructions to ensure subgroup invariance.

Similar story for Arm’s Mali, different reason though. On Mali some instructions require some arguments to be subgroup invariant and this is where non-dynamically uniform patterns become a problem.

One additional thing worth mentioning is that using **buffer addresses** to load data from buffers (exposed by VK_KHR_device_buffer_address and part of Vulkan 1.2) doesn’t require any NonUniform decoration. NonUniform is irrelevant if your shader code doesn’t index arrays of descriptors. Addresses don’t point to descriptors, they point to some raw memory.

The final bit to the puzzle is to understand which **builtins** are dynamically uniform and which are not. The answer is hidden inside the spec and only **gl_DrawID** is explicitly mentioned as dynamically uniform and everything else is not. If for example you are using **gl_InstanceIndex/SV_InstanceID** (directly or indirectly) to index resources then you technically need to use the NonUnifom decoration.

Big thanks to Christian Forfang for providing some early feedback!