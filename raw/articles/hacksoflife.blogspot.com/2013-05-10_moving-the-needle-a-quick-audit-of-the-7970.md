---
title: Moving the Needle - a Quick Audit of the 7970
url: http://hacksoflife.blogspot.com/2013/05/moving-needle-quick-audit-of-7970.html
author: Benjamin Supnik
published: '2013-05-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I dropped X-Plane into ~~ATI~~AMD's


And...


(Sigh...)


We're mostly CPU bound. Still.


You know those GDC talks where the first thing the IHVs say is "most games are CPU bound?" I can feel them glaring in my direction.


There was one case where I was able to absolutely hose the GPU: a full screen of thick particle-type clouds at 1080p + with 4x SSAA. You can tell you're GPU bound just by the amount of heat the card blows out.


What was cool though, was running a batch profile in GPU PerfStudio and sorting by GPU time. At a whopping, facemelting, eye bleeding 32 ms was a single batch of cloud puffs (about 10k vertices) that covered most of the screen. The histogram falls off from there, with the next few most expensive cloud batches taking a few ms and everything else being noise.


This isn't hugely surprising...we know our cloud system is a fill-rate pig and thus responds badly to very large render surfaces...the real surprise is how the GTX 680 copes with them so well. (What is less obvious is what to do about it; I fear the halo-type artifacts that a lot of half-res solutions provide may be a deal-breaker; re-rendering the edges with stencil will increase our geometry count and we do have a lot of puffs. Probably the right thing is to start using hardware MSAA surfaces for the G-Buffer to leverage hardware compression.)


I went looking for anything else that might be slow and finally got an answer about


With the GPU profiler, I could see that a moderate sized batch of light volumes around the Apron at our Seattle demo airport takes about 1.5 ms to render at the aforementioned rather large resolution. The scene has maybe 3 or 4 volumes of that magnitude, and the rest are small enough in screen space that we don't need to care.


That only adds up to 6-10 ms of GPU time though - and given that the sun pass is fast enough to not show up in the top 10 list, FXAA is fast and even scenery fill isn't so bad, it's clear why light fill isn't the long pole, particularly when the CPU is struggling to get around the frame in 30 ms. Cutting CPU work does appear to be the right thing here.


The real right thing, some day, in the future, when I have, like, spare time, would be to do two scene graph passes: the first one would draw lights except in the near N meters, with no stencil; the second pass would only grab the near lights and would do two passes, stenciling out the lights first. This would give us the fill rate fix in the one case where it matters: when the light is close enough to be huge in screen space. (Our non-sun lights tend to be reasonably small in world space - they are things like street lights, apron lights, and airplane landing lights.)


There is one limitation to GPU PerfStudio2 that frustrated me: because it doesn't sniff the call-stack during draw calls, it can't easily do data mining for the source of poor performance. That is, if you have a big app that generates a huge frame using a number of common subsystems, if one subsystem sucks, it doesn't data mine that for you. (Note: I did not experiment with trying to inject frame markers into the draw call stream...I don't even know if they support that using the KHR debug extension.)


My next step will be to integrate the NV and ATI performance counter APIs directly into the sim. We have, at various times, had various timing utilities to allow us to rapidly instrument a code section in a way that follows the logical design, rather than just the call stack. (Shark was so good that we didn't use any utilities for a while.) With the GPU performance counters, we could potentially build HUD-style GPU metering directly into the app.

[GPU PerfStudio 2](http://developer.amd.com/tools-and-sdks/graphics-development/gpu-perfstudio-2/)to see what might be going on on the GPU side of things. This is on a Sandy Bridge i5 with a 7970 on a 1920 x 1200 monitor. I cranked the sim up to 4x SSAA (stupidly simplistic anti-aliasing) to really push fill rate.And...

(Sigh...)

We're mostly CPU bound. Still.

You know those GDC talks where the first thing the IHVs say is "most games are CPU bound?" I can feel them glaring in my direction.

There was one case where I was able to absolutely hose the GPU: a full screen of thick particle-type clouds at 1080p + with 4x SSAA. You can tell you're GPU bound just by the amount of heat the card blows out.

What was cool though, was running a batch profile in GPU PerfStudio and sorting by GPU time. At a whopping, facemelting, eye bleeding 32 ms was a single batch of cloud puffs (about 10k vertices) that covered most of the screen. The histogram falls off from there, with the next few most expensive cloud batches taking a few ms and everything else being noise.

This isn't hugely surprising...we know our cloud system is a fill-rate pig and thus responds badly to very large render surfaces...the real surprise is how the GTX 680 copes with them so well. (What is less obvious is what to do about it; I fear the halo-type artifacts that a lot of half-res solutions provide may be a deal-breaker; re-rendering the edges with stencil will increase our geometry count and we do have a lot of puffs. Probably the right thing is to start using hardware MSAA surfaces for the G-Buffer to leverage hardware compression.)

I went looking for anything else that might be slow and finally got an answer about

[pre-stenciling lighting volumes](http://hacksoflife.blogspot.com/2012/11/deferred-lighting-stenciling-is-not-win.html). Our first deferred rendering implementation pre-stenciled lighting volumes to cut fill rate; we dropped the stencil pass when we found that we were CPU and AGP bandwidth bound; the only time losing stencil was a problem was in high-zoom lighting scenarios.With the GPU profiler, I could see that a moderate sized batch of light volumes around the Apron at our Seattle demo airport takes about 1.5 ms to render at the aforementioned rather large resolution. The scene has maybe 3 or 4 volumes of that magnitude, and the rest are small enough in screen space that we don't need to care.

That only adds up to 6-10 ms of GPU time though - and given that the sun pass is fast enough to not show up in the top 10 list, FXAA is fast and even scenery fill isn't so bad, it's clear why light fill isn't the long pole, particularly when the CPU is struggling to get around the frame in 30 ms. Cutting CPU work does appear to be the right thing here.

The real right thing, some day, in the future, when I have, like, spare time, would be to do two scene graph passes: the first one would draw lights except in the near N meters, with no stencil; the second pass would only grab the near lights and would do two passes, stenciling out the lights first. This would give us the fill rate fix in the one case where it matters: when the light is close enough to be huge in screen space. (Our non-sun lights tend to be reasonably small in world space - they are things like street lights, apron lights, and airplane landing lights.)

There is one limitation to GPU PerfStudio2 that frustrated me: because it doesn't sniff the call-stack during draw calls, it can't easily do data mining for the source of poor performance. That is, if you have a big app that generates a huge frame using a number of common subsystems, if one subsystem sucks, it doesn't data mine that for you. (Note: I did not experiment with trying to inject frame markers into the draw call stream...I don't even know if they support that using the KHR debug extension.)

My next step will be to integrate the NV and ATI performance counter APIs directly into the sim. We have, at various times, had various timing utilities to allow us to rapidly instrument a code section in a way that follows the logical design, rather than just the call stack. (Shark was so good that we didn't use any utilities for a while.) With the GPU performance counters, we could potentially build HUD-style GPU metering directly into the app.

## No comments:

## Post a Comment