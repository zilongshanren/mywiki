---
title: Creating a 3D Game Engine (Part 24)
url: https://cybereality.com/creating-a-3d-game-engine-part-24/
author: Cybereality
published: '2014-10-22'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

It’s been some time since the last 3D engine update, but I’m still sticking with it. Currently I am working on getting a physics engine implemented. The video you see above is the first glimpse of this custom physics engine. Obviously it’s ultra basic right now, but it’s a start. The algorithm is based on a verlet integrator, and the code is running using DirectCompute on the GPU.

To be honest, it’s pretty hacked together right now, and the bounds/bouncing behavior is hard-coded. But, hey, it’s something! I also tweaked the style of the demo to more closely align with other demos from researchers (and the clean flat-shaded style looks a bit more classy).

I’m planning on expanding this significantly, but still have a lot of work ahead of me. Though I’m still questioning whether GPGPU is the way to go with this, especially since there are 8-core CPUs available for consumers (and which I am running now). There is also added difficulty and limitations of DirectCompute rather than straight C++. But if there are big gains on the GPU obviously I would like to go that route. Definitely more testing to do here, but progress is being made. Stay tuned.