---
title: 'From the archive: Vegetation in COD:BO4.Another tale of twists and turns in
  R&D.'
url: https://c0de517e.com/015_vegetation_system.htm
author: Angelo Pesce
published: '2014-03-10'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

Welcome to another entry in the "from the archive" series, where I finally get around writing about stuff that there was no time to present back when it was made, hoping nobody gets upset and that my memory of things has not entirely evaporated. And I can call it now a series, having written this, which is the second post :)

I guess it's also "timely" considering that Black Ops 6 just came out (and it seems it's going to be a smash hit). For context, BO4 was... let me count... six call of duties ago!

**Setting the stage.**
The common wisdom is that COD never changes, it's simply a thin new skin over the same game and codebase. Of course, the common wisdom is... entirely wrong.

Of course, a franchise is a franchise, and I don't imagine there will be an RPG or platformer with the COD name anytime soon, but, in no small part due to having different studios alternating at the helm of development, each game in my experience brought significant innovations.

And after a bit, you might even start noticing the uniqueness in each studio culture, and way of working. For me, from my limited vantage point, Treyarch was "the crazy one".

I have to emphasize the limits of my POV: I never believed it is possible to understand a large, multifaceted production as a whole, even from within, and I certainly did not see most of it, sitting in Vancouver and working only on the technological side. That said...

Why do I say "crazy"? Well... The first Treyarch COD I helped on was COD:BO3, the studio's first entry for a new generation of consoles, the Ps4/XB1 era.

In BO3, not only Treyarch changed pretty much everything in how the game was rendered (going from forward to deferred, from

[lightmaps to volumes](https://research.activision.com/publications/archives/volumetric-global-illumination-at-treyarch), adding

[OIT and software particles](https://research.activision.com/publications/archives/atvi-tr-16-02practical-order-independent-transparency), removing lots of arcane magic from the level baking process, going to GPU instancing etc etc), how it was created (rewriting large parts of the editor and workflows) and how it was played (BO3 shipped with a ton of game modes, including a coop campaign for the first time)... but what really surprised me at the time was the willingness to take risks and accept changes up to the very last minute.

I specifically remember making some improvements in the lighting system that I thought were never going to ship, as what I had already committed was good and the new code would alter the look of all levels in the last few weeks we had to complete the game, and the leads just eagerly taking the changes.

It was no surprise then that for BO4 when it was decided not to have at all a single-player campaign in favor of adding a new battle-royale option, the team jumped on the opportunity. This was huge. Call of Duty is, famously, a "corridor shooter" - made for relatively small, cramped urban maps, not an open-world engine!

The team managed to "pivot" the tech in record time, and BO4 shipped at launch with battle royale, a feat that the same year will not be matched by Battlefield V (which will ship the mode months later, as an update), even if EA's title has always been about much larger maps than COD!

![COD:BO4 "Blackout" battle royale.](../../assets/50667dfaecadb843.png)

COD:BO4 "Blackout" battle royale.
Treyarch needed to figure out what the mode would look like (and I can assure you, many ideas were prototyped) and how to make it work in the engine.

After the dust settled enough on the gameplay for the mode, we knew that we needed to focus on a new, large terrain system and its biomes.

**Design prototype.**
IIRC, when Central Tech was called in to help, we had already a prototype to show how the system was supposed to work. Treyarch made a new terrain system and had something working in the editor to place vegetation on top of it, using artist-painted density maps and procedural rules - and they were happy with the overall workflows.

There were three main problems to solve:

1) The prototype went out of memory on console... simply trying to load the data files with the locations of all the procedurally created objects!

2) Editing was less than interactive... The performance of the procedural generation was poor.

3) Quality/variety of the patterns used for distributing objects could improve.

You might have spotted that runtime performance is not on the list! Treyarch's engine moved to an instancing-based solution that year, and already for BO3 there had been a lot of work on the streaming system, and COD tends to be quite efficient to boot.

Another researcher, Josiah, worked on improving the geometry LOD / impostor system he created to account for vegetation and bigger maps, but that's another story.

The key part of the prototype was about how placement was supposed to work with painted density maps on the terrain. Treyarch went for a solution that allowed multiple layers, in a stack.

