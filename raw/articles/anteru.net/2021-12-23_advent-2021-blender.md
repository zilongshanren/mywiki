---
title: 'Advent 2021: Blender'
url: https://anteru.net/blog/2021/advent-2021-blender
published: '2021-12-23'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’ve never been a good 3D artist, but I’ve been always interested in 3D content creation. I’ve used quite a few 3D packages over the years, but these days, there’s only one I’m using: Blender. I’ve known about it from back in the day when the source code was bought off NaN for € 100.000, but I didn’t warm up to it until much later. During my years at the university I used it to process some 3D meshes and eventually ended up organizing a lecture on 3D modelling with Blender (to be clear: I was just organizing the lecture, a proper 3D artist was taking care of the Blender side.) That made me sit down and seriously learn Blender, which resulted (among other things) in me recreating the Shelter13.net header image. That was around 2012 with an updated version in 2014.

This year, we arrived at Blender 3.0, and it’s been an incredible development. What started as a humble 3D tool with a very own and opinionated way to do things has become a fully-featured 3D package, with a state of the art rendering engine, compositing tools, and modern scene management tools. Back in the day when I started using Blender building bigger scenes was quite tricky, but now Blender ships with all the tools you need to assemble complex scenes from parts. That’s also what I like about Blender the most: It’s easy to use for simple tasks, but it can handle demanding workloads, and having all in one package is fantastic.

The most exciting recent development for me personally are the “geometry nodes”. There’s a fun story here with the Shelter 13 model, where the railing on the roof is instantiated along a curve. That was one thing that was always tricky to do in Blender, especially when you compared it to other 3D packages which shipped with a “instance along curve” feature for years (decades even…) However, with Blender 3.0, this is not only fully supported, but also in a fantastic framework that allows you to do all sorts of complex, rule based instancing (including instancing along curves!)

Geometry node network used to construct the vertical bars on the roof

I took the opportunity to update the whole scene to Blender 3.0 and update and re-render it. It’s great to see that I can do so much faster now and at higher quality due to the Cycles X render engine, which is an incredible improvement over cycles from a few years back.

Shelter 13 mesh rendered with an override material

Blender is also getting traction for “serious work”, and given with the sustainable business model, I’m optimistic we’ll see Blender thrive and grow in the coming years. If you haven’t used it before, now is the time, because this is really as good as it gets for 3D content creation, and it’s all open source and free!