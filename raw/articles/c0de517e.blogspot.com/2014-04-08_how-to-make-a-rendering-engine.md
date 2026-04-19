---
title: How to make a rendering engine
url: https://c0de517e.blogspot.com/2014/04/how-to-make-rendering-engine.html
published: '2014-04-08'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Today I was chatting on twitter about an engine and some smart guys posted a few links, that I want to record here for posterity. Or really to have a page I can point to every time someone uses a scene graph.

Remember kids, adding pointer
indirections in your rendering loops makes kitten sad. More seriously,
if in DirectX 11 and lower your rendering code performance is not bound
by the GPU driver then probably your code sucks. On a related note, you
should find that multithreaded command buffers in DX11 make your code
slower, not faster (as they can be used to improve the engine
parallelism but they are currently only slower for the driver to use,
and your bottleneck should be the driver).

**Links below**are all about the idea of ditching state machines for rendering, encoding all state for each draw and having fixed strings of bits as the encoding. I won't describe the concept here, just check out these references:

- Christer Ericson's article
[http://realtimecollisiondetection.net/blog/?p=86](http://realtimecollisiondetection.net/blog/?p=86) - Aras on using bits for rough z-sort
[http://aras-p.info/blog/2014/01/16/rough-sorting-by-depth/](http://aras-p.info/blog/2014/01/16/rough-sorting-by-depth/) - FR's Werkkzeug
[https://github.com/farbrausch/fr_public/blob/master/werkkzeug3/engine.cpp#L3757](https://github.com/farbrausch/fr_public/blob/master/werkkzeug3/engine.cpp#L3757) - BGFX engine
[https://github.com/bkaradzic/bgfx#what-is-it](https://github.com/bkaradzic/bgfx#what-is-it), see[https://github.com/bkaradzic/bgfx/blob/master/src/bgfx_p.h#L614](https://github.com/bkaradzic/bgfx/blob/master/src/bgfx_p.h#L614) - MT Framework - japanese, cedec2006 (there are translations around as well)
[http://game.watch.impress.co.jp/docs/20070131/3dlp.htm](http://game.watch.impress.co.jp/docs/20070131/3dlp.htm)[http://game.watch.impress.co.jp/docs/20070131/3dlp19.htm](http://game.watch.impress.co.jp/docs/20070131/3dlp19.htm) - Intel Nulstein sample
[http://software.intel.com/en-us/vcsource/samples/nulstein](http://software.intel.com/en-us/vcsource/samples/nulstein) - I wrote something about this on my blog a long time ago, but it's a bad article and I won't link it here :)

**Some notes / FAQs answers.**Because every time I write something about these system people start asking the same things... I think because so many books still talk about "immediate" versus "retained" 3d graphic APIs and the "retained" is usually some kind of scenegraph... Also scenegraphs are soooo OOP and books love OOP.

- Bits in the keys are usually either indices in arrays of grouped state (e.g. camera/viewport/rendertarget state, texture set, etc...) or direct pointers to the underlying 3d API data structures
*So we are following pointers anyways, aren't we?*Yes of course, bu**t the magic is in the sort,**it not only will help minimize state changes but also guarantees that all accesses in the arrays are (as-)linear(-as possible)!- Of course if you for example sort strictly over depth (not in depth chunks), then you have to accept to jump between materials at each draw, and the accesses over these might very well be random.
- If that's the case try to avoid indirections for these and store the relevant data bits directly in the draw structure.
- Another solution for this example case is to sort the material data in a way that is roughy depth coherent, i.e. all materials in a room are stored near each other. In theory you could also dynamically sort and back-patch the pointers to the material data in the game code, but we're getting too complex now...
- The same can't be guaranteed for resource pointers (GL, DX...), even if the pointers will be linearly ordered they might be far away in memory, that's unavoidable. On consoles you have control on where resources are allocated even for GPU stuff so you can pack them together, but even more importantly you can directly store the pointers that the GPU needs w/o intermediate CPU data structures
- You don't need to have a single array of keys and sort it!
- Use buckets, i.e. some bits of the key index which bucket to use. Bucketing per rendertarget/pass is wise
- "Buckets", a.k.a. separate lists. In other words don't be shy to have a list per subsystem, nobody says there should be one solution for all the draws in your engine.
- This is usually a good idea also because draw-emitting jobs can and should be sequenced by pass, e.g. in a deferred renderer maybe we want first a rough depth-prepass, then g-buffer, then shadows... These can be pulled in pass-order from the visibility system
- Doing the emission per pass means we can kick the GPU as soon as the first pass is done. Actually if we don't care for perfect sorting, and we really care about kicking draws as soon as possible, we can even divide each pass in segments and kick draws as soon as the first segment is done.
- I shouldn't say it but just in case... These systems allow to generate draws in parallel, obviously, and also to sort in parallel and to generate GPU commands in parallel, quite easily. Just keep lists per thread, sort per thread, then merge them all (the only sync point) then split in chunks and per thread create GPU command lists (if you have an API where these are fast...)
- You don't need to use the same encoding for all keys!
- Some bits can decide what the other bits mean. Typically per rendertarget/pass you need to do very different things, e.g. a shadowmap render pass doesn't need to care about materials but might want to use some more bits as a z-key for depth sorting
- Similarly, you can and should have specialized decoding loops
- Not all the bits in the key need to be used for sorting
- Bits of state that directly map to the GPU and don't incur in overheads from setting them, should not be part of the sorting, they will just slow it down.
- Culling: make the keys be part of the visibility system
- When a bounding primitive is finally deemed to be visible, it should add all the keys related to drawing its contents
- At that point you want also to patch in the bits related to the projected depth, for depth sorting
- Hierarchical transforms
- Many scenegraphs are used as a transformation hierarchy. It's silly, on most engines a tiny fraction of objects need that, mostly the animation/skinning system for its bones. Bones do express a graph, but it's not enough of a reason to base your -entire- rendering system on it.
- Group state that is (almost) always set together in the same bits
- E.G. instead of having separate bits (referring to separate state structures) for viewport, rendertarget, viewworldprojection constant data and so on, merge all that in a single state structure.
- Won't I need other rendering "commands" in my list? Clears? Buffer copies? Async CPU jobs waits? Compute shaders? Async compute shaders...
- All of these can be part of "on bind" properties of certain parts of the state. E.G. when the bits pointing to the rendertarget/pass change we look up in that state structure to see if the newly set rendertarget have to be cleared
- In practice as you should "bucket" your keys into different arrays processed by different decode loops, these decode loops will know what to do (e.g. the shadowmap decode will make sure the CPU skinning jobs are finished before trying to draw and so on)
- Are there other ways?
- Yes but this is a very good starting point...
- Depends on the game. A system like this is good when you don't know what draws you'll have, typically because they come from a visibility system which can't spit them in the right order and/or because of parallel processing.
- Games/systems where you can easily generate GPU commands in the right order and you exactly know which state changes are needed, obviously can sidestep all this architecture. E.G. Fifa, being a soccer game, doesn't need to do much visibility and knows exactly how each player is made in terms of materials, thus the code can be written to exactly process things in the right order... Something like this would be reasonable for Frostbite, but you won't use Frostbite for Fifa...

## 2 comments:

Really interesting post.

The engine I work on at work is far from what you do expect from a 2014 engine.

This post will give us some clues to improve it!

What you seem to want seems quite like Goal. See http://art-of-optimization.blogspot.com/2014/06/the-legacy-of-goal.html

Post a Comment