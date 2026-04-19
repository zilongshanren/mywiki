---
title: Creating a 3D Game Engine (Part 18)
url: https://cybereality.com/creating-a-3d-game-engine-part-18/
author: Cybereality
published: '2014-05-26'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/ceff3c582f91a5f1.jpg)


What you see above is a custom model I made in 3ds Max, exported as a COLLADA *.dae file, and imported into my DirectX engine. I figured I’d start with something simple, like a soda can, and I plan to make a lot more models going forward. Although I hadn’t touched Max in years, I found it to be a comfortable experience and was able to put the model together in a few hours.

Now, actually getting that model into DirectX was a different story. First off, the COLLADA documentation is vast, but they fail to explain basic things about the format. The examples they show all make sense, but with a real model it becomes more complex. To make matters worse, their forum was a ghost town and I found lots of people with the same basic questions I had that posted a thread with no replies for months (or years). That said, I was able to eventually figure it out by a lot of testing and trial and error. It really goes to show that you can build the best system in the world, but if the documentation is lacking and the community is thin, then it’s not worth jack.

To make matters worse, there was a small bug in my XML parsing code that was messing up the attributes. So some of the simple models I tried (and plane and a cube) worked, but the soda can didn’t. It ended up taking a while to track down this problem since Visual Studio was hanging if I tried to debug. It’s really scary to get to this point where you *need* the debugger desperately and it’s not there. While I thought it was crashing, it was actually just caught up in my slow parser, and when I waited for about 5 – 10 minutes it finally came back to life (and thankfully I only needed to get to that one breakpoint to see what the issue was).

Next up, I ran into some issues with the model orientation and texturing. Since 3ds Max using a Z-up coordinate system and DirectX is Y-up, this needed some special care. I would have thought the COLLADA exporter would handle this, but apparently not. The fix is to swap the Y and Z positions of each vertex. This will effect the winding order as well, so if you want your mesh to not be inside-out, you need to also change the order of the indices when you create the index buffer. For example, a triangle of “0, 1, 2” will become “0, 2, 1”. Finally I had to negate the V parameter of the UV coordinates so that the texture looked proper.

All-in-all, I am pretty happy considering I have wrote the importer basically from scratch. I would like to try some more complex models, but I will have to figure out what I want to build next. Since I am doing all this work myself, I’d like to use the engine to showcase my own artwork. I would rather not just download assets from the internet. Maybe I will build a refrigerator to put the soda in, or some more common products.

If you like what you read, post a comment and let me know how I’m doing. Cheers.