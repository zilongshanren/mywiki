---
title: Stream compaction using wave intrinsics
url: https://interplayoflight.wordpress.com/2022/12/25/stream-compaction-using-wave-intrinsics/
author: Kostas Anagnostou
published: '2022-12-25'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

It is common knowledge that removing unnecessary work is a crucial mechanism for achieving good performance on the GPU. We routinely create lists of visible model instances of example using frustum and other means of culling to avoid rendering geometry that will not contribute to the final image. While it is easy to create such lists on the CPU, it may not be as trivial for work generated on the GPU, for example when using GPU driven culling/rendering, or deciding which pixels in the image to raytrace reflections for. Such operations typically produce lists with invalid (culled) work items, which is not a very effective way to make use of a GPU’s batch processing nature, either having to skip over shader code or introduce idle (inactive) threads in a wave.

The approach to remove invalid work items from a list is called stream compaction. I first learned about stream compaction a few years ago, when I was prototyping [a GPU culling/driven rendering system](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/). Occlusion culling individual instances from an instance buffer causes exactly that, inactive entries that can’t be skipped without compaction of the buffer. Back then I experimented with a 2-step, parallel prefix scan approach proposed by [Blelloch ](http://www.cs.cmu.edu/~scandal/papers/CMU-CS-90-190.html)and also described in [GPU Gems](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch39.html), which produced an index buffer with the valid entries in the instance buffer. The technique worked but it was relatively complex and also restricted by the available to the threadgroup (groupshared) memory, which is limited. This [can be fixed](https://interplayoflight.wordpress.com/2018/05/25/gpu-driven-rendering-experiments-at-the-digital-dragons-conference/) but at the expense of increased complexity.

Fast forward a few years, [wave intrinsics](https://github.com/Microsoft/DirectXShaderCompiler/wiki/Wave-Intrinsics) are now available in newer shader models. Wave instrinsics are special shader instructions that allow us to retrieve data from the other threads in a wave, without the need for any synchronisation or expensive trips through memory. For example WaveActiveAllEqual() will return true is the specified expression is true for all active threads in a wave and WaveActiveMax() will return the maximum value of the expression for all wave threads.

In the set of supported instructions there are a few that are very useful when it comes to compacting streams of data. I will describe how using a concrete example, based on FidelityFX’s SSSR technique I talked about in the previous [post](https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/). There I briefly described how the technique uses material roughness to decide which pixels actually needed raymarching (very rough surfaces don’t need accurate reflections and we can often cheat using a preconvolved cubemap), storing the coordinates of the ones that do in a global buffer. Culling pixels based on roughness can lead to waves with inactive threads which, like discussed, in not ideal as it lowers the wave efficiency.

Imagine this set of pixels in an image with only the ones marked with “R” needing raymarching. In this context, most of a fictional, 16 thread wave that will be spawned to process it will be underutilised.

![](../../assets/a9715c87b746ce9b.png)


![](../../assets/a9715c87b746ce9b.png)

What we would like to do is compact the list of pixels so as to remove the inactive ones to keep the wave well utilised.

![](../../assets/16c498a08983deac.png)


![](../../assets/16c498a08983deac.png)

Moving the active pixels all together creates space in the wave to add more pixels, for example, from the second row of the image.

![](../../assets/4b57f7b5c57f450e.png)


![](../../assets/4b57f7b5c57f450e.png)

Let’s focus on a specific thread, marked in orange, and review the shader code that implements this compaction, using Fidelity FX’s SSSR implementation in the ClassifyTiles.hlsl as an example.

![](../../assets/6c7b13e21aafa870.png)


![](../../assets/6c7b13e21aafa870.png)

What we are interested in is the index of that specific thread in the compacted list. To find the packed wave index of the thread (i.e. the index in the wave with the inactive threads removed) we can call the WavePrefixCountBits() wave intrinsic.

**uint local_ray_index_in_wave = WavePrefixCountBits(needs_ray);**
uint wave_ray_count = WaveActiveCountBits(needs_ray);
uint base_ray_index;
if (is_first_lane_of_wave)
{
IncrementRayCounter(wave_ray_count, base_ray_index);
}
base_ray_index = WaveReadLaneFirst(base_ray_index);
if (needs_ray)
{
int ray_index = base_ray_index + local_ray_index_in_wave;
StoreRay(ray_index, dispatch_thread_id, copy_horizontal, copy_vertical, copy_diagonal);
}


This will return the sum of all the **needs_ray** bools set to true across all active threads with indices smaller than the current one. For this particular thread it will return 3, as only 3 threads to the left of the current one need raymarching.

It is interesting to take a quick look at what WavePrefixCountBits() does at the ISA level (RDNA2).

```
s_and_b64 s[4:5], vcc, exec
v_mbcnt_hi_u32_b32 v1, s5, 0
v_mbcnt_lo_u32_b32 v1, s4, v1
```


The 64 bit **vcc **register will store a bit per thread that represents the result of the comparison **needs_ray == true**. Only threads that need raymarching will have this bit on. On top of that we need to only consider the “active” threads, the ones that the **exec **register bit will be on for, so the compiler adds a scalar **and **instruction between the vcc and exec registers (some info on the vcc and exec registers as well as reading shader assembly in general [here](https://interplayoflight.wordpress.com/2021/04/18/how-to-read-shader-assembly/)), storing the 64 bit result to 2 SGPRs (s4 and s5). The next 2 instructions (**v_mbcnt_hi_u32_b32** and **v_mbcnt_low_u32_b32**) work on the 2 scalar registers, returning the number of bits with an index less than the current thread’s index. In the above example, only 3 threads with index less than the current one are on. The partial result from the first instruction (v1) is fed into the other one so all 64 threads are accounted for. The instructions are vector instructions because each thread will have its own count (as it depends on the thread index).

Back to the shader code, along with the packed wave thread index, we are interested in how many threads/pixels will need raymarching in the current wave, something that we can determine with a call to WaveActiveCountBits().

```
uint local_ray_index_in_wave = WavePrefixCountBits(needs_ray);
```**uint wave_ray_count = WaveActiveCountBits(needs_ray);**
uint base_ray_index;
if (is_first_lane_of_wave)
{
IncrementRayCounter(wave_ray_count, base_ray_index);
}
base_ray_index = WaveReadLaneFirst(base_ray_index);
if (needs_ray)
{
int ray_index = base_ray_index + local_ray_index_in_wave;
StoreRay(ray_index, dispatch_thread_id, copy_horizontal, copy_vertical, copy_diagonal);
}


We now know how much space we need in the buffer to store the packed thread coordinates (wave_ray_count) for this wave, so we can increase the buffer index using an atomic increase operator per wave.

```
uint local_ray_index_in_wave = WavePrefixCountBits(needs_ray);
uint wave_ray_count = WaveActiveCountBits(needs_ray);
uint base_ray_index;
```**if (is_first_lane_of_wave)
{
IncrementRayCounter(wave_ray_count, base_ray_index);
}**
base_ray_index = WaveReadLaneFirst(base_ray_index);
if (needs_ray)
{
int ray_index = base_ray_index + local_ray_index_in_wave;
StoreRay(ray_index, dispatch_thread_id, copy_horizontal, copy_vertical, copy_diagonal);
}


We only do this for first active thread in the wave which was determined with a call to WaveIsFirstLane() earlier (this particular thread isn’t the first active one). Increasing it only once per wave can bring traffic to the atomic global counter down by a lot. The offset to the current packed wave in the buffer is returned in **base_ray_index**. Only the base_ray_index from the first active thread is valid, we can retrieve it with a call to WaveReadLaneFirst(). We need to use the intrinsic and not the first value of SV_DispatchThreadID to determine the “first” thread, as a thread group can be larger than a wave.

Finally, knowing the offset of the packed wave **base_ray_index** into the buffer and the index of each active thread **local_ray_index_in_wave** we can store the ray coordinates for every thread that actually needs a ray.

```
uint local_ray_index_in_wave = WavePrefixCountBits(needs_ray);
uint wave_ray_count = WaveActiveCountBits(needs_ray);
uint base_ray_index;
if (is_first_lane_of_wave)
{
IncrementRayCounter(wave_ray_count, base_ray_index);
}
base_ray_index = WaveReadLaneFirst(base_ray_index);
```**if (needs_ray)
{
int ray_index = base_ray_index + local_ray_index_in_wave;
StoreRay(ray_index, dispatch_thread_id, copy_horizontal, copy_vertical, copy_diagonal);
}**


This is all there is to it, using the above wave intrinsics we can efficiently compact the waves removing inactive threads and increasing wave utilisation. Using wave intrinsics has the added bonus that it can encourage the compiler to use the scalar pipeline on GCN/RDNA as well.

More about the available wave intrinsics [here](https://github.com/Microsoft/DirectXShaderCompiler/wiki/Wave-Intrinsics) and [here](https://gpuopen.com/wp-content/uploads/2017/07/GDC2017-Wave-Programming-D3D12-Vulkan.pdf) (for Vulkan as well), and also some info on using them in the context of GPU driven rendering [here](https://frostbite-wp-prd.s3.amazonaws.com/wp-content/uploads/2016/03/29204330/GDC_2016_Compute.pdf).

This operation seems like a super fundamental primitive to enable general purpose parallel programming that maintains high utilization. I’ve been wondering about the details of this for a while, thank you for going in depth.

It’s like a bonus Christmas present :)