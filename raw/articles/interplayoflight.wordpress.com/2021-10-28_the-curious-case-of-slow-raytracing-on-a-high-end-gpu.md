---
title: The curious case of slow raytracing on a high end GPU
url: https://interplayoflight.wordpress.com/2021/10/28/the-curious-case-of-slow-raytracing-on-a-high-end-gpu/
author: Kostas Anagnostou
published: '2021-10-28'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I’ve typically been doing my compute shader based raytracing experiments with my toy engine on my ancient laptop that features an Intel HD4000 GPU. That GPU is mostly good to prove that the techniques work and to get some pretty screenshots but the performance is far from real-time with 1 ray-per-pixel GI for the following scene costing around 129 ms, rendering at 1280×720 (plugged in).

![](../../assets/74e099809e839855.png)


![](../../assets/74e099809e839855.png)

So once I had the opportunity to test the performance of the same scene on an NVidia RTX3060 I jumped on it, expecting the new GPU to breeze through those rays. To my astonishment, the GI cost, at the same resolution, was around 50ms, a bit less than half the HD4000 raytracing cost!

Admittedly my code does not benefit for RTX’s raytracing acceleration at all, but even without it I was expecting the RTX to be much much faster. Clearly something was not right there. Remembering that the Maxwell architecture seemed to [prefer typed buffers instead of byte address buffers](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/), maybe Ampere has the same preference, I switched to one to store the TLAS and BLASes. This didn’t seem to make a difference, so maybe not.

Next, I fired NSight Graphics up to dig deeper and did a [GPU trace](https://developer.nvidia.com/blog/optimizing-vk-vkr-and-dx12-dxr-applications-using-nsight-graphics-gpu-trace-advanced-mode-metrics/). True enough, the raytraced GI pass took an exorbitantly long time, but looking at the SM occupancy graph, it seemed that the GPU blasted through the work in about 5ms and then was apparently doing nothing for the rest of the time.

![](../../assets/97a1e69f297e954e.png)


![](../../assets/97a1e69f297e954e.png)

Zooming in a bit, and hovering over the Compute Warps lane I realised that the dispatch had in reality a very long tail, managing to spawn only a few warps per clock after about the 5ms mark.

![](../../assets/41d77316765154d6.png)


![](../../assets/41d77316765154d6.png)

This was weird, I wondered if the BVH trees were corrupted in some way that forced some rays to keep tracing for longer than the rest, so I artificially imposed a maximum step count to catch them. This made no difference as well.

It was hard to see what else could keep spawning a few rays per warp and stopped the dispatch from wrapping up, until I noticed that I forgot to guard against out of bounds texels in the shader. To elaborate on this, I am using an 8×8 thread group size which means I dispatch the compute shader using (width/8 + 1) x (height/8 + 1) thread groups to cover the whole rendertarget. This will in general create more threads than rendertarget pixels and warps in thread groups along the border that will try to access out of bounds memory. This is fine in cases we perform screen space passes to, for example, composite some images. Direct3D is ok with this and [will return a value of zero](https://docs.microsoft.com/en-us/windows/win32/direct3d11/direct3d-11-advanced-stages-cs-access) for the out of bounds indices. In this case though an out of bound access of the depth buffer will return zero which will reconstruct a valid ray origin and a zero normal which will create an invalid tangent frame to calculate the ray direction. The bottom line is that the few warps (2 per thread group) that tried to process out of bounds pixels along the border of the rendertarget got a bad set of rays which forced them to trace for longer than the rest creating this long tail effect.

Guarding against that with something like

```
if (any(screenPos.xy >= RendertargetSize.xy))
{
return;
}
```

fixed the problem, and now the RTX manages to finish the work in about 5ms, about 25 times faster than the HD4000.

![](../../assets/e6f5d7be06a4d5d9.png)


![](../../assets/e6f5d7be06a4d5d9.png)

By the way, a better way to calculate the number of threadgroups for the dispatch is as ceil(width/8.0f) x ceil(height/8.0f) which in this particular case of 1280×720 rendering would hide the problem altogether (1280 and 720 are both divisible by 8) but it would reoccur with other resolutions. Update: an even better way to calculate the threadgroup number, suggested in the comments and by a few people on Twitter is as (width+7)/8 x (height+7)/8 to avoid mixing floating point and integer operations.

The question remains why the raytraced GI pass on HD 4000 seems mostly unaffected by this. One possible answer could be that since [Ivy Bridge supports various warp sizes ](https://en.wikichip.org/w/images/d/d5/Ivy_Bridge_Graphics_Developers_Guide2.pdf)(8, 16, 32 threads per warp) as opposed to Ampere’s 32 threads per warp, perhaps the driver selects a smaller warp size which reduces the impact of large thread divergence. Another possible explanation is that due to floating point precision issues on the two GPUs the Intel one manages to produce a more meaningful tangent frame and rays during raytracing.

“By the way, a better way to calculate the number of threadgroups for the dispatch is as ceil(width/8.0f) x ceil(height/8.0f) which in this particular case of 1280×720 rendering would hide the problem altogether”

I can’t believe that this didn’t occur to me sooner. Great article, and thanks for the tip!

Instead of floating point and ceil, you could also just use (width + 7) / 8 x (height + 7) / 8

Thanks, it was also suggested by some people on Twitter, updated the post.

Would be interesting to know what made those bad rays slow. Did they have NaN/infinity components? Did you write to an out-of-bounds region of the target image buffer? (shouldn’t the program have crashed in that case?)

Out of bounds writes should not affect performance and don’t crash the shader, they are converted to no-ops. It is most likely the NaNs in the tangent frame, created by the zero normal, that propagate to the ray that slow down the raytracing

A third, even better way to compute rounded up integer division is (n / m) + (n % m != 0). This avoids mixing int and float AND avoids the potential overflow in (n + m – 1) / m. And at least with non-SIMD x86 division you’re getting that modulo operation anyway