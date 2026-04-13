---
title: 'Storing vertex data: To interleave or not to interleave?'
url: https://anteru.net/blog/2016/storing-vertex-data-to-interleave-or-not-to-interleave
published: '2016-02-14'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Recently, I’ve been refactoring the geometry storage in my home framework. Among other things, I also looked into vertex attribute storage, which we’re going to dive into today.

When it comes to storing vertex data, there’s basically two different schools of thought. One says interleave the attributes, that is, store “fat” vertices which contain position, normal, UV coordinates and so on together. I’ll refer to this as interleaved storage, as it interleaves all vertex attributes in memory. The other school says all attributes should remain separate, so a vertex consists of multiple streams. Each stream stores one attribute only with tight packing.

## Why care?

Let’s look where the vertex attribute storage matters:

**On disk**, as compression and read performance may be affected.**In memory**, as some algorithms prefer one order or the other.**At render time**, as it affects the required bandwidth and impacts performance on GPUs.

## Rendering

We’ll start by looking at the last usage first, which is GPU rendering, as it’s the easiest to explain. On the GPU, all APIs allow sourcing vertex attributes from multiple streams or from a single stream. This makes experiments very simple - and also highlights a few key differences.

The first thing that is affected is **access flexibility**. I have a geometry viewer, which may or may not have all attributes present for one mesh. With interleaved data, it’s hard to turn off an attribute, as the vertex layout needs to be adjusted. With de-interleaved data, it’s as easy as binding a null buffer or using a shader permutation which just skips the channel. One point for de-interleaved data.

The next use case is position-only rendering, which is very common for shadow maps. Again, de-interleaved data wins here, due to **cache efficiency**. It’s quite easy to see - if you only need positions, you get the best cache and bandwidth utilization if you separate it from the other attributes. With interleaved data, every cache line fetches some other attributes which you throw away immediately. Another point for de-interleaved data.

The last point is actually quite important for GPUs. On a GPU compute unit, you have very wide vector units which want to fetch all the same data in a given cycle, for instance, the position. If you have the data de-interleaved, they can fetch it into registers and evict the cache line immediately. You can see that in the figure above. In the first iteration, the red *x* coordinate is read, then *y*, and finally *z*. It takes thus three reads to consume a whole cache line, and it can be evicted right away. For interleaved data, the data has to remain in cache until everything has been read from it, polluting the already small caches - so de-interleaved data will render slightly faster due to better cache utilization.

Is there actually a good reason to use interleaved data for rendering? Actually, I can’t think of one, and as it turns out, I changed my geometry viewers to de-interleaved data back a few years ago already and never looked back :)

In the offline rendering world, attributes [also have been long specified separately](https://renderman.pixar.com/resources/current/RenderMan/geometricPrimitives.html) as a ray-tracer mostly cares about positions. For this use case, cache efficiency is most important, so you want to have them separate as well, even on the CPU.

## Processing

Here’s the more interesting part. During the recent refactoring, I changed the [mesh view abstraction](https://anteru.net/blog/2012/08/25/1904/) to take advantage of de-interleaved data when fetching a single attribute. So all algorithms I had in place needed to be refactored to work with **both** interleaved and de-interleaved data, giving me a good idea of the advantages and disadvantages of each.

Turns out, there’s only one algorithm in my toolbox which actually needs interleaved data so much for performance that it will re-interleave things if it encounters a de-interleaved mesh. This algorithm is the re-indexer, which searches for unique vertices, by storing a hash to the vertex and a pointer so it can do exact comparisons.

Except for that algorithm, all others were working on one attribute only to start with, mostly position, and will be now slightly more cache efficient for de-interleaved data. I briefly measured performance, but it turns out, for “slim” vertices with position, normal and maybe one or two more attributes, the cache efficiency differences on CPUs are rather minimal - I’d expect more gains with heavy multi-threading and in bandwidth-restricted cases. The good news is that nothing got slower.

I’d call it a tie, due to the re-indexer. As I expose a pointer and stride to all algorithms now, it’s basically trivial to swap between the representations. For the re-indexer, I’m thinking that there must be a better way to represent a vertex than a pointer and the hash, which would also resolve that issue (maybe a stronger hash which does not collide will be enough …)

## Storage

So here comes the interesting part. My geometry storage is [LZ4](https://en.wikipedia.org/wiki/LZ4_%28compression_algorithm%29) compressed, and with compression, you’d expect interleaved data to loose big time against non-interleaved. After all, all positions will have similar exponent, all normals will have the same exponent, etc., and if they are stored consecutively, a compressor should find more correlation in the data.

Turns out, with the default LZ4 compression, this is not quite true, and interleaved data actually compresses quite a bit better. For testing, I used the [XYZRGB Asian dragon](http://graphics.stanford.edu/data/3Dscanrep/), and converted it to my binary format which stores position as 3 floats, and normals as 3 floats as well.

| Storage | No Idx/Compressed | Idx/Compressed | Idx/Compressed (HC) |
| Interleaved | 169 MiB | 138 MiB | 135 MiB |
| Deinterleaved | 189 MiB | 138 MiB | 132 MiB |

It seems that LZ4 is actually able to get a better compression for interleaved data, which duplicates whole vertices and not just a single attribute. With indexed data, it’s a wash, and only with the high compression setting, the de-interleaved data pulls ahead.

This is actually really surprising for me and it looks like more analysis is warranted here. One thing that obviously got improved are loading times, as I need to de-interleave for rendering, but the difference is just a couple of percent. This is mostly due to the fact that I bulk load everything into memory, which dominates the I/O time.

So on the storage side, it’s one point for de-interleaved data in terms of performance, but one point for interleaved data for basic compression. I guess we can call it a tie!

## Verdict

Overall, the advantages of having a full de-interleaved pipeline outweigh the disadvantages I found on the storage and algorithmic front. As mentioned, except for one algorithm, everything got slightly faster, and storage space is cheap enough for me that I don’t care about the few percent bloat there in the general case. For archival storage, I get some benefit with de-interleaved data, so de-interleaved it is :)