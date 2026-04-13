---
title: Porting GPU driven occlusion culling to bgfx
url: https://interplayoflight.wordpress.com/2018/03/05/porting-gpu-driven-occlusion-culling-to-bgfx/
author: Kostas Anagnostou
published: '2018-03-05'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A few weeks ago I was invited by [@bkaradzic](https://twitter.com/bkaradzic) to port the GPU driven occlusion culling sample to [bgfx](https://bkaradzic.github.io/bgfx/index.html). I had heard a lot of positive things about bgfx at that point but I never got to use it myself. This write up describes the experiences and the modifications I made to my original sample to make it work with the new framework. I suggest you read the original blog posts ([part1](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/), [part2](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/)) first since I won’t be delving into the technique much in this one.


bgfx is a cross platform API which uses a “deferred” submission system, meaning the application submit commands on one thread which, after some optimisations, are then consumed on another. At first glance its shader language reminds of GLSL but it has abstractions to support the various platforms.

One major difference is the lack of support for Structured buffers for input/output, offering a per-context use of Vertex/Index buffers instead. This means that, based on how they are created and used, a vertex/index buffer can become a typed buffer which supports UAVs/SRVs etc. Also buffers can be static if we only need to read from them, or dynamic if we require write access on the GPU. All per instance data for all props in the example are stored in single vertex buffer stream, same with vertices and indices (in an index buffer).

The example, again, consists of 4 steps:

- Rendering the occlusion buffer
- Downscaling the occlusion buffer to produce the mip chain
- Occluding the props and producing the visible prop list
- Rendering visible props

For occlusion buffer rendering, since writing to indirect buffers from the CPU is not supported, I resorted to regular instancing, performing one drawcall per occluder. Also, since rendering with a null pixel shader is not supported currently, I used a dummy pixel shader instead.

For the downscaling step, in the original sample I used CopyResource to convert the D32 depth buffer into a regular format since UAVs on depth formats is not supported (in DX11). This time, since CopyResource is not exposed, I used the downscaling compute shader to copy the first mip over to the R32 buffer before performing any downscaling.

For the occlusion pass, once again I use the HiZ mip chain and the bounding boxes of all instances. The instance predicate buffer that signifies whether an instance is visible or not is a UINT16 index buffer this time around, same with the per drawcall instance counts that will be later used to fill in the indirect buffer.

//The compute shader will write how many unoccluded instances per drawcall there are here m_drawcallInstanceCounts = bgfx::createDynamicIndexBuffer(s_maxNoofProps, BGFX_BUFFER_INDEX32 | BGFX_BUFFER_COMPUTE_READ_WRITE); //the compute shader will write the result of the occlusion test for each instance here m_instancePredicates = bgfx::createDynamicIndexBuffer(s_maxNoofInstances, BGFX_BUFFER_COMPUTE_READ_WRITE);

The stream compaction works as in the original sample more or less, the final step of filling in the indirect buffer is slightly different in that since writing to the indirect buffer from the CPU is not supported, we need to fill in the constant data in the computer shader. This is done by allocating a static index buffer with index count and offsets to the global vertex and index buffers.

uint startInstance = 0; //copy data to indirect buffer, could possible be done in a different compute shader for (int k = 0; k < NoofDrawcalls; k++) { drawIndexedIndirect( drawcallData, k, drawcallConstData[ k * 3 ], //number of indices drawcallInstanceCount[k], //number of instances drawcallConstData[ k * 3 + 1 ], //offset into the index buffer drawcallConstData[ k * 3 + 2 ], //offset into the vertex buffer startInstance //offset into the instance buffer ); startInstance += drawcallInstanceCount[k]; drawcallInstanceCount[k] = 0; }

The final step of rendering the visible props during the main pass is again similar, this time around I simplified it a bit by using vertex push instead of vertex pull, like in the original sample, meaning that I let the GPU access the vertices/instances interpreting the offsets that we pass through the indirect arguments buffer instead of indexing buffers in the shader manually.

I’ve also tried to demonstrate a “material system” by creating a palette of colours and accessing them with a per prop Material ID. The material ID is passed to the shader through the per instance world transform to avoid creating a separate vertex stream for it.

This is the output of the example, toggling between the described technique and regular instancing:

bgfx turned out be a great API to develop graphics apps for, it is very clean and easy to use once you get your head around using vertex/index buffers for everything. Shader iteration is a bit hard since you have to use an external tool to compile them, I ended up creating a batch file for all the shaders. The included examples are great and can get you up to speed very quickly and it has integration with ImGUI and Renderdoc as well.

My hope is that without the clutter and irrelevant features of my toy-engine, this technique will be easier to understand now. The example is available from the [github repository](https://github.com/bkaradzic/bgfx).

Thanks to Branimir for the support and for cleaning up the code afterwards.