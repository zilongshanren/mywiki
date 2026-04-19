---
title: New Alternate Costume Real-Time 3D Mocap Clip and Progress Update
url: https://cybereality.com/new-alternate-costume-real-time-3d-mocap-clip-and-progress-update/
author: Cybereality
published: '2026-01-18'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Got a new demo video up with the almost final motion capture pipeline and alternate costume for the character. Despite looking highly erotic, it’s not a hentai game. Not sure the project really fits exactly any specific genre, though might best be described as a chatbot (though perhaps not what you expect). Still fleshing out exactly what’s feasible for launch, but hope to announce the name and more details soon.

For now I’m still finalizing the art, ran into a few issues with the rig that the artist is updating, so likely want to get that together before doing the retarget on all the animation (there are over 100 video clips total). It’s looking pretty good so far, and only a few small kinks that need to be addressed. Using video recorded on an iPhone, facial capture with LiveLinkFace, body motion with QuickMagic, cleaned up in Cascadeur, and then retargeted in Blender, before exporting for Degine, my custom OpenGL engine. Quite a lot of moving parts, and pretty amazing it works at all, but looks like I got it sorted out.

![](../../assets/697a2202153b46c1.png)

Performance is still looking smooth, even with the near final character animation, getting a highly suspect 666 FPS with the base graphics and post-processing disabled at 1080P. With all the effects enabled, but with 720P to 1080P upscaling, it’s in the 500 FPS range, so should be more than enough headroom after I had more assets and an actual level environment.

![](../../assets/45ac4d9286c4b887.png)

The game probably has a few months of development (at the very least) left, so considering launching the engine code open-source first, as a sort of “tech preview” or public alpha, and then a real-time demo after that point, while I continue finishing the full production, but it’s a ton of work so don’t wish to give any specific dates just yet. I’ve been setting unrealistic goals, and missing them, this entire time, though it’s been close to 3 years so might just have to push out what I have and not wait forever until it’s perfect (cause things are never perfect).