---
title: Real-time rendered animations with OctaneRender 1.5
url: http://raytracey.blogspot.com/2013/12/real-time-rendered-animations-with.html
author: Sam Lapere
published: '2013-12-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

OctaneRender 1.5 has some really powerful features like support for Alembic animations and a fully scriptable user interface. The Alembic file support allows for real-time rendered animations in the standalone version of Octane for scenes with both rigid and deformable animated geometry. Seeing your animations rendered in final quality in real-time with GI, glossy reflections and everything is a blast:

You may remember the actor in the following video from blockbuster movies like "

[Ultra high detailed dynamic character test](http://raytracey.blogspot.co.nz/2013/07/real-time-path-tracing-125k-dynamic.html)" and "[4968 daftly dancing dudes on Stanford bunny](http://raytracey.blogspot.co.nz/2013/08/real-time-path-tracing-4968-daftly.html)". Even in Octane, his dancing prowess remains unrivalled. The actor is made up of 66k triangles and there are 730 clones of him (48 million triangles in total). For every frame of the animation, Octane loads the animated geometry from an Alembic file, builds the scene and renders the animation sequence with a script, all in real-time.
Some examples of rigid body animations:

With support for Alembic animations and Lua scripting, Octane has now a very solid foundation for animation rendering in place, allowing for some very cool stuff (yet to be announced) that can be done fully in real-time on a bunch of GPUs (inspired and fueled by earlier Brigade experiments). In 2014, Octane will blow minds like never before.

## 6 comments:

Brigade >/= Octane viewport?

That was what came to my mind...

Will Brigade/Octane ever merge as a fully generalized solution?

Skif: Brigade is more optimized for dynamic scenes and interactive navigation than Octane right now, but the gap is closing


Anonymous: merging them is impossible since both engines target different markets and are specifically engineered for it. Octane has a very complex and powerful and flexible node system allowing for very high programmability, but Brigade doesn't require such extreme flexibility.

Hi Sam,




Care to share your GPU setup used for these vids?

Presuming you're using the current release candidate version?

It's good to hear we're going to see some mind-blowing stuff in Octane in 2014. Can't wait to see some of those long-awaited features finally see the light.

Nvidia's Maxwell cards will also add to the fun, no doubt. Exciting year ahead.

Best,

SeekerFinder

@Sam, then how does one create their own shader for Brigade? A node system would be the most flexible user friendly way to do just that,look at Unreal Engine 4 node base material/shader.

So what's going on with Brigade and the shift of focus to Octane?


I hope development is still going ok .

Post a Comment