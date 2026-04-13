---
title: Ray Tracing without Ray Tracing API
url: http://diaryofagraphicsprogrammer.blogspot.com/2018/09/ray-tracing-without-ray-tracing-api.html
author: Wolfgang Engel
published: '2018-09-07'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Following up on my last blog post, where I stated that a Ray Tracing API is bad for game developers and publishers because of the increase in QA effort that it will bring: based on the last 20+ years of graphics development, it is easy to project that when a large part of the ray tracing codebase is owned by a hardware vendor, there will be various bugs introduced with each driver release. For game developers and game engine middleware providers, it will make it expensive to support such an API.


The current main use cases for real-time Ray Tracing in games are Shadows, Reflections, and Ambient Occlusion.

To find out how easy it would be to avoid using the Ray Tracing APIs, we wanted to see how fast "native" implementations would be compared to the ones that are using Ray Tracing APIs.


At the time, Kostas Anagnostou


Today a new release of The Forge came out that supported his approach to Hybrid Ray Traced Shadows. It is running on all platforms that The Forge supports and the iOS version is running astonishingly well.



Here is a screenshot running on an iPhone 7 with the Sponza scene and iOS 11.4.1 (15G77). Resolution is 1334 x 750.




The current main use cases for real-time Ray Tracing in games are Shadows, Reflections, and Ambient Occlusion.

To find out how easy it would be to avoid using the Ray Tracing APIs, we wanted to see how fast "native" implementations would be compared to the ones that are using Ray Tracing APIs.

At the time, Kostas Anagnostou

[@KostasAAA](https://twitter.com/KostasAAA)had experimented with getting hybrid Ray Tracing running on lower-end GPUs. I was talking to him because he was supposed to write an article for GPU Zen 2 about a culling system. I asked him if he would be interested in integrating his experiments in the Confetti rendering framework The Forge, so that we can run them on more platforms like Linux (VLKN), macOS / iOS (Metal 2) and then the XBOX One. When he started working on this, he re-visited some of his former ideas and improved the performance substantially. He wrote a blog post here:[Interplay of Light](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/)Today a new release of The Forge came out that supported his approach to Hybrid Ray Traced Shadows. It is running on all platforms that The Forge supports and the iOS version is running astonishingly well.

We have reason to believe that when it comes to hybrid Ray Traced Shadows, at the moment it is better to not use a Ray Tracing API. When using DXR, we expect Hybrid Ray Traced Shadows to run on all hardware apart from the GeForce RTX with subpar performance. We expect our implementation when compared to a DXR version both running on a GeForce RTX, to perform admirably and most important practically useful in games.

This approach was developed on a PC running Windows DX12 / VLKN; we just ported the PC version to macOS / iOS and the other target platforms. In case we would spend some time doing iOS specific optimizations there might be opportunities to improve framerate.





The next step is to develop a Hybrid Ray Traced Reflection approach.

The general hope is to make it possible to have Hybrid Ray Traced Shadows, Reflections, and Ambient Occlusion on all GPUs and on all platforms available.

Let's see how far we can get ...






## 3 comments:

"When using DXR, we expect Hybrid Ray Traced Shadows to run on all hardware apart from the GeForce RTX with subpar performance"


I'm a bit confused by this statement. At the moment, Nvidia RTX/Volta is the only hardware that actually supports using DXR. Are you suggesting that the other vendors are going to release DXR implementations that are sub-optimal compared to what you have in Confetti?

Yep that is a bit confusing. As you say, DXR currently only runs on GeForce Volta/RTX. On everything else it is very slow.


I hinted towards the fact that even if you compare DXR on RTX GPU with our handwritten implementation, it should look favorable.

Don't take my word, download the source code and try it ... you can also try on many platforms :-)

Let me know how it goes.

I'd like to join MJP's question.



Is by DXR performance it is meant the performance of Microsoft's (reference?) implementation? Or it's something else?

I did compare it to Microsoft's implementation, and indeed it seems quite faster. But to be frank, I'm more interested in vendor DXR implementations rather than Microsoft's.

Post a Comment