---
title: 'Interior Mapping: rendering real rooms without geometry'
url: http://joostdevblog.blogspot.com/2018/09/interior-mapping-real-rooms-without.html
author: Joost van Dongen
published: '2018-09-23'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*interior mapping*: a technique I came up with in 2007 as part of my thesis research. I've never written about this on my blog before so I figure this a good moment to explain the fun little shader trick I came up with.

Let's start by having a look at some footage from Marvel's Spider-Man. The game looks absolutely amazing and Kotaku has captured some footage of the windows in particular:

As you can see around 0:40 in this video the rooms aren't actually there in the geometry: there's a door where there should clearly be a window. You also see a different interior when you look at the same room from a different corner of the building. In some cases there's even a wall that's beyond a corner of the building. All of these suggest that the rooms are faked, but nevertheless they are entirely perspectively correct and have real depth. I expect the faults of these rooms don't matter much because while playing you probably normally don't actually look at rooms as closely as in that video: they're just a backdrop, not something to scrutinise. I think creating rooms this way adds a lot of depth and liveliness to the city without eating up too much performance.

![](../../assets/7c0b16da6fafef2d.jpg)

Before I continue I'd like to clarify that this post is not a complaint: I'm thrilled to see my technique used in a big game and I'm not claiming that Insomniac is stealing or anything like that. As I stated in the original publication of interior mapping, I'd be honoured if anyone were to actually use it. If Insomniac indeed based their technique on my idea then I think that's pretty awesome. If they didn't, then they seem to have come up with something oddly similar, which is fine too and I'd be curious to know what they did exactly.

So, how does interior mapping work? The idea is that the building itself contains no extra geometry whatsoever. The interiors exist only in a shader. This shader performs raycasts with walls, ceilings and floors to figure out what you should be seeing of the interior.

![](../../assets/9504077cc73a4e76.jpg)

The ray we use is simply the ray from the camera towards the pixel. The pixel that we're rendering is part of the exterior of the building so we only use the part of the ray beyond the pixel, since that's the part of the ray that's actually inside the building.

Doing raycasts may sound complex and expensive, but it's actually really simply and fast in this particular case. The trick is to add a simple limitation: with interior mapping, ceilings and walls are at regular distances. Knowing this we can easily calculate which room we're in and where the ceiling and walls of that room are. Ceilings and walls themselves are infinite geometric planes. Calculating the intersection between an infinite plane and a ray is only a few steps and eats little performance.

![](../../assets/6e93ccf746abe9d8.gif)

A room has 6 planes: a ceiling, a floor and 4 walls. However, we only need to consider 3 of those since we know in which direction we're looking. For example, if we're looking upward then we don't need to check the floor below because we'll be seeing the ceiling above. Similarly, of the 4 walls we only need to consider the 2 that are in the direction in which we're looking.

To figure out exactly what we're seeing, we calculate the intersection of the ray with each of those 3 planes. Which intersection is closest to the camera tells us which plane we're actually seeing at this pixel. We then use the intersection point as a texture coordinate to look up the colour of the pixel. For example, if the ray hits the ceiling at position (x,y,z), then we use (x,y) as the texture coordinate, ignoring z.

A nice optimisation I could do here at the time is that we can do part of the intersection calculations for each of the three planes at the same time. Shaders used to be just as fast when using a float4 as when using a float, so by cleverly packing variables we can perform all 3 ray-plane intersections simultaneously. This saved a little bit of performance and helped achieve a good framerate with interior mapping even back in 2007 when I came up with this technique. I've been told that modern videocards are faster with float than float4, so apparently this optimisation doesn't achieve much anymore on today's hardware.

![](../../assets/55f66d285378eaef.jpg)

For more details on exactly how interior mapping works, have a look at

