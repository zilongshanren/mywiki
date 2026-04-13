---
title: Raytracing tidbits
url: https://interplayoflight.wordpress.com/2021/07/10/raytracing-tidbits/
author: Kostas Anagnostou
published: '2021-07-10'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Over the past few months I did some smaller scale raytracing experiments, which I shared on Twitter but never documented properly. I am collecting them all in this post for ease of access.

**On ray divergence**

Raytracing has the potential to introduce large divergence in a wave. Imagine a thread with a shadow ray shooting towards the light hitting a triangle and “stopping” traversal while the one next to it missing it and having to continue traversal of the BVH. Even a single long ray/thread has the potential to hold up the rest of the threads (63 on GCN and 31 on NVidia/RDNA) and prevent the whole wave from retiring and freeing up resources.

To visualise this we output total steps through the BVH the rays do and calculate the step count variance in a 8×8 tile (assuming 64 thread waves) in the case of shadow raytracing (one ray per pixel, hard shadows). A black/dark tile signify a wave with small divergence meaning that rays do approximately the same number of steps, while a brighter red tile means that number of steps vary a lot withing its threads. In the case of shadow raytracing there are tiles (waves) with a large divergence mainly on the geometric edges (which makes sense as the the tile/wave may cover areas with different orientation).

![](../../assets/ccaa7b0b67aa4f4f.png)


![](../../assets/ccaa7b0b67aa4f4f.png)

Divergence when raytracing GI (one ray per pixel) on the other hand is much worse. In this case not only are the rays selected randomly over the hemisphere, the shader may also choose to additionally cast shadow rays for hitpoints that face the light.

![](../../assets/bc1feb26f1cb799b.png)


![](../../assets/bc1feb26f1cb799b.png)

One way to improve this is to limit BVH traversal to a single ray type, for example trace rays and store the hitpoints and then run another pass to trace shadow rays for those hitpoints and calculate lighting. This can reduce divergence in a wave as showcased in the following image in which we only traverse rays and store the hitpoints for a subsequent pass (we notice the reduction in divergence as a general reduction in image intensity).

![](../../assets/41563c24465b91fa.png)


![](../../assets/41563c24465b91fa.png)

Bear in mind that splitting a complex raytracing pass is not always easy, especially when transparent objects are involved.

Another way to reduce thread divergence is to make the thread count in a wave smaller. For example 32 thread waves can reduce the variance in a wave, reducing the probability of having a few long rays/threads in the run that hold up rest. This image showcases RTGI with 64 thread waves and a large divergence as we discussed:

![](../../assets/4a89574c44405003.png)


![](../../assets/4a89574c44405003.png)

while for this one we reduce the wave/tile size to 32 threads. The overall divergence goes down (expressed by reduced image intensity and more dark tiles)

![](../../assets/66c17505856149d5.png)


![](../../assets/66c17505856149d5.png)

![](../../assets/6a34487b937d342e.png)


![](../../assets/6a34487b937d342e.png)

![](../../assets/5da0180f814770c0.png)


![](../../assets/5da0180f814770c0.png)

**On ray coherence**

When raytracing coherent rays (i.e. rays that point mostly towards the same direction as in the case of shadows) it’s likely that adjacent ones will hit the same triangle. This experiment demonstrates this for 2×2 pixel quads, casting one shadow ray and caching the triangle to test the other 3 pixels against. If the adjacent pixel rays intersect that triangle as well then traversal can stop early. Of course how efficiency this is varies depending on the mesh (triangle orientation with respect to ray, size etc). Also ray divergence and “long” rays that hold up the wave, discussed above, can become an issue in this case as well.

![](../../assets/64246f455640ea2c.jpg)


![](../../assets/64246f455640ea2c.jpg)

**On hybrid Global Illumination**

Inspired by Metro: Exodus this was a quick experiment with hybrid RTGI and how to reuse gbuffer data and light buffer. The following image showcases zbuffer collisions when raymarching in screen space with rays generated for raytraced GI. The brighter the pixels the higher the likelihood to find a collision in the zbuffer without traversing the BVH.

![](../../assets/99376d4c4afb1069.png)


![](../../assets/99376d4c4afb1069.png)

In these cases we can avoid traversing the BVH altogether and can calculate indirect contributions by lighting the hit points using material info from the gbuffer (calculating lighting again at this position or using lighting already in the light buffer). This image showcases indirect lighting from z-buffer collisions only.

![](../../assets/cbf180253d578d3f.png)


![](../../assets/cbf180253d578d3f.png)

![](../../assets/658a6a178133c290.png)


![](../../assets/658a6a178133c290.png)

Next we denoise the GI and composite all lighting with material albedo: top image is with z-buffer collisions only, bottom fully raytraced. No sky contribution in both cases to make the comparison fairer (as screen space tracing can’t see the sky). The results are fairly close.

![](../../assets/c5756952c6239159.png)


