---
title: Notes on occlusion and directionality in image based lighting.
url: https://interplayoflight.wordpress.com/2021/12/28/notes-on-occlusion-and-directionality-in-image-based-lighting/
author: Kostas Anagnostou
published: '2021-12-28'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

*Update: I wrote a follow-up post with some implementation details and some more resources here.*

Image based lighting (IBL), in which we use a cubemap to represent indirect radiance from an environment, is an important component of scene lighting. Environment lighting is not always uniform and has often a strong directional component (think sunset or sunrise or a room lit by a window) and that indirect light should interact with the scene correctly, with directional occlusion. I spent some time exploring the directionality and occlusion aspects of IBL for diffuse lighting, with a sprinkle of raytracing, and made some notes (and pretty pictures).

To begin with, I tried lighting a simple scene with diffuse indirect lighting coming only from a cubemap. In all cases I preconvolved the cubemap casting rays over the hemisphere centred around the normal to calculate the [irradiance ](https://google.github.io/filament/Filament.html)and applied it to the models sampling the cubemap using the world space normal direction.

I won’t delve into the maths much, there are great resources out there for that, like the one I included above. To get an intuition of what the above equation means though, we integrate (sum) all the light rays **L** that arrive over the hemisphere **Ω** centred around the normal **n**. Because not all light rays are equal and those that are more parallel to the normal contribute more energy to the surface, we also weigh each ray’s radiance (light along a given ray direction) by the cosine of its angle relative to the normal (this is what **n.l** dot product is about). To create what we call an “irradiance probe”, used frequently for diffuse indirect lighting in games, we calculate that integral for many different normal directions and store the values in a cubemap (this is not the only way to represent an irradiance probe, more on that later). That irradiance probe knows nothing about the surface it will be applied to (eg its material or its shape in general).

The following two images showcase what the original and an irradiance cubemap look like ([source](https://google.github.io/filament/Filament.html)).

![](../../assets/241c69e0ca803478.png)


![](../../assets/241c69e0ca803478.png)

![](../../assets/e79b765490acf682.png)


![](../../assets/e79b765490acf682.png)

Each pixel is the irradiance over the hemisphere centered on the normal (direction) we use to sample that cubemap and supports all directions from a specific point in space. It is worth mentioning that having the irradiance at hand, we can calculate the final outgoing radiance of a surface simply as **(albedo/π) * E(n)**.

This is what applying various preconvolved irradiance cubemaps to my simple scene looks like (no direct light in the scene at all).

![](../../assets/12a6592c3341f13d.png)


![](../../assets/12a6592c3341f13d.png)

![](../../assets/d3a019ca73e7e89b.png)


![](../../assets/d3a019ca73e7e89b.png)

![](../../assets/cc90c75709047524.png)


![](../../assets/cc90c75709047524.png)

![](../../assets/c90693bfe026ee9f.png)


![](../../assets/c90693bfe026ee9f.png)

One thing that becomes immediately obvious is that, like I mentioned above, the irradiance cubemap knows nothing about the surface it will be applied to. This is manifested as a total lack of light occlusion or shadows of any kind. Another thing is that the irradiance is really, really coarse. To notice a change in the indirect lighting over the surface there needs be some strong lighting directionality in the cubemap, like a sunset or sunrise, a window in dark room or, in general, a bright light source from some direction. Cubemaps with overcast skies, or even partly clouded ones register little in the irradiance producing uniform results (like in the top right screenshot).

Lighting with irradiance make objects feel part of the scene but it is clear that occlusion is also important to understand the shape of the models, spatial relationship between models as well as to ground them better. Next step was to determine what is the best case scenario in terms of irradiance occlusion, as a reference, and to achieve this the best way is to use raytracing. In the screenshots below I am tracing one ray per pixel at native resolution and the ray hit points do not contribute any lighting. To reduce noise I am averaging the results across frames instead of using spatial and temporal antialiasing methods.

![](../../assets/b276d9e541162221.png)


![](../../assets/b276d9e541162221.png)

![](../../assets/e6d6b283b11d1461.png)


![](../../assets/e6d6b283b11d1461.png)

![](../../assets/f69808397944aeea.png)


![](../../assets/f69808397944aeea.png)

![](../../assets/d4f51fe9de6cb3f6.png)


![](../../assets/d4f51fe9de6cb3f6.png)

While raytracing, I traverse the BVH tree of the model calculating self-occlusion, resorting to sampling the (original, unconvolved) environment cubemap when a ray misses. This is effectively similar to what we did to calculate the irradiance, i.e. integrate radiance along rays over a hemisphere, only this time for each ray **l** we can also calculate visibility **V** (of the cubemap in this case).

The BRDF **f(l,u)** is the simple **albedo/π** one used with Lambert diffuse. The result is great and the model now feels like it is interacting properly with the scene illumination with the expected directionality in the occlusion.

Raytracing produces correct occlusion but is quite expensive. What will occlusion look like with a cheaper screen space ambient occlusion technique? To determine that I did a basic implementation of the [Ground Truth Ambient Occlusion](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW%20VERSION_COLOR.pdf) (GTAO) method which extends the [Horizon Based Ambient Occlusion](https://developer.download.nvidia.com/presentations/2008/SIGGRAPH/HBAO_SIG08b.pdf) one to account for multiscattering in the near field and to add directionality. This diagram from the original paper summarises the core of the technique.

The technique operates in view space using a depth buffer and the normal buffer (or reconstructs the face normals from depth if not available). For every view space position, the corresponding hemisphere is “sliced” into a number of slices (in red) and for each slice the horizon angles **θ 1** and

**θ**are calculated using the view vector

2**ω**as a reference. Those 2 angles express how “open” or “closed” the area around the surface position is. By considering many such slices through the hemisphere, and calculating the corresponding

ο**θ**and

1**θ**horizon angles every time, we can calculate the occlusion for this view space position. The paper goes further to calculate interreflections but I didn’t go as far this time around. If you are looking for more featured GTAO implementation it is worth studying

2[this one](https://github.com/GameTechDev/XeGTAO).

This is what irradiance modulated by the occlusion calculated by this method looks like (1 metre radius).

![](../../assets/db985b25aafb9881.png)


![](../../assets/db985b25aafb9881.png)

![](../../assets/ee639b40d9f97841.png)


![](../../assets/ee639b40d9f97841.png)

![](../../assets/e6dc8c3e82af1b5e.png)


![](../../assets/e6dc8c3e82af1b5e.png)

![](../../assets/6b6eb74bffc78978.png)


![](../../assets/6b6eb74bffc78978.png)

The result is good in general, but if we compare it with the raytraced images the first thing that pops out is the total lack of directionality of GTAO in environments with a lot of light directionality for example (left raytraced, right GTAO):

![](../../assets/345e26359871ebf2.png)

![](../../assets/25b619f9bc2cae41.png)

In more uniform lighting environments the difference in directionality is not as pronounced (left raytraced, right GTAO):

![](../../assets/5347740986ac3790.png)

![](../../assets/ed3a5690324ef4ec.png)

The difference is AO intensity is due to wrong thickness setup in the GTAO case.

The lack of directionality is explained by the fact that, in contrast to the raytraced case, with GTAO (and most SSAO approaches) we have [separated occlusion from irradiance calculations](https://google.github.io/filament/Filament.html#lighting/occlusion/diffuseocclusion).

This means that occlusion is averaged over the hemisphere, losing all directionality by the time it is multiplied by the irradiance.

A common approach to restore some directionality in IBL is to calculate and use the surface bent normals to sample the irradiance map. [A bent normal](https://www.researchgate.net/publication/220839265_Bent_Normals_and_Cones_in_Screen-space) is effectively the average of all the unoccluded rays from a specific surface point

While using a normal to sample the irradiance cubemap will not take into account the surface point neighbourhood, and potential occlusion, the bent normal will bias the sampling toward unoccluded directions which correspond to light actually received by the surface better.

The following showcases this with the left image using the normal to sample the irradiance map and the right one using the bent normal (no AO applied in either case). There is already some directionality present in the right image.

![](../../assets/0567caa937133027.png)

![](../../assets/b79dc03f0580371c.png)

The GTAO paper describes an extension to calculate the bent normal while calculating the occlusion, but also how to use that occlusion along with the bent normal to add directionality. This technique is based on projecting the cubemap into spherical harmonics (SH) to calculate the irradiance. [Spherical](http://www.cse.chalmers.se/~uffe/xjobb/Readings/GlobalIllumination/Spherical%20Harmonic%20Lighting%20-%20the%20gritty%20details.pdf) [harmonics](http://www.ppsloan.org/publications/StupidSH36.pdf) [is](http://limbicsoft.com/volker/prosem_paper.pdf) [probably](https://seblagarde.wordpress.com/2011/10/09/dive-in-sh-buffer-idea/) [less](https://patapom.com/blog/SHPortal/) [scary](http://graphics.stanford.edu/papers/envmap/) than it sounds but it is a big topic, outside the scope of this post. I will summarise 2 points that will be needed in this discussion though. The first is that SH are functions defined on the surface of a sphere, replacing the more common cartesian x,y,z coordinates with angles θ and φ ([source](https://patapom.com/blog/SHPortal/#constructing-the-sh-coefficients)).

This is important since all we have done so far is talk about calculating things over a hemisphere and spherical harmonics seem to be in the right domain for that.

The second point is that to “transform” (or project) a signal into spherical harmonics we need a basis and to calculate its coefficients. This is nothing that we don’t already do in Euclidean spaces as well, in that case [the basis](https://en.wikipedia.org/wiki/Standard_basis) is the 3 perpendicular unit vectors (i,j,k) at the origin.

To define any point of a function in this space all we need is the x,y,z coordinates, which in reality are the “coefficients” in respect to the basis (i,j,k). Something similar is happening with spherical coordinates as well, only in this case the [basis](https://en.wikipedia.org/wiki/Spherical_harmonics), defined on the surface of a sphere, looks much weirder.

This may sound a bit confusing at first: we can start from the top row with the lone lobe as a (very low fidelity) basis to approximate a signal and progressively increase detail by adding rows (lobes) to the basis. Each lobe would correspond to the different coefficient (you can broadly consider those lobes as the unit vectors of the cartesian space we talked above). In every case we can calculate the coefficients using this formula, where **f(θ, φ)** is the image to encode, **Y i(θ, φ)** the basis and

**C**the resulting coefficients.

iThe first 3 rows in the above image with the 9 lobe-basis and coefficients are enough to represent diffuse environment lighting. For example, this is what an environment map looks like [projected to 9 SH coefficients](http://graphics.stanford.edu/papers/envmap/).

```
float3 grace00 = { 0.078908, 0.043710, 0.054161 } ;
float3 grace1_1 = { 0.039499, 0.034989, 0.060488 } ;
float3 grace10 = {-0.033974, -0.018236, -0.026940 } ;
float3 grace11 = {-0.029213, -0.005562, 0.000944 } ;
float3 grace2_2 = {-0.011141, -0.005090, -0.012231 } ;
float3 grace2_1 = {-0.026240, -0.022401, -0.047479 } ;
float3 grace20 = {-0.015570, -0.009471, -0.014733 } ;
float3 grace21 = { 0.056014, 0.021444, 0.013915 } ;
float3 grace22 = { 0.021205, -0.005432, -0.030374 } ;
```

For the following image comparison I projected the original cubemap to spherical harmonics using 9 coefficients (left image SH, right image irradiance cubemap).

![](../../assets/cec180687ad886ef.png)


![](../../assets/cec180687ad886ef.png)

![](../../assets/e16d6f3293c1cbe4.png)


![](../../assets/e16d6f3293c1cbe4.png)

SH manages to represent irradiance quite well, even in a varied lighting environment with some directionality and as an added bonus it can do it with a relatively low overhead of 9 float3s per environment map (compared to a full cubemap).

I will close this quick SH summary mentioning [a useful property](https://patapom.com/blog/SHPortal/#signal-convolution-signal-product) that we will use in a bit:

In short, this means that if we need to calculate the integral of the product of 2 functions, often complicated and expensive, we can instead project them individually to a SH basis and instead calculate the dot product of their SH coefficients. This is useful because if you remember earlier we calculated the irradiance as

which is very similar to what I mentioned above, an integral of the product of 2 signals. In this case instead of calculating the integral of the cosine (i.e. dot(n,l)) weighted radiance, we could project both to SH and calculate their dot product, which is much faster. To calculate the coefficients for the cosine function there is some theory behind it that involves Zonal Harmonics, which effectively means using the symmetric lobes in the SH basis, since the cosine is rotationally invariant around the vertical axis:

![](../../assets/f0f1051ea998283e.png)


![](../../assets/f0f1051ea998283e.png)

Ramamoorthi’s [seminal paper](http://graphics.stanford.edu/papers/envmap/envmap.pdf) on using SH for environment lighting describes a derivation of the coefficients for the cosine (as well as the radiance L) signal, if you are interested in the details. In the end, having the AH coefficients for both the cosine and incoming radiance (the original cubemap), we calculate the irradiance **E** as:

where **A l** is the SH coefficients for the cosine,

**L**the coefficients for the incoming radiance and

lm**Y**is the SH basis that we mentioned above.

lmThis formulation does not give us much improvement in regards to occlusion and directionality, we still have to calculate AO separately, as we discussed, and multiply it with the irradiance E.

The authors of GTAO discuss ways to extend their technique to account for AO directionality, based on the SH formulation of the irradiance we just described. First, they use the bent normal calculated during occlusion (AO) estimation and by mapping the AO **A(x)** to an angle **a v(x)**

they reconstruct the bent cone **C(x)**, centred around the bent normal (repeating the image from above).

Then, they go back to the original formulation of outgoing radiance which includes visibility in the integral

and project **L(l)** and **V(l)(n.l)** to SH to simplify calculations as discussed above. Focusing on the **V(l)(n.l)** component and treating it as one signal, for simplicity, an assumption is made that the cosine is calculated with respect to the bent normal (and not the normal normal) and that allows them to combine the visibility (bent) cone and cosine SH coefficients as follows (showcasing the first three):

What is worth taking away from this is that visibility, as expressed by the bent cone, is now part of the irradiance calculation, as effectively the **z** coefficients above correspond to the **A l** SH coefficients below.

This also means that we don’t have to multiply the result of the irradiance calculation with a separate AO term any more. Making visibility part of the irradiance calculations improves the occlusion directionality as is showcased in the following screenshots.

![](../../assets/dd4c0cd7e44e136d.png)


![](../../assets/dd4c0cd7e44e136d.png)

![](../../assets/c33d3393e3754f68.png)


![](../../assets/c33d3393e3754f68.png)

![](../../assets/513bcb451d78a1c3.png)


![](../../assets/513bcb451d78a1c3.png)

![](../../assets/e1aa8d631c0d0406.png)


![](../../assets/e1aa8d631c0d0406.png)

Focusing on a setup with strong light directionality, we can see that directional GTAO improves over simple GTAO significantly (left GTAO, right directional GTAO)

![](../../assets/cfef1e599115db71.png)

![](../../assets/7405b04d3ff9b457.png)

I kept the study qualitative at this stage, not focusing on performance, since both techniques (RT and GTAO) are expensive on my lowly laptop. The cubemaps are from [this page](https://www.humus.name/index.php?page=Textures&start=0).

[…] Notes on occlusion and directionality in image based lighting. […]