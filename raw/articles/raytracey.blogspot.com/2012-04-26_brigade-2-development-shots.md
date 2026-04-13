---
title: Brigade 2 development shots
url: http://raytracey.blogspot.com/2012/04/brigade-2-development-shots.html
author: Sam Lapere
published: '2012-04-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've just received some jaw-dropping Matrix-like debug screenshots from Brigade developer Jeroen van Schijndel, showing a glimpse of an in-development ultra-efficient BVH acceleration structure. The screenshots visualize the bounding volumes (nested axis-aligned bounding boxes against which rays are tested before they are tested for intersection with the primitives that are contained in these AABBs) in the "Streets of Asia" scene that was shown in

[previous](http://raytracey.blogspot.com/2012/04/720p-video-of-streets-of-asia.html)[posts](http://raytracey.blogspot.com/2012/04/real-time-photorealistic-gpu-path_23.html). Brigade also gained a dazzling__30%__increase in performance yesterday.
## 18 comments:

The amount of represented complexity is simply staggering! It's also nice to see the bounding structures to get a good idea of ray traversal.



Thanks for this!

I'm also really looking forward to the 30% performance improvement. That's quite a significant jump!

Yeah, Brigade's momentum is unstoppable at this point :)

Any way to know more about that BVH construction ? or is it the traversal (or both) that changed ?

Can't say more, sorry.

Hey Sam, I took one of your city renders and composited a (quickly) simulated bloom using a drawing program. IMO it really improves the photorealism of the scene! Considering that bloom is cheap enough to be done on mobile devices, it may be a way to kick up the photorealism of your scene with minimal cost.




Not a suggestion or anything, just something interesting that I came across that I felt was worth sharing.

Take a look!

https://docs.google.com/file/d/0B0FdA13fLr4GU3VQa3B6eFU3czA/edit#

It was formed by blurring bright areas multiple times (gausian) and compositing with the original frame.

Sean, that's awesome! The bloom really does make it look more real. Maybe it's worth taking a look at some post-process bloom and tonemapping techniques.


Thanks.

Just found some OpenGL code for HDR bloom effects, will try it tomorrow. sean, if you have any other tips to improve the image, let me know :)

God rays.

No problem! If I think of anything else I will certainly let you know, but I think this is about the limit of what I can suggest off of the top of my head. Of course I still really like the idea of realistic motion blur. Perhaps it can be done in post (like many modern games)?






Tone mapping is such a *fantastic* idea! This should add a tremendous amount of realism to the scene, and the twin 580s should handle this quite easily in post.

I also think the inherent grain of the images adds a touch of realism. I wouldn't completely remove the noise!

I think with these, you will have achieved photo-realism enough to require people to scrutinize the image closely and guess weather it's virtual or not.

Asking a photographer to play with different settings may be a good idea for the perfect look...

I'm just reaching now. You've done such a good job. You should be proud!

Thanks Sean, this is really helpful. A photoreal look is what I was aiming for and I'm glad to know that at least one person thinks I've reached that goal ;)


Motion blur in post, nice idea actually. Brigade could benefit from all the post process tricks in current high end games as well. Brigade already supports exposure adjustment and real ray traced depth-of-field, so if we throw in some tonemapping, hdr bloom and faked motion blur, it will be like a real-time movie :)

Mr Papillon: god rays are cool too and they can be done in post:



http://http.developer.nvidia.com/GPUGems3/gpugems3_ch13.html

Thanks for the suggestion. Keep them coming :)

Oooh! I just had another idea. This one is a little less obvious, though I think would help the illusion of photorealism.




Hand-held shaky camera. If the camera jitters as if it were being held by a human when moving, rather than gliding ultra-smoothly, it would give the increased perception of being a real scene rather than a virtual one. This is a subtle effect but adds a ton if pulled off right. Thankfully, it should also be cheap to implement!

I was just analysing Avatar, and I noticed that it uses a shaky cam for most of the scenes, which gave me the idea. In higher tension shots, the camera seems more shaky and it mutes somewhat for calmer shots.

Ok.. I think that's it! I'm out of ideas.. ;)

Thanks Sean, a shaky cam is a good idea and reminds me of this Pepeland video (one of the first animations rendered with Arnold):




http://www.youtube.com/watch?v=CJzJ9WuLH2w

When I saw that video for the first time in 2000 (right after Quake 3 came out), I remember thinking 'if we can have this quality in real-time, we're done'. 12 years later, I think we're almost there.

I'll give it a try.

Wow! I actually had to check the comment for that video, because I could have sworn that it was a scene being filmed rather than rendered. It's so compellingly photo-real, and the scene itself seems remarkably simple.


Thanks for that!

It's the magic of path tracing :).




You can see a high-res screenshot of that video on page 162 of this siggraph presentation:

http://www.cs.princeton.edu/courses/archive/fall02/cs526/papers/course29sig01.pdf

only 550k triangles in the scene

You aren't kidding! The image is just as impressive in high res, and no less real looking.


And thanks for this amazing document. I've saved it to my Google Drive and am looking forward to reading through it.

you're welcome :)

Don't you find it anoying when Ray Tracey's blog stays at 17 posts for 3 days and when it finally goes to 18 it's a nonsense reply like this one? ;)

Post a Comment