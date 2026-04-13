---
title: Real-time bidirectional path tracing via rasterization
url: http://raytracey.blogspot.com/2011/12/real-time-bidirectional-path-tracing.html
author: Sam Lapere
published: '2011-12-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is the title of an upcoming I3D 2012 paper by Yusuke Tokuyoshi and Shinji Ogaki, see




The title reminds me of "


If the paper lives up to the title, this could be quite interesting.


Quote from the "


[http://graphics.ics.uci.edu/I3D2012/papers.php](http://graphics.ics.uci.edu/I3D2012/papers.php)The title reminds me of "

[High-quality global illumination rendering using rasterization](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter38.html)" by Toshiya Hachisuka from 2005, which described a technique to obtain[photorealistic images on a typical 2005 GPU (like the Radeon 9700) in mere seconds](http://www.bee-www.com/parthenon/), extremely impressive for that time. Shinji Ogaki is also a co-author on the Progressive Photon Mapping paper by Hachisuka and Jensen, so this new paper is definitely going to be interesting.If the paper lives up to the title, this could be quite interesting.

[Both researchers work at Square Enix](http://www.square-enix.com/jp/info/library/)and there seems to be a connection with the recently unveiled photorealistic[Luminous engine](http://www.rockpapershotgun.com/2011/10/14/luminous-revolution-squeenixs-new-gfx-tech/)which uses high quality offline baked lightmaps (see[this page](http://www.siggraph.org/asia2011/technical-sketches-detail?id=68&session=sketches)for more details). A paper about the rasterization-based lightmap baking in Luminous can be found[here](http://local.wasp.uwa.edu.au/~pbourke/transient/SG11/sketches/25-0046.pdf)and the real-time bidirectional PT technique probably works very similarly (i.e. ray bundles computed with rasterization by parallel visibilty tests):Quote from the "

[Fast global illumination baking via ray bundles](http://local.wasp.uwa.edu.au/~pbourke/transient/SG11/sketches/25-0046.pdf)" paper (describing the tech behind the Luminous engine):7 high-quality light maps are rendered in 181 seconds with NVIDIA GeForce GTX 580. The resolution of ray-bundle is 2048x2048 pixels, and 10000 directions are sampled. The performance of our renderer is over 200 M rays per second on a commodity GPU.Assuming everything scales linearly, this means that it would take about 16 milliseconds (60 fps) on a GTX 580 to compute a GI lightmap with ray bundles of 512x512 pixels and 100 ray bundle directions (= 100 directional samples) which should still yield great quality real-time global illumination. This tech could potentially be used for making real-time photorealistic games on current GPUs. It doesn't work however for objects with highly glossy and perfectly specular materials.

## 3 comments:

The paper is online now:

http://www.square-enix.com/jp/info/library/

Thanks! This deserves a new post.

you beat me to it checking out the videos right now

Post a Comment