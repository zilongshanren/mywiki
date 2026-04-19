---
title: New Direction for Real-Time Character
url: https://cybereality.com/new-direction-for-real-time-character/
author: Cybereality
published: '2025-12-05'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/58ba0637a759832a.jpg)

Started testing a new character design for the real-time project. Even though I was happy with the artist I had, rigging and retargeting the animation was turning into a massive headache due to the extreme amount of bones. These would allow things like clothing physics and costumes, however the motion capture pipelines is already convoluted, and dealing with 200+ bones ended up being too unwieldy.

Found a different artist with a simpler stylized aesthetic. Mainly due to having a very basic rig (around 50 bones) and also much less complexity to deal with in terms of extra outfits and accessories. Thinking I may just move forward with the less complex design for now, so I can get comfortable with the art tools, and perhaps switch back to the original character later, or use the assets for a follow-up title.

Video above shows the current state of the motion-capture running in real-time in Degine, my custom OpenGL 3D game engine. Uses studio recorded iPhone video, run through QuickMagic (AI video-to-mocap solution), and then cleaned-up using Cascadeur. Still some small popping and weirdness, but I’ve only had a few days to learn the tools and still need to work with it more.