[the paper I wrote on interior mapping](http://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf). This paper was published at the Computer Graphics International Conference in 2008. Having a real peer-reviewed publication is my one (and only) claim to fame as a scientist. This paper also includes some additional experiments for adding more detail, like varying the distance between walls for rooms of uneven size and randomly selecting textures from a texture atlas to reduce repetition in the rooms. It also goes into more detail on the two variations shown in the images below.

![](../../assets/7b46510175c1094c.jpg)

Since we're only doing raycasts with planes, all rooms are simple squares with textures. Any furniture in the room has be in the texture and thus flat. This is visible in Spiderman in close-ups: the desks in the rooms are in fact flat textures on the walls. As you can see in the image below it's possible to extend our raycasting technique with one or more additional texture layers in the room, although at an additional performance cost.

![](../../assets/ebc20de7e37f812d.jpg)

After having published this blogpost one of the programmers of Simcity (2013) told me that interior mapping was also used in that game. It looks really cool there and they have a nice video showing it off. They improved my original idea by storing all the textures in a single texture and having rooms of varying depth. The part about interior mapping starts at 1:00 in this video:

If you'd like to explore this technique further you can download

[my demo of interior mapping](http://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.zip), including source code. If you happen to be an Unreal Engine 4 user you can also find interior mapping as a standard feature in the engine in the form of the InteriorCubeMap function.

After all these years it's really cool to finally see my interior mapping technique in action in a big game production! If you happen to know any other games that use something similar, let me know in the comments since I'd love to check those out.

There's a free Unity asset that does this. https://assetstore.unity.com/packages/vfx/shaders/fake-interiors-free-104029

ReplyDeleteRobo recall uses this technique as far as I can tell. I think Watchdogs also used it or something similar.

ReplyDeleteFirst appearance of this algorithm I could find was in the movie "Spider-Man" (2002), and was presented at SIGGRAPH 2002




ReplyDeletehttps://dl.acm.org/citation.cfm?doid=1242073.1242297

In 2005, I was working on this technique for an unreleased PS2 Spider-Man game. As PS2 has no pixel shaders, it was possible only to ray trace into a virtual far wall. This was done in the "vertex shader" by tracing a ray through a near wall vertex to the far wall, and calculating the far UVW. Rasterizing a quad with near XYZW and far UVW required no shader, but was identical in output to a pixel shader that ray traces into the far wall.

Glad to see this technique come back in another Spider-Man game, updated to look great for modern times.

Thanks for sharing how you approached this in Spider-Man on PS2! Sounds like a very clever rendering trick. :)



DeleteIt's quite different from what I do here because it doesn't make complete, perspectively correct rooms. I think there have also been approaches at doing this using cubemaps, which can suggest rooms but won't have actually perspectively correct rooms, but I haven't seen that in action myself.

That article on the 2002 Spider-Man movie is unfortunately behind a paywall. Do you know what they did exactly?

A friend of mine has access to the paper through his university and had a look at the SIGGRAPH paper, but it turns out that the paper only contains biographies of the presenters and not actually any content on what they presented, so I can't check whether what they did is similar to my technique.

DeleteNo, the paper is not just a list of biographies. Those are, unfortunately, the only pages I also found in a public search. A book was made with the same name as the paper, and likely has all the same info:








Deletehttps://www.amazon.com/Behind-Mask-Spider-Man-Secrets-Movie/dp/0345450043

As for exactly how Spider-Man games and movies did interior mapping in the 16 years before 2018:

* 2002: movie raytraced into a hemisphere, which actually looks pretty plausible from far away. In scenes where the camera is close to a building, they use real geometry instead.

* 2005: unreleased PS2 game had perspective-correct raytracing of the far wall of an interior. later on XB360 I compared the PS2 effect side-by-side with the movie effect, and the PS2 effect was superior.

* 2006: later work in same project (this time not by me) went further than Insomniac, by raytracing into a cubemap that stored depth-per-texel. I guess you'd call this POM nowadays, and had limited self-occlusion. at the time I felt it looked "too real," but in retrospect this was a silly thing for me to think.

it was only starting around 2006-2007, once pixel-shaded consoles hit their stride, that we saw these techniques popping up in lots of games, as documented here:

https://simonschreibt.de/gat/windows-ac-row-ininite/

Fascinating read! I think Watch Dogs (1, not sure about 2) has something similar going on with the windows.

ReplyDeleteI'm fairly sure that one of the old Gears of War games used this for shop fronts - with a far wall, and one or two alpha layers for furniture in the rooms.

ReplyDeleteOne minor correction - more recent GPUs no longer process a float4 as fast as a float, so there's no benefit from clever register packing.

ReplyDeleteI didn't know that, thanks for posting this! I've changed the text.

DeleteSmall note - "Shaders are just as fast when using a float4 as when using a float, so by cleverly packing variables we can perform all 3 ray-plane intersections simultaneously." - this was somewhat true in 2007 but isn't really true anymore - modern GPUs use scalar ALUs.

ReplyDeleteSomeone else also pointed me at this mistake, I've updated the text with this correction. Thanks for letting me know!

DeleteThe first time I saw this was in SimCity 2013. That game looked beautiful.

ReplyDeleteOne of the programmers of Simcity actually replied on Reddit with a dev video from that game. It looks really cool so I've added that video to my post.

DeletePretty sure this was in the original Crackdown (2007), too.

ReplyDeleteThe original Crackdown had a slight hint of ceiling lights, but not actual rooms. I remember checking what they did exactly back then.

Delete