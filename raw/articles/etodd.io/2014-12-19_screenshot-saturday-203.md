---
title: Screenshot Saturday 203
url: https://etodd.io/2014/12/19/screenshot-saturday-203/
published: '2014-12-19'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 203

Big update this week!

My voxel renderer now has the capability to overlay everything with any texture I want. I'm using it on a new set of interconnected winter levels. This way I don't have to manually come up with a frosty version of each texture.

Without giving away too much, this week I built a new system that has implications for both puzzle solving and movement mechanics.

I also went back to several levels and fiddled with lighting again. Basically 90% of my development time is spent adjusting colors. Before / after:

![](../../assets/02d923063717cb3e.jpg)


![](../../assets/02d923063717cb3e.jpg)

Clearly, the old version relied heavily on bloom. I'm trying to avoid that a bit more now. Bloom is like crack cocaine to game developers.

Other random things:

- When you walk off an edge, there is now a split second of forgiveness during which you can still jump. Just filing down another edge to make player movement less frustrating.
- I finally killed an old glitch that subconciously annoyed me for years.
Lemma has "bullet time", and up until this week it stuttered noticeably when running in slow-motion, despite maintaining a high framerate.
I peeked into the
[BEPUPhysics](http://www.bepuphysics.com/)source code and realized it runs on a[fixed timestep with an accumulator](http://gafferongames.com/game-physics/fix-your-timestep/). It updates at 60 FPS regardless of the actual framerate. So when I changed the time scale, that 60 FPS dropped to 30 FPS. But no more! I now scale BEPUPhysics' target framerate as well, and the result is silky smooth slow motion. - I liked using
[Jekyll](http://jekyllrb.com)for my blog so much, I also migrated the[Lemma website](http://lemmagame.com), and updated it in the process. The site was already hosted on S3 so half the work was already done.

That's it for this week. Thanks for reading!