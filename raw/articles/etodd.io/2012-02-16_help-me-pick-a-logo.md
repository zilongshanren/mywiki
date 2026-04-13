---
title: Help me pick a logo!
url: https://etodd.io/2012/02/16/help-me-pick-a-logo/
published: '2012-02-16'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Help me pick a logo!

I'm going to try and post smaller, more frequent articles. This whole "two months between massive walls of text and screenshots" thing is not working out.

So, the alpha I promised is *still* inbound. I'm working as fast as I can! And I think it's paying off. For a while I was very worried about performance. In my last post I talked about how I optimized the renderer, but there were still issues with the physics engine. I was putting each cube into the physics space as a separate entity, which was making it absolutely crawl, even on my eight core i7.

I rewrote it to take advantage of the new chunk system; now each chunk is a triangle mesh in the physics world. So the engine only has to do a few AABB checks to narrow down collisions to a single triangle mesh. BEPUphysics is happy.

While I was optimizing I also added a simple performance counter and used the fantastic [EQATEC Profiler](http://www.eqatec.com/Profiler/) to track down some other bottlenecks. You can see the result below. Notice the fantastic performance. :)

By the way, that structure was built completely in-game. More on that later when the alpha's released!

I'm starting to work on finalizing little things for the alpha, like getting the story across, figuring out what happens when the player dies, and figuring out a decent logo to use. Speaking of which, have a look at these:

Which do you like better? Any suggestions? Sound off in the comments!

Oh, before I go, I quick wanted to show off some artwork I did for school here. Done in Cinema 4D, took me roughly seventy billion hours.

Yes, those are nail clippers. :) Have a great week everybody! Keep your eyes peeled. Alpha. Seriously.