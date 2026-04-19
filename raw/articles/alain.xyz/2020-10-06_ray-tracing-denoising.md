---
title: Ray Tracing Denoising
url: https://alain.xyz/blog/ray-tracing-denoising
author: Alain Galvan
published: '2020-10-06'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Monte-carlo ray tracing is a technique that relies on accumulating random samples to reach a satisfying approximation of a given scene. This process was traditionally a *slow one* with plenty of variance, but with the advent of real time ray tracing solutions with recent graphics cards, there's been a resurgence of research in denoising techniques.

These denoising techniques include **filtering** using guided blurring kernels, **machine learning** to drive filters or importance sampling, improving **sampling** schemes through better quasi-random sequences such as blue noise and spatio-temporal reuse of either rays or the final luminance, and **approximation techniques** that attempt to quantize and cache information with some sort of spatial structure such as probes, irradiance caches, neural radiance fields (NeRFs), etc.

![4096 sample per pixel example](../../assets/3e43a4652e3017b3.png)


A robust denoiser should consider using *all* of these techniques depending on the trade-offs and needs of your application.

Recent research has focused on moving denoising to earlier in rendering by improving sampling schemes and re-sampling pixels with cached information, with prior research focused on filtering, autoencoders in machine learning, importance sampling, and real time methods that are currently in production in commercial games and renderers. We'll be discussing key papers on denoising and their implementations, **focusing on how to build your own robust real time ray tracing denoiser**.

Denoising has seen a significant number of new publications since the release of this article, with techniques such as ReSTIR, NVIDIA's denoising suite, and machine learning techniques improving significantly. This article could use some updates for these recent papers, but the ideas here are still applicable today.


![Bilateral Filter](../../assets/653949bd44bbea6d.png)