Each layer could then influence the ones below, at the very least "occluding" them, but ideally also in other ways.

For example, you might have placed big trees in the top layer, driven by the density map, and that got evaluated first, deciding where to place the tree instances. The objects would be placed checking that they could not intersect each other. Then a second layer might have been, say, big boulders - and you don't want a rock to intersect a tree, so the tree layer could be set to "inhibit" the layer below in a radius around each placed tree. A third layer might have been smaller rocks, and you wanted them not to intersect either the trees or the boulders, but favor clumping around the latter, so the boulder layer would act as negative density bias up to a given radius around a placed boulder, and then a positive bias in a small ring after that. And so on...

So, we had already lots of the pieces in place, which helped a lot, especially as we were helping from outside the studio. In total I think this vegetation effort ended up taking four engineers from Central Tech: Josh and Ryan on the actual implementation for the engine and editor, Wade made the engine system for grass on the terrain, and myself to R&D the algorithms for scattering and the visuals of the grass (i.e. shaders).

**The elephant in the room & the road not taken.**
Imagine being tasked with working on vegetation in 2018. There is no way your first thoughts don't go to the lush forests of Guerilla's 2017 Horizon Zero Dawn in their

[real-time procedurally generated glory](https://www.guerrilla-games.com/read/gpu-based-procedural-placement-in-horizon-zero-dawn).

![Love!](../../assets/d557b6c6c77c8551.png)

Love!
And so of course I went to look! If procedural placement is slow, we'll make it real-time, right? Well, to be honest, I did not get it...

It might be because I did not see their GDC presentation live, unfortunately - it might be that I'm not that smart, but I didn't fully grok it.

I appreciated the idea of using dithering for placement, good dithering is in practice an exercise in generating blue-noise distributions of variable density (even the old Floyd-Steinberg is fundamentally that), but overall I didn't fully grok it.

Moreover, it seemed to me it did not work under the same assumptions of having the placement of given objects directly affect the placement of others, I think they effectively "emulate" the same idea by virtue of being able to manipulate the density maps, but as far as I can tell, it does not work at the object level.

I had an idea in my head to make a sort of rasterizer, writing to a bitmask, to mark areas that are already occupied in a given vegetation tile. This idea of using bitmasks on the GPU is somewhat popular today, Martin Mittrig did an excellent summary

[in this EA SEED presentation](https://www.ea.com/seed/news/coverage-bitmasks), but at the time I was mostly inspired by the vague recollection of

[this blog post](https://web.archive.org/web/20160601104858/http://ginsweater.com/blog/2014/03/10/the-littlest-cpu-rasterizer/) (which I always struggle to find when I need it) where the author computer AO for a voxel world making a tiny, bitmask-based, CPU cubemap rasterizer.

![Jotting down the idea of using bitmasks.](../../assets/00492421418c9f25.png)

Jotting down the idea of using bitmasks.![Thinking about how it could work...](../../assets/ea0b23e4cf55680b.png)

Thinking about how it could work...![Realizing that the "pixels" can be entirely virtual, we could associate bits to irregular shapes.](../../assets/a6844c4890e21f02.png)

Realizing that the "pixels" can be entirely virtual, we could associate bits to irregular shapes.
I spent a bit of time on pen and paper trying to make this idea work, but ultimately ended up shelving it. Albeit I was persuaded it could work, I simply did not see the use.

It is tricky to "linearize" research into a timeline - exploration and exploitation alternate in the search of viable techniques, it looks much more like a (real-world) tree... But relatively soon it became apparent that it was unlikely we would need real-time generation - and to this day, I don't fully appreciate the appeal.

On one hand, I was working on the placement algorithms, and it seemed to me that we could efficiently store the results, directly, without needing to evaluate the logic in runtime. Remember that I mentioned someone was working on a grass system? That was a parallel decision that helped a lot - in the original prototype, there was no specialized grass rendering, but we knew pretty early on that we wanted to integrate that directly with the terrain system. Once the grass was out of the way - the number of instances we had to deal with decreased by orders of magnitude...

![COD's "radiant" editor.](../../assets/8a2cdbd2983649b9.png)

COD's "radiant" editor.
**Placement logic.**
If you are asked to place objects in a way that they don't self-intersect, you'd likely think of some minimum-distance guarantees, which leads to blue-noise point set generation ideas. The tricky part here is though that we wanted to have objects in layers, where each layer entailed a different size/minimum distance, and remember as well that we needed to check for the logic that makes layers "talk" to the ones below.

![I doubt anyone can read my notes...](../../assets/3f5475c3a36b53a6.png)

I doubt anyone can read my notes...
My first instinct was to create a point set that is "hierarchically" blue-noise, meaning that as you add more and more points, these look still blue-noise, but they become denser, and thus, the minimum-distance they guarantee shrinks. This property is guaranteed implicitly by Mitchell's best-candidate algorithm (where we generate each iteration a number of random candidate point locations and then we add to the point set one that is furthest from any other point in the set) - but we can do better than that!

![Mitchell's best candidate point generation.](../../assets/940cefe1e8d99eab.png)

Mitchell's best candidate point generation.
Let's think about it. First of all, for any point set - in any random order, we can compute how as we add points from it the minimum distance between the points decreases. So, having a decreasing minimum distance is not the objective, that is a given! What we can optimize with sorting and/or proper point location is how gradually the distance decreases. Or, in other words, how many points we can use for objects of a given size.

![Is this art? https://www.instagram.com/p/Bjf_PWWFxCJ/ No...](../../assets/5f2c7493e27f86eb.png)

Is this art? https://www.instagram.com/p/Bjf_PWWFxCJ/ No...![...it's the visualization of a small program that tries to generate point sets with as-gradual-as-possible minimum distance decrease](../../assets/567d1024188ca4d1.png)

...it's the visualization of a small program that tries to generate point sets with as-gradual-as-possible minimum distance decrease
This ends up being quite tricky to write down in a way that we can perform numerical optimization on the point locations themselves, but no worries, it won't matter. Quite simply we can take any point set and sort it to make it incremental in the sense of minimum distance. And a good heuristic on how to do the sort is provided by the best-candidate algorithm itself! Simply use the same idea, but instead of generating random candidate points, take them from the fixed, existing set. If you want the optimal sorting, you have to try N times, once per every possible point in the set as the initial one to pick. It takes time, but we have to do it only once!

Solved? Done? Not quite! In fact, this whole thing went to the trashcan, but no worries - we didn't waste time!

All this idea of building a fixed point set that we could tile, and use to guarantee non-self-intersection of objects of different sizes was still under the assumption that we needed to generate placements very fast, on the GPU! But it turns out, as the other engineers started to implement tiled, parallel updates on the prototype code, we figured out that we probably did not need to be that fast!

In fact, after a few optimizations to the collision detection/cross-layer influence system (circle-circle intersection and circles-to-point distance queries), even on CPU we already had something interactive enough for artists to use! In the end, we would have CPU and GPU compute implementations for the editor, but by the time we had the final placement algorithms, the latter ended up being somewhat overkill.

Once we became unshackled by the requirement of doing everything in runtime, it was easy to decide that to accommodate objects of different sizes - each in its own layer - we could simply use different-sized tiles per layer, effectively, scaling up or down the point set in world space, so that we can always use the whole set, and we need only to "remove" points to accommodate for the variable density as painted from the artists. And we made layers able to have multiple 3d models associated with them - as long as they were of similar size and needed to respect the same placement logic - to provide more variation with an easier workflow.

![Same as the paragraph above, "encrypted".](../../assets/69703e478a0c843e.png)

Same as the paragraph above, "encrypted".
**Making it not boring.**
So now we had something simple, working, and fast. The point ordering ended up being re-used to determine if a given location passed or not the density-map threshold test: for each point, we sampled the density map and computed the number of points that we theoretically would have enabled in the tile if that density value was constant across it.

If the current point index is < that number, we enable it, otherwise, we don't. This is the same as saving a threshold activation value per point, and making sure that each point has a unique one, but it does not require saving said threshold.

![](../../assets/c429200265247e8f.png)

This idea is also very similar to an ordered dither pattern. And exactly like a dither pattern, the order of the points creates different "styles".

![](../../assets/aaa4643d33742652.png)

Now we have all the components in place. First, we start with a fixed point set. In practice, to give more control, artists could alter the positions per layer a bit - I ended up generating a noisy set with Mitchell's best candidate, and then moving the point locations with a relaxation algorithm to distribute them more uniformly (note that if you relax too much you end up just with a hexagonal grid, as hexagonal packing is optimal for circles in a plane) - and layers had a value to interpolate between the two.

![Point locations from best-candidate, and relaxed.](../../assets/563527803bab7b00.png)

Point locations from best-candidate, and relaxed.
Then, we compute different orderings - permutations - of the point set, which will create different styles that can be selected, again, per layer. I think we ended up with a handful of options there, but I created an app to explore sorting variants and their parameters, with which technical artists could then pick the styles they wanted.

The app itself was cute, C++ using something like a graphical "printf" system - you could pass to a function a lambda with the drawing code, the lambda would receive the window inputs and execute in a separate thread, but that's also a story for another day.

![This is how the "max-spacing" style looked at 20, 40, and 60% constant density in a tile.](../../assets/5af644bcca292c31.png)

This is how the "max-spacing" style looked at 20, 40, and 60% constant density in a tile.
![Random permutation.](../../assets/19819b3cef18f89c.png)

Random permutation.
![Alternating maximum-distance point choice with minimum-to-last added: forces clumping.](../../assets/8ec45345b942351c.png)

Alternating maximum-distance point choice with minimum-to-last added: forces clumping.
![Same, but choosing a random number of points to clump in the minimum-to-last distance loop.](../../assets/9defc3cdd2dd6b95.png)

Same, but choosing a random number of points to clump in the minimum-to-last distance loop.
![Clumping around a randomly selected anchor, not the last added point.](../../assets/8509976aa21a2bf6.png)

Clumping around a randomly selected anchor, not the last added point.
![String-like clumps.](../../assets/b98a0c1d2496a824.png)

String-like clumps.
**Storage.**
Now that we have a good way to distribute instances, we only need to solve storage. Because we did all this work to be able to use only a handful of preset point locations the storage is trivial. Once we did all the logic to remove self-intersections and account for layer-to-layer influences, we ended up needing only the layer parameters and a bitmask per layer per tile. Note that we don't even need, in runtime, the various permutations used for "style" - these are needed only in the editor when the density maps are evaluated!

The bitmask is already reasonably small, in fact, smaller than storing density maps unless we use very small objects (remember, we scale tile size based on the object size, so the smaller the object the more tiles we'll have in the world). But we can do better with simple run-length encoding on top.

We sort the point set one last time - for storage. In this case, we want them in an order that preserves spatial locality, because we can imagine that even with the various dithering styles and density maps and complex logic, we often end up with patches of dense point areas and barren areas, over the map. We can use a space-filling curve to sort the points, or we can run a "traveling salesman" optimizer.

I don't remember which one I ended up using, probably the latter, but I'll put here some more hand-drawn diagrams of when I was trying to figure out beta-omega curves, which are the state-of-the-art:

![](../../assets/2be180ce1d843732.png)

![I was going slightly mad...](../../assets/e1c3bdabf2509d75.png)

I was going slightly mad...
Storing this way also ends up being a slight win rendering-wise, as the instances you'll create are spatially compact and that's a good property in a variety of settings.

![This incomprehensible mess was a debug visualization of the spatial "runs" and "breaks" in the encoding. I think.](../../assets/cb662fa7f04b5f26.png)

This incomprehensible mess was a debug visualization of the spatial "runs" and "breaks" in the encoding. I think.![Same. Maybe? Who remembers :)](../../assets/911603755280a111.png)

Same. Maybe? Who remembers :)
**Putting it all together.**
![Tiles over a density map and resulting instances.](../../assets/53ebbf09b415621e.png)

Tiles over a density map and resulting instances.![More testing...](../../assets/79e2ea29f1a96c9b.png)

More testing...![This I think was from actual game terrain data.](../../assets/cabba66294725dd7.png)

This I think was from actual game terrain data.
![Blackout map.](../../assets/5b920598bced2995.png)

Blackout map.