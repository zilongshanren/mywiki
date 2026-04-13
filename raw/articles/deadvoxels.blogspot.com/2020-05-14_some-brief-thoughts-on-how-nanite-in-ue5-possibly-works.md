---
title: Some brief thoughts on how Nanite in UE5 possibly works....
url: http://deadvoxels.blogspot.com/2020/05/some-brief-thoughts-on-how-nanite-in.html
author: Jon Greenberg
published: '2020-05-14'
source_blog: Dead Voxels
source_site: http://deadvoxels.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

So, what do we know?

- We know that Nanite takes in huge many-millions of poly meshes and somehow rasterizes them.

- We know that UE4's material model still needs to be used.

- We also know that at least right now, vertex animation isn't supported - only rigid meshes work.

- Epic hired Graham Wihlidal, the King of Clustering, to help with the development of Nanite

What might we conclude/speculate from this?

**Nanite likely employs a hierarchy of clusters**. Probably something like 32 triangles per cluster, so an easy way to think of this would be like a BVH, but instead of a binary tree, something like 32 cluster pointers in a node. Think of this like a BVH32 (or BVH64 if it s 64 triangles) block as your core inner node in a hierarchy of nodes. Using something like BVH32 would be a little dubious for a raytracer, but for a rasterizing scenario could possibly work great as its push instead of pull, but more on this in a second. In the meantime, consider that 32^6 = 1B polys. That means that by traversing a very small number of levels of this BVH would get you a lot of polygons in a contained hierarchy.

So how might this work in practice? Dice the frame into 8x8 tiles. Take your original visible object list's bounding volume set and test them against all tiles. This could be done faster by testing at coarser tile sizes first, but whatever. So, build a list of objects that overlap each working tile. This will be list of objects will be evaluating.

Now basically texel-overlap test the cluster bounds, descending down the hierarchy per thread. When testing the sub-cluster bounds, sort all the "hits" based on near-depth of the cluster. If you end up with a cluster itself smaller than the current pixel, stop descending and simply output the cluster ID instead of a triangle, along with a candidate depth as the local depth and cluster id. If you actually make it to the bottom cluster level and the cluster is still visible, add the cluster to an append buffer (cluster buffer). If while descending, you find that the local cluster's bounding near-depth is behind the current stored local depth for that thread, break. Doing the tree walk part efficiently is no joke, but that's certainly workable, possibly involving a tiny stack (possibly shared across the threads using lane access magic, or stored in LDS) like a typical manually implemented GPU ray-tracer.

Once you've resolved all the clusters in your tile, write out your depth buffer, the object/cluster ids, and construct your HTile for the tile if you're on a console and you've got a Visibility Buffer (mostly complete) and a Depth Buffer (mostly complete). On PC, reconcile depth test acceleration by a fullscreen PS that exports depth.

Now sort the leftover cluster buffer by id, and do a duplicate reduction on it. Rasterize these clusters via mesh shading, outputting depth and triangle id to the same visibility buffer, while doing depth testing of course. Note, when dealing with triangle and cluster ids in the visibility buffer, I'd do something like prepend the visibility id with a 1 bit code to identify whether the payload came from a cluster or triangle (which presumably has object ID + cluster + prim id packed together.. somehow).

Now processing the visibility data itself wouldn't be too hard. One knows either the cluster or the triangle should be enough to get to the interpolants you'd normally need to run the equivalent of a pixel shader for the material/triangle. At this point its some variant of visibility buffer processing... which wouldn't be trivial to do, but is certainly doable. I'm going to mostly hand-wave away how one gets visibility buffering working with an Unreal-style material model. Other people have done this before.

Oh wait a second - I glossed over how you do this for a cluster, right? Well, the cluster is basically an AABB containing all the vertices underneath it (or all clusters beneath it). So what makes sense is to store not simply a positional AABB, but for each cluster an AABB of *all* meaningful interpolants. This has some interesting side effects - it implies range of UVs, which implies UV coverage, which implies sampling mip levels when sampling textures for materials. One could presumably pick the midpoint for the bounds and use that as the candidate UV for the cluster. I'm not 100% sure how best to deal with normals for the cluster... perhaps the cluster stores an average normal or normal cone for its level to help in backface culling anyway during the above described traversal, and that average normal is used. At some point presumably that breaks, but one supposes that if the cluster has a normal cone over 180 degrees, one can just assume the normal faces the camera anyway.

All this cluster data should compress well, as all interpolants are relative to the cluster bounds, and vertex indices could be encoded in a small number of DWORDs if one did it naively. Clusters should compress down to nothing (relative to the original data), without needing anything particularly fancy.

There are other advantages to doing this. Since all the geometry is hidden inside clusters at such extremes of level, you can presumably stream the geometry. You can also book-keep to track what the lowest level cluster you happen to need is, and stream the next one as soon as possible. As there's such a large order of magnitude change going on here that LODs of data can be pretty easily managed, and loaded in to a virtual space. There are potentially pretty clever things you can do where all clusters (regardless of object) can live in a common cluster pool, and have mapping tables between objects and their virtual cluster ids, which could be stored in a per-object offset table.

There are a few obvious limitations to this idea: It assumes a lot of preprocessing on geometry, so one cannot animate vertices or vertex attributes trivially. No dynamic meshing of raw triangles would be supported. It also presumes that the object is opaque (at least for a more straightforward implementation...) so at least for the moment, masking and transparency wouldn't be supported either.

Anyway - those are some early thoughts. I talk a lot about AABBs, but its equally possible they're just spheres - in a lot of ways spheres can be easier to deal with in a hierarchy (although dealing with nonlinear scaling isn't fun). It'll be interesting to see if I'm close or totally missed the boat here. It wouldn't shock me if I'm totally off base, but I do think something like this could work.


I should also point out - the complexity involved in getting all this that I'm suggesting working is pretty high. I'm certainly hand-waving my way through a lot of complexity of implementation, and getting this to run fast enough to be competitive with standard rasterization when your meshes

I should also point out - the complexity involved in getting all this that I'm suggesting working is pretty high. I'm certainly hand-waving my way through a lot of complexity of implementation, and getting this to run fast enough to be competitive with standard rasterization when your meshes

*aren't*millions of polygons wouldn't be particularly easy either. Kudos to the entire team at Epic for figuring this stuff out. The imagination involved is incredible, and it really is groundbreaking work.
-Jon

Geometry Images, Vector Displacement maps, Octree coverage Rendering!

ReplyDelete