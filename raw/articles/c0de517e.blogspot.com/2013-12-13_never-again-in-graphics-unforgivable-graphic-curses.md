---
title: 'Never Again in Graphics: Unforgivable graphic curses.'
url: http://c0de517e.blogspot.com/2013/12/never-again-in-graphics-unforgivable.html
published: '2013-12-13'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Well known, zero cost things that still are ignored too often.

Do them. On -any- platform, even mobile.

Please.

**Lack of self-occlusion**.[Pre-compute aperture cones](http://www.mpi-inf.mpg.de/~oklehm/publications/2011/vmv/SS_Bent_Cones_Klehm11.pdf)on every mesh and bend the normalmap normals, change specular occlusion maps and roughness to fit the aperture cone. The only case where this doesn't apply is for animated models (i.e. characters), but even there baking in "t-pose" isn't silly (makes total sense for faces for example), maybe with some hand-authored adjustments.**Non-premultiplied alpha.****Wrong****Alpha-key mipmaps**computed via box (or regular image) filters.**Specular aliasing**(i.e. not using Toksvig or similar methods).[Analytic,](http://c0de517e.blogspot.ca/2013/12/never-again-point-lights.html)**constant emission point/spot lights**.**Halos around DOF filters**. Weight your samples! Maybe only on low-end mobile, if you just do a blur and blend, it might be understandable that you can't access the depth buffer to compute the weights during the blur.... Weight your samples! Even if for some reason you have to do SSAO over the final image (baaaad), at least color it, use some non-linear blending! Ah, and[Cartoon-shading-like](http://www.youtube.com/watch?v=LDW4Vpnjw8U)[SSAO edges](http://www.youtube.com/watch?v=vrIKW4HWrvk)**skew that f*cking SSAO "up"**, most light comes from sky or ceiling, skewing the filter upwards (shadows downwards) is more realistic than having them around objects. AND don't multiply it on top of the final shading! If you have to do so (because you don't have a full depth prepass) at least do some better blending than straight multiply!. This is the poster child of all the effects that can be done, but not quite right. Either you can do something -well enough- or -do not do it-. Tone it down! Find alternatives. Look at reference footage![2D Water ripples on meshes](../../assets/f8d33bbd198b5440.img)(after lighting), i.e. lack of tonemapping. Basic Reinhard is cheap, even on shaders on "current-gen" (if you're forced to output to a 8bit buffer... and don't care that alpha won't blend "right").[Color channel clamping](http://www.youtube.com/watch?v=iYZpR51XgW0)**Simple depth-based fog**. At least have a ground! And change the fog based on sun dot view. Even if it's constant per frame, computed on the CPU.


__If you can think of more that should go in the list, use the comments section!__
## 9 comments:

> Lack of self-occlusion.


This sounds interesting, but I'm not sure what you mean. Do you have more information?

Thanks.

Added a link (even if that talks of a SS method, not precomputed on meshes) and some more description to the post.

I have been away from the latest in real-time rendering for the past few years, so as a follow up to this post, I would appreciate it if you could do a writeup on rendering techniques you would consider a must for upcoming games / engines. For instance which splitting, warping and filtering you suggest for shadow mapping, or what variation of screen space ambient occlusion you prefer or which tone mapping operator you like best, and so on and so forth.


Thanks.

Mah the thing is most good stuff lasts, it's reasonable and always will be, just different goals and compromises...










That's why what I mention in the article are basically common "bugs", not really techniques.

That said, there are a few things that are almost always a safe choice...

If you want to look around for a few modern concepts in game engines, search for these

- Shadows: stable cascaded shadowmaps (CSM), the latest cool is Intel's sample distribution shadowmaps (SDSM) maybe with EVSM for filtering

- SSAO: McGuire's Alchemy AO and Line Sampling from the paper "Volumetric Obscurance"

- Shading: Physically based, GGX (Walter BRDF) you'll find a lot of info from Siggraph 2013

- Lighting: tiled deferred or tiled forward (forward plus), AMD and Intel have code samples

- Culling and visibility: rasterized occlusion culling (Intel has samples), maybe using voxelization or planar sections to automaticaly derive occluders... Reprojection of previous frame zbuffer also works, Crysis did present that at the past GDC iirc

Well, this should keep you busy... You can look at presentations from Crytek, Epic's Unreal, EA|Dice's Frostbite, Amd and Intel and you'll have a good idea of many of the things that go into a modern engine.

Looking at the list, as a matter of fact, one must admit that many things aren't zero cost.


About the first point -- "Lack of self-occlusion": You probably still need to store the original normals additionally to the blended normals? Otherwise I do not see any way to evaluate a specular BRDF correctly.

Nope. You could store the original but even if you don't you'll see a huge improvement.


All these things are zero cost, even when they add some instructions, i.e. Ssao weighting is alu cost on something that will be texture bound...

MJP had similiar list, though it has couple different ones:


http://mynameismjp.wordpress.com/2011/12/06/things-that-need-to-die/

Pet peeve, mainly from fixed pipeline era:

For materials, ambient and diffuse colour should typically be the same value.

Often, you see diffuse colour set to e.g. 1,0,0 and ambient to 0.2,0,0 by which the designer tries to achieve a low ambient light.

However, this should be expressed in ambient light colour, not ambient material colour.

Post a Comment