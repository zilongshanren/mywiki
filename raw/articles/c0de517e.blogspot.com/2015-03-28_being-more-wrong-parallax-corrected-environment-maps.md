---
title: 'Being more wrong: Parallax corrected environment maps'
url: https://c0de517e.blogspot.com/2015/03/being-more-wrong-parallax-corrected.html
published: '2015-03-28'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Introduction**

A follow-up to my article on how

Here I'll have a look at the errors we incur when we want to adopt "parallax corrected" (a.k.a. "localized" or "proxy geometry") pre-filtered cube-map probes,

[wrong we do environment map lighting](http://c0de517e.blogspot.ca/2014/06/oh-envmap-lighting-how-do-we-get-you.html), or how to get researchers excited and engineers depressed.Here I'll have a look at the errors we incur when we want to adopt "parallax corrected" (a.k.a. "localized" or "proxy geometry") pre-filtered cube-map probes,

[a](http://www.slideshare.net/philiphammer/the-rendering-technology-of-lords-of-the-fallen)[technique](http://www.frostbite.com/wp-content/uploads/2014/11/course_notes_moving_frostbite_to_pbr.pdf)[so](http://petersikachev.blogspot.ca/2014/08/siggraph-2014-talk-reflections-in-thief.html)[very](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/ReflectionEnvironment/index.html)[popular](http://docs.unity3d.com/Manual/class-ReflectionProbe.html)[nowadays](http://www.slideshare.net/guerrillagames/lighting-of-killzone-shadow-fall).
I won't explain the base technique here, for that please refer to the following articles:

[Sebastien Lagarde in GPU Pro 4](https://seblagarde.wordpress.com/tag/cubemap/)and his[presentation at Siggraph 2012](https://seblagarde.wordpress.com/2012/11/28/siggraph-2012-talk/)were very influential[Approximating ray-tracing on the GPU with distance impostors](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.162.1876&rep=rep1&type=pdf)is an earlier, closely related technique.- Going even further back in time Brennan from AMD, following ideas from Apodaca,
[suggested to intersect reflection with a bounding sphere](http://developer.amd.com/wordpress/media/2012/10/ShaderX_CubeEnvironmentMapCorrection.pdf), but in a fast approximated way. For par condicio, here is a similar article by[NVidia](http://http.developer.nvidia.com/GPUGems/gpugems_ch19.html), surely the same ideas have been "rediscovered" many times by different people. - See the
[STAR on Specular Effects on the GPU](http://sirkan.iit.bme.hu/~szirmay/specstar11.pdf)for a wider overview.

**Errors, errors everywhere...**



All these are in -addition- to the errors we commit when using the standard cubemap-based specular lighting.

**1) Pre-filter shape**

Let's imagine we're in an empty rectangular room, with diffuse walls. In this case the cubemap can be made to accurately represent radiance from the room.

We want to prefilter the cubemap to be able to query irradiance in a fast way. What shape does the filter kernel have?

- The cubemap is not at infinite distance anymore -> the filter doesn't depend only on angles!
- We have to look at how the BRDF lobe "hits" the walls, and that depends on many dimensions (view vector, normal, surface position, surface parameters)
- Even in the easy case where we assume the BRDF lobe to be circularly symmetric around the reflection, and we consider the reflection to hit a wall perpendicularly, the footprint won't be exactly identical to one computed only on angles.
- More worryingly, that case won't actually happen often, the BRDF will often hit a wall, or many walls, at an angle, creating an
[anisotropic footprint](https://graphics.stanford.edu/papers/trd/)! - Pre-filtering "from the center", using angles, will skew the filter size near the cube vertices, but unlike infinite cubemaps, this is not exactly justified in this case, it optimizes for a single given point of view (query position)
- Moreover! This is not radiance emitted from some magic infinitely distant environment. If we consider geometry, even through a proxy, we should then consider how that geometry emits radiance. Which is a 2D function (spherical). So we should bake a 4D representation, e.g. a cube map of spherical harmonic coefficients...

It doesn't have a direct, one-to-one relationship with the material roughness... We can try, knowing we have a prefiltered cube, to approximate what fetch or fetches best approximate the actual BRDF footprint on the proxy geometry.

This problem can be seen also from a different point of view:

- Let's assume we have a perfectly prefiltered cube for a given surface location in space (query point or "point of view").
- Let's compute a new cubemap for a different point in space, by re-projecting the information in the first cubemap to the new point of view via the proxy geometry (or even the actual geometry for what matters...).
- Let's imagine the filter kernel we applied at a given cubemap location in the original pre-filter.

How will it become distorted after the projection we do to obtain the new cubemap? This is the

[distortion](http://math.etsu.edu/multicalc/prealpha/Chap3/Chap3-3/printversion.pdf)that we need to compensate somehow...


*T*

*his issue is quite apparent with rougher objects near the proxy geometry, it r*

*esults in a reflection that looks sharper, less rough than it should be, usually as we underfilter compared to the actual footprint.*

*A common "solution" is to not use parallax projection as the surfaces get rougher, which creates lighting errors.*



![]() |

while working on area lights, the problem with cubemaps is identical

**2) Visibility**

In most real-world applications, the geometry we use for the parallax-correction (commonly a box) is doesn't match exactly the real world geometry. Environment with all perfectly rectangular, perfectly empty rooms might be a bit boring.

As soon as we place an object on the ground, its geometry won't be captured by the reflection proxy, and we will be effectively raytracing the reflection past it, thus creating a light leak.

This is really quite a hard problem, light leaks are one of the big issues in rendering, they are immediately noticeable and they "disconnect" objects. Specular reflections in PBR tend to be quite intense, and so it's not easy even to just occlude them away with standard methods like SSAO (and of course considering only occlusion would be per se an error, we are just subtracting light).

An obvious solution to this issue is to just enrich somehow the geometrical representation we have for parallax correction, and this could be done in quite a lot of ways, from having richer analytic geometry to trace against, to using signed distance fields and so on.

All these ideas are neat, and will produce absolutely horrible results. Why? Because of the first problem we analyzed!

The more complex and non-smooth your proxy geometry is, the more problems you'll have pre-filtering it. In general if your proxy is non-convex your BRDF can splat across different surfaces at different distances and will horribly break pre-filtering, resulting in sharp discontinuities on rough materials.

Any solution to this that wants to use non-convex proxies, needs to have a notion of prefiltered visibility, not just irradiance, and the ability of doing multiple fetches (blending them based on the prefiltered visibility)

*A common trick to partially solve this issue is to "*

[renormalize](http://blog.selfshadow.com/publications/s2013-shading-course/lazarov/s2013_pbs_black_ops_2_slides_v2.pdf)" the cube irradiance based on the ratio between the diffuse irradiance at the cube center and the diffuse irradiance at the surface (commonly known via lightmaps).*The idea is that such ratio would express somewhat well how different (due to occlusions/other reflections) how intense the cubemap would be if it was baked from the surface point.*

*This trick works for rough materials, as the cubemap irradiance gets more "similar" to diffuse irradiance, but it breaks for sharp reflections... Somewhat ironically here the parallax cubemap is "best" with rough reflections, but we saw the opposite is true when it comes to filter footprint...*

![]() |

[Screen Space Raytracing](http://casual-effects.blogspot.ca/2014/08/screen-space-ray-tracing.html)**3) Other errors**

For completeness, I'll mention here some other relatively "minor" errors:

- Interpolation between reflection probes. We can't have a single probe for the entire environment, likely we'll have many that cover everything. Commonly these are made to overlap a bit and we interpolate while transitioning from one to another. This interpolation is wrong, note that if the two probes reprojected identically at a border between them, we wouldn't need to interpolate to being with...
- These reflection proxies capture only radiance scattered only at a specific direction for each texel. If the scattering is not purely diffuse, you'll have another source of error.
- Baking the scattering itself can be complicated, without a path tracer you risk to "miss" some light due to multiple scattering.
- If you have fog (
[atmospheric scattering](http://cseweb.ucsd.edu/~ravir/papers/singlescat/scattering.pdf)), its influence has to be considered, and it can't really be just pre-baked in the probes correctly (it depends on how much fog the reflection rays traverses, and it's not just attenuation, it will scatter the reflection rays altering the way they hit the proxy) - Question: what is the best point inside the proxy geometry volume from which to bake the cubemap probe? This is usually hand authored and artists tend to place it as possible away from any object (this could be a heuristic indeed, easy to implement).
- Another way of seeing parallax-corrected probes is to treat think of them really
[as textured area lights](http://gpupro.blogspot.ca/2014/03/gpu-pro-5-physically-based-area-lights.html)

*A common solution to mitigate many issues is to use*

[screen space reflections](http://jcgt.org/published/0003/04/04/paper.pdf)(especially if you have the performance to do so,[fading to baked cubemap proxies](http://bartwronski.com/2014/01/25/the-future-of-screenspace-reflections/)only where the SSR doesn't have data to work.*I won't delve into the errors and*

[issues](http://bartwronski.com/2014/03/23/gdc-follow-up-screenspace-reflections-filtering-and-up-sampling/)of SSR here, it would be off-topic, but beware of having the two methods represent the same radiance. Even when that's done correctly, the transition between the two techniques can be[very noticeable and distracting](https://www.youtube.com/watch?v=Y6PQ19BEE24), it might be better to use one or the other based on location.


![]() |

[GPU-Based Importance Sampling](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch20.html).**Conclusions**



If you think you are not committing large errors in your PBR pipeline, you didn't look hard enough. You should be aware of many issues, most of them having a real, practical impact and you should assume many more errors exist that you haven't discovered yet.

Do your own tests, compare with real-world, be aware, critical, use "ground truth" simulations.

Remember that in practice artists are good at hiding problems and working around them, often asking to have non-physical adjustment knobs they will use to tuning down/skew certain effects.

Listen to these requests as they probably "hide" a deep problem with your math and assumptions.

Finally, some tips on how to try solve these issues:

- PBR is not free from hacks (not even
[offline...](http://offline.../)), there are many things we can't derive analytically. - The main point of PBR is that now we can reason about physics to do "well motivated" hacks.
- That requires having references and ground truth to compare and tune.
- A good idea for this problem is to write an importance sampled shader that does glossy reflections via many taps (doing the filtering part in realtime, per shaded point, instead of pre-filtering).
- A full raytraced ground truth is also handy, and you don't need to recreate all the features of your runtime engine...
- Experimentation requires fast iteration and a fast and accurate way to evaluate the error against ground truth.
- If you have a way of programmatically computing the error from the realtime solution to the ground truth, you can figure out models with free parameters that can be then numerically optimized (fit) to minimize the error...

## 5 comments:

Perhaps we can use some smart BRDFish screen-space blur to produce variable roughness look from mirror reflection render? This way any crazy cubemap projections, SSR and whatnot could be unified. Something like this? http://www.nvidia.com/docs/IO/78196/HPG09-ISG.pdf

Yes that indeed can be a good idea and I wouldn't be surprised if someone already used it to some extent, as there are people that do SSR via a post-blur and most SSR techniques do fallback to some sort of cubemaps...


But of course that is at a cost of an extra pass.

Modern game lighting = a bunch of stupid hacks



And the reality is that the result doesn't even look that good.

Take Destiny vs Mario Kart 8, technically Destiny is more accurate, but in reality I'd rather stare at MK.

Yeah Ive always thought it kinda funny that everyone spends a lot of time matching their cube maps to their BRDF function and then make it completely wrong by projecting it. But most people think it looks great because wrong reflections are better than no reflections. I showed people at the office the Unreal Paris demo and they were blown away. Tons of places where the reflections are breaking down or just flat out wrong. For instance the cube map on the chrome light fixture in the hallway is not even from the hallway, they are from the room that isnt visible from that position. But from a distance it looks like chrome and thats all most gamers care about.

"But most people think it looks great because wrong reflections are better than no reflections. I showed people at the office the Unreal Paris demo and they were blown away. Tons of places where the reflections are breaking down or just flat out wrong."




"But from a distance it looks like chrome and thats all most gamers care about."

Physics provide one great BASIS for beautiful imagery, but that's it. Just look at art and pictures brought to life by people from scratch. They don't calculate the fresnel term in their head when they draw those images. The lighting in them is 'wrong' but the end result can be quite beautiful. Photorealism is merely one stylistic choice among many.

I never saw the flaws of realtime rendering in games until I started to do graphics programming myself. Now, unfortunately, I do see the static image jitters of TAA, cascade seams, fading SSR, flickering half-res SSAO, wrong static cubemaps... you name it. But the regular gamer does not because he is too busy caring about the actual game. They also could not care less if you use hacks / fake effects. The final result is what counts. NOT how it was achieved. It's just that it it's in engineers' nature to be obsessed with correctness, even when dealing with creative and subjective things. I'm guilty of this myself.

Post a Comment