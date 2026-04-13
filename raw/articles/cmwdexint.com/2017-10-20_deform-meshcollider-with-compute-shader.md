---
title: Deform MeshCollider with Compute Shader
url: https://cmwdexint.com/2017/10/20/deform-meshcollider-with-compute-shader/
author: Ming Wai Chan
published: '2017-10-20'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

If you want to do something like this:


In **C#** : You need a for loop which

-> iterates a few ten-thousands vertices, and then

-> for each vertex, you need to calculate the distance between each bead…

All these instructions are run 1 by 1 on CPU. You can imagine the time needed for this.

——–

But with **compute shader**, those several ten-thousands iterations can be done “at the same time” in GPU (it depends how you setup the data). And the result data will be transferred back to CPU, and directly apply to Mesh.vertices array.

And this is what you can see in this video, the fps stays above 70.

**Update: This can be done much faster using AsyncGPUReadback. Visit here for example: **[https://github.com/cinight/MinimalCompute](https://github.com/cinight/MinimalCompute)

Thanks for your fantastic example references!

LikeLike