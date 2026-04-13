---
title: A gentler introduction to ReSTIR
url: https://interplayoflight.wordpress.com/2023/12/17/a-gentler-introduction-to-restir/
author: Kostas Anagnostou
published: '2023-12-17'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Recently I started exploring ReSTIR, using mainly the [Gentle Introduction to ReSTIR](https://intro-to-restir.cwyman.org/) Siggraph course and the [original paper](https://research.nvidia.com/sites/default/files/pubs/2020-07_Spatiotemporal-reservoir-resampling/ReSTIR.pdf). I began with direct illumination (ReSTIR DI), to quickly set it up and get something working. ReSTIR is a very interesting technique that gives great results but there is a lot of Maths behind it that might dissuade people that want to dip their toes in it, which is a shame. Resources like the Gentle Introduction help a lot towards clarifying some of the theory behind it but it is still Maths heavy. In this post I will be attempting a more “qualitative” discussion of ReSTIR, going straight to the results, avoiding referencing the Maths behind it too much.

Let’s consider one of the still hard to solve problems in real-time graphics, how to light a scene with a very large number of shadowed lights. For example this is Sponza with 400 (unshadowed) point lights.

![](../../assets/0b0fa902d2bea19c.png)


![](../../assets/0b0fa902d2bea19c.png)

The scene looks wrong and unnatural without shadows, with light leaking through walls and pillars. What we would really like instead is this, in which every light is correctly shadowed:

![](../../assets/021ca7584b82dd37.png)


![](../../assets/021ca7584b82dd37.png)

Calculating shadows for a very large number of lights, either through shadowmaps or raytracing, can be very expensive though, in both memory and performance, and for this reason, for real time graphics, we tend to keep the number of shadow casting lights low. There is also the issue of sources of lights that are not really point lights, for example emissive surfaces/area lights, which for it is even harder to calculate shadows. If we can’t raytrace shadows for a large number of lights, what can we do with the typically low per pixel ray budgets? It turns out quite a lot.

Enter ReSTIR. Key to ReSTIR is the assumption that we shouldn’t need to process many lights in the scene per pixel but only a small subset of randomly chosen ones, and from this subset only select one, as the “most important” (important in this context means it has the biggest influence on the surface) and representative which we store in a structure called the “Reservoir”. At the heart of ReSTIR is a technique called Weighted Reservoir Sampling (WRS). ReSTIR builds on this technique to add reservoir reuse across time and space.

Setting up Weighted Importance Sampling is relatively straight forward (pseudocode from [this paper](https://research.nvidia.com/sites/default/files/pubs/2020-07_Spatiotemporal-reservoir-resampling/ReSTIR.pdf)).

Like mentioned, we store a Reservoir per pixel and each Reservoir holds the light index Y of the most influential light in this pixel and its weight W_y.

```
struct Reservoir
{
uint Y; // index of most important light
float W_y; // light weight
float W_sum; // sum of all weights for all lights processed
float M; // number of lights processed for this reservoir
};
bool UpdateReservoir(inout Reservoir reservoir, uint X, float w, float c, inout RngStateType rngState)
{
reservoir.W_sum += w;
reservoir.M += c;
if ( rand01(rngState) < w / reservoir.W_sum )
{
reservoir.Y = X;
return true;
}
return false;
}
```

rand01() is a method that returns a uniformly sampled random number between 0 and 1. This is used to randomly select a light, based on its weight w. Worth noting that the larger the weight (importance) of a light the more likely it is to be selected.

With this at hand we can go ahead and implement weighted reservoir sampling (pseudocode from the same paper):

![](../../assets/04b25d5c253c0ee6.png)


![](../../assets/04b25d5c253c0ee6.png)

Since I promised that this is a mostly qualitative introduction without Maths, I did a quick annotation of the pseudocode to explain what each term is. In code it would look something like that

```
float pdf = 1.0 / N;
float p_hat = 0;
//initial selection of 1 light of M
for (uint i = 0; i < M; i++)
{
uint lightIndex = uint(rand01(rngState) * (NoofPoint - 1));
p_hat = length(GetPointLightRadiance(LightsBuffer[lightIndex], worldPos, CameraPos.xyz, surfaceData));
float w = p_hat / pdf;
UpdateReservoir(reservoir, lightIndex, w, 1, rngState);
}
if (IsReservoirValid(reservoir))
{
PointLightData lightData = LightsBuffer[GetReservoirLightIndex(reservoir)];
RayDesc ray;
ray.Origin = worldPos.xyz;
ray.TMin = 0.05;
ray.TMax = length(lightData.Position.xyz - worldPos.xyz);
ray.Direction = normalize(lightData.Position.xyz - worldPos.xyz);
float shadowFactor = FindHit(Scene, ray); // is this ray occluded?
//pixel radiance with the selected light
float3 radiance = shadowFactor * GetPointLightRadiance(LightsBuffer[GetReservoirLightIndex(reservoir)], worldPos, CameraPos.xyz, surfaceData);
p_hat = length(radiance );
// calculate the weight of this light
reservoir.W_y = p_hat > 0.0 ? rcp(p_hat) * reservoir.W_sum / reservoir.M : 0.0;
// apply it to the radiance to get the final radiance.
radiance *= reservoir.W_y;
}
```

Let’s consider the “simple” case of lighting the scene with only N point lights, 400 of them in this instance. Also let’s assume that we will randomly pick M=32 of them for each pixel. Since we are using the uniform distribution to randomly select lights (i.e. each light has the same probability of being selected) from a total of N, the pdf p(x) is 1/N. Worth noting that we select 32 lights knowing nothing about them, how far away they are, if they are fully occluded or not, we are even unaware if we are selecting the same light multiple times.

The “p_hat” quantity used in the light weight is more interesting. This is the measure of how “important” the light is for this pixel and to approximate that we use the length of the output radiance at the pixel (i.e. the output of the brdf). Above, I have included both diffuse and specular response to the GetPointLightRadiance() that feeds into p_hat. It is also important to add light attenuation and ideally visibility to p_hat (more on this later). How does the p_hat quantity represent the “importance” of the light? If a blue light shines on a red albedo surface the output will be dark and the weight (importance) of the light reduced for example. Or if the light is far away, attenuation will reduce its intensity scaling down the brdf response.

I mentioned that, ideally, we would like to add light visibility (shadows) to p_hat as well, but it might not be possible for all M lights due to cost. Instead we calculate the light weight without visibility during WRS and then apply shadows once to the selected and (we hope) most important light. This is not always accurate though as the light response might be strong on the surface but it might ultimately be occluded. This is a source of noise as we will discuss later.

Finally we calculate the weight reservoir.W_y for the selected light and apply it to the radiance to get the final radiance at the pixel. If the light is shadowed, the radiance will be zero.

A quick warning here, if you usually store your lights in a constant buffer, a common approach with current lighting techniques, you may notice a sever performance degradation in this context of random selection and access of lights. In this case better store the lights in a Structured buffer instead which can support random access.

Like any stochastic technique, ReSTIR can suffer from noise and bias (this is where good understanding of the Maths behind ReSTIR becomes important). Noise is easy to understand. Bias, in practical terms, refers most commonly to a difference in intensity between the reconstructed and the real (ground truth) image. Attempts to denoise the image, for example, can lead to bias.

So, before we begin, it is worth having a reference image to compare to. This one was produced by averaging the results of weighted reservoir sampling discussed above without using any denoising at all, so it should be pretty close to ground through.

![](../../assets/6ab7d5f1d499d7aa.png)


![](../../assets/6ab7d5f1d499d7aa.png)

To begin with, this is the output of weighted reservoir sampling discussed above, selecting 32 lights out of 400. I went ahead and added light visibility to the p_hat during the initial selection to see the effect.

![](../../assets/ea80280f99f07d72.png)


![](../../assets/ea80280f99f07d72.png)

The result is noisy but nothing a good denoiser can’t fix. The bigger issue here is the cost, tracing 32 shadow rays per pixel. Alternatively we can remove light visibility from the initial selection and add it only to the final, selected light. This is the result, tracing one shadow ray per pixel.

![](../../assets/a4137e0ec3fcf836.png)


![](../../assets/a4137e0ec3fcf836.png)

First of all a quick observation, being able to render so many shadowcasting lights using one shadow ray per pixel is very impressive! Getting more into the details, the image is noticeably noisier, and also we have lost some detail in the darker areas compared to the reference and the previous result (compare the bottom right of the images for example). This is, as discussed, the result of not including the light visibility to the p_hat during initial selection. To visualise, white pixels in the following image have selected a valid light which was ultimately shadowed (apologies for the poor choice of colour, hard to find one that stands out in such a multicoloured lit scene).

![](../../assets/ca31fcbd3268df24.png)


![](../../assets/ca31fcbd3268df24.png)

In the mentioned bottom right corner, almost all selected lights are ultimately shadowed contributing no lighting in the area.

Also, since the whole process is stochastic, pixels can end up selecting no light. To showcase of this, white pixels have received no valid light index and receive no light, another source of noise.

![](../../assets/15ef5c5fd45c8aad.png)


![](../../assets/15ef5c5fd45c8aad.png)

Results are good so far, we managed to calculate shadows for 400 lights using one shadow ray per pixel like discussed, but we can do better. The per-pixel reservoirs for the current frame contain an “important” light for the pixel but so do the reservoirs from the previous frame, so why not combine them?

Temporal reuse is pretty straightforward, all we need to do is keep around the reservoirs from the previous frame and combine them using the UpdateReservoir() method above.

```
Reservoir temporalReservoir;
InitialiseReservoir(temporalReservoir);
//reproject using the motion vectors.
int2 screenPosPrevious = (uv - velocityBuffer[screenPos]) * RTSize.xy;
float3 normalPrevious = normalize(normalBufferPrevious[screenPosPrevious].xyz);
Reservoir reservoirPrevious = reservoirBufferPrevious[screenPosPrevious.y * RTSize.x + screenPosPrevious.x];
//restrict influence from past samples.
reservoirPrevious.M = min(20.f * reservoir.M, reservoirPrevious.M);
//some simple rejection based on normals' divergence, can be improved
bool validHistory = dot(normalPrevious, surfaceData.Normal) >= 0.99;
if (validHistory)
{
//add current reservoir sample
UpdateReservoir(temporalReservoir, GetReservoirLightIndex(reservoir), p_hat * reservoir.W_y * reservoir.M, reservoir.M, rngState);
float p_HatPrev = validHistory?
length(GetPointLightRadiance(PointLights[GetReservoirLightIndex(reservoirPrevious)], worldPos, CameraPos.xyz, surfaceData)) :
0.0;
//add sample from previous frame
UpdateReservoir(temporalReservoir, GetReservoirLightIndex(reservoirPrevious), p_HatPrev * reservoirPrevious.W_y * reservoirPrevious.M, reservoirPrevious.M, rngState);
p_hat = IsReservoirValid(temporalReservoir) ?
length(GetPointLightRadiance(LightsBuffer[GetReservoirLightIndex(temporalReservoir)], worldPos, CameraPos.xyz, surfaceData)) : 0.0;
//calculate weight of the selected lights
temporalReservoir.W_y = p_hat > 0.0 ? rcp(p_hat) * temporalReservoir.W_sum / temporalReservoir.M : 0.0;
reservoir = temporalReservoir;
}
```

You will need to add reprojection and some sort of rejection in case the previous sample is not valid (due to disocclusion etc).

Effectively what this does is to give another chance to the current pixel to select an “important” light, in case it failed the first time around, due to the reasons we discussed. This is expected to improve the quality of the result and it does:

![](../../assets/e153eb483e46a534.png)


![](../../assets/e153eb483e46a534.png)

We can take the idea of sample reuse even further. It is reasonable to assume that in the neighbourhood of a pixel the surface material properties will be similar so the selected “important” light in their reservoirs will in all likelihood be suitable for the current pixel as well. We can randomly select a few reservoirs in the vicinity of a pixel and combine them similarly to how we combined the temporal reservoir as well. How many reservoirs and the radius of the area is configurable, in this case I tried 5 samples (plus the central one) and a radius of 30 pixels, as suggested in the original paper.

```
// combine current pixel's reservoir
float p_hat = IsReservoirValid(reservoir) ?
length(GetPointLightRadiance(LightsBuffer[ GetReservoirLightIndex(reservoir) ], worldPos, CameraPos.xyz, surfaceData)) : 0;
UpdateReservoir(reservoirNew, GetReservoirLightIndex(reservoir), p_hat * reservoir.W_y * reservoir.M, reservoir.M, rngState);
for (int i = 0; i < noofNeighbours; i++)
{
float2 offset = 2.0 * float2(rand01(rngState), rand01(rngState)) - 1;
offset.x = screenPos.x + int(offset.x * radius);
offset.y = screenPos.y + int(offset.y * radius);
offset.x = max(0, min(RTSize.x - 1, offset.x));
offset.y = max(0, min(RTSize.y - 1, offset.y));
float neighbourDepthLinear = LineariseDepth(depthBuffer[int2(offset)].x);
if ( (neighbourDepthLinear > 1.1f * depthLinear || neighbourDepthLinear < 0.9f * depthLinear) ||
dot(surfaceData.Normal.xyz, normalBuffer[int2(offset)].xyz) < 0.906)
{
// skip this neighbour sample if not suitable
continue;
}
neighbourReservoir = reservoirBuffer[offset.y * RTSize.x + offset.x];
p_hat = IsReservoirValid(neighbourReservoir) ?
length(GetPointLightRadiance(LightsBuffer[ GetReservoirLightIndex(neighbourReservoir) ], worldPos, CameraPos.xyz, surfaceData)) : 0;
UpdateReservoir(reservoirNew, GetReservoirLightIndex(neighbourReservoir), p_hat * neighbourReservoir.W_y * neighbourReservoir.M, neighboruReservoir.M, rngState);
}
radiance = IsReservoirValid(reservoirNew) ? GetPointLightRadiance(LightsBuffer[ GetReservoirLightIndex(reservoirNew) ], worldPos, CameraPos.xyz, surfaceData, diffuse, specular) : 0;
p_hat = length(radiance);
reservoirNew.W_y = p_hat > 0.0 ? rcp(p_hat) * reservoirNew.W_sum / reservoirNew.M : 0.0;
reservoir = reservoirNew;
//apply weight to both specular and diffuse
diffuse *= reservoir.W_y;
specular *= reservoir.W_y;
//Find visibility for the selected light
RayDesc ray;
ray.Origin = worldPos.xyz;
ray.TMin = 0.05;
PointLightData lightData = PointLights[GetReservoirLightIndex( reservoir )];
ray.TMax = length(lightData.Position.xyz - worldPos.xyz);
ray.Direction = normalize(lightData.Position.xyz - worldPos.xyz);
bool visible = FindHit(Scene, ray);
diffuse *= visible;
specular *= visible;
```

The reservoir combining logic is exactly the same as in the Temporal reuse case. We only keep samples that are similar to the current one both in terms of normal direction and depth. This is the output of the spatial reuse only, again the visual improvement and noise reduction is evident.

![](../../assets/d24e06dc3bd8327d.png)


![](../../assets/d24e06dc3bd8327d.png)

You might have noticed that at the end of the code we recalculate visibility for the selected light. Lights in the reservoirs have visibility applied to them from the initial gather pass (their weight W_y becomes zero in this case so they don’t contribute), but during spatial reuse surface positions may change and the calculated visibility might not be valid any more. In the next screenshot I calculate final radiance without visibility as an example.

![](../../assets/faf5df4792a7a0f8.png)


![](../../assets/faf5df4792a7a0f8.png)

Shadows are broadly correct but not as accurate as in the previous case, some light leaking is noticeable (check the base of the pillar on the right for example)

Finally, we can combine both temporal and spatial reuse and get good quality with much reduced noise.

![](../../assets/3b13917c8990c461.png)


![](../../assets/3b13917c8990c461.png)

In this case we feed the output of the spatial reuse back to the temporal reuse pass something that will continue to improve the quality of the selected lights over time. ReSTIR won’t remove noise entirely, it will need additional denoising for that but we start at a very good place with little variance in the image. As a reminder, this is what we started with

![](../../assets/a4137e0ec3fcf836.png)


![](../../assets/a4137e0ec3fcf836.png)

Regular TAA at the end can further suppress some of the remaining noise to produce a cleaner image.

![](../../assets/3fb40e169c458cf7.png)


![](../../assets/3fb40e169c458cf7.png)

With this article I made an attempt to demonstrate that it is possible to set up and get basic ReSTIR working without first delving too deep in the Maths behind it, to encourage and pique people’s interest in this great technique. I need to stress though that to implement it correctly and get the correct results one **will **need a good understanding of the supporting Maths. I would also suggest that you start with the [original paper](https://research.nvidia.com/sites/default/files/pubs/2020-07_Spatiotemporal-reservoir-resampling/ReSTIR.pdf) and the pseudocode in it as it is all you will need to get it working and then study [The Gentle Introduction to ReSTIR](https://intro-to-restir.cwyman.org/), as it does a great job at explaining the foundations and many improvements. There is so much to explore with ReSTIR still, support for area lights and emissive surfaces for example and how it can be used for GI.

Finally, I have just started exploring ReSTIR as well, if anything in this post is not accurate please let me know!

Wow, I think this is my favorite post yet! This breakdown is so useful. I definitely understood a few things from your code more clearly than when I read the paper. Thank you so much for this.

The a tiny error in the 3rd code sample; it checks ‘validHistory’ inside the validHistory clause.

Great article finally gives me guts to touch restir after so many years, just want to add a little bit, “biased” in ray tracing usually means our algorithm (estimator) can no longer converge to ground truth no matter how many samples are used due to additional variance introduced, for restir in particular, it usually comes from the reservoir sharing between neighbour pixels, otherwise the naive restir can be considered as an unbiased estimator if not consider noise reduction part.