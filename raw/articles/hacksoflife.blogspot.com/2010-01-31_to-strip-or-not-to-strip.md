---
title: To Strip or Not To Strip
url: http://hacksoflife.blogspot.com/2010/01/to-strip-or-not-to-strip.html
author: Benjamin Supnik
published: '2010-01-31'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In this post I will try to explain why a performance-focused OpenGL application like X-Plane does not use triangle strips. Since triangle strips were the best way to draw meshes a few years back, a new user searching for information might be confronted by a cacophony of tutorials advocating triangle strips and game developers saying "indexed triangles are better" without explaining why. Here's the math.


Please note: this article applies to OpenGL desktop applications, typically targeting NVidia and ATI GPUs. In the mobile/embedded space, it's a very different world, and certain GPUs (cough, cough, PowerVR, cough cough) have some fine print attached to them that might make you reconsider.




If you are drawing a bunch of connected triangles, the logic in favor of triangle strips is very simple: the number of vertices in the strip will be almost 66% fewer than the number you'd have if you simply made triangles. The longer the strip, the closer to that savings you get. Since geometry throughput is generally limited by total vertex count, this is a big win.


Ten years ago, that's all you needed to know. Of course, making triangle strips is not so easy - some meshes simply won't form strips. The general idea was to make as many strips as you can, and draw the rest of your triangles as "free triangles" (e.g. GL_TRIANGLES, where each triangle is 3 vertices, and no vertices are shared).


