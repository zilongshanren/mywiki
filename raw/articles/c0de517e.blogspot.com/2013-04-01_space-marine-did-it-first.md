---
title: Space Marine did it first!
url: https://c0de517e.blogspot.com/2013/04/space-marine-did-it-first.html
published: '2013-04-01'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

You know, I don't usually post links to news or so, but all the guys behind Space Marine worked so hard and were so amazing I have to do this shameless plug. I think you get more attached to a product when people work really their ass off, and they are super smart, and in the end, sales are not great... Oh well...

Nowadays a few people are doing "medium range" ambient occlusion using top-down projected and blurred depth buffers. No one credited Space Marine and I think very honestly, as we didn't publish much at all on it. Still, it might be worth a second look at the slides I've pushed, as SM's technique

**still has a few tricks**that I didn't see in the others I've seen around so far, with titling to keep the update times small and depth peeling to handle interiors and areas with multiple heights.- See page 18 here
[http://www.scribd.com/doc/109384407/33-Milliseconds-Public-With-Note](http://www.scribd.com/doc/109384407/33-Milliseconds-Public-With-Notes) - IQ's version is
[here](http://www.iquilezles.org/www/articles/multiresaocc/multiresaocc.htm) - Assassin's Creed 3 technique was
[presented at GDC13](http://schedule2013.gdconf.com/session-id/822310)

**Shadowmaps and cascades rant/thoughts...**

On a only slightly partially related note, and to add some "novel" content to this post, I was wondering for a bit about shadowmaps. We tried a

[couple of ways](http://c0de517e.blogspot.ca/2012/08/service-update-cached-shadowmaps.html)couple of ways of caching them, but in SM they failed.

Simply updating some cascades every other frame didn't work with self-occlusions of dynamic objects, and re-rendering dynamics (and more

[advanced methods](http://c0de517e.blogspot.ca/2011/03/stable-cascaded-shadow-maps-ideas.html)) failed because the bandwidth required to move shadowmaps around was huge on 360/ps3.
What I don't remember anymore is if we tried to solve the problem of the self-shadowing by accessing the cascades of the dynamic objects using the position they had at the previous frame (when the cascade was computed). My memory is very bad (that's partially why I keep this blog...), I'll have to ask my then coworkers about this. If we didn't try, I was dumb. If we did, I wonder why it failed. Food for thought, maybe I'll post an update on this later on. As far as I gathered, Crytek didn't do this in their every other frame update on Crysis 2.



There are ways, like stenciling and using a MRT containing last frame's world position... which could have been later used for motion blur vectors (which we did compute), so it's not crazy even in that scenario, but I'm quite sure now we didn't try all this, for how bad my memory is I would have remembered such a large change :)



**Update**: I see the catch. Space Marine did "splat" the shadows in screen space, for good reasons. And if you do so, you reconstruct the position of the objects to be shadowed using the current frame depth buffer from a depth prepass (in our case, from the GBuffer pass, being a deferred renderer), there is no easy way to implement this.There are ways, like stenciling and using a MRT containing last frame's world position... which could have been later used for motion blur vectors (which we did compute), so it's not crazy even in that scenario, but I'm quite sure now we didn't try all this, for how bad my memory is I would have remembered such a large change :)

*Bonus hint: always point your SSAO towards the sky...*
## 1 comment:

It is true. I have read your posts, before AC3 presentations.





Your posts about Space Marine optimizations are extremely helpful for everybody that wants to learn something.

Thanks for sharing.

Post a Comment