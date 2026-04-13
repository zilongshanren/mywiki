---
title: Screenshot Saturday 185
url: https://etodd.io/2014/08/16/screenshot-saturday-185/
published: '2014-08-16'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 185

Hello friends. Yesterday I finished the 5th level! It took much longer than anticipated because it's actually 10 separate maps connected together. It includes some simple but hopefully interesting puzzle mechanics.

It also advances the story through notes and several text conversations scattered throughout.

It's hard to see in screenshots, but I added a subtle cloud shadow effect as well. It doesn't respond to the actual clouds, so in a sense it's slightly faked. Because of that I was able to do the projection easily with a ray-plane intersection rather than a full matrix multiplication. Here's the shader code, edited for clarity:

```
float t = -worldPosition.y / SunLightDirection.y;
float p = worldPosition.xz + t * SunLightDirection.xz;
output.lighting *= tex2D(CloudSampler, p * CloudUVMultiplier + CloudOffset).a;
```


I already started on the next level. My plan calls for a night scene with falling water, so Thursday I worked on the beginnings of a cute little waterfall effect. It's just a Blender model with the UVs stretched so that the texture moves faster as it reaches the bottom.


That's it for this week. Thanks for reading!