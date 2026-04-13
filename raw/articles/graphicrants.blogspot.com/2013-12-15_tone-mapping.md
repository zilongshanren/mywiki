---
title: Tone mapping
url: http://graphicrants.blogspot.com/2013/12/tone-mapping.html
author: Brian Karis
published: '2013-12-15'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The first happens when one tries to encode an HDR color using an encoding that has a limited range, for instance RGBM. Values outside the range still need to be handled gracefully, ie not clipped.

The second happens when an HDR signal is under sampled. One very bright sample can completely dominate the result. In path tracing these are commonly called fireflies.

In both cases the obvious solution is to reduce the range. This sounds exactly like tonemapping so break out those tone mapping operators, right? Well yes and no. Common tone mapping operators work on color channels individually. This has the downside of desaturating the colors which can look really bad if later operations attenuate the values, for instance reflections, glare, or DOF.

Instead I use a function that modifies only the luminance of the color. The simplest of which is this:

$$
T(color) = \frac{color}{ 1 + \frac{luma}{range} }
$$
Where $T$ is the tone mapping function, $color$ is the color to be tone mapped, $luma$ is the luminance of $color$, and $range$ is the range that I wish to tone map into. If the encoding must fit RGB individually in range then $luma$ is the max RGB component.

Inverting this operation is just as easy. $$ T_{inverse}(color) = \frac{color}{ 1 - \frac{luma}{range} } $$

This operation, when used to reduce fireflies, can also be thought of as a weighting function for each sample: $$ weight = \frac{1}{ 1 + luma } $$

For a weighted average, sum all samples and divide by the summed weights. The result will be the same as if the samples were tone mapped using $T$ with $range$ of 1, averaged, then inverse tone mapped using $T_{inverse}$.

If a more expensive function is acceptable then keeping more of the color range linear is best. To do this use the functions below where 0 to $a$ is linear and $a$ to $b$ is tone mapped. $$ T(color) = \left\{ \begin{array}{l l} color & \quad \text{if $luma \leq a$}\\ \frac{color}{luma} \left( \frac{ a^2 - b*luma }{ 2a - b - luma } \right) & \quad \text{if $luma \gt a$} \end{array} \right. $$ $$ T_{inverse}(color) = \left\{ \begin{array}{l l} color & \quad \text{if $luma \leq a$}\\ \frac{color}{luma} \left( \frac{ a^2 - ( 2a - b )luma }{ b - luma } \right) & \quad \text{if $luma \gt a$} \end{array} \right. $$

These are same as the first two functions if $a=0$ and $b=range$.

I have used these methods for lightmap encoding, environment map encoding, fixed point bloom, screen space reflections, path tracing, and more.

## 5 comments:

Cool. Do you use a version of this technique during the importance sampling stage of the IBL pre-compute you outlined in this years Unreal Shader Model Notes?


If so, I'm wondering if it would be useful to introduce roughness into the weight. Higher roughness values being more susceptible to "firefly" artifacts. Where as it might be desirable to maintain very hot samples for accuracy in low roughness values that are less susceptible to fireflies.

I did not. In that case the accuracy outweighed the necessity for speed. The env map are prefiltered (mip-mapped) before importance sampling, similar to this: http://http.developer.nvidia.com/GPUGems3/gpugems3_ch20.html. Beyond that just take as many samples as possible. This was only done in editor so it only needed to be fast enough to be interactive.



Aliasing wasn't non-existent but it only showed up in artificial cases, not real scenes.

I did use this to handle out of range values when storing the env maps with RGBM encoding for some specific low end platforms.

Thanks, that makes sense. Incidentally, interesting that you mention using RGBM for low end platforms. Does that mean you've found situations where floating point IBLs, when performant, give you noticeable quality gains?

Yes, definitely. RGBM doesn't filter correctly. Sometimes the error isn't visible. High mips of an environment map it definitely is.


The best choice is using BC6H. That isn't supported on all platforms unfortunately.

Right! That part totally slipped my mind. I've encountered the incorrect blending issue as well, and have relied on detail normal maps, and avoided infinite geometric representations of environments to mitigate the problem's visibility.

When you first mentioned it I imagined it was a matter of preserving a greater range of intensities.

Post a Comment