![](../../assets/c5756952c6239159.png)

![](../../assets/534c67bb8ad9305a.png)


![](../../assets/534c67bb8ad9305a.png)

Screenspace raymarching alone is not enough to give full indirect lighting but it can be the base for a hybrid system. The final image is fully tracing only rays that don’t manage to find a collision in the z-buffer. Although done in one complex pass (which can make the thread divergence we discussed earlier pretty bad), hybrid is still about 20% faster.

![](../../assets/8c208d1044e6e0a5.png)


![](../../assets/8c208d1044e6e0a5.png)

**On shadowmapped GI**

When raytracing GI it’s worth considering using the shadowmap to occlude direct lighting at a hit point instead of casting a shadow ray. In this quick test it cut RTGI time by 25% with no visual impact in that scene. The first image has no shadows on the direct light that reaches a hit point.

![](../../assets/bb237f171b01bf04.png)


![](../../assets/bb237f171b01bf04.png)

This one traces shadow rays at hit points.

![](../../assets/505acbcf8d013058.png)


![](../../assets/505acbcf8d013058.png)

And the final one uses the shadowmap to occlude light at hitpoints.

![](../../assets/da4c5ad2e678a100.png)


![](../../assets/da4c5ad2e678a100.png)

Visually the images are very close. It is worth bearing in mind that shadowmaps are usually produced using cascades/bounding volumes fit tightly to the camera frustum, which means that they may not cover offscreen areas.

**On second bounce indirect lighting**

When raytracing indirect lighting with one bounce we often use direct lighting only to illuminate the hitpoints and this will be a source of noise when the hitpoint is shadowed with respect to the light (raytracing @ 0.25 rays per pixel w/blue noise to distribute rays) .

![](../../assets/65d6457a1096128a.png)


![](../../assets/65d6457a1096128a.png)

![](../../assets/d5f527a5f24abbb6.png)


![](../../assets/d5f527a5f24abbb6.png)

Introducing second bounce indirect lighting, i.e. cast another ray from the hitpoint to a random direction and calculate indirect lighting, can make the previously shadowed hitpoint contribute more lighting. The image showcases second bounce lighting only @ 0.25 rays per pixel with animated noise and a history buffer to accumulate indirect lighting.

![](../../assets/fa2998e2d51b0d36.png)


![](../../assets/fa2998e2d51b0d36.png)

The impact of second bounce lighting, although noticeable (you can clearly see it in the lion head area for example), it appears small when combined with first bounce indirect lighting. Top screenshot showcases first bounce only, bottom first and second bounce combined, same raytracing configuration.

![](../../assets/31c96a506aae8411.png)


![](../../assets/31c96a506aae8411.png)

![](../../assets/cea0a7511f13b50a.png)


![](../../assets/cea0a7511f13b50a.png)

This is particularly true when direct lighting and textures are added to the scene, making the substantial extra cost to calculate second bounce lighting hard to justify. Again, top image is first bounce indirect, bottom image is first plus second ray indirect lighting.

![](../../assets/f981460ab039fb6f.png)


![](../../assets/f981460ab039fb6f.png)

![](../../assets/80d4aa84febb7bd8.png)


![](../../assets/80d4aa84febb7bd8.png)

Taking into account second bounce indirect lighting can make a difference though in enclosed spaces that light doesn’t reach easily. Top image showcases one bounce, bottom image two bounce indirect lighting.

![](../../assets/c3b99a3c15369e00.png)


![](../../assets/c3b99a3c15369e00.png)

![](../../assets/48b414befd98bd69.png)


![](../../assets/48b414befd98bd69.png)

**On using** **a** **reverse depth buffer**

If you need yet another reason to adopt a reverse depth buffer: in hybrid raytracing scenarios where we reconstruct the ray origin from the depth buffer, the increased depth precision afforded by the reverse z configuration, which in turn improves world position precision, while not removing them entirely, it helps reduce self-shadow artifacts (false ray hits). Top image showcase normal z direction and the bottom one reverse z direction.

![](../../assets/9bacd185bf56556e.jpg)


![](../../assets/9bacd185bf56556e.jpg)

![](../../assets/278f4b91ca7615ce.jpg)


![](../../assets/278f4b91ca7615ce.jpg)

The improvement is noticeable especially in distant areas where normal z precision drops significantly. No offsetting of the ray origin is used to improve self shadowing artifacts in both cases.

Thank you so much for posting this! Super useful info here.

I really think the issue of divergence is something that GPU architectures will need to address, striking a careful balance between efficiency and programmability. My feeling is that they need to let us chop up work into smaller units that can be clustered into coherent waves and then heavily pipelined wrt each other. So in your example of hybrid ray tracing, the programming model should let you specify the two types of processing (screen space ray march VS BVH ray march) and the data that passes between them, such that the GPU knows it can (and probably should) execute them separately, without complicating your code.