---
title: Trailer of Brigade powered real-time path traced game "It's about time"!
url: http://raytracey.blogspot.com/2012/02/trailer-of-brigade-powered-real-time.html
author: Sam Lapere
published: '2012-02-03'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Today, the Brigade developers released an astonishing trailer for "It's about time", a puzzle game set in an Aztec city which is real-time path traced using the Brigade 2 engine.

Some of the features that are showcased in the video:

-

__dynamic day/night cycles__: with this technology, high quality precomputed light maps like the ones used in Mirror's Edge (which by far has the best static lighting in a game) are no longer needed. Pixel-perfect soft or hard shadows and indirect lighting are calculated on-the-fly
-

__real-time path traced diffuse color bleeding:__no instant radiosity or derivatives are used, which only affect
-

__real depth-of-field:__no z-buffer based post-process hack, but the real thing computed by stochastically jittering the origins of eye rays to simulate a physical lens
-

__real raytraced ambient occlusion__: no screen space AO using the depth buffer
- dynamic objects receive the exact same direct and indirect lighting as their environment and their material properties can also affect their surroundings

- an unlimited number of lights can be used

- reflections/refractions/glossy surfaces don't seem to be used in this video but can be handled effortlessly as shown by the Reflect game (reflective spheres, glass tubes)

Long stretched shadows are rendered with pixel-perfect accuracy, which is plainly impossible with today's rasterization based shadowing techniques:

Reddish diffuse color bleeding + true raytraced depth of field:

An overview of the game world:

It's evident that real-time path tracing is a feasible option for games with many outdoor environments, even today. With some selective filtering of diffuse indirect lighting, even indoors shouldn't be too problematic when avoiding pathological cases such as a room that is only lit by light coming through a narrow opening.

The ease of creating a game with this tech is unrivaled: artists don't have to worry about wrong looking or badly aliased shadows, reflections, transparency or any combinations of those. It will look just as expected right out of the box. There would also be no waiting time (for baked lighting) between iterations any longer.

To end this post with a cheesy conclusion: Yes, we are witnessing the future of real-time game graphics today! It's about time really.

I really can't wait to play this game (and mod the hell out of it).

## 5 comments:

Waiting for release :)!

This is looking awesome.

In just 2 years I'm pretty sure it will be mainstream.

I'm curious if the next-gen consoles will manage to deliver path-traced rendered games...

Yes, in 2 years GPUs will have enough power (and maybe also contain some fixed function ray tracing HW) to run complex outdoor games using an optimized form of real-time path tracing. Consoles... not so much :)

I'm pretty sure it will be mainstream.

This movies is fab i like to recommend you to watch that em sure you will enjoyed really...



and try to visit with your own self like

Cheap Flights to PakistanPost a Comment