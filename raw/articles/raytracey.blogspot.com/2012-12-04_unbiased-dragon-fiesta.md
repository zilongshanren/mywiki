---
title: Unbiased Dragon Fiesta
url: http://raytracey.blogspot.com/2012/12/unbiased-dragon-fiesta.html
author: Sam Lapere
published: '2012-12-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

It's been a long time since I posted a video about Brigade (blame Octane Render, which is so fucking awesome and addictive it's not even funny anymore, check for example this video:

[http://www.youtube.com/watch?v=7zfCn24bGGk&list=UL](http://www.youtube.com/watch?v=7zfCn24bGGk&list=UL)). But the latest addition on Brigade definitely deserves a new video: we now have instancing working, it's really useful (best part of the video at the end):
What you see here are 32x32 (1024) Stanford dragons, each containing 100k triangles for a total of more than 100 million triangles, all path traced in real-time. This number is actually quite modest, as we can easily scale up to billions of triangles and still be real-time. This is impossible to achieve with a rasterization based game engine. I'm convinced that instancing will be the decisive factor for game engines to switch to ray tracing and is actually going to be more important than having perfect shadows, reflections, refractions, indirect lighting, diffuse color bleeding, physically based materials, raytraced ambient occlusion and DOF.

The next step is to make practical use of this feature in a game like setting: I want to use the city scene from one of my earlier demos (see

## 13 comments:

Wow! Is it possible for each instance to have its own material while maintaining the same level of performance?

hey, nicely done!


I wanted to ask, who works on Brigade ? it's Jacco and you ?

Congratulations, Sam! You have invented instancing. But there are 25 other rendering engines, Maxwell, vray and others.

Your blog is hired, and you became just an adverticer. It is not yet as informative as it has been.

To the Anonymous poster above me, well done for your excellent comment, twats like you are not welcome please dont ever come back!




Im also curious as to who is doing the current development of this as brigade is now I think owned by OTOY, I would hope its still Jakko...

Nice to see Brigade shaping up well, it would be good to see an OpenCL or DirectCompute version so that all the AMD Radeon owners out there could participate... It could let those without GPU's also have some fun with it, I wonder how much slower it would actually by running on an i5 or i7 ?

Otherwise excellent progress...

Instancing is nice, but it's been done - although don't get me wrong, it's fantastic that Brigade now has it. But, what I personally would like to see (for interactive ray tracers in general) is a stress test in smooth skinning and character animations - maybe even crowds of characters.

While I disagree with the the sarcasm of the 3rd annonymous post (and the response of the 4th post for that matter), the quality of information in this blog has dropped ever so slightly since Sams joining OTOY. The details, the nitty gritty...the numbers...its all but dried up. The diversity in posts has also greatly reduced, less about RT in general and more an advert. I still pop by here every few days to check things, but I'm not as excited as I used to be.




Keep up the good work, there still is no other blog like this, but please more of the old stuff.

Instancing is important, nice feature. I hope you could add something like shader/material variations like it was said in a previous post.

If the instancing is so good, is it possible to use it as a volumetric particle system (high amount of very optimized stuff) ?

I will do my best to answer every comment, although I'm very limited in time right now (I wish there were 48 hours in a day).
















Dima: thanks. It should be possible, I will try once I find some time again

Mirror: also thanks :) I'm not working on the core of Brigade, others are, can't go into details

Anonymous1: thanks, I'm glad I'm the first who came up with instancing. Well, I've been advertising and promoting Octane since Jan 2010 (do a search on my blog), long before I became a part of it. It just happens to be the best rendering experience by far.

Anonymous2: yes, OTOY owns Brigade. Can't say much more about OpenCL and DX

Reaven: instancing of this many dynamic objects in a real-time path tracing context hasn't been done before (except for Octane), correct me if I'm wrong. Instanced animated character are possible as well, the problem is that they will all have the same pose.

Antzrhere: I hear ya, but other things have more priority now. Thanks for your loyalty.

MrPapillon: yep, particles can be done this way :) about the material variations: it should be possible.

Thanks for your response Sam. I did think other things would take focus, and things are bound to be different now your working for OTOY. I still enjoy the blog and has inspired me to make my own little OpenCL PT after my viva next week (hopefully will have more time soon).


One Q. - can you have multiple instances that overlap each others (i.e. dragons intersecting each other) ?

Yes, that's possible, but performance sinks when you have overlapping bounding boxes. I accidentally rendered all thousand dragons at the same spot and it ran at 0.5 fps.


Show me the results of your OpenCL PT once it's finished, as you may know I like everything GPU path tracing related ;)

Hmm, concerning the character animation... If you separate triangles that belong only to one bone from the rest of the character's mesh, these pieces can be instanced. I guess it would be reasonable to expect some amount of speed-up (and memory efficiency) depending on how rigid the character is (i.e. good for armoured/mechanical characters).

Also, I'm curious if such trick would introduce "glitches" when rays exactly hit a seam between the skinned and the instanced pieces.

Dima, that's actually an excellent idea and I'm pretty sure it will work great, because I tested it with Octane and 3ds Max a few months ago and it worked amazingly well: http://www.youtube.com/watch?v=31FvXIOxEVk

How many users, who actually pay, does Octane have?

Post a Comment