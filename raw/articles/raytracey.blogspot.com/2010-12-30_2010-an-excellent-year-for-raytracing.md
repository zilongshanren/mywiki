---
title: 2010, an excellent year for raytracing!
url: http://raytracey.blogspot.com/2010/12/2010-excellent-year-for-raytracing.html
author: Sam Lapere
published: '2010-12-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

What an exciting year this has been, for raytracing at least. There has been a huge buzz around accelerated ray tracing and unbiased rendering, in which the GPU has played a pivotal role. A little overview:


- Octane Render is publicly announced. A demo is released which lets many people experience high quality unbiased GPU rendering for the first time. Unparallelled quality and amazing rendertimes on even a low-end GTX8800, catch many by surprise.


- Arion, the GPU sibling of Random Control's Fryrender, is announced shortly after Octane. Touts hybrid CPU+GPU unbiased rendering as a distinguishing feature. The product eventually releases at a prohibitively expensive price (1000€ for 1 multi-GPU license)


- Luxrender's OpenCL-based GPU renderer SmallLuxGPU integrates stochastic progressive photon mapping, an unbiased rendering method which excels at caustic-heavy scenes


- Brigade path tracer is announced, a hybrid (CPU+GPU) real-time path tracer aimed at games. Very optimized, very fast, user-defined quality, first path tracer with support for dynamic objects. GI quality greatly surpasses virtual point light/instant radiosity based methods and even photon mapping, can theoretically handle all types of BRDF, is artefact free (except for noise) and nearly real-time. No screen-space limitations. The biggest advantage over other methods is progressive rendering which instantly gives a good idea of the final converged image (some filtering and LOD scheme,


- release of Nvidia Fermi GPU: caches and other enhancements (e.g. concurrent kernel execution) give ray tracing tasks an enormous boost, up to 3.5x faster in scenes with many incoherent rays compared to the previous architecture. Design Garage, an excellent tech demo featuring GPU path tracing is released alongside the cards


- Siggraph 2010 puts heavy focus on GPU rendering


- GTC 2010: Nvidia organizes a whole bunch of GPU ray tracing sessions covering OptiX, iray, etc.


- John Carmack re-expresses interest in real-time ray tracing as an alternative rendering method for next-generation games (besides sparse voxel octrees). He even started twittering about his GPU ray tracing experiments in OpenCL:


- GPU rendering gets more and more criticized by the CPU rendering crowd (Luxology, Next Limit, their userbase, ...) feeling the threat of decreased revenue


- release of mental ray's iray


- release of V-Ray RT GPU, the product that started the GPU rendering revolution


- Caustic Graphics is bought by Imagination Technologies, the maker of PowerVR GPU. A surprising and potentially successful move for both companies. Hardware accelerated real-time path tracing at very high sampling rates (higher than on Nvidia Fermi) could become possible. PowerVR GPUs are integrated in Apple TV, iPad, iPhone and iPod Touch, so this is certainly something to keep an eye on in 2011. Caustic doesn't disappoint when it comes to hype and drama :)


- one of my most burning questions since the revelation of path tracing on GPU, "is the GPU capable of more sophisticated and efficient rendering algorithms than brute force path tracing?" got answered just a few weeks ago, thanks to Dietger van Antwerpen and his superb work on GPU-based Metropolis light transport and energy redistribution path tracing.


All in all, 2010 was great for me and delivered a lot to write about. Hopefully 2011 will be at least equally exciting. Some wild speculation of what might happen:


- Metropolis light transport starts to appear in commercial GPU rendering software (very high probability for Octane)

- more news about Intel's Knight's Corner/Ferry with maybe some perfomance numbers (unlikely)

- Nvidia launches Kepler at the end of 2011 which offers 3x path tracing performance of Fermi (to good to be true?)

- PowerVR GPU maker and Caustic Graphics bring hardware accelerated real-time path tracing to a mass audience through Apple mobile products (would be great)

- Luxology and Maxwell Render reluctantly embrace GPU rendering (LOL)

- finally a glimpse of OTOY's real-time path tracing (fingers crossed)

- Brigade path tracer gains exposure and awareness with the release of the first path traced game in history (highly possible)

- ...


Joy!


- Octane Render is publicly announced. A demo is released which lets many people experience high quality unbiased GPU rendering for the first time. Unparallelled quality and amazing rendertimes on even a low-end GTX8800, catch many by surprise.

- Arion, the GPU sibling of Random Control's Fryrender, is announced shortly after Octane. Touts hybrid CPU+GPU unbiased rendering as a distinguishing feature. The product eventually releases at a prohibitively expensive price (1000€ for 1 multi-GPU license)

- Luxrender's OpenCL-based GPU renderer SmallLuxGPU integrates stochastic progressive photon mapping, an unbiased rendering method which excels at caustic-heavy scenes

- Brigade path tracer is announced, a hybrid (CPU+GPU) real-time path tracer aimed at games. Very optimized, very fast, user-defined quality, first path tracer with support for dynamic objects. GI quality greatly surpasses virtual point light/instant radiosity based methods and even photon mapping, can theoretically handle all types of BRDF, is artefact free (except for noise) and nearly real-time. No screen-space limitations. The biggest advantage over other methods is progressive rendering which instantly gives a good idea of the final converged image (some filtering and LOD scheme,

[similar to VoxLOD](http://voxelium.wordpress.com/2010/07/25/shadows-and-global-illumination/), could produce very high quality results in real-time). Very promising, it could be the best option for high-quality dynamic global illumination in games in 2 to 3 years.- release of Nvidia Fermi GPU: caches and other enhancements (e.g. concurrent kernel execution) give ray tracing tasks an enormous boost, up to 3.5x faster in scenes with many incoherent rays compared to the previous architecture. Design Garage, an excellent tech demo featuring GPU path tracing is released alongside the cards

- Siggraph 2010 puts heavy focus on GPU rendering

- GTC 2010: Nvidia organizes a whole bunch of GPU ray tracing sessions covering OptiX, iray, etc.

- John Carmack re-expresses interest in real-time ray tracing as an alternative rendering method for next-generation games (besides sparse voxel octrees). He even started twittering about his GPU ray tracing experiments in OpenCL:

[http://raytracey.blogspot.com/2010/08/is-carmack-working-on-ray-tracing-based.html](http://raytracey.blogspot.com/2010/08/is-carmack-working-on-ray-tracing-based.html)- GPU rendering gets more and more criticized by the CPU rendering crowd (Luxology, Next Limit, their userbase, ...) feeling the threat of decreased revenue

- release of mental ray's iray

- release of V-Ray RT GPU, the product that started the GPU rendering revolution

- Caustic Graphics is bought by Imagination Technologies, the maker of PowerVR GPU. A surprising and potentially successful move for both companies. Hardware accelerated real-time path tracing at very high sampling rates (higher than on Nvidia Fermi) could become possible. PowerVR GPUs are integrated in Apple TV, iPad, iPhone and iPod Touch, so this is certainly something to keep an eye on in 2011. Caustic doesn't disappoint when it comes to hype and drama :)

- one of my most burning questions since the revelation of path tracing on GPU, "is the GPU capable of more sophisticated and efficient rendering algorithms than brute force path tracing?" got answered just a few weeks ago, thanks to Dietger van Antwerpen and his superb work on GPU-based Metropolis light transport and energy redistribution path tracing.

All in all, 2010 was great for me and delivered a lot to write about. Hopefully 2011 will be at least equally exciting. Some wild speculation of what might happen:

- Metropolis light transport starts to appear in commercial GPU rendering software (very high probability for Octane)

- more news about Intel's Knight's Corner/Ferry with maybe some perfomance numbers (unlikely)

- Nvidia launches Kepler at the end of 2011 which offers 3x path tracing performance of Fermi (to good to be true?)

- PowerVR GPU maker and Caustic Graphics bring hardware accelerated real-time path tracing to a mass audience through Apple mobile products (would be great)

- Luxology and Maxwell Render reluctantly embrace GPU rendering (LOL)

- finally a glimpse of OTOY's real-time path tracing (fingers crossed)

- Brigade path tracer gains exposure and awareness with the release of the first path traced game in history (highly possible)

- ...

Joy!

## 2 comments:

I was surprised you didn't mentioned ratGPU ( www.ratgpu.com )

Well, there is a lot that I did not mention. I've seen ratGPU, it's cool because it's free, but it's not as feature rich as Octane for example. I especially listed the things that impressed me most in 2010 and the Brigade path tracer and the MLT on GPU implementation are at the top of that list: state-of-the-art, groundbreaking and pioneering stuff, going against common sense and popular belief, it's what I like most. It's also for these reasons that I like OTOY and Octane so much.

Post a Comment