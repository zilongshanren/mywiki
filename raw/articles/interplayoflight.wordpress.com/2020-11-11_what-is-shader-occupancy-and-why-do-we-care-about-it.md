---
title: What is shader occupancy and why do we care about it?
url: https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/
author: Kostas Anagnostou
published: '2020-11-11'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I had a good question through Twitter DMs about what occupancy is and why is it important for shader performance, I am expanding my answer into a quick blog post.

First some context, GPUs, while running a shader program, batch together 64 or 32 pixels or vertices (called wavefronts on AMD or warps on NVidia) and execute a single instruction on all of them in one go. Typically, instructions that fetch data from memory have a lot of latency (i.e. the time between issuing the instruction and getting the result back is long), due to having to reach out to caches and maybe RAM to fetch data. This latency has the potential to stall the GPU while waiting for the data.

When it comes across a memory instruction the GPU issues it (i.e. asks for the data) and continues to execute instructions following it in the shader program. When it needs to use the data it stops to check if it is available. If the data is ready it uses it, if not it needs to stop execution to wait for it. As an example check the following semi fictional shader, in which we do some Maths and read a uvScale from a texture:

```
Texture1D Materials : register(t0);
PSInput VSMain(VSInput input)
{
PSInput result = (PSInput)0;
result.position = mul(WorldViewProjection, float4(input.position.xyz, 1));
float uvScale =
```**Materials****[MeshIndex].x;**
result.uv = **uvScale *** input.uv;
return result;
}


this is compiled to the following ISA

```
s_swappc_b64 s[0:1], s[0:1]
s_buffer_load_dword s0, s[20:23], 0x00
s_waitcnt lgkmcnt(0)
v_mov_b32 v0, s0
v_mov_b32 v1, 0
```**image_load_mip v0, v[0:3], s[8:15] unorm**
s_buffer_load_dwordx8 s[0:7], s[16:19], 0x40
s_buffer_load_dwordx8 s[8:15], s[16:19], 0x60
s_waitcnt lgkmcnt(0)
v_mul_f32 v1, s4, v5
v_mul_f32 v2, s5, v5
v_mul_f32 v3, s6, v5
v_mul_f32 v5, s7, v5
v_mac_f32 v1, s0, v4
v_mac_f32 v2, s1, v4
v_mac_f32 v3, s2, v4
v_mac_f32 v5, s3, v4
v_mac_f32 v1, s8, v6
v_mac_f32 v2, s9, v6
v_mac_f32 v3, s10, v6
v_mac_f32 v5, s11, v6
v_add_f32 v1, s12, v1
v_add_f32 v2, s13, v2
v_add_f32 v3, s14, v3
v_add_f32 v4, s15, v5
exp pos0, v1, v2, v3, v4 done
v_mov_b32 v5, 0
exp param0, v5, v5, v5, off
**s_waitcnt vmcnt(0)**
**v_mul_f32 v6, v8, v0 **
v_mul_f32 v0, v9, v0
exp param1, v5, v5, v5, off
exp param2, v6, v0, off, off
exp param3, v5, v5, v5, off
s_endpgm


I have annotated with the same colour instructions in the shader and the corresponding instruction in the ISA code. The GPU will issue the** texture load** towards the beginning of the program and then continue executing instructions. At some point, towards the end of the program, it will need to actually **use the uvScale**. Just before that it will insert a **wait **instruction to make sure that the data has arrived. This is a stalling instruction meaning that the GPU must wait until the data is available (so to summarise, the GPU stalls when using the data, not when requesting it).

To avoid wasting time waiting, the GPU will try to find some other work to do by swapping the now stalled batch (warp/wavefront) with another one, to execute another instruction. Because stalls are common, the GPU preemptively prepares a buffer of batches and assigns them to each of the [Compute Units](https://en.wikipedia.org/wiki/Graphics_Core_Next) (that do the execution) ready to be used. How many batches the GPU can preassign depends on the number of vector registers (VGPRs) the shader declares it needs for its execution. That is something that is determined during compilation. As each Compute Unit has a limited number of VGPRs available to it by design, how many batches the GPU can schedule to it depends on the number of VGPRs used by the shader. Avoiding getting too deep into GPU architecture, a quick example to try to clarify this: On AMD’s GCN architecture, the unit that actually does the execution, called the SIMD, has room for only 256 vector registers. The more registers the shader program uses, the smaller the buffer of batches the GPU can schedule for this SIMD to swap to in case of stalls (image from [this GCN presentation](https://www.slideshare.net/DevCentralAMD/gs4106-the-amd-gcn-architecture-a-crash-course-by-layla-mah)).

Finally: the Max Waves/SIMD quantity is what we call **occupancy** and is the size of the buffer of batches (wavefronts) the SIMD can have assigned to it for swapping stalled ones. For the GCN architecture this is a maximum of 10 batches (wavefronts) per SIMD .

In practical terms this means that if you allocate for example 32 VGPRs in the shader, the SIMD will have a buffer of 8 wavefronts to swap to in case the GPU hits a stall due to a memory read which is good because it means that it won’t have to wait much or at all. If, on they other hand, you allocate more that 128 VGPRs, it will have nothing to swap to and the GPU will have to actuallywait for the memory read to complete before it can continue the shader execution, which is bad and a waste of a perfectly good GPU.

With that out of the way, there are 2 more questions to consider:

- Is low occupancy always bad?
- Is high occupancy always good?

For the first question the answer is no. If you notice in the above code, the shader compiler goes to great lengths to add as much distance between the **instruction that requests** the memory and **the instruction that uses** it by rearranging the order of any instruction that it can. It may be the case that it manages to fit enough instructions so that by the time it needs to use the memory it is already here and there is no need to stall (and to swap to another batch) at all. Bottom line is not to rely only on a low occupancy metric to start optimising the shader, check for other bottlenecks like stalls due to memory reads (texture reads) first. If they are high then your shader program may benefit from increasing the occupancy (normally by reducing the number of VGPRs it uses).

For the second question the answer is also no. If a shader program has many memory read instructions and requires a lot of memory traffic, a large buffer of active batches (high occupancy) will fight over the limited cache resources, each batch potentially invalidating cache lines for data belonging to another batch/instruction. Determining how to achieve a good balance with take some profiling within the context of your application and platform. **Update:** There is another reason why high occupancy/low VGPR count can be bad, especially for shaders with a lot of memory reads. The compiler in its effort to keep the VGPR count low may “serialise” the memory reads in order to reuse the registers more (for example issue a memory fetch, wait for the data, store the value in a register, use it, and then reuse that register to store the value from the next memory read). This can lead to bad memory fetch scheduling and increased memory latency. If the compiler has more registers available it can schedule many memory reads upfront, wait for the data and cache the values in registers before using them, improving memory latency overall. This memory latency is what higher occupancy (large number of in flight waves to swap) is supposed to improve but it does not always achieve to, so the advice to always profile to determine the actual effect of the shader changes still stands.

[…] whenever possible to reduce the number VGPRs required for the ALU operations. This can increase the shader occupancy, which can help hide the latency due to memory reads. The sample allocates quite a few internal […]