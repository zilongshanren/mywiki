---
title: Low-level thinking in high-level shading languages 2023
url: https://interplayoflight.wordpress.com/2023/12/29/low-level-thinking-in-high-level-shading-languages-2023/
author: Kostas Anagnostou
published: '2023-12-29'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

“[Low-level thinking in high-level shading languages](https://www.humus.name/index.php?page=Articles&ID=6)” (Emil Persson, 2013), along with its followup “[Low-level Shader Optimization for Next-Gen and DX11](https://www.humus.name/index.php?page=Articles&ID=9)“, is in my top 3 most influential presentations, one that changed the way I think about shader programming in general (since I know you are wondering the other 2 are Natty Hoffman’s [Physically Based Shading](https://renderwonk.com/publications/s2010-shading-course/hoffman/s2010_physically_based_shading_hoffman_a.pdf) and John Hable’s [Uncharted 2 HDR Lighting](https://www.slideshare.net/ozlael/hable-john-uncharted2-hdr-lighting)). When I started graphics programming shaders were handcrafted in assembly, the HLSL compiler being in its infancy. It used to be the case that you could beat the compiler and manually produce superior shader assembly. This changed over the years, the compiler improved immensely and I learned to rely more on it and not pay much attention to, or think about the produced assembly code.

This, and the followup, is a presentation that I recommend as required reading to people wanting to get deeper into shader programming, not just for the knowledge but also the attitude towards shader programming (check compiler output, never assume, always profile). It has been 10 years since it was released though; in those 10 years a lot of things have changed on the GPU/shader model/shader compiler front and not all the suggestions in those presentations are still valid. So I decided to do a refresh with a modern compiler and shader model to see what still holds true and what doesn’t. I will target the [RDNA 2](https://www.amd.com/system/files/TechDocs/rdna2-shader-instruction-set-architecture.pdf) GPU architecture on PC using HLSL, the 6.7 shader model and the DXC compiler (using [https://godbolt.org/](https://godbolt.org/)) in this blog post.

One of the big themes, if not the biggest, in the presentation was that the compiler, however good, can’t always optimise the code in a way it should, and among the many examples of this is its inability to simplify operations to multiply-add instructions although it could. Starting with a simple 2-operation HLSL instruction (which could clearly implement as a multiply with a simple refactoring)

```
result = (x + a) * b;
```

the compiler will return 2 separate instructions, an add and a multiply. It doesn’t rearrange the operations to use a single multiply-add instruction instead.

```
v_add_f32 v0, s0, v0
v_mul_f32 v1, s1, v0
```

Does it matter if we use literal constants instead?

```
result = (x + 1.2) * 3.2;
```

It doesn’t.

```
v_add_f32 v0, lit(0x3f99999a), v0
v_mul_f32 v1, lit(0x404ccccd), v0
```

The compiler won’t change the order of floating point operations in case this has an impact on the result ([this document](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) has more details on the why, here is [an example](https://onlinegdb.com/LbMSY_h_I) of this in action). The shader author knows the problem they are trying to solve and is best placed to do the re-ordering manually. This happens very commonly in shaders, to give you a real world scenario, the typical lighting formula which looks something like this (for the diffuse component)

```
float3 diffuse = lightIntensity * lightColour.rgb * shadowFactor * (albedo.rgb/PI) * NdotL;
```

often mixes float3 and float operands, which the compiler won’t reorder, and this particular formulation produces 10 instructions. Simply rearranging the operands to group float and float3 operations

```
float3 diffuse = lightIntensity * shadowFactor * NdotL / PI * lightColour.rgb * albedo.rgb ;
```

drops the number of instructions to 6.

This ties well with another good practice during shader development, i.e. to [finish the derivations](https://fgiesen.wordpress.com/2010/10/21/finish-your-derivations-please/) and implement features using the minimum number of operations needed as the compiler won’t do it for you.

Instruction modifiers is still a great way to get a lot of operations for free. For example saturate(), x2, x4, /2, /4 on output and abs(), negate on input are free and and can allow for a lot extra mileage out of an instruction for example this

```
saturate(4*(-x*abs(z)-abs(y)))
```

is just a single instruction

```
v_fma_f32 v1, -v2, abs(v0), -abs(v1) mul:4 clamp
```

The “on input” or “on output” part is important and means applying the modifier on each operand separately or on the result of the whole operation. For example using saturate on an input:

```
float x = saturate(a) + b;
```

will force an extra instruction and a copy to a register

```
v_max_f32 v1, s0, s0 clamp
v_add_f32 v1, v0, v1
```

exp() and log() are still implemented using exp2() and log2()

```
//exp()
v_mul_legacy_f32 v0, lit(0x3fb8aa3b), v0 // premultiply by 1.4427
v_exp_f32 v1, v0
//log()
v_log_f32 v0, v0
v_mul_f32 v1, lit(0x3f317218), v0 // post multiply by 0.693147
```

pow(x,y) is calculated using exp2 and log2

```
v_log_f32 v1, v2
v_mul_legacy_f32 v0, v0, v1
v_exp_f32 v1, v0
```

The compiler will calculate integer literal powers up to 4 (eg pow(x, 3)) using multiplies and then it will revert back to exp(log()). Any negative power value will also use exp(log()). Curiously, it will calculate pow(x,1) using exp(log()) as well, worth avoiding it altogether.

```
//pow(x,1)
v_log_f32 v0, v0
v_exp_f32 v1, v0
```

1/sqrt(x) now yields a “reverse square root” instruction.

```
// 1/sqrt(x)
v_rsq_f32 v1, v0
```

sign() and inline conditionals are quite similar in terms of instructions produced (sign() will also handle the case where x==0)

```
//sign(x)
v_cmp_gt_f32 vcc, 0, v0
v_cndmask_b32 v1, 1.0, -1.0, vcc
v_cmp_neq_f32 vcc, 0, v0
v_cndmask_b32 v0, 0, v1, vcc
v_trunc_f32 v1, v0
//x >=0?1:-1
v_cmp_le_f32 vcc, 0, v0
v_cndmask_b32 v1, -1.0, 1.0, vcc
v_mov_b32 v0, lit(0x00003c00)
v_cndmask_b32 v1, lit(0x0000bc00), v0, vcc
```

but the latter has an advantage when we don’t care about x==0 and also when used in operations, such as sign(x) * y

```
//sign(x) * y
v_cmp_gt_f32 vcc, 0, v1
v_cndmask_b32 v2, 1.0, -1.0, vcc
v_cmp_neq_f32 vcc, 0, v1
v_cndmask_b32 v1, 0, v2, vcc
v_trunc_f32 v1, v1
v_mul_f32 v1, v0, v1
// x>=0 ? y:-y
v_cmp_le_f32 vcc, 0, v1
v_cndmask_b32 v1, lit(0x80000000), 0, vcc
v_xor_b32 v1, v0, v1
```

Inverse trigonometric function are still not native and continue to be bad. This is acos() for example:

```
v_mov_b32 v1, lit(0x3be3b0b4)
s_waitcnt vmcnt(0)
v_fma_legacy_f32 v1, lit(0xbaac860d), abs(v0), v1
v_fma_legacy_f32 v1, v1, abs(v0), lit(0xbc90489a)
v_fma_legacy_f32 v1, v1, abs(v0), lit(0x3d0070e2)
s_denorm_mode 0x000f
v_add_f32 v2, -abs(v0), 1.0
v_fma_legacy_f32 v1, v1, abs(v0), lit(0xbd4e589e)
v_sqrt_f32 v3, v2
v_fma_legacy_f32 v1, v1, abs(v0), lit(0x3db64f94)
v_cmp_neq_f32 vcc, 0, v2
v_fma_legacy_f32 v1, v1, abs(v0), lit(0xbe5bc07d)
v_fma_legacy_f32 v1, v1, abs(v0), lit(0x3fc90fdb)
v_cndmask_b32 v2, 0, v3, vcc
v_mul_legacy_f32 v1, v1, v2
v_sub_f32 v2, lit(0x40490fdb), v1
v_cmp_gt_f32 vcc, 0, v0
v_cndmask_b32 v1, v1, v2, vcc
```

It is worth [avoiding](https://iquilezles.org/articles/noacos/) inverse trigonometric functions altogether if possible. If you absolutely need to use them in shaders, it is preferable to [evaluate](https://michaldrobot.com/2014/05/12/low-level-optimizations-for-gcn-digital-dragons-2014-slides/) [approximations](https://seblagarde.wordpress.com/2014/12/01/inverse-trigonometric-functions-gpu-optimization-for-amd-gcn-architecture/) instead but always profile to see if there actually any perf gain.

Even native instructions like sin()/cos()/log()/sqrt() as well as rcp() can come at a cost as they are quarter rate on RDNA (the GPU can issue one every 4 clocks), something to keep in mind as it can increase the instruction latency.

Rolling out your own matrix/vector multiply function can still save you 3 instructions, the compiler won’t treat a .w of “1.0” any differently.

```
//mul(float4(a, 1.0), m)
v_mul_f32 v3, s4, v0
v_mul_f32 v4, s8, v0
v_mul_f32 v0, s0, v0
v_fmac_f32 v3, s5, v1
v_fmac_f32 v4, s9, v1
v_fmac_f32 v0, s1, v1
v_fmac_f32 v3, s6, v2
v_fmac_f32 v4, s10, v2
v_fmac_f32 v0, s2, v2
v_fma_mixlo_f16 v1, s7, 1.0, v3
v_fma_mixlo_f16 v0, s3, 1.0, v0
v_fma_mixhi_f16 v1, s11, 1.0, v4
//a.x * m[0] + (a.y * m[1] + (a.z * m[2] + m[3]))
v_fma_f32 v3, v2, s6, s7
v_fma_f32 v4, v2, s10, s11
v_fma_f32 v2, v2, s2, s3
v_fmac_f32 v3, s5, v1
v_fmac_f32 v4, s9, v1
v_fmac_f32 v2, s1, v1
v_fma_mixlo_f16 v1, v0, s4, v3
v_fma_mixhi_f16 v1, v0, s8, v4
v_fma_mixlo_f16 v0, v0, s0, v2
```

In terms of sharing subexpressions between some functions it is still true that the compiler will reuse parts of length() and distance()

```
// a = length(x-y)
// b = distance(x,y)
v_subrev_f32 v1, v2, v5
v_subrev_f32 v2, v3, v6
v_mul_legacy_f32 v0, v1, v1
v_subrev_f32 v1, v4, v7
v_fmac_legacy_f32 v0, v2, v2
v_fmac_legacy_f32 v0, v1, v1
v_sqrt_f32 v1, v0
```

but only if the order matches (eg, it won’t for distance(y, x)). This is not true for normalize() and length() though, they both seem to do their own calculations, instead of using the output of length() for the normalization, in all likelihood due to floating point precision issues between calculating “reverse sqrt()” and 1/sqrt() — although as we saw above the compiler will calculate 1/sqrt() with the “reverse sqrt()” instruction.

```
//a = length(x)
//b = normalize(x)
v_mul_legacy_f32 v3, v0, v0
v_fma_f32 v4, v1, v1, v3
v_fmac_legacy_f32 v3, v1, v1
v_fmac_f32 v4, v2, v2
v_fmac_legacy_f32 v3, v2, v2
v_rsq_f32 v4, v4
v_sqrt_f32 v3, v3
v_mul_legacy_f32 v0, v0, v4
v_mul_legacy_f32 v1, v1, v4
v_mul_legacy_f32 v2, v2, v4
```

In HLSL the [loop] directive is now even more of hint to the compiler to keep a loop in the code and the compiler seems to mostly ignore it if the loop count is known at compile time.

```
[loop]
for(int i = 0; i < N; i++)
{
float3 v = tex.SampleLevel(state, input.uv + i,0).rgb;
result.xyz += mul(float4(v.rgb, 1), m).xyz;
}
```

The compiler will fully unroll the loop for N up to ~ 50 and then partially unroll it for greater values. This value might change if the VGPR allocation in the shader is higher. The compiler will keep the loop with an unknown loop count though, with or without the [loop] directive.

It used to throw an error when one tried to force a [loop] or a [branch] when sampling a texture with uv coordinates calculated in the branch, without specifying a mip level (i.e. SampleLevel()) as in the example below

```
[branch]
if ( data.x > 0 )
{
float2 uv = input.uv * data.x;
result.xyz = tex.Sample(state, uv).rgb;
}
v_cmpx_ngt_f32 exec, v1, 0
v_mov_b32 v3, 0
v_mov_b32 v4, 0
v_mov_b32 v5, 0
s_cbranch_execz label_006C
label_006C:
s_andn2_b64 exec, s[2:3], exec // mark active threads that passed the test in the execution mask
s_cbranch_execz label_00A8
s_mov_b64 vcc, exec
s_wqm_b64 exec, vcc // Force all pixels in a quad (that contains a pixel that passed the test) ON
v_mul_f32 v2, v2, v1 // Calculate uv coordinates for all pixels in the quad
v_mul_f32 v0, v0, v1
s_mov_b64 exec, vcc // Now activate the pixels in the quad/wave that have actually passed the test.
s_load_dwordx8 s[4:11], s[0:1], null
s_load_dwordx4 s[12:15], s[0:1], 0x000040
s_waitcnt lgkmcnt(0)
// Sample texture only for pixels that have passed the test but with always correct mip level.
image_sample v[3:5], [v2,v0], s[4:11], s[12:15] dmask:0x7 dim:SQ_RSRC_IMG_2D
label_00A8:
s_mov_b64 exec, s[2:3]
```

The problem with this code is that for threads/pixels that won’t follow the branch, the uv coordinates are undefined so the shader can’t calculate the uv derivatives to calculate the mip level. Instead of failing, the compiler does something interesting, it forces all the pixels in the quad on, makes them calculate the uv coordinates regardless of whether they will follow the branch and then take the branch as needed. Bottom line is that [loop] and [branch] might not have the result you expect and it is worth inspecting the final code to determine what they do.

Unfortunately integer division is still really bad. I won’t fill the post with shader ISA but a simple A/B division, both scalar integers, will emit around 34 instructions. Unsigned ints are slightly better (but still expensive) at 24 instructions. Regarding mul24() mentioned for faster integer multiplication, it doesn’t seem to be supported any more. You could use 16 bit data types instead (-enable-16bit-types) and the new uint16_t/int16_t data types to speed up integer operations (division is still bad though).

Cubemap sampling still has an overhead in terms of ALU to calculate the appropriate texture coordinates

```
//cubeTex.Sample(state, coords.xyz).xyz;
v_cubema_f32 v3, v0, v1, v2
v_rcp_f32 v3, abs(v3)
v_cubetc_f32 v4, v0, v1, v2
v_cubesc_f32 v5, v0, v1, v2
v_cubeid_f32 v0, v0, v1, v2
v_fmaak_f32 v1, v4, v3, lit(0x3fc00000)
v_fmaak_f32 v2, v5, v3, lit(0x3fc00000)
s_and_b64 exec, exec, s[20:21]
image_sample v[0:2], [v2,v1,v0], s[12:19], s[0:3] dmask:0x7 dim:SQ_RSRC_IMG_CUBE
```

Register indexing is supported (eg for register arrays) but is another example of why one should always inspect the output ISA to understand what the compiler is doing. Indexing the components of a vector using an index unknown to the compiler (eg coming from a constant buffer) is not supported and will emit this code which checks every possible index value.

```
float4 result = tex.Sample(state, input.uv);
return result[index]; // index from constant buffer
s_cmp_eq_i32 s0, 2
s_cselect_b64 s[2:3], s[16:17], 0
s_cmp_eq_i32 s0, 1
s_cselect_b64 s[4:5], s[16:17], 0
s_cmp_eq_i32 s0, 0
s_cselect_b64 vcc, s[16:17], 0
v_cndmask_b32 v2, v3, v2, s[2:3]
v_cndmask_b32 v1, v2, v1, s[4:5]
v_cndmask_b32 v1, v1, v0, vcc
```

Changing it slightly to index into an array of floats instead will use proper register indexing:

```
float result[4];
return result[index] // index from constant buffer
s_cmp_lt_u32 s0, 4
s_cbranch_scc0 label_0084
s_mov_b32 m0, s0
v_movrels_b32 v4, v0 // use v0 as an index into the register array starting at v4.
```

About indexing in general, for both register arrays and textures/buffers, another thing worth mentioning is that every time we use a floating point as a index that’ll force a conversion to int (v_cvt_u32_f32) and potentially a register allocation. It is preferable to pass indices though buffers in integer formats to begin with.

Worth briefly discussing about scalar vs vector operations mentioned in the presentation: that is done mainly from the point of view of single floats vs vectors of floats (i.e float4). Under the hood all instructions are scalar, i.e. work on a single float value (or int), you can see it with a simple matrix-vector multiplication for example.

```
result.xyz = mul(float4(vec.xyz, 1), m).xyz;
v_fma_f32 v3, v0, s4, s7 // Each register vN holds a single float value
v_fma_f32 v4, v0, s8, s11
v_fma_f32 v0, v0, s12, s15
v_fmac_f32 v3, s5, v1
v_fmac_f32 v4, s9, v1
v_fmac_f32 v0, s13, v1
v_fmac_f32 v3, s6, v2
v_fmac_f32 v4, s10, v2
v_fmac_f32 v0, s14, v2
v_add_f32 v1, 1.0, v3
```

What is more interesting is how those floats are stored in the above example and this is in something called VGPRs (Vector General Purpose Register, using the letter “v” above) and SGPRs (Scalar General Purpose Register, using the letter “s” above). A single VGPR holds one float value for each thread of the wave, while a single SGPR holds one float value common to and accessible by all threads in a wave.

![](../../assets/9284fafb4a818f00.png)


![](../../assets/9284fafb4a818f00.png)

With a VGPR, a thread can only access the float value that corresponds to its index, eg thread 0 can’t access the second float in VGPR0 (this is not strictly true, more on this later). SGPRs typically hold data common to all waves like the matrix m above, originating from a constant buffer (more on this [here](https://interplayoflight.wordpress.com/2021/04/18/how-to-read-shader-assembly/)). To cut a long story short, SGPR instructions (starting with s_ in the assembly code above), registers and cache have dedicated units in the RDNA and GCN GPUs and are great to offload work common to all threads there to reduce pressure on the main vector pipeline (instructions starting with v_ in the code above). This is again something the shader author should be aware of and work with the compiler to achieve. For example a read from a constant buffer will be a scalar load and the result will be stored in SGPRs. If the constant buffer contains an array on the other hand, it depends on whether the index is common to all threads (and the compiler can prove that statically — eg from a constant buffer or a literal) or can vary per thread:

```
cbuffer Data
{
float4 values[30];
};
result = values[i]; // index is provably the same for all threads (eg a literal or from a constant buffer)
s_buffer_load_dwordx4 s[0:3], s[0:3], s4 // scalar load
result = values[i]; // index changes per thread, or the compiler can't infer if the same for all threads
tbuffer_load_format_xyzw v[0:3], v0, s[0:3], 0 offen format:[BUF_FMT_32_32_32_32_FLOAT] // vector load
```

In case the compiler knows that the index is constant to all the threads in the wave it will take a fast path and do a scalar load, else it will issue a vector load. Same with a Structured Buffer, the compiler can issue either a scalar or vector load depending on the index. The same is not true for a typed buffer though, the compiler will issue a vector load in both cases. A quick note that an array in a constant buffer will be performant for sequential access, random access may come with a performance penalty on some platforms, better use different type of buffer if that is your use case.

Finally, the scalar unit doesn’t support all types of Maths operations.

```
int result = a * b; // a,b integers
s_mul_i32 s0, s0, s1 // operation can be performed on the scalar unit fully. Same for addition.
float result = a * b; //a, b float
v_mul_f32 v0, s0, s1 // operation not supported, it has to use a vector instruction even if source the same for all threads.
```

Integer division on the scalar unit is even worse than the vector unit, ~46 instructions and involves a mix of scalar and vector operations and conversions between them, one to avoid.

In general I found that most of the things mentioned in the follow-up presentation ([Low-level Shader Optimization for Next-Gen and DX11](https://www.humus.name/index.php?page=Articles&ID=9)) still hold today as well, so I’d like to focus next on what has changed since.

GPUs have evolved massively since and have become very wide (i.e. ALU capacity has increased a lot), but memory latency/bandwidth and fixed function units haven’t scaled by the same amount. Some back of the napkin Maths, using stats from [https://www.techpowerup.com/gpu-specs/](https://www.techpowerup.com/gpu-specs/) for example, show that the ALU (GFlops/sec) to Memory bandwidth (GB/sec) ratio has increased from AMD Radeon 4870’s (the GPU referenced in the original presentation) 10 to 76 for a recent Radeon RX 7600 and the ALU to Texture Rate (GTex/sec) ratio from 40 to 65. This means that rendering passes that rely on fixed functionality a lot will struggle to fill the GPU with work even more.

With the arrival of DirectX 12 graphics programmers have more control over how they set up and feed data to the shaders but this also means that there are more things peripheral to shader authoring that can affect its performance. For example the followup presentation on DX11 talks about descriptors and binding resources to shaders, DirectX 12 makes the interaction with shaders and how we feed data to it with root signatures and a choice of root parameter types, more explicit. The most efficient way to pass a piece of data to the shader is directly in the root signature, the most expensive via a double indirection with a descriptor table. Things can get even more expensive if due to a high number of root parameters part of the root signature has to be stored to memory instead of SGPRs. It is worth spending some time [studying](https://developer.nvidia.com/blog/advanced-api-performance-descriptors/) the different ways and the pros/cons of each and how it affects performance. [Barriers and resource transitions](https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12) can affect an execution of a drawcall/dispatch and can hinder parallelisation of work on the GPU and now need extra consideration.

GPUs will overlap shader work from different drawcalls/dispatches if there are no dependencies but now we have the ways to make that overlap more explicit with [Async Compute](https://developer.nvidia.com/blog/advanced-api-performance-async-compute-and-overlap/). This is great for complementary workloads that are bottlenecked by different resources/fixed units, for example a shadowmap rendering pass will likely be limited by the vertex rate where an SSAO pass mainly by ALU (and maybe texture reads) and could be overlapped to make use of the unused GPU resource. Worth bearing in mind that the workload assigned to the compute queue should be sizeable (avoid small dispatches) and also that the same task running async on the compute queue will take longer than when ran on graphics queue. Your mileage may vary with Async compute based on type of workload and platform, as always profiling will be needed to determine actual benefits.

Material complexity and lighting model complexity has increased a lot since, increasing both ALU but also texture reads in a shader. Also, divergence in shaders has increased a lot, screen space lighting techniques (SSAO, SSR, raymarched shadows) and raytracing more recently have reduced execution and data coherence among wave threads. There is a plethora of ways to address this, worth looking into, for example.

[Tile classification](https://advances.realtimerendering.com/s2016/s16_ramy_final.pptx): instead of a single complex shader with all possible functionality on dynamic branches, classify image tiles based on required shader functionality and create a set of simpler shaders to implement it. This brings down the shader complexity and also VGPR allocation which may improve occupancy and memory latency (discussed below).- Binning: implemented in the context of
[raytracing](https://interplayoflight.wordpress.com/2022/05/08/increasing-wave-coherence-with-ray-binning/)but with wider applicability, the idea behind this is to reorder the thread indices in a wave to bring similar input data (rays in this context that point towards the same general direction) closer together to reduce divergence and increase cache coherence. - Variable rate shading: this technique does not affect the shader functionality per se, but the rate the shader is executed, based on the similarity of the output, i.e a shader can be executed per pixel, every 2 pixels and the result shared, every 4 pixels etc. It can be either
[hardware](https://devblogs.microsoft.com/directx/variable-rate-shading-a-scalpel-in-a-world-of-sledgehammers/)based, for pixel shader or[software](https://www.youtube.com/watch?v=-exWLpgnOJ4)based for compute shaders.

Memory latency can affect shader performance significantly, especially with the increased shader complexity discussed above and the increased amount of texture read instructions. [Occupancy](https://gpuopen.com/learn/occupancy-explained/) can be important to shader performance, as it is an indication (but not the only one) of how well the GPU can hide memory latency. In short this refers to the amount of waves the [SIMD](https://www.rastergrid.com/blog/gpu-tech/2022/02/simd-in-the-gpu-world/) can have in flight (warmed up and ready to run) in case a wave/instruction gets blocked by a memory read. It is mainly affected by the number of vector registers (VGPRs) allocated by the shader. This is an area that get possibly improved by using the advice in the original presentation and simplifying the ALU work. Occupancy [is not the only measure](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/) of how well memory latency can be hidden though. The compiler will also try to put as much space (i.e. instructions) between the memory read issue and the memory used instruction.

```
float3 vec = tex.Sample(state, input.uv).rgb; // issue a texture read
result.xyz += mul(float4(data.xyz, 1), m).xyz;
result.xyz += mul(float4(vec.xyz, 1), m).xyz; // use the result
image_sample v[0:2], [v2,v0], s[4:11], s[12:15] dmask:0x7 dim:SQ_RSRC_IMG_2D // issue memory read
s_buffer_load_dwordx8 s[4:11], s[0:3], 0x000010
s_buffer_load_dwordx8 s[12:19], s[0:3], 0x000030
s_waitcnt lgkmcnt(0)
v_mov_b32 v3, s11
v_mov_b32 v4, s15
v_mov_b32 v5, s19
v_fma_f32 v3, s4, s8, v3
v_fma_f32 v4, s4, s12, v4
v_fma_f32 v5, s4, s16, v5
v_fma_f32 v3, s9, s5, v3
v_fma_f32 v4, s13, s5, v4
v_fma_f32 v5, s17, s5, v5
v_fma_f32 v3, s10, s6, v3
v_fma_f32 v4, s14, s6, v4
v_fma_f32 v5, s18, s6, v5
s_waitcnt vmcnt(0) // block until data has arrived
v_fma_f32 v6, v0, s8, s11 // use the result
// rest of instructions
```

In the above example the compiler can insert a lot of instruction between the memory read instruction until the data is needed, so the impact of memory latency is reduced. There are things we can do to help it, such as partially unrolling loops to give it more instructions to work with. Also we may need to manually rearrange instructions to give the compiler more opportunities to hide some latency. In the example above, if I switch the order of the two operations as such

```
float3 vec = tex.Sample(state, input.uv).rgb; // issue a memory read
result.xyz += mul(float4(vec.xyz, 1), m).xyz; // use the data first
result.xyz += mul(float4(data.xyz, 1), m).xyz;
image_sample v[0:2], [v2,v0], s[4:11], s[12:15] dmask:0x7 dim:SQ_RSRC_IMG_2D // issue read
s_buffer_load_dwordx8 s[4:11], s[0:3], 0x000030
s_buffer_load_dwordx8 s[12:19], s[0:3], 0x000010
s_waitcnt lgkmcnt(0)
v_mov_b32 v4, s11
v_fma_f32 v4, s8, s12, v4
v_fma_f32 v4, s9, s13, v4
v_fma_f32 v4, s10, s14, v4
s_waitcnt vmcnt(0) // block until the data is ready
v_fma_f32 v5, v0, s16, s19 // we need to use the data now
v_fma_f32 v3, v0, s8, s11
v_fma_f32 v0, v0, s4, s7
v_fmac_f32 v5, s17, v1
v_fmac_f32 v3, s9, v1
v_fmac_f32 v0, s5, v1
v_mov_b32 v1, s7
v_fmac_f32 v3, s10, v2
v_fmac_f32 v5, s18, v2
v_fma_f32 v1, s4, s12, v1
v_add_f32 v3, 1.0, v3
v_fmac_f32 v0, s6, v2
v_fma_f32 v1, s5, s13, v1
v_add_f32 v3, v3, v4
```

now there are many less instructions to insert between the memory read and the block instruction because the compiler won’t change the order of the operations in case it affects the result (as discussed above), this a decision the shader author will have to make. There can be side-effects though, increased occupancy may lead to cache trashing, as a large number of waves compete for cache access. Additionally, once, when we removed a long inactive branch in a shader to reduce VGPR allocation and improve occupancy, the shader cost went up not down because the compiler had less VGPR to cache the results of the memory reads to it had to issue a read, get the result, use it, and free up the VGPR to reuse for another memory read, effectively serialising them. I can’t stress the need to profile any change you make enough, it is likely that the result defies expectation.

Another new tool in the shader author’s toolbox is [Wave Intrinsics](https://github.com/Microsoft/DirectXShaderCompiler/wiki/Wave-Intrinsics) which allow the threads within a wave to talk to each other and exchange data. Wave intrinsics [have many uses](https://gpuopen.com/wp-content/uploads/2017/07/GDC2017-Wave-Programming-D3D12-Vulkan.pdf), which revolve around using VGPRs (which is the fastest form of storage) to store and share intermediate data instead of groupshared memory or plain memory and making decisions about the state of each thread in a wave and perform collective actions based on that. I have discussed how they can be used for example to implement stream compaction in a [previous post](https://interplayoflight.wordpress.com/2022/12/25/stream-compaction-using-wave-intrinsics/), using a per wave atomic instead of one per thread. We discussed earlier how the compiler can make decisions on whether to use the scalar pipeline (particularly loads) if it can infer that the index is wave invariant. This involves mainly indices from constant buffers and literals, but wave intrinsics offer new ways to communicate this to the shader, even for data sources that we have no prior knowledge of uniformity.

```
int i = ... // some index value that may or may not change per thread
int i0 = WaveReadLaneFirst(i); // get the index's value for the first thread in the wave
if ( WaveActiveAllTrue( i == i0 ) ) // if all indices are the same as the first one issue a scalar load
{
result = structured_buffer[i0];
}
else // else issue a vector load
{
result = structured_buffer[i];
}
v_readfirstlane_b32 s0, v0 // get index for first thread
v_cmp_eq_i32 vcc, s0, v0 // compare to indices from all threads
s_mov_b32 s2, s3
s_mov_b32 s3, s1
s_load_dwordx4 s[12:15], s[2:3], 0x00
s_cmp_eq_u64 exec, vcc
s_cbranch_scc1 label_000F
s_waitcnt lgkmcnt(0)
tbuffer_load_format_x v2, v0, s[12:15], 0 idxen format:[BUF_DATA_FORMAT_32,BUF_NUM_FORMAT_FLOAT] // if not all the same, do a vector load
s_branch label_0015
label_000F:
s_lshl_b32 s0, s0, 2
s_waitcnt lgkmcnt(0)
s_buffer_load_dword s0, s[12:15], s0 // if all indices are the same do a scalar load.
s_waitcnt lgkmcnt(0)
```

This idea can be expanded into more complex scenarios and is called [scalarisation](https://flashypixels.wordpress.com/2018/11/10/intro-to-gpu-scalarization-part-1/), which involves having cheaper and more expensive paths in the shader and making decisions about which to follow in the runtime, using wave intrinsics to determine data variance between the threads in a wave.

The last new feature I would like to briefly talk about is support for [16 bit floating point numbers](https://interplayoflight.wordpress.com/2022/12/30/experimenting-with-fp16-in-shaders/) (fp16). On paper, a great feature of the fp16 representation are that it allows packing two 16 bit fp numbers into a single 32 bit register, reducing the VGPR allocation for a shader and increasing occupancy, and also allows reduction of ALU instruction count by performing instructions to packed 32 bit registers directly (i.e. affecting the two packed fp16 numbers independently). Your mileage will vary a lot with fp16, it needs quite a bit of planning for all stages of the pipeline, resources and shaders to ensure that all data and operations remain in fp16, else the shader will be spending time converting between fp16 and fp32.

I haven’t covered all recent developments that may affect shader authoring but the post is getting a bit long. I have collected some more [good practices during shader development](https://interplayoflight.wordpress.com/2022/01/22/shader-tips-and-tricks/) if you are interested.

To try to summarise the original presentation’s point, as I understood it, and this post’s: it is less about saving the odd ALU instruction but more about understanding the tools/platform you are working with and working with the compiler instead of blindingly relying on it.

- Compiler technology has evolved significantly since the early days but the compiler can’t know the author’s intent. We need to work with the compiler to achieve the best code and performance result.
- Don’t make assumptions about what the compiler will do, instead learn to
[read and understand](https://interplayoflight.wordpress.com/2021/04/18/how-to-read-shader-assembly/)the compiler’s output where you have the opportunity to do so. - You don’t always have to worry about the extra instructions. This is more about developing good habits, eg batching operations by type, not using integer division and too much inverse trigonometry etc.
- What is more important is understanding the bottlenecks in each case and making sure that GPU resource is not wasted (ALU, bandwidth etc)
- Always profile to see the impact of any shader change/performance improvement, the result may surprise you.
- Look at the shader execution in context, there may be other things outside it that may affects its performance.

Wow, this is a fantastic resource! I will be referring back to this one regularly.

Thanks so much for putting this together!

You mean SGPR here:

“Wave intrinsics have many uses, which revolve around using VGPRs (which is the fastest form of storage) to store and share intermediate data instead of…”

Great resource, cheers :)?

No, what this means is that a thread can actually access a VGPR at another thread’s index to read data directly, instead of relying on other types of memory to exchange data.

Ah yes, I misread it. Sorry!