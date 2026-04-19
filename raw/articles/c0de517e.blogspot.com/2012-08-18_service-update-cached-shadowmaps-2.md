---
title: 'Service Update: Cached Shadowmaps'
url: https://c0de517e.blogspot.com/2012/08/service-update-cached-shadowmaps.html
published: '2012-08-18'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

This is probably not news, and I don't often post links or summaries of conferences, as there are many people that do a better job than I would at that, but since I posted a bad sketch of an half-tested idea a while ago about

[caching cascaded shadowmaps](http://c0de517e.blogspot.ca/2011/09/bad-ideas-dont-require-much-explanation.html)I got some inquiries about it. So why didn't I wrote something decent? Let me digress :)
At that time our team at work was trying to optimize a game's GPU performance, and among the various things, shadows were a problem. We were already experimenting with some forms of caching of static objects, we had this idea (inspired by looking at Crysis 2 in action... if you look closely you can see this) of rendering our far cascaded every other frame (five in total, in a frame we would

update the first one and two of the remaining four).

This worked only so-so due to dynamic casters being able to walk "into" their own shadows, so we tried to cache the static objects and render only the dynamic objects every frame (for the two cached cascades). This turned out not to be a win with the size of our shadowmaps, we were basically using half of the shadow generation time in bandwidth/resolve, so the caching didn't really bring anything.

This consideration, killed for us the incentive to go further implementing other caching schemes, and left me wondering if on this generation of consoles this scheme could really turn out to be faster.

Well, wonder no more! Luckily, decent ideas tend to eventually be discovered many times and recently Mike Day published an excellent work (presented by Mike Acton) on something that he implemented which is closely related to the bad idea sketch I posted on the blog.

[His work is very detailed](http://www.insomniacgames.com/mike-day-siggraph-2012-csm-scrolling/)and provides all the information on how to implement the technique, so go and read this paper if you haven't already.
He does the caching by reprojecting the old information both in UV and in depth before splatting in the dynamic occluders, as at the time I was already concerned about the bandwidth, I was speculating of using the stencil to tag the z-near and z-far used to render a given region (that though would have worked only on 360 and ps3 where with some trickery you can access the stencil information while sampling the depth shadowmap, not on dx9) and using other hacks which are probably not worth their complexity as they would still result in the same worst-case scenario.

*P.S. You might have noticed the little "posted with Blogsy" logo at the bottom of this article, this is the first time I use my iPad for the blog and I have to say, I'm pleased. This little app lets you write the post with all the formatting features (which I don't use) and integrates a browser and image functionalities so you don't have to fight with the broken (absent) multitasking of iOS.*

*And here, let me go*

**full hipster**with a photo taken with HDR Camera on Android, then abused on Instagram and uploaded to the blog via its Picasa account... It will burn your eyes :)![](../../assets/8b47da7ef7271c9a.jpg)


![](../../assets/8b47da7ef7271c9a.jpg)

## 2 comments:

The paper was presented by Mike Acton, but the author is Mike Day. Please give Mike Day credit as well.

Sorry about that, fixed!

Post a Comment