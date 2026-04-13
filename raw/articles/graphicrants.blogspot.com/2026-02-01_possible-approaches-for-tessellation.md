---
title: Possible approaches for tessellation
url: http://graphicrants.blogspot.com/2026/02/possible-approaches-for-tessellation.html
author: Brian Karis
published: '2026-02-01'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

### Requirements

All the original goals of Nanite should apply to our approach here as well. One of them implicitly covers the rest:**authoring decisions should have no impact on performance**. While not 100% realized, Nanite mostly behaves that way so that principle should be maintained if at all possible. Applied here would mean a run-time tessellated and displaced mesh should render just as fast as an offline tessellated and displaced Nanite mesh. So the performance characteristics of Nanite, and thus its goals to the extent they were realized, should ideally be shared by Nanite Tessellation. This is not strictly a requirement because, as we'll see by the end, it was not achieved. But it very much was a goal and the closer we can get to this ideal the better.

## Tracing

Tessellation is actually not a requirement, it’s an implementation detail. Displacement is the artist facing feature. There are a variety of tracing based approaches to scalar displacement.

[Shell mapping](https://dl.acm.org/doi/10.1145/1073204.1073239)and its descendants find the ray enter and exit point through the prism formed by the base triangle extruded along its vertex normals, then ray march the displacement function in tangent space.

[Displaced Micro Maps](https://github.com/NVIDIAGameWorks/Displacement-MicroMap-Toolkit)are similar except the ray march is replaced with a quadtree traversal that acts as an acceleration structure for the barycentric space. Neither have any acceleration in the displacement direction. This means if the displacement range is large compared to the size of base triangles there will be performance problems. There will be many tall skinny prisms with high overdraw and no way to quickly skip empty space. The expectation with these techniques is that the prisms will be shallow. In the case of DMMs this comes from their creation offline. That does not apply here since the base mesh will be an arbitrary Nanite mesh that could be dense and the displacement function is a shader with a range specified by an artist.

[Thonat et al.](https://perso.telecom-paristech.fr/boubek/papers/TFDM/)traverse a quadtree acceleration structure that bounds the displacement direction as well. Unfortunately it assumes that displacement is a single texture, not a shader, and that minmax mipmaps (the acceleration structure) can be generated for that texture. If the shader results were cached in texture space this might be viable. The

[origins](https://graphicsinterface.org/proceedings/gi1998/gi1998-2/)of the approach to bound displacement with interval or affine arithmetic were actually for the purpose of tracing shaders, so it is possible. Unfortunately, the cost, even in the simple single texture case, puts this outside our needs.

That leaves us with rasterization and thus some form of tessellation.

## Work within the current framework

Tessellation and displacement mapping were in mind with the original design of Nanite. The idea being triangle clusters could be synthesized instead of streamed from disk when finer detail levels were requested. Once we have the core Nanite based on offline simplification working well and shipped we can add on with tessellation being the first obvious extension.

This is a really elegant approach to the problem. It means the same framework can be used to solve that problem as well. Tessellation and displacement mapping in addition to other potential forms of geometry synthesizing, maybe marching cubes or subd surfaces, could be implemented and at basically no additional run-time cost. IO and transcoding would be traded for generation. The per frame cull and rasterization would be identical regardless of the source the triangles came from. All the work of generating that geometry is cached and reused across many frames. Going this route makes it conceivable that the goals from the Nanite dream could be achieved instead of this just adding cost.

As the design of Nanite was being realized, little by little it was becoming clear this idea wasn’t realistic. Every step of the Nanite build process was a bit more complicated than expected with extra details, constraints, or edge cases that weren’t obvious until we seriously implemented them and battle tested it all. Synthesizing tessellated clusters changes the process from simplification to amplification. Basically this amounts to running the Nanite build process in reverse. Now that the details of that process were better understood, doing it in reverse, in a random access sort of way where a complete level worth of clusters isn’t all available at once, in constrained memory, in the same budget that transcoding is currently costing, is not remotely straightforward and potentially not even possible.

I have ideas on how the process could be modified by maybe replacing graph cuts with something more spatial or precomputing portions but not all of the task. There are some important flaws though that were discovered that are inherent to the idea.

### Both simplification and amplification

Tessellation to a uniform sampling resolution suitable for displacement mapping is not simply a matter of adding additional levels, like generating a level -1 past level 0, (0 being the original source triangles). Triangles from the source mesh larger than 1 pixel may not be flat anymore and need to be tessellated but at the same time tiny triangles may be far smaller than a pixel. Levels can’t simply be divided into exclusively simplification or amplification, both are needed simultaneously.The base Nanite structure accounts for only the error against the base mesh, not the error against the displaced mesh. A simple way to solve that is the stored levels are tessellated at build time to a desired resolution matching that level’s error. Then runtime amplification picks up from there by generating more such levels. But that means the Nanite mesh needs to be built differently to support displacement mapping and at a significant cost. Far more triangles and vertices will need to be stored and rendered than otherwise needed compared to the normal Nanite mesh.

### Adaptive tessellation

Another major flaw with this idea is that base Nanite adapts the triangle density to the content. This happens naturally with quadric based mesh simplification. Flatter areas can use fewer larger triangles to hit the same error. To achieve the same rendering performance and run-time memory overhead from generated triangle clusters the triangles would need to be just as efficiently placed. This simply isn’t possible. Even getting half way there with good content adaptive tessellation is incredibly challenging. So the reality is there is no chance generated triangle clusters will be the same cost to store and render as offline simplified ones, even if the cost to generate them is free. Far more of them will be needed to hit the same error due to less efficient use of triangles to approximate the surface.Not only is it very difficult to adaptively place triangles to efficiently represent the underlying signal, unlike core Nanite, the signal is not known up front. Displacement comes from a user defined shader. It must be sampled. This presents a problem. The error, or the difference between the limit surface and the tessellated one, can’t be known exactly. The best we can do is consider the error to be the sampling rate. This is reasonable if the signal is band limited. Hopefully it is due to mipmaps but given it is user defined there is no guarantee of that.

### True micropoly

With this new measurement for error it is clear that what we will be rendering are true micropolys. To hit 1 pixel error all triangles must be <=1 pixel wide. Many people mistakenly think this is what Nanite was already doing. Our software rasterizer is designed to be efficient for micropolys but that is not the LOD target. Nanite targets a LOD with 1 pixel of error not 1 pixel triangles. Some triangles need to be pixel sized to be within that error but most aren’t. Losing content adaptive thus means far more triangles for the same content so there is no chance this doesn’t cost more than an offline tessellated Nanite mesh.That assumes all else being equal, as in the original Nanite rendering pipeline is still the fastest way to render this. Maybe not. Nanite’s LOD decisions are very coarse. It works on decently large cluster group granularity with conservative bounding volumes and jumps in power of 2 increments. Ignoring the spatial granularity and conservativeness, pow2 alone means on average the triangle count is at least 33% greater than the ideal. Could a different design make up for the increase in triangle count from losing content adaptive by hitting closer to the optimal number of uniformly sized triangles? Doing so means stepping outside the existing framework and dynamically tessellating patches every frame.

## Reyes

The

[Reyes](https://graphics.pixar.com/library/Reyes/paper.pdf)rendering architecture was the first to support displacement mapping and is designed around efficiently tessellating surfaces into micropolys. Therefore it is an obvious reference point for this problem.

In Reyes a primitive goes through the following pipeline:

- Bound
- Split
- Dice
- Shade
- Rasterize

The bounding box for a primitive is computed. If it is off screen, cull it. If it is too large the primitive is split, usually in two, and the sub primitives are sent back to Bound. This will continue recursively until a primitive is small enough to dice. Dicing converts the primitive into a uniform grid of micropolys. The vertices of that grid are shaded and finally the micropolys are rasterized.

Why have both split and dice? Recursive splitting allows visibility to be retested at a more uniform granularity. It also allows surfaces that cover a large depth range to tessellate at a varying density, better matching the view. This recursive splitting is actually very similar to Nanite’s cluster hierarchy traversal, both in the approach and the reasons for it. Why not only split? There are efficiencies that are important at the leaf level that motivate dicing being special.

Reyes has been used heavily in offline renderers and film production for decades. Even after the move away from Reyes to path tracing, some production path tracers (

[Manuka](https://jo.dreggn.org/home/2018_manuka.pdf),

[PRMan](https://graphics.pixar.com/library/RendermanTog2018/paper.pdf), etc) still run the majority of this pipeline. Instead of rasterizing the micropolys they trace rays against them.

### Real-time Reyes

Because of its success in film, real-time Reyes adapted for GPUs has long been a target with numerous research papers ([Patney and Owens](https://anjulpatney.com/docs/papers/2008_Patney_RRA.pdf),

[RenderAnts](http://kunzhou.net/2009/renderants.pdf),

[DiagSplit](https://graphics.stanford.edu/papers/diagsplit/),

[FracSplit](https://cg.ivd.kit.edu/english/FracSplit.php),

[Sattlecker and Steinberger](https://www.markussteinberger.net/papers/GPUReyes.pdf), etc) dedicated to possible approaches. As far as I know Nanite Tessellation in Unreal Engine 5.4 is the first shipping real-time Reyes implementation and Fortnite is the first it has shipped in a game (although only used on the ground).

While Nanite Tessellation retains every aspect of the high-level Reyes algorithm, there are many differences in the details, more than just in how it integrates with the base Nanite algorithm. Starting with the most basic: the primitives in our case are triangular patches. They start as triangles from a triangle mesh which are further split into triangular subpatches. This continues recursively until the subpatches are small enough to dice. Dicing uniformly tessellates the patch into microtris.

Shade only evaluates the displacement function at the diced triangle vertices. All other shading is done at pixel frequency in screen space. This is simply more efficient due to the amount of overshade that object space shading incurs. True preshading is a relic of the past. Modern production path tracers either shade on hit for everything not displacement as well or at most evaluate material shaders into BxDF lobes similar to a GBuffer and then shade with that on hit.

## No comments:

Post a Comment