(By the way, to see how to use the tri_stripper library to create triangle strips, look at the function DSFOptimizePrimitives in the




In an indexed mesh, each vertex is stored only once, and the triangles are formed from a set of indices. (In OpenGL this is done by moving from glDrawArrays to glDrawElements.) With an index, you pay more (2 or 4 bytes) per each vertex, but you don't ever have to repeat the geometry of a vertex.


When is it worth it to index? It depends on the size of your indices and vertices, but it is almost always a win. For example, in an X-Plane object our vertices are 32 bytes (XYZ, normal, one UV map, all floating point) and our indices are 4 bytes (unsigned integer indices). Thus a vertex is 8x more expensive than an index. So if we can reduce 1/8th of the geometry via sharing, we will have a win.


Consider a simple 2-d grid: even with triangle strips, each adjacent strip except the edges are going to share a common edge. Thus if we use indexing, our 2-d mesh is going to have a savings that nearly approaches 2x for the geometry! That is way more than enough to pay for the cost of the indices.


So the moral of the story is: any time your geometry has shared vertices, use indexing. Note that this won't always happen. If you have a mesh of GL_POINTS, you will have no sharing, so indexing is a waste. In X-Plane, our "trees" are all individual quads, no sharing, so we turn off indexing because we know the indexing will do no good.


But for most "meshed" art assets (e.g. anything someone built for you in a 3-d modeler) it is extremely likely that indexing will cut down the total amount of data you have to send to the GPU, and that is a good thing.




Now in the old school world, a triangle strip cut the amount of geometry down by almost 3x. Awesome! But in the indexed world, a triangle strip only cuts down the size of the


The take-away thing to observe: once we start indexing (which really makes geometry storage efficient) triangle strips aren't nearly as important as they used to be.




So far we've talked about ideal cases, where your triangle strips are very long, so we really approach a 3x savings. Here's the hitch: in real life triangle strips might be very short.


The problem with triangle strips is that we have to tell the card where the triangle strips begin and end, and that can get expensive. You might have to issue a separate glDrawElements call for each strip.


You don't want to make additional CPU calls into the GL to minimize the size of a buffer (the index buffer) that is already held in VRAM. CPU calls are much slower. And this is why X-Plane doesn't use strips internally: it's faster to be able to make one draw call only for mesh, even if it means a slightly bigger element list.


Now if you are a savvy OpenGL developer you are probably screaming one of two things:





Thus the X-Plane solution: any time we have a mesh, we use indexed triangles and we go home happy.


Please note: this article applies to OpenGL desktop applications, typically targeting NVidia and ATI GPUs. In the mobile/embedded space, it's a very different world, and certain GPUs (cough, cough, PowerVR, cough cough) have some fine print attached to them that might make you reconsider.

**Why Triangle Strips Are Good**If you are drawing a bunch of connected triangles, the logic in favor of triangle strips is very simple: the number of vertices in the strip will be almost 66% fewer than the number you'd have if you simply made triangles. The longer the strip, the closer to that savings you get. Since geometry throughput is generally limited by total vertex count, this is a big win.

Ten years ago, that's all you needed to know. Of course, making triangle strips is not so easy - some meshes simply won't form strips. The general idea was to make as many strips as you can, and draw the rest of your triangles as "free triangles" (e.g. GL_TRIANGLES, where each triangle is 3 vertices, and no vertices are shared).

(By the way, to see how to use the tri_stripper library to create triangle strips, look at the function DSFOptimizePrimitives in the

[X-Plane scenery tools code](http://dev.x-plane.com/cgit/cgit.cgi/xptools.git/tree/src/DSF/DSFPointPool.cpp). Why DSFLib does this will have to be explained in another post, but suffice it to say, there is no hypocrisy here: X-Plane disassembles the triangle strips in the DSF into "free triangles" on load.)**Indexing Is Better**In an indexed mesh, each vertex is stored only once, and the triangles are formed from a set of indices. (In OpenGL this is done by moving from glDrawArrays to glDrawElements.) With an index, you pay more (2 or 4 bytes) per each vertex, but you don't ever have to repeat the geometry of a vertex.

When is it worth it to index? It depends on the size of your indices and vertices, but it is almost always a win. For example, in an X-Plane object our vertices are 32 bytes (XYZ, normal, one UV map, all floating point) and our indices are 4 bytes (unsigned integer indices). Thus a vertex is 8x more expensive than an index. So if we can reduce 1/8th of the geometry via sharing, we will have a win.

Consider a simple 2-d grid: even with triangle strips, each adjacent strip except the edges are going to share a common edge. Thus if we use indexing, our 2-d mesh is going to have a savings that nearly approaches 2x for the geometry! That is way more than enough to pay for the cost of the indices.

So the moral of the story is: any time your geometry has shared vertices, use indexing. Note that this won't always happen. If you have a mesh of GL_POINTS, you will have no sharing, so indexing is a waste. In X-Plane, our "trees" are all individual quads, no sharing, so we turn off indexing because we know the indexing will do no good.

But for most "meshed" art assets (e.g. anything someone built for you in a 3-d modeler) it is extremely likely that indexing will cut down the total amount of data you have to send to the GPU, and that is a good thing.

**Triangle Strips Aren't That Cool When We Index**Now in the old school world, a triangle strip cut the amount of geometry down by almost 3x. Awesome! But in the indexed world, a triangle strip only cuts down the size of the

*index list*by 3x. That is...not nearly as impressive. In fact, in X-Plane's case it is only 1/8th as impressive as it would have been for non-indexed geometry.The take-away thing to observe: once we start indexing (which really makes geometry storage efficient) triangle strips aren't nearly as important as they used to be.

**Restarting a Primitive Hurts**So far we've talked about ideal cases, where your triangle strips are very long, so we really approach a 3x savings. Here's the hitch: in real life triangle strips might be very short.

The problem with triangle strips is that we have to tell the card where the triangle strips begin and end, and that can get expensive. You might have to issue a separate glDrawElements call for each strip.

You don't want to make additional CPU calls into the GL to minimize the size of a buffer (the index buffer) that is already held in VRAM. CPU calls are much slower. And this is why X-Plane doesn't use strips internally: it's faster to be able to make one draw call only for mesh, even if it means a slightly bigger element list.

Now if you are a savvy OpenGL developer you are probably screaming one of two things:

- What about glMultiDrawElements? I point you to
[here](http://lists.apple.com/archives/mac-opengl/2005/Dec/msg00039.html), and[here](http://www.opengl.org/registry/specs/NV/primitive_restart.txt). Basically both Apple and NVidia are suggesting that the multi-draw case may not be as ball-bustingly fast as it could be. There is always a risk that the driver decomposes your carefully consolidated strips into individual draw calls, and at that point you lose. - What about primitive restart? Well, it's nvidia only, so if you use it, you need to case your basic meshing code to handle its not being there. And even if it is there, you pay with an extra index per restart. If you have really good strips, this might be a win, but when the strips get small, you're starting to eat away at the benefit of shrinking down your indices in the first place. (The worst case is a triangle soup with no sharing, so you get no benefit from tri strips and you have to put a "restart" primitive into every 4th slot.)

*real*draw calls (even with multi-draw) just to shrink an index list down.**Index Triangles**Thus the X-Plane solution: any time we have a mesh, we use indexed triangles and we go home happy.

- We always draw every mesh in only one draw call.
- We share vertices as much as possible.
- We are in no way dependent on the driver handling multi-draw or having a restart extension.
- We run at full speed even if the actual mesh doesn't turn to strips very well.
- The code handles only one case.

Some notes:

ReplyDeletePrimitive restart is not Nvidia only. ATI also supports it from GL3.1 version - i.e. all HDxxx cards.

Also you can have indexed triangle strips not only indexed triangle lists.

Another alternative to primitive restart for strips is to use degenerate triangles.

ReplyDeletePrimitive restart: good to know that ATI picked it up ... HD - in other words, safe to use if you already require DX10 class hw or better.



ReplyDeleteDegenerate triangles: this still assumes _connectivity_. Given a mesh where triangles have been selected out (maybe by OGL state) you might have islands of triangles, and a restart will be necessary.

(Hrm - I admit I might be wrong about this. I do not know whether degenerate triangles get rasterized.

I don't think degenerate triangles are rasterized, but I could be wrong. Even if they are, as long as they only run through the interior of your shape, you should be okay.


ReplyDelete(As an aside, if you're interested, I believe tomsdxfaq wrote briefly about vertex cache optimization from a DX perspective at one point.)

Just for your information, as far as I know:



ReplyDelete1) Degenerate triangles do not imply connectivity:

indices[] = {1, 2, 3, 3, 4, 4, 5, 6};

This strip draws 2 separate triangles with vertice (1,2,3) and (4,5,6). Of course you lose 2 indices to make the "jump"...

2) Degenerate triangles (zero-area) are NOT rasterized, since they cover a null area. See the OpenGL spec.: only pixels/fragments whose center is inside the interior of a triangle is emitted.

I like indexes too, but what tool do you use to merge all vertices that share the same UVs and normals ?



ReplyDeleteI mean, most 3D formats ( .x, .obj, .x3d, .dae, ...) have three indices : one for vertices, one for UVs, one for normals. How do you do you generate a single index buffer from that ?

@spate, djee : Thanks for the "jump" trick !

Arnaud1602, we index the mesh ourselves - that is, the various pieces of the art toolchain that we coded in C or python index the mesh by treating each vertex as a tuple (typically 8 coords, vertex, normal and UV map) and hashing or sorting on that.


ReplyDeleteOnce we sort it, we can run the indices through a strip program _if_ desired...this helps the powerVR MBX a lot, and it's not bad for cache coherency either.

Benjamin, how exactly does PowerVR differ from other cards in the matter you discuss here? I mean, can indexing really be that inefficient? Also, do you know if same applies to new ES 2.0 chipsets like SGX-535 or SGX-543?


ReplyDeleteBtw, I just finished a marathon with two years worth of your posting - thanks for a really great read (and killing my plans for today;).

Karol: the big difference is between the PowerVR SGX (ES 2.0) vs MBX (ES 1.1) cores...the MBX is highly dependent on getting 'real' triangle strips (whether by indexes in tri-strip order or by using the tri strip command). The MBX stores strips as its native primitive when it "buckets" geometry for its tile based renderer, so if you are targeting the original iphone (for example) it's really worth it to be sure you have strip-order indexed meshes.


ReplyDeleteI am not sure if it's as important on the SGX - the SGX has a ton more geometry throughput capacity, while the MBX is really vertex limited.

Late to the party here, but just pointing out that in the game development world we often use indexed triangle strips to represent complex objects. Each object is drawn as a single degenerate strip, so it executes in one call, and the degenerate triangles are indeed discarded early in the pipeline, so no transformations get applied to them etc.

ReplyDeleteAs long as you are supporting more modern drivers primitive restart should be even cheaper.

Commonly used is not the same as more efficient. The most likely reason game development often uses indexed triangle strips is that before indexed models were common triangle strips were more efficient, then instead of analyzing efficiency for indexed strips versus other options, game developers just assumed that strips would be more efficient with indexed models (sadly, assumptions like this are common in industry).




DeleteNote that I am not trying to say that indexed triangle strips are always less efficient. In fact, I have some cases where straight (non-indexed) triangle strips are much more efficient than indexed anything. The point is that just because everyone does it one way, does not mean that that way is the best. (In fact, there are some places where the gaming industry really fails on efficiency, which is part of the reason why many games require much faster computers or video cards than they strictly should.) In many cases, efficiency is sacrificed for ease of development (and in some cases, this may even be justified), but again, this does not necessarily make the common way the best.

That aside, I really enjoyed the article. I had made some assumptions about the best way to handle mesh data that were wrong. The explanations of why I was wrong really helped me understand the problems better.

Typo: "Thus a vertex is 8x more expensive than a vertex."

ReplyDeleteThanks -- fixed.

Delete