**Filtering techniques** such as *Gaussian*, *Bilateral*, *À-Trous* [[Dammertz et al. 2010]](https://alain.xyz#ref_dammertz2010), *Guided* [[He et al. 2012]](https://alain.xyz#ref_he2012), and *Median* [[Mara et al. 2017]](https://alain.xyz#ref_mara2017) filters have been used to blur monte-carlo ray traced images. In particular Guided filters driven by *feature buffers* such as common G-Buffer attachments in Deferred Rendering like *normals*, *albedo*, *depth/position*, as well as specialized buffers such as *first-bounce data*, *reprojected path length*, or *view position* have been used in recent denoising papers and commercial implementations.

While these filtering techniques are effective and cheap to compute, they come at the cost of a lossy representation of the scene and the reduction of high frequency information like sharp edges. This loss of information can be so drastic that it can even lead to differences in the level of brightness in scenes with salt & peppering occurring in either highlights or shadows.

![1 Sample Per Pixel OIDN](../../assets/42cf44384b51e878.png)


**Machine Learning** has been used in a wide range of problem domains related to denoising, from general image reconstruction to real time ray tracing denoising through the use of *denoising autoencoders* [[Khademi Kalantari et al. 2013]](https://alain.xyz#ref_kalantari2013) [[Khademi Kalantari et al. 2015]](https://alain.xyz#ref_kalantari2015) [[R. Alla Chaitanya et al. 2017]](https://alain.xyz#ref_chaitanya2017) [[Vogels et al. 2018]](https://alain.xyz#ref_vogels2018), driving filtering techniques [[Wang et al. 2018]](https://alain.xyz#ref_wang2018) [[Xu et al. 2019]](https://alain.xyz#ref_xu2019) [[Meng et al. 2020]](https://alain.xyz#ref_meng2020) [[Işık et al. 2021]](https://alain.xyz#ref_isik2021), varying convolution sizes to reduce computational costs [[Jiang et al. 2022]](https://alain.xyz#ref_jiang2022), spatio-temporal techniques [[Hasselgren et al. 2020]](https://alain.xyz#ref_hasselgren2020), NeRFs to approximate view dependent effects like reflections [[Verbin et al. 2021]](https://alain.xyz#ref_verbin2021) or to denoise a scene [[Mildenhall et al. 2022]](https://alain.xyz#ref_mildenhall2022), and upscaling images while maintaining detail through super-resolution/super-sampling [[Dong et al. 2015]](https://alain.xyz#ref_dong2015) [[Ledig et al. 2016]](https://alain.xyz#ref_ledig2016) [[Xiao et al. 2020]](https://alain.xyz#ref_xiao2020). Denoising and supersampling can even be done together using a neural network [[Mathew Thomas et al. 2022]](https://alain.xyz#ref_thomas2022), with NVIDIA integrating both in [DLSS 3.5](https://www.nvidia.com/en-us/geforce/news/nvidia-dlss-3-5-ray-reconstruction/).

Industry leaders such as Intel and NVIDIA have sponsored research in machine learning based denoisers, [Intel Open Image Denoise](https://openimagedenoise.github.io/) and the [NVIDIA Optix Autoencoder](https://developer.nvidia.com/optix) both use a denoising autoencoder to denoise images to great success. [NVIDIA's Deep Learning Super Sampling (DLSS 2.0)](https://www.nvidia.com/en-us/geforce/news/nvidia-dlss-2-0-a-big-leap-in-ai-rendering/) has also been used to upscale ray traced applications such as Minecraft RTX, Remedy Entertainment’s [Control](https://controlgame.com/), and more, with the goal of reducing computational costs by upscaling to native resolutions a *fraction* of the original image.

![1 Sample Per Pixel](../../assets/59ea1d256770f323.png)


**Sampling techniques** have seen a resurgence in new literature. While a naive monte carlo ray tracer would simply accumulate samples on an unchanging scene, it's possible to reuse samples in a moving scene. Examples include Temporal Anti-Aliasing [[Korein et al. 1983]](https://alain.xyz#ref_korein1983) [[Yang et al. 2020]](https://alain.xyz#ref_lei2020), the Spatio-Temporal Filter [[Mara et al. 2017]](https://alain.xyz#ref_mara2017), the Spatio-Temporal Variance Guided Filter (SVGF) [[Schied 2017]](https://alain.xyz#ref_schied2017), Spatial Denoising employed by [[Abdollah-shamshir-saz 2018]](https://alain.xyz#ref_baktash2018), Adaptive SVGF (A-SVGF) [[Schied et al. 2018]](https://alain.xyz#ref_schied2018), Blockwise Multi-Order Feature Regression (BMFR) [[Koskela et al. 2019]](https://alain.xyz#ref_koskela2019)).

These techniques would rely on using high frequency quasi-random sequences such as blue noise (which would be used in combination with filtering) [[Benyoub 2019]](https://alain.xyz#ref_benyoub2019) , as well as common tools such as firefly rejection [[Liu et al. 2019]](https://alain.xyz#ref_liu2019), next event estimation (NEE), and importance sampling [[Veach 1998]](https://alain.xyz#ref_veach1998).

There have also been attempts to move denoising to earlier in rendering by making sampling less biased through ray hashing [[Pantaleoni 2020]](https://alain.xyz#ref_pantaleoni2020) or reusing statistics from neighboring sampling probabilities [[Bitterli et al. 2020]](https://alain.xyz#ref_bitterli2020). Variations of these techniques have emerged that target a smaller subset of ray tracing such as Global Illumination [[Boisse 2021]](https://alain.xyz#ref_boisse2021) and motion blur [[Oberberger et al. 2022]](https://alain.xyz#ref_oberberger2022), or using tiles for point lights [[Tokuyoshi 2022]](https://alain.xyz#ref_tokuyoshi2022).

![Light Probes](../../assets/4a505d4d2a6ed1af.png)


In addition, there's **approximation techniques** that attempt to fine tune behavior for different aspects of a path tracer. The *RTX Global Illumination* paper approximated ray traced global illumination (GI) with light probes which used ray tracing to better determine the proper radiance of each probe and to position probes in the scene to avoid bleeding or inaccurate interiors. Techniques that can avoid screen space monte carlo integration entirely such as RTXGI also avoid the need for real time denoising routines *but can be used together with screen space techniques*. RTXGI have been recently integrated to commercial game engines such as Unreal Engine 4 and Unity [[Majercik et al. 2020]](https://alain.xyz#ref_majercik2020).

The **Spatio-Temporal Variance Guided Filter (SVGF)** [[Schied 2017]](https://alain.xyz#ref_schied2017) is a denoiser that uses spatio-temporal reprojection along with feature buffers like normals, depth, and variance calculations to drive a bilateral filter to blur regions of high variance.

[Minecraft RTX](https://alain.xyz/blog/frame-analysis-minecraftrtx) uses a form of SVGF, with the addition of irradiance caching, the use of ray length for better driving reflections, and splitting rendering for transmissive surfaces such as water. SVGF, while very effective, does introduce temporal lag that is [noticable in game](https://twitter.com/NateMorrical/status/1262187056911970306).

**Adaptive Spatio-Temporal Variance Guided Filtering (A-SVGF)** [[Schied et al. 2018]](https://alain.xyz#ref_schied2018) improves on SVGF by adaptively reusing previous samples that have been spatially reprojected according to temporal hueristics such as the change in variance, viewing angle, etc. encoded in a *Moment Buffer*, and filtering that with a fast bilateral filter. So rather than accumulating samples based on history length, the moment buffer acts as an alternative hueristic that uses the change in variance to drive the proportion of old samples and newer samples, resulting in less ghosting. While SVGF only used the moment buffer to drive blurring, A-SVGF uses it for both the filtering and accumulation steps.

Though the introduction of a moment buffer helps with temporal lag it doesn't completely get rid of it. There can be differences in brightness between regions with a high number of accumulated samples and new regions. This is especially evident in darker regions of a raytraced scene such as interiors. To mitigate this, rather than using 1 sample per pixel (1 spp), it's best to use 2 spp in dark areas of a scene.

[Quake 2 RTX](https://store.steampowered.com/app/1089130/Quake_II_RTX/) uses A-SVGF as its denoising solution.

**Spatiotemporal Importance Resampling for Many-Light Ray Tracing (ReSTIR)** [[Bitterli et al. 2020]](https://alain.xyz#ref_bitterli2020) attempts to move the spatio-temporal reprojection step of real time denoisers to earlier in rendering, reusing statistics from neighboring sampling probabilities. This is essentially a combination of an earlier paper by [[Talbot et al. 2005]](https://alain.xyz#ref_talbot2005) discussing Resampled Importance Sampling, and adding ideas introduced by spatio-temporal denoisers.

ReSTIR will be available for use in [NVIDIA's RTXDI SDK](https://news.developer.nvidia.com/render-millions-of-direct-lights-in-real-time-with-rtx-direct-illumination-rtxdi/).

These remarkable results show yet another example of how rapidly DNNs are finding their place in and evolving modern renders. ~ Marco Salvi (

[@marcosalvi])

Machine learning techniques such as denoising autoencoders, sample map estimators driving sample counts or importance sampling, neural bilateral grids driving filtering, and super-sampling result in the most drastic improvements in image quality, though these techniques are slower than other algorithms such as A-SVGF.

![OIDN Denoise](../../assets/b396c7079312406a.jpg)


Intel Open Image Denoise (OIDN) is a machine learning autoencoder that takes in a albedo, first bounce normals, and your input noisy image and output a filtered image.

```
// 👋 Declare Handles
// Images loaded from stb as 3 components
float* color;
float* normal;
float& output;
unsigned width;
unsigned height;
oidn::DeviceRef device = oidn::newDevice();
device.commit();
oidn::FilterRef filter = device.newFilter("RT");
filter.setImage("color", color, oidn::Format::Float3, width, height);
filter.setImage("normal", normal, oidn::Format::Float3, width, height);
filter.setImage("output", output, oidn::Format::Float3, width, height);
filter.set("hdr", true);
filter.commit();
filter.execute();
```


![Optix Denoise](../../assets/7472b4b53cf0535d.jpg)


NVIDIA's **Optix 7 Denoising Autoencoder** [[R. Alla Chaitanya et al. 2017]](https://alain.xyz#ref_chaitanya2017) takes in the same inputs as OIDN, an optional albedo, normal, and input noisy image, and outputs a filtered image much faster than Intel's solution at the cost of quality.

```
// 👋 Declare Handles
OptixContext ctx;
OptixDevice device;
unsigned width;
unsigned height;
CUDABuffer denoiserState;
CUDABuffer denoiserScratch;
// https://github.com/ingowald/optix7course/blob/master/example12_denoiseSeparateChannels/SampleRenderer.cpp#L764
OptixDenoiser denoiser;
OptixDenoiserOptions opt;
opt.inputKind = OPTIX_DENOISER_INPUT_RGB_ALBEDO;
opt.pixelFormat = OPTIX_PIXEL_FORMAT_FLOAT4;
optixDenoiserCreate(ctx, &opt, &denoiser);
optixDenoiserSetModel(denoiser, OPTIX_DENOISER_MODEL_KIND_HDR, nullptr, 0);
OptixDenoiserSizes denoiserReturnSizes;
optixDenoiserComputeMemoryResources(denoiser, width, height, &denoiserReturnSizes);
denoiserState.resize(denoiserReturnSizes.stateSizeInBytes);
optixDenoiserSetup(denoiser,0,
width, height,
denoiserState.d_pointer(),
denoiserState.size(),
denoiserScratch.d_pointer(),
denoiserScratch.size());
```


Deep Learning Super Sampling (DLSS) is an upscaling technique that that uses a small color buffer and a direction map to multiply the resolution of the output 2-4 times. This is exclusive to developers pre-approved by NVIDIA, so there's currently no way to use this publicly, that being said there's alternatives such as [DirectML's SuperResolution Sample](https://github.com/microsoft/DirectML/tree/master/Samples/DirectMLSuperResolution/Samples/ML/DirectMLSuperResolution).

An ideal denoiser that combines ideas from the latest state of the art papers could look like the following:

**Prepass** - Calculate the NDC space velocity of the scene, write common G-Buffer attachments such as albedo, normals etc. You may also want first bounce versions of those buffers, which would require a ray-trace based prepass rather than a raster based one.

**Ray Trace** - Use AI Adaptive sampling from [[Kuznetsov et al. 2018]](https://alain.xyz#ref_kuznetsov2018) [[Hasselgren et al. 2020]](https://alain.xyz#ref_hasselgren2020) with a sample map to better determine which regions should recieve more samples, generally highlights/shadows to help avoid salt/peppering and maintain luminance over time. A split denoiser with Specular Reflections and Global Illumination written to separate attachments would be ideal as *Reflection* denoising would do better 1st bounce data, *Global Illumination/Ambient Occlusion/Shadows* can afford to use simpler spatio-temporal accumulation based off less data.

**Accumulation** - Use Spatio-Temporal Reprojection as often as possible, this is easier to do with lambertian data such as Global Illumination/Ambient Occlusion, and harder with specular data like reflections. For better results, use heuristic data like normals/albedo/object IDs to translate previous samples to the current position, as well as 1st bounce data such as view direction, 1st bounce normals/albedo, etc. Any successful reprojections can then be used to either importance sample [[Bitterli et al. 2020]](https://alain.xyz#ref_bitterli2020) or their radiance encoded to a radiance history buffer [[Schied et al. 2018]](https://alain.xyz#ref_schied2018).

**Statistical Analysis** - estimate the variance of the current ray traced image, calculate the change in variance in luminance/velocity and use that to drive spatio-temporal reprojection and filtering. Attempt to reject fireflies with that variance information.

**Filtering** - This can be done quickly with an À-Trous bilateral filter, repeat this step 3-5 times depending on how strong of a blur you want, and decrease the `stepWidth`

by [a power of 2 each time](https://twitter.com/NateMorrical/status/1180302300549500928) (so a sequence of `4`

, `2`

, `1`

in the case of 3 iterations). Alternatively, you could use a denoising autoencoder which will be slower, but can produce better filtering results. That result could then be fed into a super sampling autoencoder that could upscale your results, similar to NVIDIA's DLSS 2.0.

**History Blit** - Write the current prepass data such as *Albedos*, *Depth*, etc. for reprojection next frame.

NVIDIA released an example implementation of a denoiser similar to this that uses ReSTIR [[Wyman et al. 2021]](https://alain.xyz#ref_wyman2021).

![]() | ![]() |
![]() | ![]() |
![]() | ![]() |

Prior to denoising, it's important to encode material information such as Normals, Albedo, Depth/Position, Object ID, Roughness/Metalness, etc. with some sort of General Pass (G-Pass). In addition, having access to velocity makes it possible to translate previous samples to the current position.

A **Velocity Buffer** can be calculated by determining the previous and current NDC space coordinate positions of each vertex being rendered, and taking the difference of the two.

Therefore, one would need the previous `modelViewProjection`

matrix of an object, as well as that object's *animation vertex velocity*, the difference between in position between the current and previous animation sample.

![Motion Buffer Example](../../assets/6dfb24c3bc0b512e.jpg)


```
// 🏃 NDC space velocity
float3 ndc = inPosition.xyz / inPosition.w;
float3 ndcPrev = inPositionPrev.xyz / inPositionPrev.w;
outVelocity = ndc.xy - ndcPrev.xy;
```


It's possible to take this concept further, such as using a motion vector for first bounce glossy reflections, a shadow motion vector for better shadow reprojection while objects are moving, and even dual motion vectors for occlusions. [[Zeng et al. 2021]](https://alain.xyz#ref_yan2021)

**Spatiotemporal reprojection** is reusing the data from previous frames, *spatially* reprojecting them to the current frame. Translating previous samples to the current frame requires that you first find the coordinates in view space for previous frame data, which can be done by just adding the velocity buffer. By comparing difference between the current position/normal/object ID/etc of this screen space coordinate with that of it's previous, you can tell if an object has been previously occluded and is now in view, or reuse previous samples.

![Normalized history buffer](../../assets/aa7da70f1502de1e.jpg)


When performing spatio-temporal reprojection, having a buffer describing the time for which a given sample had to accumulate is very valuable, a **History Buffer**. It can be used to drive a filter to blur stronger in regions with few accumulated samples or be used to estimate the variance of the current image (higher history would mean less variance).

Your history length can then be used as an *accumulation factor* , the contribution factor that current samples should have over the final radiance.

While a history buffer is a useful thing to have, there's better ways of determining an accumulation factor than the ratio of successful reprojections such as the use of the change in luminance, we can use statistical analysis to prevent temporal lag instead.

**Variance** is the squared difference of a signal's average (mean). One can take the average of the current signal and that signal squared with a 3x3 gaussian kernel (what is essentially a tensor, [Bart Wronski](https://t.co/SviUAUe897?amp=1) ([@BartWronsk](https://twitter.com/BartWronsk)) [goes into more detail as to different ways of writing tensor operations here](https://bartwronski.com/2021/02/28/computing-gradients-on-grids-forward-central-and-diagonal-differences/)), then taking the difference of the two.

```
const float radius = 2; //5x5 kernel
float2 sigmaVariancePair = float2(0.0, 0.0);
float sampCount = 0.0;
for (int y = -radius; y <= radius; ++y)
{
for (int x = -radius; x <= radius; ++x)
{
// ⬇️ Sample current point data with current uv
int2 p = ipos + int2(xx, yy);
float4 curColor = tColor.Load(p);
// 💡 Determine the average brightness of this sample
// 🌎 Using International Telecommunications Union's ITU BT.601 encoding params
float samp = luminance(curColor);
float sampSquared = samp * samp;
sigmaVariancePair += float2(samp, sampSquared);
sampCount += 1.0;
}
}
sigmaVariancePair /= sampCount;
float variance = max(0.0, sigmaVariancePair.y - sigmaVariancePair.x * sigmaVariancePair.x);
```


Christoph Schied ([@c_schied](https://twitter.com/c_schied)) does this in A-SVGF estimating the spatial variance as a combination of an edge avoiding guassian filter (similar to the a-trous guided filter) and using this in a feedback loop to drive the `accumulationFactor`

during spatio-temporal reprojection. In addition to managing accumulation, estimating variance can also allow for you to tone down the weight of your filter temporally, [[Olejnik et al. 2020]](https://alain.xyz#ref_olejnik2020) uses a poisson disk filter similar to A-SVGF to better render contact shadows.

```
/**
* Variance Estimation
* Copyright (c) 2018, Christoph Schied
* All rights reserved.
* 🎓 Slightly simplified for this example:
*/
// ⛏️ Setup
float weightSum = 1.0;
int radius = 3; // ⚪ 7x7 Gaussian Kernel
float2 moment = tMomentPrev.Load(ipos).rg;
float4 c = tColor.Load(ipos);
float histlen = tHistoryLength, ipos, 0).r;
for (int yy = -radius; yy <= radius; ++yy)
{
for (int xx = -radius; xx <= radius; ++xx)
{
// ☝️ We already have the center data
if (xx != 0 && yy != 0) { continue; }
// ⬇️ Sample current point data with current uv
int2 p = ipos + int2(xx, yy);
float4 curColor = tColor.Load(p);
float curDepth = tDepth.Load(p).x;
float3 curNormal = tNormal.Load(p).xyz;
// 💡 Determine the average brightness of this sample
// 🌎 Using International Telecommunications Union's ITU BT.601 encoding params
float l = luminance(curColor.rgb);
float weightDepth = abs(curDepth - depth.x) / (depth.y * length(float2(xx, yy)) + 1.0e-2);
float weightNormal = pow(max(0, dot(curNormal, normal)), 128.0);
uint curMeshID = floatBitsToUint(tMeshID, p, 0).r);
float w = exp(-weightDepth) * weightNormal * (meshID == curMeshID ? 1.0 : 0.0);
if (isnan(w))
w = 0.0;
weightSum += w;
moment += float2(l, l * l) * w;
c.rgb += curColor.rgb * w;
}
}
moment /= weightSum;
c.rgb /= weightSum;
varianceSpatial = (1.0 + 2.0 * (1.0 - histlen)) * max(0.0, moment.y - moment.x * moment.x);
outFragColor = float4(c.rgb, (1.0 + 3.0 * (1.0 - histlen)) * max(0.0, moment.y - moment.x * moment.x));
```


Firefly rejection can be done in a variety of ways, from adjusting how you're sampling during raytracing, to using filtering techniques or huristics about your output radiance.

```
//https://twitter.com/YuriyODonnell/status/1199253959086612480
//http://cg.ivd.kit.edu/publications/p2013/PSR_Kaplanyan_2013/PSR_Kaplanyan_2013.pdf
//http://jcgt.org/published/0007/04/01/paper.pdf
float oldRoughness = payload.roughness;
payload.roughness = min(1.0, payload.roughness + roughnessBias);
roughnessBias += oldRoughness * 0.75f;
```


```
// 🗜️ Ray Tracing Gems Chapter 17
float3 fireflyRejectionClamp(float3 radiance, float3 maxRadiance)
{
return min(radiance, maxRadiance);
}
```


```
// 🧯 Ray Tracing Gems Chapter 25
float3 fireflyRejectionVariance(float3 radiance, float3 variance, float3 shortMean, float3 dev)
{
float3 dev = sqrt(max(1.0e-5, variance));
float3 highThreshold = 0.1 + shortMean + dev * 8.0;
float3 overflow = max(0.0, radiance - highThreshold);
return radiance - overflow;
}
```


A-Trous avoids sampling in a slightly dithered pattern to cover a wider radius than would normally be possible in a 3x3 or 5x5 guassian kernel while at the same time having the ability to be repeated multiple times, and avoid bluring across edges thanks number of different inputs.

This can be done in combination with:

Subsampling according to a dithering pattern, thus reducing the number of samples in your bluring kernel even more.

Drive your blur with more information such as surface roughness [[Abdollah-shamshir-saz 2018]](https://alain.xyz#ref_baktash2018), the aproximate Specular BRDF lobe [[Tokuyoshi 2015]](https://alain.xyz#ref_tokuyoshi2015), shadow penumbras [[Liu et al. 2019]](https://alain.xyz#ref_liu2019), etc.

All of these classes of algorithms rely on reusing data, thus when that isn't possible, such as in the case of fast moving objects, highly complex geometry, or areas with little history information, the quality of each method decreases. There are ways to make use of some cached data to help avoid this, such as using irradiance caching to have a better default color as in the case of Minecraft RTX.

| Direct Normals | First Bounce Normals |
|---|---|
![]() | ![]() |

Spatio-temporal reprojection is also significantly more difficult with reflections, so often times denoisers will rely on *first-bounce* data, where the normals of a reflective surface, positional data, etc. are based on the first reflection rather than the original surface.

Denoising can help bridge the gap between a low sample per pixel image and ground truth by *reusing previous samples* through spatio-temporal reprojection - adaptively resampling radiance or statistical information for importance sampling, and using *filters* such as fast gaussian/bilateral filters or *AI techniques* like denoising autoencoders and upscaling though super sampling.

While denoising isn't perfect as temporal techniques can introduce a lag in radiance and any filter will introduce some loss of sharpness due to it attempting to blur the original image, guided filters can help maintain sharpness, and adaptively sampling or increasing samples per pixels for each frame can make the difference between denoised and ground truth images negligable. Still, there's no substitute for higher samples per pixel, so experiment with these techniques with different sample per pixel (spp) counts.

Dihara Wijetunga ([@diharaw94](https://twitter.com/diharaw94)) [released a blog post that discusses denoising different aspects of a hybrid renderer](https://diharaw.github.io/post/adventures_in_hybrid_rendering/).

NVIDIA released their Real-Time Denoiser for limited review. You can sign up to view it [here](https://developer.nvidia.com/nvidia-rt-denoiser).

[Interactive Path Tracing and Reconstruction of Sparse Volumes](https://research.nvidia.com/publication/2021-03_Interactive-Path-Tracing) uses a machine learning denoiser to denoise volumes with adaptive sampling.

Peter Kristof of Microsoft made a really robust DirectX Ray Tracing Ambient Occlusion example with SVGF [here](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop/D3D12Raytracing/src/D3D12RaytracingRealTimeDenoisedAmbientOcclusion).

The Apple Metal Team released an example of using [Metal Performance Shaders, Temporal Anti-Aliasing (MPSTAA), and SVGF (MPSSVGF)](https://developer.apple.com/documentation/metalperformanceshaders/mpssvgfdenoiser) to [denoise a ray traced scene](https://developer.apple.com/documentation/metalperformanceshaders/animating_and_denoising_a_raytraced_scene).

AMD's FidelityFX SSSR features spatio-temporal reprojection to denoise screen space reflections. Here's their [Github](https://github.com/GPUOpen-Effects/FidelityFX-SSSR/tree/cc1bb86af57f385c6532e41020b5e3a11200d654). AMD also released several denoisers for reflections and shadows on this[Github Repo](https://github.com/GPUOpen-Effects/FidelityFX-Denoiser).

NVIDIA has released an SDK to itegrate Deep Learning Super Sampling [here](https://developer.nvidia.com/dlss-getting-started). AMD's [Fidelity FX Super resolution](https://github.com/GPUOpen-Effects/FidelityFX-FSR) is also available for developers to integrate into their applications.

![Ingo Wald's picture](../../assets/bd7aab57f64fb162.png)

[@IngoWald](https://twitter.com/IngoWald))) released a Optix course
which showcases how to use the Optix denoiser [here](https://github.com/ingowald/optix7course/blob/master/example12_denoiseSeparateChannels/SampleRenderer.cpp#L794).

Christof Shied ([@c_schied](https://twitter.com/c_schied)) and Alexey Panteleev ([@more_fps](https://twitter.com/more_fps)) of NVIDIA wrote the denoiser for Quake 2 RTX which is on Github [here](https://github.com/NVIDIA/Q2RTX/blob/master/src/refresh/vkpt/shader/).

[Microsoft's DirectML Super Resolution Example](https://github.com/microsoft/DirectML-Samples/tree/master/DirectMLSuperResolution), while not NVIDIA Deep Learning Super Sampling 2.0 (DLSS 2.0), is similar in that both perform upscaling.

![Xiaoxu Meng's picture](../../assets/9baf949b182be5d4.png)

[Xiaoxu Meng](https://xiaoxumeng1993.wixsite.com/xiaoxumeng) released the source
of their Neural Bilateral Grid paper [here](https://github.com/xmeng525/RealTimeDenoisingNeuralBilateralGrid).

In the [University of Pennsylvania's CIS565 course](https://cis565-fall-2020.github.io/), a number of students, teaching assistants, and former students made awesome projects that implement the latest in denoising research:

[CUDA SVGF](https://github.com/ZheyuanXie/CUDA-Path-Tracer-Denoising) by Zheyuan Xie, Yan Dong, and Weiqi Chen

[Blockwise Multi-Order Feature Regression for Real-Time Path Tracing Reconstruction (BMFR)](https://github.com/gztong/BMFR-DXR-Denoiser) by Jiangping Xu, Gangzheng Tong, and Tianming Xu

[Interactive Reconstruction of Monte Carlo Image Sequences using a Recurrent Denoising Autoencoder](https://github.com/Black-Phoenix/Ai-Path-Tracer-Denoiser) by Dewang Sultania & Vaibhav Arcot implemented with Pytorch.

[ReSTIR in DirectX 12](https://github.com/tatran5/Reservoir-Spatio-Temporal-Importance-Resampling-ReSTIR) by [Sydney Miller](https://youtu.be/8jFfHmBhf7Y), [Sireesha Putcha](https://sites.google.com/view/sireeshaputcha/home), [Thy Tran](https://tatran5.github.io/demo-reel.html).

[ReSTIR in DirectX 12](https://github.com/lindayukeyi/ReSTIR_DX12) by Jilin Liu ([@Jilin18043110](https://twitter.com/Jilin18043110)), Keyi Yu, and Li Zheng.

Chris Wyman's High Performance Graphics 2020 [talk on ReSTIR is available here](https://youtu.be/hhUUb5Op1-4?t=1590).

![Eric Haines's picture](../../assets/47f59cf9f4cb88e9.png)

[@pointinpolygon](https://twitter.com/pointinpolygon)) released
[Ray Tracing Essentials Part 7: Denoising for Ray Tracing](https://www.youtube.com/watch?v=6O2B9BZiZjQ),
a great introduction to denoising.

Tomasz Stachowiak ([@h3r2tic](https://twitter.com/h3r2tic)) et al. designed the Pica Pica renderer, an amazing reference hybrid renderer featured in Ray Tracing gems. Their [talk is available here](https://www.ea.com/seed/news/seed-dd18-presentation-slides-raytracing).

Kostas Anagnostou ([@KostasAAA](https://twitter.com/KostasAAA)) wrote [an article describing a method of handling global illumination denoising inspired in part by Metro Exodus](https://interplayoflight.wordpress.com/2022/03/26/raytraced-global-illumination-denoising/).

Chris Wyman and a number of co-authors for denoising papers at NVIDIA released [A Gentle Introduction to ReSTIR: Path Reuse in Real-time](https://intro-to-restir.cwyman.org/).

I've also written blog posts on [image based denoising with adaptive spatiotemporal filtering, bilateral filtering](https://alain.xyz/blog/ray-tracing-filtering), and using [machine learning autoencoders](https://alain.xyz/blog/machine-learning-denoising), and denoisers of commercial games like [Minecraft RTX](https://alain.xyz/blog/frame-analysis-minecraftrtx):

| [Dammertz et al. 2010] |
| [He et al. 2012] |
| [Mara et al. 2017] |
| [Khademi Kalantari et al. 2013] |
| [Khademi Kalantari et al. 2015] |
| [R. Alla Chaitanya et al. 2017] |
| [Vogels et al. 2018] |
| [Wang et al. 2018] |
| [Xu et al. 2019] |
| [Meng et al. 2020] |
| [Işık et al. 2021] |
| [Jiang et al. 2022] |
| [Hasselgren et al. 2020] |
| [Verbin et al. 2021] |
| [Mildenhall et al. 2022] |
| [Dong et al. 2015] |
| [Ledig et al. 2016] |
| [Xiao et al. 2020] |
| [Mathew Thomas et al. 2022] |
| [Korein et al. 1983] |
| [Yang et al. 2020] |
| [Schied 2017] |
| [Abdollah-shamshir-saz 2018] |
| [Schied et al. 2018] |
| [Koskela et al. 2019] |
| [Benyoub 2019] |
| [Liu et al. 2019] |
| [Veach 1998] |
| [Pantaleoni 2020] |
| [Bitterli et al. 2020] |
| [Boisse 2021] |
| [Oberberger et al. 2022] |
| [Tokuyoshi 2022] |
| [Majercik et al. 2020] |
[Talbot et al. 2005]Importance Resampling for Global IlluminationEurographics 2005 |
| [Kuznetsov et al. 2018] |
| [Wyman et al. 2021] |
| [Zeng et al. 2021] |
[Olejnik et al. 2020]Raytraced Shadows in Call of Duty: Modern WarfareDigital Dragons 2020 |
| [Tokuyoshi 2015] |