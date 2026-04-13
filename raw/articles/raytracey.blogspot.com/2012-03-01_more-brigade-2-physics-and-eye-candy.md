---
title: More Brigade 2 physics and eye candy
url: http://raytracey.blogspot.com/2012/03/more-brigade-2-physics-and-eye-candy.html
author: Sam Lapere
published: '2012-03-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Same physics bricks + shooting as in the previous post, but now with a light emitting sphere (mesh lights are particularly hard for a path tracer and a dreaded source of noise). All videos and screenshots were rendered on 2 GTX 580s with 20 spp/frame.

Video:

[http://www.youtube.com/watch?v=bbg_KOZhdKM](http://www.youtube.com/watch?v=bbg_KOZhdKM)

And an interior scene

Video:

[http://www.youtube.com/watch?v=wTJ1cjyVQRU](http://www.youtube.com/watch?v=wTJ1cjyVQRU)

Glossy bricks:

The sense of realism in this scene when all the bricks are moving is totally out of this world.

For my next demo, I'm planning to make a very simple first person shooter game with this scene. You will have the choice between two powerful weapons: the














**UTL**(Utah Teapot Launcher) and the**SBL**(Stanford Bunny Launcher). I may throw in an animated character as well (I'm thinking of the Amiga juggler).**someone asked me to create an interior scene with the falling tower of bricks which is only illuminated by a light emitting sphere. The results are pretty cool:**__UPDATE:__[http://www.youtube.com/watch?v=V-8pFdQeWqA](http://www.youtube.com/watch?v=V-8pFdQeWqA)

__: first person shooter gun is in and working (it can shoot projectiles with physical weight):__**UPDATE 2**
## 7 comments:

Hi Ray, did you try to tweak physics a bit? Like scale of scene or substeps or something? Or it is not important at his point?



And do you have any ideas, possibilities (some techniques and papers) on how make creating bvh tree faster?

And btw nice videos! Specialy scene with light sphere and bricks outdoor is beatiful..

Hi,




yep, I tried everything you can imagine. When building a new physics demo, I always use Bullet's built-in OpenGL debug drawer, in which the physics usually work flawlessly. I copied the exact same parameters for ground size, timestep, maxsimsubsteps, contact processing threshold, ... everything to the demo in Brigade but I'm still having these weird issues when many blocks hit the ground at the same time. I might switch to a different physics engine, but it's not a priority at this point.

For faster BVH, I would say Rasterized BVH by Novak and Dachsbacher (it came out last month), BVH for animated scenes by Kopta et al. or HLBVH with work queues by Garanzha which builds the BVH on the GPU.

Thanks btw, I personally like the indoor scene better :-)

noo don't switch, Bullet is awesome =). For your block issue, why not just have time spawn closer to the floor, so they won't land as hard(that should give you a nice tower)

Can't you simply do more than one simulation step per frame? That shoudl also make the simulation more stable.

I wish to have first person shooter style controls in Brigade it would make moving around a joy.


W,A,S,D for moving and mouse for looking around.

Awesome results!

Will the engine be open source?

@ anonymous 1, 2, 3: I'm looking into the physics issue asap. WASD controls are already in, it's what I'm using in the videos btw.


@ jedi89: the path tracing kernels in Brigade will probably not be open sourced, only the game portion is open source and can be downloaded with precompiled rendering libs at http://brigade.roenyroeny.com/

Post a Comment