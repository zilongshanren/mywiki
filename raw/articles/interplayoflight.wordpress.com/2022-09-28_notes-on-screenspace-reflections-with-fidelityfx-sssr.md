---
title: Notes on screenspace reflections with FidelityFX SSSR
url: https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/
author: Kostas Anagnostou
published: '2022-09-28'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Today I set out to replace the old SSR implementation in the toy engine with [AMD’s FidelityFX’s](https://gpuopen.com/fidelityfx-sssr/) one but in the end I got distracted and spent the day studying how it works instead. This is a modern SSR solution that implements a lot of good practices so I’ve gathered my notes in a blog post in case someone finds it of interest. This is not intended as an exhaustive description of the technique, more like a few interesting observations.

The technique takes as an input the main rendertarget, the worldspace normal buffer, a roughness buffer, a hierarchical depth buffer and an environment cubemap. The hierarchical depth buffer is a mip chain where each mip level pixel is the minimum of the previous level’s 2×2 area depths (mip 0 corresponds to the screen-sized, original depth buffer). It will used later to speed up raymarching but can also used in many other techniques, like GPU occlusion culling.

A straightforward but inefficient way to create this depth mip chain is to calculate each mip level using a compute shader dispatch, using the previous mip level as an input. This will cause the GPU to drain the pipeline between each dispatch to ensure that a mip level has been fully written to before it proceeds to the next one. I don’t have such an implementation in the toy engine to demonstrate how this looks so I will borrow the trace from [AMD’s Single Pass Downsampler presentation](https://interplayoflight.wordpress.com/Users/kostas.anagnostou/Downloads/FidelityFX_SPD.pdf) that showcases the effect well.

![](../../assets/ea30d695f75a6415.png)


![](../../assets/ea30d695f75a6415.png)

In the end, the stalls between each dispatch become longer than the actual dispatch duration wasting a lot of GPU time. A [more modern alternative](https://github.com/GPUOpen-Effects/FidelityFX-SPD) is to calculate all mip levels in a single dispatch, using the groupshared memory to exchange data between the mip levels, removing the need for barriers and pipeline drains.

![](../../assets/d8dfbdacb0034cdf.png)


![](../../assets/d8dfbdacb0034cdf.png)

This pass costs 0.12ms on a RTX 3080 mobile at 1080p.

The actual SSR work starts with a classification pass (ClassifyTiles, 0.17ms), which has a dual purpose, first to add all pixels needing tracing rays to a global buffer, along with their screen space coordinates. Also, in case coarse tracing has been selected (less than 4 samples per pixel quad), it marks whether that pixel should be copied to its neighbours in the pixel quad or not. The decision whether a pixel needs a ray or not is made based on the roughness, very rough surfaces don’t get any, relying on the prefiltered environment map instead as an approximation. The other purpose of this pass is to mark tiles that contain “reflective” pixels (i.e. that need tracing). This is to later speed up denoising allowing us to process only tiles that actually need it.

Worth noting in this pass is that it will sample the environment map and write the radiance for pixels that don’t need rays (because of high roughness) in a separate rendertarget. The environment map is pre-blurred and the roughness is used to select the appropriate cubemap mip level. The reason this is done here is because we won’t be touching pixels that don’t require tracing any more, although if on a pinch for memory it could be done when adding the SSR result to main rendertarget later. The other thing worth noting is that it extracts and writes the roughness to a separate, single channel rendertarget to improve memory bandwidth in subsequent passes. Finally, the shaders remaps the linear group thread index to a [Morton order](https://en.wikipedia.org/wiki/Z-order_curve) one (FFX_DNSR_Reflections_RemapLane8x8) to improve locality of texture accesses. This can speed up memory reads by [improving cache coherence](https://developer.nvidia.com/blog/optimizing-compute-shaders-for-l2-locality-using-thread-group-id-swizzling/).

Next step is to prepare a 128×128 texture with screen-space (animated) blue noise (PrepareBlueNoiseTexture, <0.01ms), based on [the work of Eric Heitz](https://eheitzresearch.wordpress.com/762-2/). This will be used later to drive the stochastic sampling of the specular lobe.

Once this done we are (almost) ready to to ray march, the only problem is that we don’t know the size of the global array of pixels to trace on the CPU to launch a Dispatch. For that reason, the technique fills a buffer with indirect arguments, with data already known to the GPU and uses a ExecuteIndirect instead. The indirect arguments buffer is populated during the PrepareIndirectArgs pass, at <0.01ms. Nothing particular to mention here apart from that it adds 2 entries to the indirect buffer, one for the pixels to trace and one for the tiles to denoise later.

The real work starts in the next pass (Intersect, 0.88ms) where ray marching for the pixels that need it finally happens, using an ExecuteIndirect with the arguments computed earlier.

There is a couple of things worth discussing here. To reduce the raymarching cost, typically, a maximum of one ray per pixel is raymarched, drawn from the GGX distribution (image [from](https://www.ea.com/seed/news/seed-dd18-presentation-slides-raytracing))

This can lead to rays that are below the horizon (as showcased above) or masked or shadowed by the BRDF’s geometric function. To improve the quality of the raymarched rays the sample uses the distribution of [visible only normals](https://jcgt.org/published/0007/04/01/paper.pdf), which is effectively the potential set of unoccluded, valid rays.

Next, to accelerate raymarching, the hierarchical z-buffer produced earlier is used (images [from](https://www.ea.com/frostbite/news/stochastic-screen-space-reflections)). Raymarching starts at mip 0 (highest resolution) of the depth buffer.

If no collision is detected, we drop to a lower resolution mip and continue raymarching. Again, if no collision is detected we continue dropping to lower resolution mips until we detect one.

If we do, we climb back up to a higher resolution mip and continue from there. This allows quickly skipping large parts of empty space in the depth buffer.

The raymarcing loop in the shader is pretty straightforward, you can see the current_mip increasing or decreasing based on the collision result, but it is worth calling out a interesting trick.

![](../../assets/d7cd3591028a179b.png)


![](../../assets/d7cd3591028a179b.png)

In many cases raymarching is a highly divergent operation meaning that some rays will take many more steps than others to find a hit (SSAO, glossy reflections etc). This means that a single long ray can stall the whole wave from retiring, keeping a lot of threads inactive. To improve this, the sample stops raymarching (exit_due_to_low_occupancy) when the number of active threads (counting them with WaveActiveCountBits(true)) has fallen below a threshold. This will prevent a small number of long rays holding back the whole wave.

Finally, the technique “validates” the result (FFX_SSSR_ValidateHit) to make sure that it is not out of screen but also we didn’t hit a backface. Also a depth buffer “thickness” is used which is a content specific quality improvement that stops very thin geometry (like grass, hair) occluding more than they should be (eg a single blade of grass is a massive canyon in the depth buffer, stopping all rays that will go under it). I would imagine parts of the validation step (eg, the thickness test) could be integrated into the raymarching loop above to continue marching even if the ray misses a surface due to it being too thin (i.e. to allow the ray to go “beneath” a surface). The validation step produces a “confidence” value which is used to interpolate between a sample from the main rendertarget (valid screen space reflection) and the environment map fallback. As a final step the shader copies the calculated radiance to the neighbouring pixels, if rendering SSR at lower resolution.

This is the result of the intersection pass, we can notice that mirror-like reflections (low roughness) are relatively noise free unlike areas with high roughness. Areas like to top of the pawns, where no screenspace information is available to raymarch, fall back to the environment map.

![](../../assets/2b2ae9522be0380b.png)


![](../../assets/2b2ae9522be0380b.png)

Any stochastic technique will introduce noise due to low sample count, so the sample wraps up with some denoising passes, typically both spatial and temporal. The first pass, (DNSR Reproject, 0.66ms) will prepare the history buffer used in the temporal resolve later by reprojecting the SSR result from the previous frame onto the current one. This works on the list of tiles produced earlier during the ClassifyTiles pass, using an ExecuteIndirect.

Typical reprojection, as used in TAA for example, is not suitable for reflections, as the objects in the reflections move based on their own depth and not the depth of the surfaces they reflect on (captured in the depth buffer). That is, we need to determine where the **reflected **objects were in the previous frame. To get the reflected point uv position FFX_DNSR_Reflections_GetHitPositionReprojection() reconstructs the hit point 3d position using the surface point and surface relative hit point distance, stored during the raymarching pass earlier. The technique uses a lot of information from the previous frame (radiance, roughness, depth and normals) to determine sample similarity, supporting paths for various cases (like mirror or glossy surfaces) and determines disocclusion using both normals and depths from current and previous frames. The outcome of the reprojection pass is a “reprojected” radiance and a disocclusion factor. This factor is used to determine if the reprojected sample is good enough to keep or it belongs to a newly exposed surface that we have no information for in the previous frame (in which case 0 is written out).

![](../../assets/cca6114425b02990.png)


![](../../assets/cca6114425b02990.png)

The variance of the pixel reflection luminance (between new and previous frame radiance) is also stored, one thing to note is that the code uses a technique described [here](https://developer.download.nvidia.com/video/gputechconf/gtc/2020/presentations/s22699-fast-denoising-with-self-stabilizing-recurrent-blurs.pdf), counting the number of frames (num_samples) after dissoclusion of the pixel to stabilise the variance (variance_mix) after a disocclusion event (i.e. it will interpolate towards the old variance initially, ending up towards the new variance as the number of frames after the disocclusion increases). This variance will be later used to guide spatially filtering of the SSR image. Finally this pass calculates the average radiance per 8×8 tile, using groupshared memory, and stores to a rendertarget. Since all intermediate values as stored as halves, the shader does some extra work to pack the halves to uints to store to the groupshared memory, using the f32tof16() function which will return the half floating point precision number in the bottom 16 bits of a uint (the bit representation). Like mentioned, the output of this pass will act as the history buffer for the Temporal Resolve pass later.

This is the result of the reprojection pass, we can notice the tile-based processing and also that the sample does not clear the rendertarget (so you can see results from previous frame as the camera moves around) because it doesn’t need to — we know exactly which tiles contain valid data for this frame.

![](../../assets/e0a1a6d8b12543e8.png)


![](../../assets/e0a1a6d8b12543e8.png)

After reprojection, a spatial filtering pass follows (DNSR Prefilter, 0.34ms) that processes the result of the Intersect pass, to reduce noise. This works with the tiles marked as needing denoising during the ClassifyTiles as well. Filtering is performed using 15 samples (+ the central one) drawn from the Halton sequence and converted to integer offsets:

![](../../assets/b9c16be756a39cef.png)


![](../../assets/b9c16be756a39cef.png)

The filtering itself uses normal, depth, radiance and variance differences to adjust the weight of each sample, to avoid overblurring.

![](../../assets/8976288991514524.png)


![](../../assets/8976288991514524.png)

This is the result of the spatial filter pass, we notice that blurring is stronger in noisy areas, which have higher variance.

![](../../assets/7fd8ffec899a63b0.png)


![](../../assets/7fd8ffec899a63b0.png)

The final pass is a temporal resolve to converge to the final image (DNSR Resolve Temporal, 0.53ms). This uses the reprojected image from the Reprojection pass (as the history buffer) and the spatially filtered image from the Prefilter pass (as the current buffer). It clips the history sample using local area statistics like variance and mean. Blending current and history sample doesn’t use a constant factor as it is usual in temporal antialiasing but uses the trick mentioned already to bias the factor based on the number of frames since disocclusion:

This will result in starting with the current sample (new_signal) right after disocclusion, gradually blending towards the history (clipped_old_signal) as the number of frames since disocclusion inscreases.

This is the result of the temporal resolve pass, most of the noise has be suppressed.

![](../../assets/3805934f22b85367.png)


![](../../assets/3805934f22b85367.png)

A few more observations, the code uses 16bit floats whenever possible to reduce the number VGPRs required for the ALU operations. This can increase the [shader occupancy](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/), which can help hide the latency due to memory reads. The sample allocates quite a few internal rendertargets, I counted 13, to store the history of almost all provided inputs and various other data, prioritising speed over memory.

This technique achieves good SSR quality, it is educational to study with lots of good practices in place and kudos to AMD for releasing the code to the public.

Now, I should go back and actually do some work to integrate this to the toy engine!

This one was especially informative. The single pass downscaling was new to me, that’s a very useful case study in using modern GPU capabilities effectively.