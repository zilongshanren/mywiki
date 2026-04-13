---
title: Scalable geometry handling
url: https://anteru.net/blog/2012/scalable-geometry-handling
published: '2012-08-25'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

At work, I often have to process large geometric data sets. Recently, I have overhauled my geometry pipeline so it is more scalable now and easier to use at the same time. When it comes to geometry data, I usually run into the following problems:

- Data sets come in various formats: Meshes are usually stored as OBJ or PLY. Some data sets are procedurally generated though and have no natural storage format.
- Data sets can be very large: The meshes have between a few thousand up to several hundred million triangles. The largest mesh I had to process has over 900 million triangles.
- Slow algorithms: Some of the algorithms I have to run are rather slow; the easiest solution to speed them up is to run them in parallel. However, memory per thread is usually limited (1-2 GiB per thread), so the meshes need to processed in small chunks.

Given this problems, I’ve recently come up with a simple solution which resolves them elegantly: Geometry streams and mesh views.

## Mesh views

Mesh views are a simple abstraction for geometry data. Instead of passing around the geometry, I use a simple interface which allows for efficient retrieval of per-vertex attributes and connectivity.

The tricky part here is how to make the interface efficient, as calling one virtual function per vertex will definitely result in bad performance. The way the mesh interface works is that the virtual functions only handle batch requests. The client must gather a bunch of requests first, which are then processed with a single function call. Usually, this ends up in a single pass through memory with some stride on the reading side into a tightly packed output buffer.

For non-indexed meshes, the index accessors simply return consecutive indices. This is potentially a waste, but it unifies the handling on the client side and if a non-indexed mesh is later converted into one with shared vertices, clients immediately benefit from reduced memory usage.

Constructing mesh views over various file and data formats is easy; allowing me to create a view onto a PLY file just as easily as onto an OBJ or some other custom in-memory representation.

## Geometry streams

With mesh views, all geometric data is treated uniformly on the client side. What’s missing is a geometry format which is compact, easy to create and consume, handles large data sets easily and allows for efficient processing.

What I ended up with is geometry streams: A geometry stream is a stream of geometry chunks, and each chunk is a block of geometry with additional per-chunk attributes. Each geometry chunk is completely independent of all others in a stream. There is no special header information which starts a stream; rather, a stream consists simply of chunks concatenated one after another.

This makes it trivial to process streams in parallel and merge the results. On all operating systems I care about, I can directly write individual chunks from multiple threads – the final ordering inside the file will be undefined, but this hasn’t been a problem so far. Removing or skipping chunks in a stream is also efficient.

For the on-disk format, I’m using a minimal header followed by a dictionary which stores per-chunk attributes. A dictionary makes versioning much simpler; instead of changing the file format, I just add new attributes. This is similar to how a [protobuf](http://code.google.com/p/protobuf/) implementation would work, but it’s even easier as the keys are human-readable and can be easily inspected if necessary.

Geometry chunks can contain indexed meshes, but the most common use is just a list of triangles without shared vertices. This usually results in a slightly larger memory use than necessary, but makes processing trivial. Most of the time, the vertices are very small, containing only position and maybe normals, and by adding some compression, shared vertices are just compressed away. I’m a big fan of [LZ4](http://code.google.com/p/lz4/), an extremely fast compression method which gives reasonably good compression rates. For archival use, I simply use the high-compression mode, which further reduces memory usage but results in much slower processing. This can be easily offset though by processing each chunk in parallel.

Of course, I can construct a mesh view for each geometry chunk, so the fact that I’m using them is transparent to all clients. Both the mesh views and the geometry streams have dramatically changed how I process geometry data. Compared to loading an .OBJ, loading from a geometry stream is roughly 10x faster while using less disk space, and by converting all data into geometry streams, I can skip lots of checks in the various importers and move them to geometry stream filters.

Overall, I’m very happy with the results and I expect to build all my processing algorithms in the future to work on streams and view exclusively. Some stuff that I have to implement are re-indexing triangle soups to verify whether it helps for regular and procedural geometry and how to store and expose adjacency information.