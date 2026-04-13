---
title: Update on CentiLeo, the out-of-core GPU ray tracer
url: http://raytracey.blogspot.com/2011/06/update-on-centileo-out-of-core-gpu-ray.html
author: Sam Lapere
published: '2011-06-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

CentiLeo, the awesome out-of-core interactive GPU path tracer for massive models (like the 400 million polygon Boeing 777 model) that I've blogged about in




According to the


As mentioned in the last post, Kirill Garanzha will also present a paper entitled


Update: This week, Garanzha also presented a paper at the Computer Graphics International 2011 conference on a novel way to build high quality BVH's on the GPU (quality measured by GPU path tracing on a GTX 480) with the title "



[this post](http://raytracey.blogspot.com/2011/04/centileo-brand-new-interactive-out-of.html), is going to be presented this summer at Siggraph:[http://www.siggraph.org/s2011/content/out-core-gpu-ray-tracing-complex-scenes](http://www.siggraph.org/s2011/content/out-core-gpu-ray-tracing-complex-scenes)According to the

[video on youtube](http://www.youtube.com/watch?v=mxx9dyPO0js)"CentiLeo implementation uses CUDA and is based on Kirill Garanzha's PhD research in Keldysh Institute of Applied Mathematics, Russian Academy of Sciences."As mentioned in the last post, Kirill Garanzha will also present a paper entitled

**"Simpler and Faster HLBVH with Work Queues"**at High Performance Graphics 2011, which aims to make real-time ray tracing of highly dynamic scenes possible by fully rebuilding (instead of refitting which significantly degrades ray traversal performance) the BVH from scratch in real-time. Combined with the out-of-core path tracing tech from CentiLeo, this could be very compelling and make photoreal animations of highly dynamic multi-million polygon scenes render very fast on the GPU.Update: This week, Garanzha also presented a paper at the Computer Graphics International 2011 conference on a novel way to build high quality BVH's on the GPU (quality measured by GPU path tracing on a GTX 480) with the title "

## No comments:

Post a Comment