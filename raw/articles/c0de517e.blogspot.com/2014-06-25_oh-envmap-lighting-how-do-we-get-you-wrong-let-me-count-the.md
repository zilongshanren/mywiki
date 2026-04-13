---
title: Oh envmap lighting, how do we get you wrong? Let me count the ways...
url: http://c0de517e.blogspot.com/2014/06/oh-envmap-lighting-how-do-we-get-you.html
published: '2014-06-25'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The basics are well known:

- Generate a cubemap of your environment radiance (a probe, even offline or in realtime).
[Blur](http://developer.amd.com/tools-and-sdks/archive/legacy-cpu-gpu-tools/cubemapgen/)[it](http://seblagarde.wordpress.com/2012/06/10/amd-cubemapgen-for-physically-based-rendering/)with a cosine hemisphere kernel for diffuse lighting (irradiance) and with a number of phong lobes of varying exponent for specular. The various convolutions for phong are stored in the mip chain of the cubemap, with rougher exponents placed in the coarser mips.- At runtime we fetch the diffuse cube using the surface normal and the specular cube using the reflection vector, forcing the latter fetch to happen at a mip corresponding to the material roughness.

[We can avoid filtering by using multiple taps of a regular mip pyramid](http://graphics.cs.williams.edu/papers/EnvMipReport2013/), which is a tradeoff that could be better in runtime.[We can warp the cubemap](http://seblagarde.wordpress.com/2012/09/29/image-based-lighting-approaches-and-parallax-corrected-cubemap/)[to try to adjust it](http://www.guerrilla-games.com/presentations/Valient_Killzone_Shadow_Fall_Demo_Postmortem.pdf)to be used[from positions that are not exactly the point from where the environment](http://sirkan.iit.bme.hu/~szirmay/ibl3.pdf)was captured.[We can extend the reasoning past a simple Phong specular](http://blog.selfshadow.com/publications/s2013-shading-course/lazarov/s2013_pbs_black_ops_2_slides_v2.pdf)to[more complex Cook-Torrance models](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_slides.pdf).

Especially the last extension allowed a huge leap in quality and applicability, it's so nifty it's worth explaining a second.

The problem with

[Cook-Torrance BRDFs](http://en.wikipedia.org/wiki/Specular_highlight)is that they depend from three functions: a distribution function that depends on N.H, a shadowing function that depends on N.H, N.L and N.V and the Fresnel function that depends on N.V.
While we know we can somehow solve functions that depend on N.H by fetching a prefiltered cube in the reflection direction (not really the same, but the same different that there is between the

[Phong and Blinn specular models](http://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_shading_model)), if something depends on N.V it would add another dimension to the preintegrated solution (requiring an array of cubemaps) and we completely wouldn't know what to do with N.L as we don't have a single light vector in environment lighting.
The cleverness of the solution that was found can be explained

[by observing the BRDF](http://www.disneyanimation.com/technology/brdf.html)and how its shape changes when manipulating the Fresnel and shadowing components.
You should notice that

**the BRDF shape, thus the filtering kernel on the environment map, is mostly determined by the distribution function**, that we know how to tackle. The other two components don't change much of the shape but scale it and "shift" it away from the H vector.
So we can imagine an approximation that integrates the distribution function with a preconvolved cubemap mip pyramid, and the other components are somehow relegated into a scaling component by preintegrating them against an all-white cubemap, ignoring specifically how the lighting is distributed.

And this is the main extension we employ today, we correct the cubemap that has been preintegrated only with the distribution lobe with a (very clever) biasing factor.

All good, and works, but now, is all this -right-? Obviously not! I won't offer (just yet) solutions here but can you count the ways we're wrong?

- First and foremost the reflection vector is not the half-vector, obviously.
- The preconvolved BRDF expresses a radially symmetric lobe around the reflection vector, but an half-vector BRDF is not radially symmetric at grazing angles (when H!=N), it becomes stretched.
**It's also different from the its reflection-vector based one**but there it can be adjusted with a simple constant roughness modification (just remember to do it!).[when R=H=N](http://seblagarde.wordpress.com/2012/03/29/relationship-between-phong-and-blinn-lighting-model/)- As we said, Cook-Torrance is not based only on an half-vector lobe.
- We have a solution that works well but it's based only on a bias, and while that accounts for the biggest difference between using only the distribution and using the full CT formulation, it's not the only difference.
- Fresnel and shadowing
**also "push" the BRDF lobe**so it doesn't reach its peak value on the reflection direction. - If we bake lighting from points close enough that perspective matters, then discarding position dependence is wrong.
- It's true that perceptually is hard for us to judge where lighting comes from when we see a specular highlight (good!) but for reflections of nearby objects the error can be easy to spot.
- We can employ warping as we mentioned, but then the preconvolution is warped as well.
- If for example we warp the cubemap by considering it representing light from a box placed in the scene, what we should do is to trace the BRDF against the box and see how it projects onto it. That projection won't be a radially symmetric filtering kernel in most cases.
- In the "box" localized environment map scenario the problem is closely related to texture card area lights.
- We disregard occlusions.
- Any form of shadowing of the preconvolved enviroment lighting that just scales it down is wrong as occlusion should happen before prefiltering.
**Still -DO- shadow environment map lighting**somehow. A good way is to use screen-space (or voxel-traced) computed occlusion by casting a cone emanating from the reflection vector, even if that's done without considering roughness for the cone size, or somehow precomputing and baking some form of directional occlusion information.- Really this is still due to the fact that we use the envmap information at a point that is not the one from which it was baked.
- Another good alternative to try to fix this issue is
**renormalization**as shown by[Call](http://advances.realtimerendering.com/s2011/Lazarov-Physically-Based-Lighting-in-Black-Ops%20(Siggraph%202011%20Advances%20in%20Real-Time%20Rendering%20Course).pptx)of[Duty](http://blog.selfshadow.com/publications/s2013-shading-course/lazarov/s2013_pbs_black_ops_2_slides_v2.pdf). - We don't clip the specular lobe to the normal-oriented hemisphere
- So, even for purely radial-symmetric BRDFs around the reflection vector (Phong), in an environment without occlusion, the approximations are not correct.
- Not clipping is similar to the issues we have integrating area lights (where we should clip the area light when it dips below the surface horizon, but for the most part we do not)
- This is expected to have a Fresnel-like effect - we are messing up with the grazing angles.
- A possible correction would be to skew the reflection vector away from the edges of the hemisphere, and shrink it (fit it to the clipped lobe)
- We disregard surface normal variance.
- Forcing a given miplevel (
[texCubeLod](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509690(v=vs.85).aspx)) is needed as mips in our case represent different lobes at different roughnesses, but that means we don't antialias that texture considering how normals change inside the footprint of a pixel (note: some HW gets that wrong even with regular texCube fetches) **The solution here is "simple"**as it's related to[the specular antialiasing](http://blog.selfshadow.com/2011/07/22/specular-showdown/)[we do by pushing normal variance](http://www.nvidia.com/object/mipmapping_normal_maps.html)into[specular roughness](http://c0de517e.blogspot.ca/2012/02/normalmaps-everywhere.html).- But that line of thought, no matter the details, is also provably wrong (still -do- that). The problem is closesly related to the
["roughness modification" solution](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_notes_v2.pdf)for spherical area lights and it suffers from the same issue, the proper integral of the BRDF with a normal cone is flatter than what we get at any roughness on the original BRDF. - Also, the footprint of the normals won't be a cone with a circular base, and even what we get with the finite difference ddx/ddy approximation
[would be elliptical](http://www.csee.umbc.edu/~olano/papers/lean/). *Bonus: compression issues for cubemaps and dx9 hardware.**Older hardware couldn't properly do bilinear filtering across cubemap edges, thus leading to visibile artifacts that some corrected*[by making sure the edge texels were the same across faces](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Isidoro-CubeMapFiltering-Sketch-SIG05.pdf).*What most don't consider though is that if we use a block-compression format on the cubemap (DXT, BCn and so on) there will be discontinuities between blocks which will make the edge texels different again. Compressors in these cases should be modified so the edge blocks share the*[same reference colors](http://en.wikipedia.org/wiki/S3_Texture_Compression).[Adding borders is better](http://the-witness.net/news/2012/02/seamless-cube-map-filtering/).*These techniques are relevant also for hardware that does bilinear filter across cubemap edges, as that might be slower... Also, avoid using the very bottom mips...*

I'll close with some links that might inspire further thinking:

[An overview](http://people.mpi-inf.mpg.de/~jnkautz/projects/unifiedenvmaps/egrws00.pdf)[Solving non-symmetric filters with multiple lobes](http://ntp-0.cs.ucl.ac.uk/staff/j.kautz/publications/glossyGI00.pdf)[A way of solving occlusion](http://people.csail.mit.edu/green/papers/NonLinPreFilt_lowres_old.pdf)- Remember that you can and SHOULD check the errors you're making by comparing the prefilterd solution with
[an importance sampled reference](http://hal.inria.fr/hal-00996995/en)which is possible to compute (slowly) in runtime by doing many taps on a non-prefiltered envmap. - A recent, well done,
[testbed](https://github.com/dariomanesku/cmftStudio)for cubemap environment lighting - Filtering
[done fast via multiple fetches](http://graphics.cs.williams.edu/papers/EnvMipReport2013/)

## 6 comments:

We precompute a 3D texture parameterized by V.N, roughness, and "F0" (spec intensity at normal incidence) which encodes the direction, spread, and intensity of the incidence lobe for our BRDF, and use that to sample the envmap. The spread is stored as an oblong gaussian with major axis assumed to be in the plane of N and V. Works pretty well.

You sample a 3D texture to avoid a dot product? Are they really *that* expensive? Or am I being too thick or noobish here?

I think he was saying that he samples a 3d texture to know how to sample the prefiltered envmap.



The 3d texture stores some parameters that tell how the BRDF looks like, or in other words which prefiltered mip level of the envmap does represent the BRDF best.

That is because as I wrote in the article even if you do the state-of-the-art Cook-Torrance D/FG split (see Brian Karis Unrealengine 4 presentation, all the links are in the article) you still commit certain errors

Right, the 3D texture encodes the best-fit specular lobe to integrate the envmap with.

English is my second language so please feel free to correct me.




When we convolve a cubemap with diffuse or specular convolution, shouldn've convolve each texel differently depending on material of the surface from which that texel is coming from? Say one cubemap texel is metal and another is dielectric?

Something tells me we can ignore difference in materials if we create our cubemap from a point that's far enough from surfaces and we use correct parameters when rendering objects in source cubemap, but I'm still not sure on how correct diffuse and specular convolutions of arbitrary cubemap are.

Am I missing something?

Anonym: sorry for the late reply!




You are right. The standard solution for that problem is to use mipmaps for specular (and maybe a second cubemap or SH or something else for diffuse).

In the specular cubemap, we convolve each mip with a different specular lobe, observing that as the lobes get wider, we need less resolution

see https://github.com/dariomanesku/cmftStudio

Post a Comment