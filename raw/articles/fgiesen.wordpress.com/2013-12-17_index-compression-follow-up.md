---
title: Index compression follow-up
url: https://fgiesen.wordpress.com/2013/12/17/index-compression-follow-up/
published: '2013-12-17'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Index compression follow-up

I got a few mails about the [previous post](https://fgiesen.wordpress.com/2013/12/14/simple-lossless-index-buffer-compression/), including some pretty cool suggestions that I figured were worth posting.

Won Chun (who wrote a book chapter for [OpenGL insights](http://openglinsights.com/toc.html) on the topic, “WebGL Models: End-to-End”) writes: (this is pasted together from multiple mails; my apologies)

A vertex-cache optimized list is still way more compressible than random: clearly there is lots of coherence to exploit. In fact, that’s pretty much with the edge-sharing-quad business is (OK, some tools might do this because they are working naturally in quads, but you get lots of these cases with any vertex cache optimizer).

So you can also get a pretty big win by exploiting pre-transform vertex cache optimization. I call it “high water mark encoding.” Basically: for such a properly optimized index list, the next index you see is either (a) one you’ve seen before or (b) one higher than the current highest seen index. So, instead of encoding actual indices, you can instead encode them relative to this high water mark (the largest index yet to be seen, initialized to 0). You see “n” and that corresponds to an index of (high water mark – n). When you see 0, you also increment high watermark.

The benefit here is that the encoded indices are very small, and then you can do some kind of varint coding, then your encoded indices are a bit more than a byte on average. If you plan on zipping later, then make sure the varints are byte-aligned and LSB-first.

There are lots of variants on this, like:


- keep a small LRU (~32 elements, or whatever transform cache size you’ve optimized for) of indices, and preferentially reference indices based on recent use (e.g. values 1-32), rather than actual value (deltas are offset by 32),
- make the LRU reference edges rather than verts, so a LRU “hit” gives you two indices instead of one,
- do two-level high water mark encoding, which makes it efficient to store in multi-indexed form (like .OBJ, which has separate indices per attribute) and decode into normal single-indexed form
And also, these approaches let you be smart about attribute compression as well, since it gives you useful hints; e.g. any edge match lets you do parallelogram prediction, multi-indexing can implicitly tell you how to predict normals from positions.


### “High watermark encoding”

I really like this idea. Previously I’d been using simple delta encoding on the resulting index lists; that works, but the problem with delta coding is that a single outlier will produce two large steps – one to go from the current region to the outlier, then another one to get back. The high watermark scheme is almost as straightforward as straight delta coding and avoids this case completely.

Now, if you have an index list straight out of vertex cache optimization and vertex renumbering, the idea works as described. However, with the hybrid tri/paired-tri encoding I described last time, we have to be a bit more careful. While the original index list will indeed have each index be at most 1 larger than the highest index we’ve seen so far, our use of “A ≥ B” to encode whether the next set of indices describes a single triangle or a pair means that we might end up having to start from the second or third vertex of a triangle, and consequently see a larger jump than just 1. Luckily, the fix for this is simple – rather than keeping the high watermark always 1 higher than the largest vertex index we’ve seen so far, we keep it N higher where N is the largest possible “step” we can have in the index list. With that, the transform is really easy, so I’m just going to post my code in full:

static void watermark_transform(std::vector<int>& out_inds, const std::vector<int>& in_inds, int max_step) { int hi = max_step - 1; // high watermark out_inds.clear(); out_inds.reserve(in_inds.size()); for (int v : in_inds) { assert(v <= hi); out_inds.push_back(hi - v); hi = std::max(hi, v + max_step); } }

and the inverse is exactly the same, with the `push_back`

in the middle replaced by the two lines

v = hi - v; out_inds.push_back(v);

So what’s the value of N (aka `max_step`

in the code), the largest step that a new index can be from the highest index we’ve seen so far? Well, for the encoding described last time, it turns out to be 3:

- When encoding a single triangle, the worst case is a triangle with all-new verts. Suppose the highest index we’ve seen so far is k, and the next triangle has indices (k+1,k+2,k+3). Our encoding for single triangles requires that the first index be larger than the second one, so we would send this triangle as (k+3,k+1,k+2). That’s a step of 3.
- For a pair of triangles, we get 4 new indices. So it might seem like we might get a worst-case step of 4. However, we know that the two triangles share an edge; and for that to be the case, the shared edge must have been present in the first triangle. Furthermore, we require that the smaller of the two indices be sent first (that’s what flags this as a paired tri). So the worst cases we can have for the first two indices are (k+2,k+3) and (k+1,k+3), both of which have a largest step size of 2. After the first two indices, we only have another two indices to send; worst-case, they are both new, and the third index is larger than the fourth. This corresponds to a step size of 2. All other configurations have step sizes ≤1.

And again, that’s it. Still very simple. So does it help?

### Results

Let’s dig out the table again (new entries bold, all percentages relative to the “Vertex cache optimized” row):

| Stage | Size | .zip size | .7z size |
|---|---|---|---|
| Original mesh | 6082k | 3312k | 2682k |
| Vertex cache optimized | 6082k | 2084k | 1504k |
Vcache opt, watermark |
6082k | 1808k (-13.2%) | 1388k (-7.7%) |
| Postprocessed | 4939k (-18.8%) | 1830k (-12.2%) | 1340k (-10.9%) |
Postproc, watermark |
4939k (-18.8%) | 1563k (-25.0%) | 1198k (-20.3%) |

In short: the two techniques work together perfectly and very nicely complement each other. This is without any varint encoding by the way, still sending raw 32-bit indices. Variable-sized integer encoding would probably help, but I haven’t checked how much. The code on [Github](https://github.com/rygorous/simple-ib-compress) has been updated in case you want to play around with it.

### Summary

I think this is at a fairly sweet spot in terms of compression ratio vs. decoder complexity. Won originally used this for WebGL, using UTF-8 as his variable-integer encoding: turn the relative indices into Unicode code points, encode the result as UTF-8. This is a bit hacky and limits you to indices that use slightly more than 20 bits (still more than a million, so probably fine for most meshes you’d use in WebGL), but it does mean that the Browser can handle the variable-sized decoding for you (instead of having to deal with byte packing in JS code).

Overall, this approach (postprocess + high watermark) gives a decoder that is maybe 30 lines or so of C++ code, and which does one linear pass over the data (the example program does two passes to keep things clearer, but they can be combined without problems) with no complicated logic whatsoever. It’s simple to get right, easy to drop in, and the results are quite good.

It is not, however, state of the art for mesh compression by any stretch of the imagination. This is a small domain-specific transform that can be applied to fully baked and optimized game assets to make them a bit smaller on disk. I also did not cover vertex data; this is not because vertex data is unimportant, but simply because, so far at least, I’ve not seen *any* mesh compressors that do something besides the obvious (that is, quantization and parallelogram prediction) for vertex data.

Finally, if what you actually want is state-of-the art triangle mesh compression, you should look elsewhere. This is outside the scope of this post, but good papers to start with are “[Triangle Mesh Compression](http://www.cs.technion.ac.il/~gotsman/AmendedPubl/TriangleMesh/Convert-Triangle.pdf)” by Touma and Gotsman (Proceedings of Graphics Interface, Vancouver, June 1998) and “[TFAN: A low complexity 3D mesh compression algorithm](http://www.researchgate.net/publication/220357295_TFAN_A_low_complexity_3D_mesh_compression_algorithm/file/d912f50b380269a6a0.pdf)” by Khaled, Zaharia, and Prêteux (Computer Animation and Virtual Worlds 20.2‐3 (2009)). I’ve played around with the former (the character mesh in Candytron was encoded using an algorithm descended from it) but not the latter; however, Touma-Gotsman and descendants are limited to 2-manifold meshes, whereas TFAN promises better compression and handles arbitrarily topologies, so it looks good on paper at least.

Anyway; that’s it for today. Thanks to Won for his mail! And if you should use this somewhere or figure out a way to get more mileage out of it without making it much more complicated, I’d absolute love to know!