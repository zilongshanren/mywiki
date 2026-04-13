---
title: Sparse shadows through tracing
url: http://graphicrants.blogspot.com/2012/05/sparse-shadows-through-tracing.html
author: Brian Karis
published: '2012-05-14'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Before I get to that though I want to talk about a concept I think is going to be very important for next gen renderers and that is having more than one representation for scene geometry. Matt Swoboda talked about this in his GDC presentation this year [1] and I am in complete agreement with him. We will need geometry in similar formats as we've had in the past for efficient rasterization (vertex buffers, index buffers, displacement maps). This will be used whenever the rays are coherent simply because HW rasterization is much faster than any other algorithm currently for coherent rays. Examples of use are primary rays and shadow rays in the form of shadow maps.

Incoherent rays will be very important for next gen renderers but we need a different representation to efficiently trace rays. Any that support tracing cones will likely be more useful than ones which can only trace rays. Possible representations are signed distance fields [2][1][9], SVOs [3], surfel trees [4], and billboard cloud trees [5][9]. I'll also include screen space representations although these don't store the whole scene. These include mip map chains of min/max depth maps [6], variance depth maps [7] and adaptive transparency screen buffers [8]. Examples of use for these trace friendly data structures are indirect diffuse (radiosity), indirect specular (reflections) and sparse shadowing of direct specular. The last one is what helps with our current issue.

The Samaritan demo[9] from Epic had a very similar issue that they solved in the same way I am suggesting. They had many point lights which generated specular highlights at any distance. To shadow them they did a cone trace in the direction of the reflection vector against a signed distance field that was stored in a volume texture. This was already being done for other reflections so using that data to shadow the point lights doesn’t come at much cost. The signed distance field data structure could be swapped with any of the others I listed. What is important is that the shadowing is calculated with a cone trace.

**What I propose as the solution to our problem is to use traditional shadow maps only within the diffuse radius. Do a cone trace down the reflection vector. The cone trace will return a visibility function that any specular outside the range of a shadow map can cheaply use to shadow.**


Actually, having shadowing data independent from the lights means it can be used for culling as well. The max unoccluded ray distance can be accumulated per tile which puts a cap on the culling cone for light sources. I anticipate this form of occlusion culling will actually be a very significant optimization.


This shadowing piece of the puzzle means the changes I suggested in my last post, in theory, come at a fairly low cost assuming you already do cone tracing for indirect specular. That may seem like a large assumption but to demonstrate how practical cone tracing is, a very simple, approximate form of cone tracing can be done purely against the depth buffer. This is what I do with screen space reflections on current gen hardware. I don’t do cone tracing exactly but instead reduce the trace distance with low glossiness and fade out the samples at the end of the trace. This acts like occlusion coverage fades by the radius of the cone at the point of impact which is a visually acceptable approximation. In other words the crudest form of cone tracing can already be done in current gen. It is fairly straightforward to extend this to true cone tracing on faster hardware using one of the screen space methods I listed. Replacing screen space with global is much more complex but doable.


The result is hopefully point light specularity “just works”. The problem is then shifted to determining which lights in the world to attempt to draw. Considering we have >10000 in one map in Prey 2 this may not be easy :). Honestly I haven’t thought about how to solve this yet.


I, like everyone else who has talked about tiled light culling, am leaving out an important part which is how to efficiently meld shadow maps and tiled culling for the diffuse portion. I will be covering ideas on how to handle that next time.


Finally, I want to reach out to all that have read these posts that if you have an idea on how the cone based culling can be adapted to a blinn distribution please let me know.

Actually, having shadowing data independent from the lights means it can be used for culling as well. The max unoccluded ray distance can be accumulated per tile which puts a cap on the culling cone for light sources. I anticipate this form of occlusion culling will actually be a very significant optimization.

This shadowing piece of the puzzle means the changes I suggested in my last post, in theory, come at a fairly low cost assuming you already do cone tracing for indirect specular. That may seem like a large assumption but to demonstrate how practical cone tracing is, a very simple, approximate form of cone tracing can be done purely against the depth buffer. This is what I do with screen space reflections on current gen hardware. I don’t do cone tracing exactly but instead reduce the trace distance with low glossiness and fade out the samples at the end of the trace. This acts like occlusion coverage fades by the radius of the cone at the point of impact which is a visually acceptable approximation. In other words the crudest form of cone tracing can already be done in current gen. It is fairly straightforward to extend this to true cone tracing on faster hardware using one of the screen space methods I listed. Replacing screen space with global is much more complex but doable.

The result is hopefully point light specularity “just works”. The problem is then shifted to determining which lights in the world to attempt to draw. Considering we have >10000 in one map in Prey 2 this may not be easy :). Honestly I haven’t thought about how to solve this yet.

