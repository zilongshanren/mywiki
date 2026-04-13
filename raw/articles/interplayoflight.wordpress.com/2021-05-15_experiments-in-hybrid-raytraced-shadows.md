---
title: Experiments in Hybrid Raytraced Shadows
url: https://interplayoflight.wordpress.com/2021/05/15/experiments-in-hybrid-raytraced-shadows/
author: Kostas Anagnostou
published: '2021-05-15'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A few weeks ago I implemented a simple shadowmapping solution in the toy engine to try as a [replacement for shadow rays during GI raytracing](https://twitter.com/KostasAAA/status/1380577649953808395?s=20). Having the two solutions (shadomapping and RT shadows) side by side, along with some offline discussions I had, made me start thinking about how it would be possible to combine the two into a hybrid raytraced shadowed solution, like I did with [hybrid raytraced reflections](https://interplayoflight.wordpress.com/2019/09/07/hybrid-screen-space-reflections/) in the past. This blog post documents a few quick experiments I did to explore this issue a bit.

To begin with, this is what full resolution raytraced shadows look like in the toy engine:

![](../../assets/92687ed39799f7c3.png)


![](../../assets/92687ed39799f7c3.png)

![](../../assets/4e4219e84215ca9e.png)


![](../../assets/4e4219e84215ca9e.png)

Comparing the two images, it looks like the biggest divergence appears on the shadow to light transitions, the shadowmap managing to capture the bulk of the sun occlusion in other areas (mostly) successfully. It feels like focusing on the transition areas, identifying and raytracing only those and using the shadowmap for the rest of the pixels should give some good speedups and overall shadow quality improvements, compared to shadowmap shadows alone.

Edges are a frequent source of aliasing and isolating and raytracing the edges only is not a new idea, it has been used successfully for [hybrid image antialiasing](https://developer.nvidia.com/siggraph/2019/video/sig937-vid) in the past. The problem with shadowmap shadows is that, unlike geometric edges in the main image, which mainly depend on the image resolution and are of predictable size, shadow “edges” depend on the direction of the light in relation to the surface, which causes shadowmap texels to correspond to a varying number of surface pixels. This is apparent in the above image, the shadows on the floor appear high resolution because the light is almost perpendicular to the surface and there is a good shadowmap texel to image pixel mapping. Shadows on the walls and curtains appear very aliased because, due to the direction of the light (almost parallel to the surface), a shadowmap texel can map to a large number of image pixels. This indicates that the size of shadow “edge” varies in the image. This also indicates that naive edge detection in the image to isolate the shadow edges probably won’t be enough.

For the first experiment I rendered the shadows to a screenspace rendertarget i.e. I created a [shadowmask ](https://www.realtimeshadows.com/sites/default/files/Playing%20with%20Real-Time%20Shadows_0.pdf)where a value of 0 means pixel is in shadow, and a value of 1 means pixel not in shadow. This is a nice technique to trade some shader complexity with memory bandwidth and also allows us to process the shadows further in screenspace, like in this case. Running a 3×3 [Sobel filter](https://en.wikipedia.org/wiki/Sobel_operator) on the shadowmask to highlight the edges:

![](../../assets/cf26cafde6a50349.png)


![](../../assets/cf26cafde6a50349.png)

![](../../assets/8fbfa5bcf760a6ee.png)


![](../../assets/8fbfa5bcf760a6ee.png)

This confirm what we discussed above, screen space edge detection seems to work well on the floor shadows but not on the wall, vertical, shadows in which case the actual “edge” is much wider, due to the projection. Also, the Sobel filter will need a threshold that will dictate what we consider an edge and that will be scene dependent. At any rate, we pay an additional 1.2ms for the shadowmask edge detection and the cost of raytracing drops to 13.2ms.

It looks like it will take some effort to extract an accurate, variable width shadow edge using the typical edge methods alone. What if instead of using a filter based on differentiation we just blurred the shadowmask using a 5×5 Gaussian filter and raytraced pixels with values more than 0 and less than 1 (meaning that they fall on the edge of the shadows).

![](../../assets/ce358c7407de23e0.png)


![](../../assets/ce358c7407de23e0.png)

Blurring the shadowmask creates a wider “edge” which captures the aliased area caused by the shadowmap projection, especially on the walls, better. Raytracing only the pixels highlighted we get the following result.

![](../../assets/01d77ae6417948a5.png)


![](../../assets/01d77ae6417948a5.png)

Shadow quality has improved markedly but, due to the increased number of pixels, the raytracing cost increased to 26.8 ms, plus an additional 2.6 ms for the blurring pass and still, the shadows are not glitch free. The quality of the shadows depend on the size of the Gaussian filter, which is another parameter to tune and also the filter affects all areas the same, both the floor that doesn’t need very wide edges in this instance and the walls that do. Clearly, filtering the shadows in screen space, i.e. after we have projected the shadowmap and done the depth test, is not ideal. What if we moved the filtering in light space before the projection?

Let’s begin by running the Sobel filter on the shadowmap directly, keeping shadowmap texels that fall above a threshold, in an attempt to detect depth discontinuities:

![](../../assets/1d0cc914951897f1.png)


![](../../assets/1d0cc914951897f1.png)

Then, we can project this texture from the point of view of the light to mark the areas with shadow to light transitions. One thing to pay attention to is that naive projection will be wrong if we don’t take the shadowmap depths into account, as the edges will appear to leak through to surfaces that the light can’t actually see. To fix that we need to calculate min and max depths for all the shadowmap texels touched by the Sobel filter kernel into a separate texture and use them when projecting the edges texture (if the receiving surface depth, from the point of view of the light, is not between the min and max shadowmap depth values then it won’t receive the projected texture). This technique is described in [this paper](https://developer.amd.com/wordpress/media/2012/10/Isidoro-ShadowMapping.pdf).

So the depth-aware shadowmap edge projection highlights the following shadow edge areas:

![](../../assets/b80d5a1f7e9163af.png)


![](../../assets/b80d5a1f7e9163af.png)

This is interesting, now the shadow edge “width” varies based on the relative light direction, the floor receiving much thinner edges than the walls.

Raytracing only the highlighted areas gives us this image:

![](../../assets/4cc29c392deb9e53.png)


![](../../assets/4cc29c392deb9e53.png)

The shadow quality has improved in areas that the screen space shadowmask processing couldn’t and also the quality is more consistent. The technique seems to struggle though in areas with high depth complexity, from the light’s point of view, like under small ledges. The raytracing cost is now 16.5 ms, with an additional overhead of 1.2 ms for the shadowmap edge detection, which is good for hybrid shadows of that quality. We still need to consider the Sobel filtering threshold though which isolates the shadowmap edges, which is scene specific.

What if we used something that can give us shadow edges from the point of view of the light which won’t need thresholds, like Percentage Closer Filtering? Like in the Gaussian filtering experiment above we can keep as in transition areas pixels that have values larger than zero and smaller than one.

Trying a 3×3 PCF kernel, highlights the following areas as transitions.

![](../../assets/8d105a724145dfe4.png)


![](../../assets/8d105a724145dfe4.png)

This is promising, the shadow edge “width” still varies based on the relative light/surface orientation.

Raytracing the highlighted pixels only produces this result:

![](../../assets/d86a75e0369fa01f.png)


![](../../assets/d86a75e0369fa01f.png)

While I was writing this blog post AMD published a sample that implements [hybrid raytracing shadows](https://gpuopen.com/learn/hybrid-shadows/) so I was curious to try this technique as well. In spirit it is similar to the shadomap processing techniques discussed about, it projects each pixel to light space and runs a Poisson filter to sample the covered shadowmap area and calculate the min and max shadowmap depths. Then it rejects pixels where the light-space depth is less than the minimum or larger than the max shadowmap depth (as fully lit or fully shadowed) and only keeps for raytracing pixels that fall in-between. The sample also implements some other nice optimisations worth studying.

A quick and dirty implementation of this idea, using a 12 sample Poisson filter, highlights the following areas as shadow transitions:

![](../../assets/622ce400c16ed349.png)


![](../../assets/622ce400c16ed349.png)

Raytracing those areas we get the following image:

![](../../assets/f6053e42fa17e412.png)


![](../../assets/f6053e42fa17e412.png)

The shadows quality is similar to the other shadowmap processing techniques, along with the difficulty to improve the quality under ledges. It seems measurably cheaper though at 13.2 ms.

So hybrid raytraced shadows is a promising way to improve the quality of shadowmap shadows. It has some issues with achieving consistent shadow quality across the image and there will be edge cases to be handled depending on the scene. The final result will depend a lot on the quality of the shadow map, engines typically implement cascading shadowmap systems to improve shadowmap texel distribution already, so they may start from a better place. Also, it is likely that area shadows will be able to hide subtle artifacts better like in the following case.

Fully raytraced area shadows:

![](../../assets/f2c5a1299361d2b5.png)


![](../../assets/f2c5a1299361d2b5.png)

Hybrid area shadows:

![](../../assets/8c23a35dc1492ba6.png)


![](../../assets/8c23a35dc1492ba6.png)

This drops the raytracing cost from 96.1ms to 15.2ms (using the Poisson filtered method) for area shadows, which is not bad at all.

Great blog, thanks! So it’s essentially running PCSS penumbra check to create shadow mask for raytracing if I understand correctly. One more reason to still keep shadow maps code around for a while. For this and volumetrics rendering.

remember the valve font rendering technique, where the alpha is converted to a distance field, and the text is rendered with high quality. why not generate a distance field from the lightmap and render the shadow like the font? im sure softness of shadows can be encoded somehow with a map too.