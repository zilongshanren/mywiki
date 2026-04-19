---
title: Portals are misunderstood.Portals, cells, predicated rendering and their mirrors.
url: https://c0de517e.com/011_portals.htm
author: Angelo Pesce
published: '2013-02-17'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

It's not hyperbole to say that there isn't a visibility system known to real-time rendering, that can beat cells and portals in terms of efficiency, for heavily occluded scenes (e.g. architecture, indoors).

Yet portals seem to have fallen somewhat out of fashion "lately" - likely due to the game maps becoming bigger and more varied. Hardly there are games that happen entirely indoors, quite some time has passed since Doom! Yet, portals are simple enough and can work easily enough that probably should be an option for most visibility systems.

I blame Carmack (or Abrash - not sure) - for being too influential! And for his love of BSPs!

**A quick history tour.**
It all starts with Doom (true in so many ways...), the

[BSP there](https://fabiensanglard.net/doomIphone/doomClassicRenderer.php) provides perfect front-to-back sorting and clipping to enable zero-overdraw rendering.

Moving from barely 3d must optimize "filling" routines as much as possible, to true 3d, triangles, and all in Quake, the BSP is still the protagonist.

There it's used to divide the world into cells (convex areas), and then

[precompute](https://fabiensanglard.net/quakeSource/quakeSourceRendition.php) the

[cell-to-cell visibility](https://www.youtube.com/watch?v=IfCRHSIg6zo) (a PVS) using the edges between cells (portals) during map compilation. Then, in software rendering the visible cells triangles (after frustum) are drawn back to front (BSP again!) using a span buffer to avoid overdraw and do the expensive filling still without overdraw. If a GPU is present (GLQuake), then the hardware z-buffer will deal with everything.

![From real-time rendering.](../../assets/425aa5916d12b163.png)

From real-time rendering.
Doom 3 takes similar concepts: the BSP, cells, and portals, but

[uses them in runtime](https://fabiensanglard.net/doom3/renderer.php): you start with the camera frustum, the current cell the camera is in, and then test each portal of the cell against the frustum.

If a portal is visible, one can clip the frustum with it (shrinking it), then use the resulting planes (it's not going to be a frustum anymore unless one bounds the results of the clip with one) to cull the content of the connected cell, and so an so forth, recursively.

This is now far from perfect, zero overdraw visibility, you can even decide where the portals are - it's not compulsory for them to be all the connecting faces between convex areas - and you can use them to cull all the objects inside a cell. The idea is that you will have lots of 3d objects (meshes) inside a room, and you want to cull these. There's no doing things per triangle, we're in the land of work amplification: draws->triangles->pixels.

And this is what, I think, today most people think when they think of portal-based visibility.

![Portals in the Hammer (Source engine) editor.](../../assets/acd68a3a2df7d6a8.png)

Portals in the Hammer (Source engine) editor.
Portals are associated with levels made with "BSP brushes" (convex solids), that then are automatically fused (boolean union) by a map compiler. Certain brushes are placed and marked by the artists as portals. Doors will have portals, windows, sections of corridors, and so on. Hammer, UnrealEd (the original!), Radiant - google portals and "map optimization" for any of these "classic" editors and you'll find (still) a ton of tutorials on how that workflow is supposed to look like.

Nothing wrong with CSG-based level editing, it can be an amazingly productive way of blocking out levels, typically followed by "set decoration" where detail mesh geometry is added.

In theory, nothing wrong even with automatically determining cells at map building and objects inside them - even if in practice there are often annoyances due to the finicky nature of CSG (precision issues, especially when you have to guarantee that an entire level merges correctly and always have a well defined inside and outside).

FWIW and AFAICT Unreal Engine 4 BSP-based editing was

[still supported](https://docs.unrealengine.com/4.27/en-US/Basics/Actors/Brushes/) even if I don't think it was used for visibility (and the same seems true for UE3). In UE5 it seems that a new mesh-based level editing system was added, replacing the BSPs, but I imagine many of the good parts of that workflows were preserved.

But, bottom line, a certain kind of games (content), a certain kind of level-editing is coupled with portals, and it does not need to be.

**Portals are predicated rendering!**
Fundamentally, portals are a simple form of predicated rendering: if the portal is visible, then render this set of geometries. One can do this recursively - a portal can be associated with other portals - so if we "enter a branch" other tests might be performed. That's all.

A "cell" then, at its most minimal definition, is a set of objects that should be rendered only if at least one of the portals that reference the cell is visible. Technically, it also always needs to define a volume - we have to know if we are inside a cell (in that case, we don't need to test the portals for it, its objects have to be considered visible), but even that is predicated rendering, and the volume does not need to be a tight bound.

None of the predicates need to be tight. Portals don't need to exactly correspond to openings - disocclusions, they can bound them (be bigger) and that would cause only some loss in culling efficiency, but not in correctness.

This interpretation opens the door, in my view, to many different workflows! Imagine an engine that works on collections of meshes, triangle soups, nothing fancy or solid. One could have a building, modeled in whatever way... An artist could select all the objects, rooms, and walls inside the building, and say (express): if we are outside the bounding box of the building, and none of the windows (portals) are visible, all of these objects should not render.

Portals can move! "If none of the windows of this car are visible, nothing of the interior should render" - and so on. In fact, this idea is quite conducive to a GPU-based implementation!

**Antiportals and occluders.**
Here things get even more funny (for my sense of humor at least). Portals express disocclusions very efficiently, but in many cases, levels are not made of tightly bound areas with a few openings - they are not heavily occluded.

In these cases, trying to capture visibility via portals is quite painful. Imagine even a room with a big feature, say a piece of furniture, a cabinet, in the middle. For a traditional portal system to be able to occlude objects behind it, one must divide the room into sections (cells) around it, and then place portals between each. Both painful and inefficient.

For this reason, many portal-based engines also offered the idea of "antiportals", areas that can be marked as occluders. But because all of this was in the times of BSPs, exact geometric operations, and the like, typically the antiportals are limited to

[simple geometries](https://docs.unrealengine.com/udk/Two/LevelOptimizationAntiportals.html), planes or convex volumes, that can then be extruded from the camera point of view into frustums and participate that way to culling objects behind them, and other portals.

Some engines then started to use antiportals only, especially if they were more open-world, more about levels without many occlusions. Then, we imagined using

[software rasterization for occlusion culling](https://fgiesen.wordpress.com/2013/02/17/optimizing-sw-occlusion-culling-index/), in part to allow for arbitrary geometry to be used as occluders (but typically, still artist-made as budgets are limited) and because it's (relatively) hard to "fuse" frustum-based antiportals (requires going to the pain of a beam-tree) - i.e. account for the effects of multiple antiportals on objects that might be occluded when considering them together, but are not by any single one of them.

![From Unreal Engine 2: antiportals and the problem of not fusing them.](../../assets/40ff0dfe6d73a8bc.png)

From Unreal Engine 2: antiportals and the problem of not fusing them.
Anyhow. Going down this path, we went from BSPs to portals to antiportals to software raster, and for the most part, it seems we have not noticed that the two concepts are dual of each other, and work great with one another! Or maybe it was just me...

At the most basic level, if a set of objects (e.g. bounding volume) is fully behind an occluder (or a set of occluders) - then the objects are not visible. It's the opposite test - we test objects against occluders instead of testing for portals to enable objects. It expressed the opposite concept: occlusion versus disocclusion. And it "relaxes" in the opposite direction - a proper occluder should be fully inside (inscribed) visible geometry, while a proper portal should be fully outside (circumscribe) the hollow area it marks.

![From Intel's software occlusion culling rasterizer demo.](../../assets/49ffd0c99e3a6af6.png)

From Intel's software occlusion culling rasterizer demo.
**Bottom line.**
(Especially) in the world of artist-authored "map optimization", creating simplified geometry for occlusion culling, or marking big objects for that - one should probably consider adding the ability to express portals and cells.

In runtime, both work with each other, and it's trivial for raster-based occlusion systems. Just raster (test) the portal, and voila' - you know if it's visible or not. If it's visible, raster the cell's occluders, and add all of the cell objects (meshes and other portals) to the list of things to be tested next - rinse and repeat.

Have fun!