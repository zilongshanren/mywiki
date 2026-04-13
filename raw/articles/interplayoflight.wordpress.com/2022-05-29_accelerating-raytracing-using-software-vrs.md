---
title: Accelerating raytracing using software VRS
url: https://interplayoflight.wordpress.com/2022/05/29/accelerating-raytracing-using-software-vrs/
author: Kostas Anagnostou
published: '2022-05-29'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I discussed in [the previous post](https://interplayoflight.wordpress.com/2022/05/08/increasing-wave-coherence-with-ray-binning/) how divergence in a wave can slow down the execution of a shader. This is particularly evident during raytracing global illumination (GI) as ray directions between neighbouring wave threads can differ a lot forcing different paths through the BVH tree with different number of steps. I described how ray binning can be used to improve this but it is not the only technique we can use. For this one we will use a different approach, instead of “binning” based on the similarity of input rays we will “bin” threads based on the raytraced GI’s output. This makes sense because it is usually quite uniform, with large and sudden transitions happening mainly at geometric edges.

![](../../assets/7571513be4aa1690.png)


![](../../assets/7571513be4aa1690.png)

We can take advantage of this, varying the number rays we trace based on how uniform the GI output is, tracing fewer in such areas and more in areas of large variation (like edges). Varying the shader invocation frequency per pixel is called [Variable Rate Shading](https://devblogs.microsoft.com/directx/variable-rate-shading-a-scalpel-in-a-world-of-sledgehammers/) (VRS), introduced in recent GPUs and graphics APIs like DX12 and Vulkan. Since the hardware supported VRS only works for pixel shaders, we will emulate this feature using “software” VRS in the compute shader. There have been a [few](https://research.activision.com/publications/2020-09/software-based-variable-rate-shading-in-call-of-duty--modern-war) [good](https://www.youtube.com/watch?v=Sswuj7BFjGo) talks recently on the topic, this particular investigation is inspired by The Coalition’s [software VRS implementation for Gears 5’s screen space global illumination](https://www.youtube.com/watch?v=-exWLpgnOJ4).

We talked about how diffuse GI appears to exhibit transitions on “edges” and indeed identifying them is the first step we need to do. This is straight forward, we can run a [Sobel filter](https://en.wikipedia.org/wiki/Sobel_operator) over the previous frame’s raytraced GI output to identify the edges, based on a threshold, split the image in tiles and identify a per tile shading rate. I used DX12’s [shading rate values](https://docs.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_shading_rate) for that purpose.

```
#define SHADING_RATE_1X1 0 // run shader per pixel
#define SHADING_RATE_1X2 1 // run shader once per 1x2 pixel area
#define SHADING_RATE_2X1 4 // run shader once per 2x1 pixel area
#define SHADING_RATE_2X2 5 // run shader once per 2x2 pixel area
```

A shading rate of 1×2 on the whole image, for example, effectively means that we will shade half the pixels in the vertical direction while a rate of 2×1 half the pixels in the horizontal direction. To determine this I apply the Sobel filter and calculate the two gradients in the horizontal (gx) and vertical (gy) directions.

```
const float3 luminanceCoeff = float3(0.2126, 0.7152, 0.0722);
float sobel[8];
for (int i = 0; i < 8; i++)
{
float3 gi = inputRT.Load(int3(DTid.xy + texAddrOffsets[i], 0)).rgb;
sobel[i] = dot(gi, luminanceCoeff);
}
float gx = abs(sobel[0] + 2 * sobel[3] + sobel[5] - sobel[2] - 2 * sobel[4] - sobel[7]);
float gy = abs(sobel[0] + 2 * sobel[1] + sobel[2] - sobel[5] - 2 * sobel[6] - sobel[7]);
const float threshold = EdgeDetectThreshold;
uint rate = SHADING_RATE_2X2;
if (gx > threshold && gy > threshold)
{
rate = SHADING_RATE_1X1;
}
else if ( gx > threshold)
{
rate = SHADING_RATE_2X1;
}
else if (gy > threshold)
{
rate = SHADING_RATE_1X2;
}
```

We decide the rate based on whether the 2 gradients are above the EdgeDetectThreshold or not. This shading rate is per pixel but we need to determine a single value for the whole tile (I am using an 8×8 tile in this instance). For that, we can use some groupshared memory and use the first thread in the group to write the value out.

```
InterlockedMin(ShadingRate, rate);
GroupMemoryBarrierWithGroupSync();
if (GroupIndex == 0)
{
outputRT[Gid.xy] = ShadingRate;
}
```

We conservatively select the minimum shading rate value as representative of the whole tile to ensure that we are correctly expressing detail and variation in the tile.

Now, the question is what should we use as the input image to this pass. A common option is to feed the final render target, post exposure and tonemapping. This makes sense in the general case, the image might have a depth of field or fog effect applied to it which will make parts of the screen blurred and low res, shadowed areas might need less detailed shading, similarly for uniform materials (eg same albedo, normals). While the reduced detail in the DOF blurred areas may be desirable for indirect diffuse detail reduction as well, typically detail in and contribution of the GI is more noticeable in shadowed areas and also material detail (eg albedo), which doesn’t really affect diffuse GI may influence shading rate calculations unnecessarily. So there are few things to consider and YMMV, in my case I used the denoised raytraced GI rendertarget, like the one above, as an input, with a threshold of 0.1 and a tile size of 8×8.

![](../../assets/4c274d02ee5fd320.png)


![](../../assets/4c274d02ee5fd320.png)

Red means a shading rate of 1×1, yellow 2×1, blue 1×2 and green 2×2. As expected, most of the tiles are of 2×2 shading rate, with mostly tiles that cover edges needing higher shading rates (this is a bit unintuitive, higher numbers actually mean lower shading rates as we invoke the shader less times, i.e. at a lower frequency, per pixel).

Now we can use this shading rate image to determine how to spawn rays during raytracing. A straightforward approach is to consider 2×2 pixel quads in the compute shader and kill the unneeded threads (per thread rejection) based on the shading rate for this tile.

```
uint2 tileDims = uint2(SHADING_RATE_TILE_WIDTH, SHADING_RATE_TILE_HEIGHT);
uint rate = shadingRate[screenPos.xy / tileDims].r;
//check if we need to reject that thread. The 2x2 rate is the bitwise OR of 1x2 and 2x1
if ((rate & SHADING_RATE_2X1) && (screenPos.x & 1))
{
return;
}
if ((rate & SHADING_RATE_1X2) && (screenPos.y & 1))
{
return;
}
// trace ray for this thread
outputRT[screenPos.xy] = result;
// copy result to the other pixels according to the shading rate
if ( rate & SHADING_RATE_1X2 )
outputRT[screenPos.xy + uint2(0, 1)] = result;
if (rate & SHADING_RATE_2X1)
outputRT[screenPos.xy + uint2(1, 0)] = result;
if (rate == SHADING_RATE_2X2)
outputRT[screenPos.xy + uint2(1, 1)] = result;
```

In terms of visual quality, this is original RTGI in the final output

![](../../assets/7331caf5e3ae8d33.png)


![](../../assets/7331caf5e3ae8d33.png)

and this is with thread rejection

![](../../assets/b0d3029403c84bfd.png)


![](../../assets/b0d3029403c84bfd.png)

In any other context, killing threads and allowing the wave to run half empty would be inadvisable. In the context of RTGI though, and for any technique which can introduce large thread divergence, any opportunity to decrease unpredictable thread execution cost and allow for early retirement of a wave is welcomed by the GPU.

Even though the thread rejection approach performs well, the GPU still has to run waves potentially mostly empty, which is not great. Ideally we would like to be able to reuse that resource for other work. For that we will follow The Coalition’s approach for wave rejection in Gears 5′ software VRS technique. This is a bit more involved than thread rejection, I will list some extended code snippets to explain it better.

```
#define THREADGROUPSIZE (GI_THREADX*GI_THREADY)
[numthreads(GI_THREADX, GI_THREADY, 1)]
void CSMain(uint3 GroupThreadID : SV_GroupThreadID, uint3 DTid : SV_DispatchThreadID, uint3 GroupID : SV_GroupID, uint GroupThreadIndex : SV_GroupIndex)
{
uint2 screenPos = DTid.xy;
uint2 tileDims = uint2(SHADING_RATE_TILE_WIDTH, SHADING_RATE_TILE_HEIGHT);
uint rate = shadingRate[screenPos.xy / tileDims].r;
const uint WaveSize = WaveGetLaneCount();
const uint GroupWaveIndex = GroupThreadIndex / WaveSize;
uint TotalWaveCount = THREADGROUPSIZE / WaveSize;
if (rate & SHADING_RATE_1X2)
TotalWaveCount /= 2;
if (rate & SHADING_RATE_2X1)
TotalWaveCount /= 2;
if (GroupWaveIndex >= TotalWaveCount)
{
return;
}
```

The wave rejection logic is pretty simple, assuming a GI_THREADX*GI_THREADY threadgroup size, how many waves do I need according to this tile’s shading rate? A shading rate of 2×2 means that I only need a quarter of the waves, a rate of 1×2 means I only need half etc. Having the number of actually needed waves in this threadgroup to cover the current shading rate, if the current thread (GroupThreadIndex) belongs to a wave that is not needed, we simply reject it. The difference with the per-thread rejection approach is that, this way, we will now reject the whole wave the thread belongs to. We are essentially packing the active threads in a reduced number of waves, instead of keeping the rejected ones around, returning the inactive waves to the pool to be used for potentially other work.

Packing the threads in a subset of the waves will need some thread index reordering to work correctly. This remapping is based on a 16×8 thread group size.

```
//origin of the current threadgroup in screen space
screenPos = GroupID.xy * uint2(GI_THREADX, GI_THREADY);
if (rate == SHADING_RATE_2X1) // X dim coarse
screenPos += uint2(2, 1) * uint2(GroupThreadIndex % 8, GroupThreadIndex / 8);
else if (rate == SHADING_RATE_1X2) // Y dim coarse
screenPos += uint2(1, 2) * uint2(GroupThreadIndex % 16, GroupThreadIndex / 16);
else if (rate == SHADING_RATE_2X2) // X and Y dim coarse
screenPos += uint2(2, 2) * uint2(GroupThreadIndex % 8, GroupThreadIndex / 8);
else
screenPos = DTid.xy;
```

Using the new screenPos, we can continue to generate the ray or sample it from a ray buffer and trace as usual. At the end of the shader we just copy the result to neighbouring pixels as needed, this code is the same as in the thread rejection approach above.

```
outputRT[screenPos.xy] = result;
// copy result to the other pixels according to the shading rate
if ( rate & SHADING_RATE_1X2 )
outputRT[screenPos.xy + uint2(0, 1)] = result;
if (rate & SHADING_RATE_2X1)
outputRT[screenPos.xy + uint2(1, 0)] = result;
if (rate == SHADING_RATE_2X2)
outputRT[screenPos.xy + uint2(1, 1)] = result;
```

I mentioned above that the thread group size is set at 16×8, this is because I am running this demo on a NVidia GPU with a wave size of 32 threads. This thread group size fits exactly 4 waves and gives us the ability to repack threads and reject up to 3 waves per group. For this to work I had to tie the raytracing thread group size to the shading rate image tile size and calculate shading rate per 16×8 tiles (SHADING_RATE_TILE_WIDTH, SHADING_RATE_TILE_HEIGHT). This makes the shading rate image coarser compared to the 8×8 one, with the same threshold.

![](../../assets/6118c17b7ddf1ffa.png)


![](../../assets/6118c17b7ddf1ffa.png)

Still, there is a lot of opportunity to lower the shading rate during raytracing. The per wave rejection version of VRS reduces the RTGI cost by 27.3% while the per thread rejection by 28.1%, which is a quite similar gain (I rerun the comparison for the 16×8 threadgroup in both case — the thread rejection version now performs slightly worse because of the coarser shading rate image).

In terms of visuals, this is the wave-rejected GI image, very similar to the per thread rejected one and the original.

![](../../assets/f23be6679139e591.png)


![](../../assets/f23be6679139e591.png)

If per thread rejection performs similarly or even slightly better than the per wave rejection approach, why would we be interested in the latter? The reason is that per wave rejection returns the unneeded waves to the pool and reduces the overall wave allocation on the GPU, as can be seen comparing the 2 GPU traces with NSight Graphics

This brings the SM throughput down and allows more room to async overlap other work over the raytracing pass.

Both per thread and per wave rejection have a small impact on the GI noise and in the Gears 5 VRS presentation the authors mention adjusting the denoising pass based on the shading rating image but I didn’t investigate this in this instance.

To wrap things up, this is another interesting form of thread binning, based on the similarity of the output instead of the input rays, that can help bring down the cost of techniques with large thread divergence.