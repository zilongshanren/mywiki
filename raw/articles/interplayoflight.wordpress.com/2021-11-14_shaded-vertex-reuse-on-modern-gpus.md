---
title: Shaded vertex reuse on modern GPUs
url: https://interplayoflight.wordpress.com/2021/11/14/shaded-vertex-reuse-on-modern-gpus/
author: Kostas Anagnostou
published: '2021-11-14'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A well known feature of a GPU is the post transform vertex cache, used in cases where a drawcall uses an index buffer to index the vertex to be processed, to cache the output of the vertex shader for each vertex. If subsequently the same vertex is indexed, as part of another triangle, the results are already in the cache and the GPU needs not process that particular vertex again. Since all caches are of limited capacity, rendering engines typically rearrange the vertex indices in meshes to encourage more locality in vertex reuse and better cache hit ratio.

In 2018 the [Revisiting The Vertex Cache: Understanding and Optimizing Vertex Processing on the modern GPU](https://www.markussteinberger.net/papers/ShadingRate.pdf) paper by Kerbl et al was published in which the authors investigate the extent GPUs actually use a post-transform cache to facilitate vertex reuse. They conducted a simple experiment of rendering using a simple index buffer that repeats a {0,1,2} index pattern to ensure that the vertex shader output will always be in the post-transform cache and counted the number of vertex shader invocations. The theory is that that number should always be 3, since the same 3 unique vertices are always being referenced. The authors noticed that this did not hold true on all tested, modern GPUs.

![](../../assets/41eae3d1fa31ab4c.png)


![](../../assets/41eae3d1fa31ab4c.png)

Instead of the expected flat line they noticed a staircase-like increase in the number of shader invocations. This indicates that there is some reuse of vertices, not global, but within a local batch of vertices, which size depends on the GPU architecture. They observed that, for example in the case of the NVidia GPU the batch size is 96 indices, or 32 triangles something that is linked to NVidia’s warp size of 32 threads. The authors also pointed out that this is a characteristic of modern GPUs and older Intel GPUs do not exhibit this behaviour.

I found this interesting so I quickly put together a test, replicating their experiment to try this on 3 different GPUs: my ancient Intel HD 4000, a newer Intel 620 and an NVidia 3090. Effectively I used a index buffer with the repeated {0,1,2} index sequence of increasing size and wrapped the drawcall around a query to collect the number of vertex shader invocations. The following graph plots the results for each GPU.

![](../../assets/34339c9ea7b408a5.png)


![](../../assets/34339c9ea7b408a5.png)

True enough, the old HD 4000 never invokes the vertex shader more than 3 times, once for each of the 3 unique vertices indexed, the NVidia one demonstrates the staircase increase in the number shader of invocations, same as the newer Intel GPU. The NVidia batch size is indeed 32 triangles/96 indices while the Intel 620 one is more irregular with 3 batches of 22, 24, 22 triangles followed by a brief jump. The number of vertex attributes did not seem to make a difference, at least for the small number of them I tried.

The authors go on to argue that algorithms for per batch vertex reuse improvement should perform better than global post-transform specific ones and evaluate their proposed one, which seems to exhibit improvement in vertex reuse in most test cases on NVidia’s GPUs but not on AMD’s (GCN) and Intel’s.

The apparent lack of global post-transform vertex caching does not make existing approaches that optimise for it of less value and indeed still seem to provide a good improvement in vertex reuse on many GPU architectures. The batch-level vertex reuse view is a useful one though that could potentially enable further optimisations.

Thank you for yet another useful post!! :)

[…] for triangles that survive culling, the traditional approach often underutilizes the post-transform vertex cache. This is because index buffers are often not sorted such that vertices belonging to adjacent […]