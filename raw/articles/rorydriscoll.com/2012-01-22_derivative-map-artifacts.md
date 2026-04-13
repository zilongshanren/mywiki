---
title: Derivative Map Artifacts
url: https://www.rorydriscoll.com/2012/01/22/derivative-map-artifacts/
author: Rory
published: '2012-01-22'
source_blog: CodeItNow
source_site: https://www.rorydriscoll.com
category: graphics
fetched: '2026-04-13'
---

I had been suffering from some strange artifacts on the edges of my objects when using derivative maps. After much time spent in GPU Perf Studio, I finally realised that my mipmap generation was not correct. It was introducing one extra column of garbage at every level.

My use of FXAA and anisotropic filtering was just making the problem more evident. I would recommend using regular trilinear filtering for derivative maps anyway.

So, mea culpa and all that. Let the name of Morten Mikkelsen and derivative maps be cleared!