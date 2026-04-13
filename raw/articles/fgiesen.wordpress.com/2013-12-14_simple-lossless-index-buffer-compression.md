---
title: Simple lossless(*) index buffer compression
url: https://fgiesen.wordpress.com/2013/12/14/simple-lossless-index-buffer-compression/
published: '2013-12-14'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Simple lossless(*) index buffer compression

(Almost) everyone uses indexed primitives. At this point, the primary choice is between indexed triangle lists, which are flexible but always take 3 indices per triangle, and indexed triangle strips; since your meshes are unlikely to be one big tri strip, that’s gonna involve primitive restarts of some kind. So for a strip with N triangles, you’re generally gonna spend 3+N indices – 2 indices to “prime the pump”, after which every new index will emit a new triangle, and finally a single primitive restart index at the end (supposing your HW target does have primitive restarts, that is).

Indexed triangle strips are nice because they’re smaller, but finding triangle strips is a bit of a pain, and more importantly, long triangle strips actually aren’t ideal because they tend to “wander away” from the origin triangle, which means they’re not getting very good mileage out of the vertex cache (see, for example, [Tom Forsyth’s old article](http://home.comcast.net/~tom_forsyth/papers/fast_vert_cache_opt.html) on vertex cache optimization).

So here’s the thing: we’d like our index buffers for indexed tri lists to be smaller, but we’d also like to do our other processing (like vertex cache optimization) and then not mess with the results – not too much anyway. Can we do that?

### The plan

Yes we can (I had this idea a while back, but never bothered to work out the details). The key insight is that, in a normal mesh, [almost all triangles share an edge with another triangle](http://realtimecollisiondetection.net/blog/?p=12). And if you’ve vertex-cache optimized your index buffer, two triangles that are adjacent in the index buffer are also quite likely to be adjacent in the geometric sense, i.e. share an edge.

So, here’s the idea: loop over the index buffer. For each triangle, check if it shares an edge with its immediate successor. If so, the two triangles can (in theory anyway) be described with four indices, rather than the usual six (since two vertices appear in both triangles).

But how do we encode this? We could try to steal a bit somewhere, but in fact there’s no need – we can do better than that.

Suppose you have a triangle with vertex indices (A, B, C). The choice of which vertex is first is somewhat arbitrary: the other two even cycles (B, C, A) and (C, A, B) describe the same triangle with the same winding order (and the odd cycles describe the same triangle with opposite winding order, but let’s leave that alone). We can use this choice to encode a bit of information: say if A≥B, we are indeed coding a triangle – otherwise (A<B), what follows will be two triangles sharing a common edge (namely, the edge AB). We can always pick an even permutation of triangle indices such that A≥B, since for *any* integer A, B, C we have

Because the sum is 0, not all three terms can be negative, which in turn means that at least one of A≥B, B≥C or C≥A must be true. Furthermore, if A, B, and C are all distinct (i.e. the triangle is non-degenerate), all three terms are nonzero, and hence we must have both negative and positive terms for the sum to come out as 0.

### Paired triangles

Okay, so if the triangle *wasn’t* paired up, we can always cyclically permute the vertices such that A≥B. What do we do when we have two triangles sharing an edge, say AB?

For this configuration, we need to send the 4 indices A, B, C, D, which encode the two triangles (A, B, C) and (A, D, B).

If A<B, we can just send the 4 indices directly, leading to this very simple decoding algorithm that unpacks our mixed triangle/double-triangle indexed buffer back to a regular triangle list:

- Read 3 indices A, B, C.
- Output triangle (A, B, C).
- If A<B, read another index D and output triangle (A, D, B).

Okay, so this works out really nicely if A<B. But what if it’s not? Well, there’s just two cases left. If A=B, the shared edge is a degenerate edge and both triangles are degenerate triangles; not exactly common, so the pragmatic solution is to say “if either triangle is degenerate, you have to send them un-paired”. That leaves the case A>B; but that means B<A, and BA is also a shared edge! In fact, we can simply rotate the diagram by 180 degrees; this swaps the position of (B,A) and (C,D) but corresponds to the same triangles. With the algorithm above, (B, A, D, C) will decode as the two triangles (B, A, D), (B, C, A) – same two triangles as before, just in a different order. So we’re good.

### Why this is cool

What this means is that, under fairly mild assumptions (but see “limitations” section below), we can have a representation of index buffers that mixes triangles and pairs of adjacent triangles, with no need for any special flag bits (as recommended in Christer’s article) or other hackery to distinguish the two.

In most closed meshes, every triangle has at least one adjacent neighbor (usually several); isolated triangles are very rare. We can store such meshes using 4 indices for every pair of triangles, instead of 6, for about a 33% reduction. Furthermore, most meshes in fact contain a significant number of quadriliterals (quads), and this representation supports quads directly (stored with 4 indices). 33% reduction for index buffers isn’t a huge deal if you have “fat” vertex formats, but for relatively small vertices (as you have in collision detection, among other things), indices can actually end up being a significant part of your overall mesh data.

Finally, this is simple enough to decode that it would probably be viable in GPU hardware. I wouldn’t hold my breath for that one, just thought I might point it out. :)

### Implementation

I wrote up a quick test for this and put it on [Github](https://github.com/rygorous/simple-ib-compress), as usual. This code loads a mesh, vertex-cache optimizes the index buffer (using Tom’s algorithm), then checks for each triangle whether it shares an edge with its immediate successor and if so, sends them as a pair – otherwise, send the triangle alone. That’s it. No attempt is made to be more thorough than that; I just wanted to be as faithful to the original index buffer as possible.

On the “Armadillo” mesh from the [Stanford 3D scanning repository](http://graphics.stanford.edu/data/3Dscanrep/), the program outputs this: (**UPDATE**: I added some more features to the sample program and updated the results here accordingly)

172974 verts, 1037832 inds. before: ACMR: 2.617 (16-entry FIFO) 62558 paired tris, 283386 single IB inds: list=1037832, fancy=975274 (-6.03%) after: ACMR: 0.814 (16-entry FIFO) 292458 paired tris, 53486 single IB inds: list=1037832, fancy=745374 (-28.18%) 745374 inds packed 1037832 inds unpacked index buffers match. ACMR: 0.815 (16-entry FIFO)

“Before” is the average cache miss rate (vertex cache misses/triangle) assuming a 16-entry FIFO cache for the original Armadillo mesh (not optimized). As you can see, it’s pretty bad.

I then run the simple pairing algorithm (“fancy”) on that, which (surprisingly enough) manages to reduce the index list size by about 6%.

“After” is after vertex cache optimization. Note that Tom’s algorithm is cache size agnostic; it does not assume any particular vertex cache size, and the only reason I’m dumping stats for a 16-entry FIFO is because I had to pick a number and wanted to pick a relatively conservative estimate. As expected, ACMR is much better; and the index buffer packing algorithm reduces the IB size by about 28%. Considering that the best possible case is a reduction of 33%, this is quite good. Finally, I verify that packing and unpacking the index buffer gives back the expected results (it does), and then re-compute the ACMR on the unpacked index buffer (which has vertices and triangles in a slightly different order, after all).

Long story short: it works, even the basic “only look 1 triangle ahead” algorithm gives good results on vertex cache optimized meshes, and the slight reordering performed by the algorithm does not seem to harm vertex cache hit rate much (on this test mesh anyway). Apologies for only testing on one 3D-scanned mesh, but I don’t actually have any realistic art assets lying around at home, and even if I did, loading them would’ve probably taken me more time than writing the entire rest of this program did.

### UPDATE: Some more results

The original program was missing one more step that is normally done after vertex cache optimization: reordering the vertex buffer so that vertices appear in the order they’re referenced from the index buffer. This usually improves the efficiency of the *pre*-transform cache (as opposed to the *post*-transform cache that the vertex cache optimization algorithm takes care of) because it gives better locality of reference, and has the added side effect of also making the index data more compressible for general purpose lossless compression algorithms like Deflate or LZMA.

Anyway, here’s the results for taking the entire Armadillo mesh – vertices, which just store X/Y/Z position as floats, and 32-bit indices both – and processing it with some standard general-purpose compressors at various stages of the optimization process: (all sizes in binary kilobytes, KiB)

| Stage | Size | .zip size | .7z size |
|---|---|---|---|
| Original mesh | 6082k | 3312k | 2682k |
| Vertex cache optimized | 6082k | 2084k | 1504k |
| Postprocessed | 4939k (-18.8%) | 1830k (-12.2%) | 1340k (-10.9%) |

So the post-process yields a good 10% reduction in the compressed size for what would be the final packaged assets here. This value is to be taken with a grain of salt: “real” art assets have other per-vertex data besides just 12 bytes for the 3D position, and nothing I described here does anything about vertex data. In other words, this comparison is on data that favors the algorithm in the sense that roughly half of the mesh file is indices, so keep that in mind. Still, 10% reduction post-LZMA is quite good for such a simple algorithm, especially compared to the effort it takes to get the same level of reduction on, say, [x86 code](https://fgiesen.wordpress.com/2011/01/24/x86-code-compression-in-kkrunchy/).

Also note that the vertex cache optimization by itself *massively* helps the compressors here; the index list for this mesh comes from a 3D reconstruction of range-scanned data and is pathologically bad (the vertex order is really quite random), but the data you get out of a regular 3D mesh export is quite crappy too. So if you’re not doing any optimization on your mesh data yet, you should really consider doing so – it will reduce both your frame timings and your asset sizes.

### Limitations

This is where the (*) from the title comes in. While I think this is fairly nice, there’s two cases where you can’t use this scheme, at least not always:

- When the order of vertices within a triangle matters. An example would be meshes using flat attribute interpolation, where the value chosen for a primitive depends on the “provoking vertex”. And I remember some fairly old graphics hardware where the Z interpolation depended on vertex specification order, so you could get Z-fighting between the passes in multi-pass rendering if they used different subsets of triangles.
- When the order of triangles within a mesh matters (remember that we in the two-tris case, we might end up swapping them to make the encoding work). Having the triangles in a particular order in the index buffer can be very useful with alpha blending, for example. That said, the typical case for this application is that the index buffer partitions into several chunks that should be drawn in order, but with no particular ordering requirements within that chunk, which is easy to do – just prohibit merging tris across chunk boundaries.

That said, it seems to me that it really should be useful in every case where you’d use a vertex cache optimizer (which messes with the order anyway). So it’s probably fine.

Anyway, that’s it. No idea whether it’s useful to anyone, but I think it’s fairly cute, and it definitely seemed worth writing up.

An alternative proof for the fact that at least one of A≥B, B≥C or C≥A must be true:

Assume the opposite: A<B, B<C and C<A. It would follow that A<B<C<A and thus A<A which would contradict the assumption. Hence, A≥B, B≥C or C≥A.

Great idea,

I wonder how much merit there is in extending this to encode triangle fans of an arbitrary length?

i.e. If two triangles have been output, A,B,C and A,C,D, if the next index is A (or perhaps D as this might compress better), read one more index and the next triangle would be A,D,E. Again a 33% saving on index memory when it happens.

There’s far better ways to compress triangle meshes when you’re willing to actively seek out larger groups, e.g. large triangle strips or fans (or, even more generally, connected 2-manifold components). See the follow-up post for some pointers in that direction. Both large triangle strips and large fans do end up with about one post-transform vertex cache miss per triangle, though (as soon as the strips/fans get larger than the vertex cache size, this is pretty much guaranteed).

The idea in this post was specifically to search for shared edges

only between triangles that are adjacent in the index list, preserving the index list output from vertex cache optimization as much as possible; the average number of cache misses per triangle is then a good deal less than 1.The likelihood of sequential triangles grouping into a single strip/fan goes down as you increase the target strip/fan length. I only use single or paired triangles for three reasons:

1. It allows this very simple encoding that does not need any extra bits (you can’t pull the same trick for arbitrary N-gons).

2. Finding such combinations in a linear scan is simple and works well with vertex cache-optimized index list (anything larger and you really want to build a connectivity structure and look for adjacency there).

3. It allows coding quadriliterals directly, using only 4 indices, which is extremely useful on its own.

4. For collision applications (see link in post), a pair of triangles with a shared edge is just as cheap to test against as a single triangle. This is not true for longer strips/fans.

In other words, if you want higher compression (or spend more time encoding/decoding), you could extend this idea, but you’d need extra metadata and there are already well-known better approaches for high compression. Using only single or paired triangles is a simple, local postprocess, it makes the index lists more compressible, it is directly consumable for applications such as collision detection, and it allows for an encoding that doesn’t need any extra metadata anywhere; that makes this a fairly sweet spot.

Thanks for sharing this idea. I have a question about calculating ACMR in your test program. It seems that you’re adding each and every index to the simulated cache buffer. There’s no check to to see if an index already is in the cache (except the one check you do to increment the number of misses. But after that you put the index in the cache no matter if it’s already there or not. Is this done on purpose or do I understand the code incorrectly?

This is simply a bug. Thanks for notifying me!

All ‘normal’ triangle meshes can be perfectly subdivided into pairs of triangles. I have a proof for that if you’re interested.

If by “normal” you mean “2-manifold and without boundary”, then sure: triangle mesh without boundary implies that every face has exactly 3 edges and each edge is shared by exactly two faces, so number of edges e=(3/2)*f (where f=number of faces), and since e is an integer, f must be even.

But that’s not what we use index buffers for. Suppose you take a single triangle out of your connected mesh and assign it custom texture coordinates that are discontinuous with the rest of the mesh. You end up getting three new vertices at the same position as three existing vertices, but with different texture coordinates. And these three new vertices are used in the newly created triangle but nowhere else, so it can’t be paired up with anything.

And this is still assuming you start out with a single connected mesh. A lot of things that get drawn either have holes or are simply polygon soups (e.g. particle systems).