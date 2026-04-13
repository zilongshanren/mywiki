---
title: What I've learned from shipping a deferred lighting renderer
url: http://c0de517e.blogspot.com/2011/09/what-ive-learned-from-shipping-deferred.html
published: '2011-09-08'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- You're going to draw every mesh three times on average (considering shadows), if you don't fuck up the GPU badly, chances are that you're going to be CPU bound.
- Cache-misses in your rendering pipeline are going to kill you.
- Use indirections VERY sparingly. Control where resources can be created and destroyed to be able to avoid to have to reference count everything. Prefer "patching" pointers in place to keeping references around.
- Don't iterate multiple times on "drawable" objects collections to isolate which ones to draw in each pass. Store only the draw data needed for a given pass. Scene trees are dumb but by now everyone should be well aware of that.
- Parallel rendering is really important.
- Especially if you don't double buffer and add frames of latecy here and there (bad for gameplay and memory), you won't find much to do later in the command buffer generation to keep the cores busy otherwise.
- Batching, "sort-by-material" is needed.
- My best bet on how to handle all this is still the old design I've blogged about of having every "drawable" object correspond to a drawcall and represent it as fixed length sort-key whose bits are an encoding of all the state needed for the draw.
- You'll either need to have a robust geometrical pipeline to split/aggregate meshes and generate LODs and occluders...
- ...or you'll have to schedule a sizable chunk of your artist's time for that. And you'd better not think that you can do these optimizations at the very last...
- On the upside, software occlusion culling is a big win and not that hard!
- Carmack's megatextures (clipmaps) are not (only) attractive to achieve a given art-style, but they have in a deferred setting the big plus of requiring very few material shaders (as you don't need to combine textures, which is most of what material shaders do in a deferred lighting renderer) and less objects (no need of static decals), thus requiring less work on the CPU and making easier to split/merge meshes.
- A tiled lighting stage (as opposed to the stencil marked volumes) is a good idea
- ...especially if you need shader variations in the lighting stage to render some decent materials, consoles have a one bit hi-stencil that won't help you
- Point, spot and directional lights are not enough. You'll need some kind of ambient lighting devices to create volume.
- If your game can stream in chunks (regions), don't think about continuous streaming.
- Edge-filtering AA can work pretty decently and extremely fast. Not limited only to the final framebuffer...
*PS3 early-z is a bitch, PC Dx9 tools are non-existent*

## Search this blog

## 08 September, 2011


## 2 comments:

"Especially if you don't double buffer"


Don't double buffer what?

Double buffer "stuff". Add latency to ease parallelism.

Post a Comment