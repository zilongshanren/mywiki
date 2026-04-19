---
title: Activision @ Siggraph 2016
url: https://c0de517e.blogspot.com/2016/08/activision-siggraph-2016.html
published: '2016-08-13'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Siggraph 2016 recently ended, as always it was inspiring and lots of great discussions were had. Activision presence was quite strong this year after we shipped Black Ops 3.

If you missed any of our presentations, this post might help. I'll try to keep this updated with links relative to our presentations, as soon as they come online.

*Note: for convenience, I've written a summary of the techniques in the text below but keep in mind that, as always, this blog is truly made of personal opinions and observations - which come from my limited, R&D centric point of view.*

Call of Duty has always been a lightmapped title, but lightmaps come with a quite large set of issues: large baking times, complexity in representing runtime materials and effects, lighting discontinuities with dynamic objects and the inability of "kit-bash" geometric detail (compenetrating meshes).

![]() |

all lit with the same illumination data!

It's incredible that after all this time, there still isn't in real-time rendering much research on ways of solving the problem of baked irradiance. Naive lightmaps are not enough to generate an image that does look coherent, without leaks and discontinuities.

This new development at Treyarch tackles all these issues at once with a new runtime representation of baked irradiance that works seamlessly with deferred shading and is tightly coupled with prefiltered irradiance cubemaps and new, state of the art, heuristics for parallax-corrected reflections and a baking system that cut down iteration times substantially for artists without having to resort to renderfarms.

![]() |

Now all our art production happens in a fully WYSIWYG editor, and all the lighting is unified, regardless of the object type (dynamic, static, skinned, particles, volumetrics...).

This is achieved by employing hardware-filtered volumetric textures as the only representation of baked irradiance.

![]() |

Artists place irradiance volumes quickly in a level, and author clipping convex volumes to avoid light leaks (note that these have to be authored anyways for reflection probes, so it's not really extra work, and our editor supports very fast workflows for placing volumes and planes), and the authored volumes are usually robust to iterations in the level geometry.


As part of this system,

As part of this system,

[Josiah Manson also further developed his fast GGX pre-integration scheme, now presented at EGSR 2016](http://josiahmanson.com/research/ggx_filtering/).
Kevin Myers presented in the "dark hides the light" session our new compression technology for baked shadowmaps.

Call of Duty had a system for caching shadowmaps since Ghosts, as the new generation of consoles saw a bigger increase in memory than in computation, caching techniques have seen a resurgence.

This work is a quite radical improvement of our shadowmap caching technology, and allows to fully pre-bake a shadowmaps for entire levels, achieving thousand-fold compression ratios.

In comparison with

[precomputed voxelized shadows](http://www.cse.chalmers.se/~kampe/compactPrecomputedVoxelizedShadows.pdf)this technique allows for easily recovering the shadowmap depth, which makes it easier to integrate with other effects (i.e. volumetric lighting). It's also fast to traverse. The closest relative to SSTs are the[Compressed Multiresolution Hierarchies](https://graphics.tudelft.nl/Publications-new/2016/SBE16/sbe16.pdf)of Scandolo et al., but our solution was developed independently in parallel, so the data encoding employed is not the same.
To my knowledge the first use of compressed shadowmaps in game production. It also enabled savings in the g-buffer, as we can use the SST to quickly shadow far objects, instead of having to bake a lightmap space occlusion map.

This is the continuation of the

[subdivision surface](http://gpupro.blogspot.ca/2016/01/gpu-pro-7-table-of-content.html)research started by[Wade](http://wadeb.com/blog/publications/)on[Call of Duty Ghosts](http://www.gdcvault.com/play/1020252/Advanced-Visual-Effects-with-DirectX), (which to my knowledge is the first videogame to make extensive use of Catmull-Clark subdivision surfaces in real-time).
It's a quite neat technique, which sidesteps a limitation in current hardware tessellation pipelines by passing a variable number of control points to the hull shader via L2 read/writes.

This is the only presentation at Siggraph 2016 that is not directly linked with a shipped Call of Duty title.

Natasha and Wade gave a compelling presentation at the open problems in computer graphics course, surveying artists in many companies, even going outside the videogame companies circle we work in.

This is one of my favorite courses at Siggraph, and the only presentation from Activision that I haven't reviewed beforehand, so it was truly interesting for me to watch it live.

Jorge Jimenez presented a new version of his SMAA antialiasing technique, greatly improving both performance and quality (sharpness and stability) with a plethora of tweaks and innovations. The slides also summarize relevant previous published techniques and their image quality tradeoffs.

![]() |

In my opinion, with Jorge's Filmic SMAA, the quest for antialiasing techniques is largely over, and we can say that temporal reprojection has "won".

Not only temporal reprojection often achieves better quality than MSAA when using comparable performance budgets, but it's being easier to integrate into deferred renderers and nowadays it's becoming unavoidable anyways because so many other effects can benefit from the ability to perform temporal supersampling (e.g. shadows, reflections, ambient occlusion...).

[Hybrid techniques](https://michaldrobot.com/2014/08/13/hraa-siggraph-2014-slides-available/)are still very interesting, and there are probably still improvements possible (and probably Jorge will come yet again on stage in the future to show something amazing in that space), but in general the interest on MSAA reconstruction techniques for edge antialiasing has diminished from being a must-have and a pain point for deferred rendering, to a much less important solution.

MSAA is still a great feature to have in hardware though as it allows to subsample or supersample certain effects and render passes (

[e.g. particles](https://mynameismjp.wordpress.com/2015/09/13/programmable-sample-points/)), but it should be more thought as a way to do mixed resolution than strictly for edge antialiasing.
Jorge, Xian, Adrian and myself worked on extending rendering ambient occlusion state of the art by crafting techniques that are based on modeling the (ray traced) ground truth solution for diffuse and specular occlusion.

![]() |

We derived closed-form analytic solutions when possible, and when such models could not be found for ampler generalizations of the problems at hand, we extended the analytic solutions by fitting "residual" functions to the ground truth data, or by employing look-up tables.

![]() |

GTAO has already been used in production, as a drop-in replacement of the previous state-of-the-art technique we were employing (HemiAO), yielding better image quality (actually, even better than HBAO, which is a very popular high-quality solution) in the same performance budget (0.5ms).

## 2 comments:

Will the slides for the Sparse Shadow Trees be going up anywhere? Would have loved to have gone, but the scheduling had it conflicting with the PBR course...

Yep, they will, just waiting for final clearance.


Post a Comment