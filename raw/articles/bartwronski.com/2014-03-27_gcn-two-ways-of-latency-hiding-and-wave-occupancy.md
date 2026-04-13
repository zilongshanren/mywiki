---
title: GCN – two ways of latency hiding and wave occupancy
url: https://bartwronski.com/2014/03/27/gcn-two-ways-of-latency-hiding-and-wave-occupancy/
published: '2014-03-27'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

I wanted to do another follow-up post to my GDC presentation, you can grab its slides [here](https://bartwronski.com/publications/).

I talked for quite long about shader occupancy concept, which is extremely important and allows to do some memory latency hiding.

The question that arises is “when should I care”?

It is a perfect question, because sometimes high wave occupancy can have no impact on your shader cost, sometimes it can speed up whole pass couple times and sometimes it can be counter-productive!

Unfortunately my presentation showed only very basics about our experiences with GCN architecture, so I wanted to talk about it a bit more.

I’ve had some very good discussions and investigations about it with my friend Michal Drobot (you can recognize his work on [area lights in Killzone: Shadowfall [1]](http://www.guerrilla-games.com/publications.1) and earlier work on Parallax Occlusion Mapping [acceleration techniques [2]](http://drobot.org/)) about it and we created set of general rules / guidelines.

Before I begin, please download [AMD Sea Islands ISA [3] ](http://developer.amd.com/wordpress/media/2013/07/AMD_Sea_Islands_Instruction_Set_Architecture1.pdf)(modern GCN architecture), [AMD GCN presentation[4]](http://developer.amd.com/wordpress/media/2013/06/2620_final.pdf) and [AMD GCN whitepaper [5] ](http://www.amd.com/Documents/GCN_Architecture_whitepaper.pdf)and have them ready! 🙂

## Wait instruction

One of most important instructions I will be referring to is


S_WAITCNT

According to the ISA this is dependency resolve instruction – waiting for completion of loading scalar or vector data.

Wait for scalar data (for example constants from a constant buffer that are coherent to a whole wavefront) are signalled as:


LGKM_CNT

In general we don’t care as much about them – you will be unlikely bound by them, as latency of constant cache (separate, faster cache unit – page 4 in the GCN whitepaper) is much lower and you should have all such values ready.

On the other hand, there is:


VM_CNT

Which is vector register memory load/write dependency resolve and has much higher potential latency and/or cost – if you have L2 or L1 cache miss for instance…

So if we look at example extremely simple shader disassembly (from my presentation):

s_buffer_load_dwordx4 s[0:3], s[12:15], 0x08

s_waitcnt lgkmcnt(0)

v_mov_b32 v2, s2

v_mov_b32 v3, s3

s_waitcnt vmcnt(0) & lgkmcnt(15)

v_mac_f32 v2, s0, v0

v_mac_f32 v3, s1, v1


We see some batched constant loading followed by an immediate wait for it, before it is moved to vector register, while later there is a wait for vector memory load to v0 and v1 (issued by earlier shader code, which I omitted – it was just to load some basic data to operate on it so that compiler doesn’t optimize out everything as scalar ops 🙂 ) before it can be actually used by ALU unit.

If you want to understand the numbers in parenthesis, read the explanation in ISA – counter is arranged in kind of “stack” way, while reads are processed in sequential way.

I will be mostly talking about *s_waitcnt* on vector data.

## Latency hiding

We have two ways of latency hiding:

- By issuing multiple ALU operations on different registers before waiting for load of specific value into given register. Waiting for results of a texture fetch obviously increases the register count, as increases the lifetime of a register.
- By issuing multiple wavefronts on a CU – while one wave is stalled on
*s_waitcnt*, other waves can do both vector and scalar ALU. For this one we need multiple waves active on a CU.

The first option should be quite familiar for every shader coder, previous hardware also had similar capabilities – but unfortunately is not always possible. If we have some dependent texture reads, dependent ALU or nested branches based on a result of data fetch, compiler will have to insert *s_waitcnt* and stall whole wave until the result is available. I will talk later about such situations.

While second option existed before, it was totally hidden from PC shader coders (couldn’t measure its impact in any way… Especially on powerful nVidia cards) and in my experience it wasn’t as important on X360 and its effects as pronounced as on GCN. It allows you to hide lots of latency on dependent reads, branches or shaders with data-dependent flow control. I will also mention later shaders that really need it to perform well.

If we think about it, those two ways are a bit contradictory – one depends on register explosion (present for example when we do loop unrolling that contains some texture reads and some ALU on it), while the other one can be present when we have low shader register count and large wave occupancy.

## Practical example – latency hiding by postponing s_waitcnt

Ok, so we know about two ways of hiding latency, how are they applied in practice? By default, compilers do lots of loop unrolling.

So let’s say we have such a simple shader (old-school poisson DOF).

for(int i = 0; i < SAMPLE_COUNT; ++i)


{

float4 uvs;uvs.xy = uv.xy + cSampleBokehSamplePoints[i].xy * samplingRadiusTextureSpace;


uvs.zw = uv.xy + cSampleBokehSamplePoints[i].zw * samplingRadiusTextureSpace;float2 weight = 0.0f;


float2 depthAndCocSampleOne = CocTexture.SampleLevel(PointSampler, uvs.xy, 0.0f ).xy;

float2 depthAndCocSampleTwo = CocTexture.SampleLevel(PointSampler, uvs.zw, 0.0f ).xy;weight.x = depthCocSampleOne.x > centerDepth ? 1.0f : depthAndCocSampleOne.y;


weight.y = depthCocSampleTwo.x > centerDepth ? 1.0f : depthAndCocSampleTwo.y;colorAccum += ColorTexture.SampleLevel(PointSampler, uvs.xy, 0.0f ).rgb * weight.xxx;


colorAccum += ColorTexture.SampleLevel(PointSampler, uvs.zw, 0.0f ).rgb * weight.yyy;weightAccum += weight.x + weight.y;


}

Code is extremely simple and pretty self-explanatory, there is no point to write about it – but just to make it clear, I batched two sample reads for the reason of combining 2 poisson xy offsets inside a single float4 for constant loading efficiency reasons (they are read into 4 registers with a single instruction).

Just a part of the generated ISA assembly (simplified a bit) could look something like:

image_sample_lz v[9:10], v[5:8], s[4:11], s[12:15]


image_sample_lz v[17:19], v[5:8], s[32:39], s[12:15]

v_mad_legacy_f32 v7, s26, v4, v39

v_mad_legacy_f32 v8, s27, v1, v40

image_sample_lz v[13:14], v[7:10], s[4:11], s[12:15]

image_sample_lz v[22:24], v[7:10], s[32:39], s[12:15]

s_buffer_load_dwordx4 s[28:31], s[16:19]

s_buffer_load_dwordx4 s[0:3], s[16:19]

s_buffer_load_dwordx4 s[20:23], s[16:19]

s_waitcnt lgkmcnt(0)

v_mad_legacy_f32 v27, s28, v4, v39

v_mad_legacy_f32 v28, s29, v1, v40

v_mad_legacy_f32 v34, s30, v4, v39

v_mad_legacy_f32 v35, s31, v1, v40

image_sample_lz v[11:12], v[27:30], s[4:11], s[12:15]

v_mad_legacy_f32 v5, s0, v4, v39

v_mad_legacy_f32 v6, s1, v1, v40

image_sample_lz v[15:16], v[34:37], s[4:11], s[12:15]

s_buffer_load_dwordx4 s[16:19], s[16:19]

image_sample_lz v[20:21], v[5:8], s[4:11], s[12:15]

v_mad_legacy_f32 v8, s3, v1, v40

v_mad_legacy_f32 v30, s20, v4, v39

v_mad_legacy_f32 v31, s21, v1, v40

v_mad_legacy_f32 v32, s22, v4, v39

v_mad_legacy_f32 v33, s23, v1, v40

s_waitcnt lgkmcnt(0)

v_mad_legacy_f32 v52, s17, v1, v40

v_mad_legacy_f32 v7, s2, v4, v39

v_mad_legacy_f32 v51, s16, v4, v39

v_mad_legacy_f32 v0, s18, v4, v39

v_mad_legacy_f32 v1, s19, v1, v40

image_sample_lz v[39:40], v[30:33], s[4:11], s[12:15]

image_sample_lz v[41:42], v[32:35], s[4:11], s[12:15]

image_sample_lz v[48:50], v[30:33], s[32:39], s[12:15]

image_sample_lz v[37:38], v[51:54], s[4:11], s[12:15]

image_sample_lz v[46:47], v[0:3], s[4:11], s[12:15]

image_sample_lz v[25:26], v[7:10], s[4:11], s[12:15]

image_sample_lz v[43:45], v[7:10], s[32:39], s[12:15]

image_sample_lz v[27:29], v[27:30], s[32:39], s[12:15]

image_sample_lz v[34:36], v[34:37], s[32:39], s[12:15]

image_sample_lz v[4:6], v[5:8], s[32:39], s[12:15]

image_sample_lz v[30:32], v[32:35], s[32:39], s[12:15]

image_sample_lz v[51:53], v[51:54], s[32:39], s[12:15]

image_sample_lz v[0:2], v[0:3], s[32:39], s[12:15]

v_cmp_ngt_f32 vcc, v9, v3

v_cndmask_b32 v7, 1.0, v10, vcc

v_cmp_ngt_f32 vcc, v13, v3

v_cndmask_b32 v8, 1.0, v14, vcc

v_cmp_ngt_f32 vcc, v11, v3

v_cndmask_b32 v11, 1.0, v12, vcc

s_waitcnt vmcnt(14) & lgkmcnt(15)

v_cmp_ngt_f32 vcc, v15, v3

v_mul_legacy_f32 v9, v17, v7

v_mul_legacy_f32 v10, v18, v7

v_mul_legacy_f32 v13, v19, v7

v_cndmask_b32 v12, 1.0, v16, vcc

v_mac_legacy_f32 v9, v22, v8

v_mac_legacy_f32 v10, v23, v8

v_mac_legacy_f32 v13, v24, v8

s_waitcnt vmcnt(13) & lgkmcnt(15)

I omitted the rest of waits and ALU ops – this is only part of the final assembly – note how much scalar architecture makes your shaders longer and potentially less readable!

So we see that compiler will probably do loop unrolling, decide to pre-fetch all the required data into multiple VGPRs (huge amount of them!).

Our *s_waitcnt* on vector data is much later than the first texture read attempt.

But if we count the actual cycles (again – look into ISA / whitepaper / AMD presentations) of all those small ALU operations that happen before it, we can estimate that if data was in the L2 or L1, (probably it was, as CoC of central sample must have been fetched before the actual loop) there probably will be no actual wait.

If you just look at the register count, it is huge (remember that the whole CU has only 256 VGPRs per a SIMD!) and the occupancy will be very low. Does it matter? Not really 🙂

My experiments with forcing loop there (it is tricky and involves forcing loop counter into a to uniform…) show that even if you get much better occupancy, the performance can be the same or actually lower (thrashing cache, still not hiding *all* the latency, limited amount of texturing units).

So the compiler will probably guess properly in such case and we got our latency hidden very well even within one wave. It is not always the case – so you should count those cycles manually (it’s not that difficult nor tedious) or rely on special tools to help you track such stalls (I cannot describe them for obvious reasons).

## Practical example – s_waitcnt necessary and waits for data

I mentioned that sometimes it is just impossible to do *s_waitcnt* much later than the actual texture fetch code.

Perfect example of it can be such code (isn’t useful in any way, just an example):

int counter = start;


float result = 0.0f;

while(result == 0.0f)

{

result = dataRBuffer0[counter++];

}

It is quite obvious that every next iteration of loop or an early-out relies on a texture fetch that has just happened. 😦

Shader ISA disassembly will look something like:

label_before_loop:


v_mov_b32 v1, 0

s_waitcnt vmcnt(0)& lgkmcnt(0)

v_cmp_neq_f32 vcc, v0, v1

s_cbranch_vccnz label_after_loop

v_mov_b32 v0, s0

v_mov_b32 v1, s0

v_mov_b32 v2, 0

image_load_mipv0, v[0:3], s[4:11]

s_addk_i32 s0, 0x0001

s_branch label_before_loop

label_after_loop:

So in this case having decent wave occupancy is the only way to hide latency and keep the CU busy – and only if you have somewhere else in your shader or in a different wave on the CU ALU-heavy code.

This was the case in for instance screenspace reflections or parallax occlusion mapping code I implemented for AC4 and that’s why I showed this new concept of “wave occupancy” on my GDC presentation and I find it very important. And in such cases you must keep your vector register count very low.

## General guidelines

I think that in general (take it with a grain of salt and always check yourself) low wave occupancy and high unroll rate is good way of hiding latency for all those “simple” cases when you have lots of not-dependent texture reads and relatively moderate to high amount of simple ALU in your shaders.

Examples can be countless, but it definitely applies to various old-school simple post-effects taking numerous samples.

Furthermore, too high occupancy could be counter-productive there, thrashing your caches. (if you are using very bandwidth-heavy resources)

On the other hand, if you have only small amount of samples, require immediate calculations based on them or even worse do some branching relying on it, try to go for bigger wave occupancy.

I think this is the case for lots of modern and “next-gen” GPU algorithms:

- ray tracing
- ray marching
- multiple indirection tables / textures (this can totally kill your performance!)
- branches on BRDF types in deferred shading
- branches on light types in forward shading
- branches inside your code that would use different samples from different resource
- in general – data dependent flow control

But in the end and as always – you will have to experiment yourself.

I hope that by this post I also have convinced you how important it is to look through the ISA and all documents / presentations on hardware, its architecture and all low-level and final disassembly code – even if you consider yourself a “high level and features graphics / shader coder” (I believe that there is no such thing as “high level programmer” that doesn’t need to know target hardware architecture in real-time programming and especially in high-quality, console or PC games). 🙂

Thanks for writing this up Bart, very useful! The GCN whitepaper link does not work or is it unaccessible outside the US? This one does work though: http://www.amd.com/Documents/GCN_Architecture_whitepaper.pdf

Thanks! I will update the link. 🙂

Pingback: CodeXL for game developers: How to analyze your HLSL for GCN | AMD

Pingback: Designing a next-generation post-effects pipeline | Bart Wronski

Pingback: Quick dump of GCN links – Dreams of flashy pixels (on a white website)

Pingback: Where do I start graphics programming? – Yosoygames

Excellent article. I have a related question about an OpenCL kernel I have running Polaris card:

This kernel that writes results to a global buffer; these results are never read back into the kernel (they are processed by another kernel at a later time).

So, I don’t want this data sitting in the L1 cache if I can help it. Is there a way of ensuring that it is not cached? I need L1 for another array that is frequently read from and written to. This array is around 4kb, so it should stay in the L1 cache.

Any insight here would be greatly appreciated.

Thanks!

Hi Aaron! In general buffer or UAV writes on AMD hw don’t go through L1 cache so you don’t need to do anything for it not getting written this way. To turn off reads through L1 you need to rely on driver figuring our proper mode,usually it’s enough if a resource is read/write. However L1 is so extremely tiny that in general there is not much you can do to keep data there, literally more than 1 accessed resource is almost guaranteed that it won’t be in L1. So just make sure that single wavefront has good access locality. 🙂

From the AMD GCN whitepaper, “The L1 data (L1D) cache is 16KB and 4-way set associative with 64B lines and LRU replacement.” LRU stands for “Least Recently Used.” This means if you request data to the cache and it’s full, the last data you touched gets replaced. So once you write those results to the global buffer, any new data you use will eventually replace that.

Pingback: Dimensionality reduction for image and texture set compression | Bart Wronski

Pingback: Is this a branch? | Bart Wronski