I, like everyone else who has talked about tiled light culling, am leaving out an important part which is how to efficiently meld shadow maps and tiled culling for the diffuse portion. I will be covering ideas on how to handle that next time.

Finally, I want to reach out to all that have read these posts that if you have an idea on how the cone based culling can be adapted to a blinn distribution please let me know.

[http://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/](http://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/)

[2]

[http://iquilezles.org/www/material/nvscene2008/rwwtt.pdf](http://iquilezles.org/www/material/nvscene2008/rwwtt.pdf)

[3]

[http://maverick.inria.fr/Publications/2011/CNSGE11b/GIVoxels-pg2011-authors.pdf](http://maverick.inria.fr/Publications/2011/CNSGE11b/GIVoxels-pg2011-authors.pdf)

[4]

[http://www.mpi-inf.mpg.de/~ritschel/Papers/Microrendering.pdf](http://www.mpi-inf.mpg.de/~ritschel/Papers/Microrendering.pdf)

[5]

[http://graphics.cs.yale.edu/julie/pubs/bc03.pdf](http://graphics.cs.yale.edu/julie/pubs/bc03.pdf)

[6]

[http://www.drobot.org/pub/M_Drobot_Programming_Quadtree%20Displacement%20Mapping.pdf](http://www.drobot.org/pub/M_Drobot_Programming_Quadtree%20Displacement%20Mapping.pdf)

[7]

[http://www.punkuser.net/vsm/vsm_paper.pdf](http://www.punkuser.net/vsm/vsm_paper.pdf)

[8]

[http://software.intel.com/en-us/articles/adaptive-transparency/](http://software.intel.com/en-us/articles/adaptive-transparency/)

[9]

[http://www.nvidia.com/content/PDF/GDC2011/GDC2011EpicNVIDIAComposite.pdf](http://www.nvidia.com/content/PDF/GDC2011/GDC2011EpicNVIDIAComposite.pdf)

## 6 comments:

its still not clear how to quick update \ reconstruct signed distance field or something similar for a scene.

Signed distance field is only one option. If I were to use that I probably wouldn't generate it dynamically. I would probably stream it using something like clip maps. Some of the other structures such as surfel trees have been shown to be fast to update. Check out Bunnell's work.






Personally I would probably put static geometry in a global structure and do dynamic geometry like characters with screen space. So, a hybrid of two of the options.

If you want dynamic signed distance fields check out these references for generating them on the GPU.

http://developer.amd.com/media/gpu_assets/Evans-Fast_Approximations_for_Lighting_of_Dynamic_Scenes-print.pdf

and

http://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/

Nice thoughts Brian. Keep it up!


I had the same main takeaway from Matt's talk; I'm still mulling over the rest of your post, so I'll keep this short for now, but one thing I've wondered in the past is how effective cone culling is in practice if you have a lot of bumpy content. It partly depends on tile size, of course. On a related note, since you’re reducing the tracing distance with roughness, there may be a side benefit to specular AA here. :)

Hi Brian,



It's an interesting topic. Better visibility information would definitely make a whole load of things possible. (And unsurprisingly, it's also something I've been thinking about.) I'm not sure about volumetric signed distance fields, but it's just the volumetric bit I worry about. 2D or 2.5D signed distance fields are great.

Simple, coherent tracing is definitely possible these days, but I'm not sure the memory and bandwidth exists to really go to town with volumetric structures. So I'm looking for acceleration structures that you can efficiently trace against, but don't require crazy amounts of memory. Shadow maps are actually quite cool in this regard, but the fixed resolution aspect is a major pain.

Stephen,




Thanks!

It depends on the frequency of the bumps. High frequency bumps should have their gloss reduced automatically to prevent aliasing like you've discussed before. This turns it into the low gloss case where the number of pixels that have to compute specular is balanced between far reaching but small highlights and short reaching and broad highlights. In other words, energy conservation causes the number of pixels above a certain energy tolerance to be roughly constant over a large distance. If the frequency of bumps is about half the tile size though, culling will be ineffective. You could easily construct such a case artificially. I haven't tried this idea to know whether those cases come up much in practice though. I hope not.

To be clear, the trace distance reduction is only with basic SSR to fake a cone trace. With a data structure that supports a proper cone trace, the trace distance would probably be constant. As for spec AA, you're right but a real cone trace would do a better job of that as well.

Sam,




I was trying to list various options. So long as they support cone tracing, what I talked about applies. The idea isn't specific to signed distance fields. The reason I talked a bit more about them than others is that that is was the sameritan demo used.

I agree with you. I'm not a big fan of distance fields stored in large volume textures. It is very hard to have much detail without consuming huge amounts of memory. Also they don't store color so you can only really get occlusion information from them, not bounce.

Personally I'm rooting for surfel trees for global and a mip hierarchy of adaptive transparency maps for screen space. As I mentioned I think a hybrid might be useful.

Post a Comment