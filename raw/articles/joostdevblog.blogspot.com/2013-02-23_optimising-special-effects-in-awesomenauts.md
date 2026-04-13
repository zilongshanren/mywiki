---
title: Optimising special effects in Awesomenauts
url: http://joostdevblog.blogspot.com/2013/02/optimising-special-effects-in.html
author: Joost van Dongen
published: '2013-02-23'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)patch increased the framerate a lot for players with older videocards, especially during fierce battles. We managed to optimise our special effects without making them look noticeably different. Today I would like to explain how we did that!

Before I dive into the details, let me first give some background. In a 2D game like Awesomenauts, most objects are just a square with a texture on it. The texture contains an image, and you only see that image, not the entire square. However, the videocard renders the entire square. So from a performance perspective, it doesn't matter how much of the texture is actually

*visible*. The entire square is rendered and the every pixel uses performance!

![](../../assets/e93cf1cb78348611.jpg)

Our artists know this, so they try to crop the image to have as few transparent pixels as possible (without changing the actual looks of the end result, of course).

Since objects in Awesomenauts contain so many (partially) transparent pixels, we cannot easily detect whether an object is hidden entirely behind another object or not. So we always render

*every*object that is on the screen, from back to front, regardless of whether an object is actually visible or not. All objects are rendered on top of each other until the image is complete.

![](../../assets/935a1be14e8ffd8f.jpg)

This introduces a big performance issue: massive

*overdraw*. Overdraw is when a single pixel needs to be drawn several times each frame. On 1920x1080, the screen contains over 2 million pixels. If we draw every pixel 10 times, that is already 20 million pixels per frame. Now do that 60 times per second, and we are rendering a whopping 1.2

*billion*pixels per second. That's a mindbogglingly large number of pixels per frame!

The fun thing, however, is that modern videocards are totally okay with that. However, for slightly older ones, it might become a problem to pull this off fluently...

In

[a previous blogpost](http://joostdevblog.blogspot.nl/2012/04/depth-of-field-blur-swiss-army-knife.html)I explained how I abused my depth of field blur as an excuse to render the backgrounds in Awesomenauts on a much lower resolution. This greatly reduces the number of pixels that need to be rendered every frame, but it only helps for the background, since the rest of the scene needs to be sharp.

Since the background are optimised this way already, the biggest remaining overdraw in Awesomenauts happens during special effects, mostly those of nauts' special skills. This is because they have a lot of overlapping particles for smoke, fire, dust and debris. Having several of those special skills on screen at the same time decreased the framerate on older and mobile videocards too much. This is extra problematic because during fierce battles, high framerate is needed most!

![](../../assets/4304401214560573.jpg)

Once I figured out that overdraw was the cause of the framedrops we were seeing on older videocards, the solution seemed simple: decrease the number of particles on screen. The difficulty, however, is that it is difficult for artists to optimise things without being able to see

*what*they need to optimise. Having a ton of large particles for thin smoke looks very subtle, but eats performance like crazy. And if an effect needs to be optimised, what part of that effect is the problem exactly?

So I made a small addition to our engine to visualise overdraw. Internally we have a shortcut now to enable this, and when this is pressed, the screen shows how often each pixel is rendered. White means a pixel is rendered 85 times (!), while black means it is rendered 0 times. Technically, this is a very simple thing to make: all objects are simply rendered on a very dark additive blend mode. So each rendered object adds a little bit of brightness.

This is not just informative, but also looks pretty awesome! Have a look at this video of going through the menus and then some gameplay with Skølldir to see how weird and cool this looks:

As you can see, the character itself is not every expensive to render, since it is only one square. The problem comes from the tons of particles.

Using the overdraw visualisation, our artists (in this case mostly Koen, Ralph and Gijs) were able to quickly identify which parts of which special effect needed to be changed. These changes are usually pretty simple: 40 smoke particles that are 10% opaque, look nearly exactly the same as 20 smoke particles that are 20% opaque. So in most cases the trick was to drastically decrease the number of particles and then just modify some colours to compensate for that.

The video above shows what the overdraw looks like after these optimisations were already done, so here are some comparison shots that show how massively the overdraw was decreased while hardly changing the looks of these effects:

![](../../assets/ace65e7162d14dd0.jpg)

![](http://www.proun-game.com/Oogst3D/BLOG/Overdraw Earthquake.jpg)

We tested the results on our Mac (even fast, expensive Macs usually have mobile videocards, which are not very fast and far from ideal for gaming) and indeed the game runs a

*lot*smoother now. Several users reported that while they could previously only run Awesomenauts smoothly on Normal graphics quality, they can now run on High!

These improvements were released on Steam in patch 1.14 two weeks ago, so I hope players with older videocards are enjoying the smoother framerate they are getting!

The video is marked as private

ReplyDeleteFixed. Thanks!

DeleteWhoops, thanks for noting! :)

DeleteDo you guys use some form of Occlusion Culling?

ReplyDeleteNope, none at all! We only cull things that are completely outside the screen. Doing occlusion culling with textures that contain irregular shapes and lots of transparent pixels is theoretically possible, but so much work and so complex to do that we decided not to implement that. Also, most overdraw comes from things like fog layers and fire particles, in which every pixels is partially transparent and thus hardly ever completely occlude any pixels behind it.

Delete1.2 billion pixels per *second?

ReplyDeleteGood read, small typo: 1.2 billion pixels per [second].

ReplyDeleteThat's a mindbogglingly large number of pixels per [second].

No, that seems about right. 60fps * (.75-2.5 million pixels) * 40 overdraw could very easily be about 1.2 gigapixels.....

ReplyDeleteActually, it was indeed a typo: I had written "per frame" instead of "per second", but I had already fixed that by now. :)

ReplyDeleteDefinitely helped a lot; playing on Ubuntu here (via PlayOnLinux), and now I can play the game on high, while before only medium worked well. Thanks!


ReplyDelete;-)

AWESOME, is a very cool visualization!

ReplyDeleteWAIT so these optimizations are suppose to reduce lag in the next patch! IF SOO THATS AWESOME because in 1.14 I began to alot of lag spikes and that didnt happen before. Keep up the kinky updates.

ReplyDelete"Lag" can mean several things. If the entire screen is stuttery or freezes, then that is a framerate problem and these optimisations indeed improve that. However, these optimisations were already in 1.14.



DeleteHowever, what is usually meant by the word "lag" is a bad internet connection. When this happens really badly in Awesomenauts, your own character remains fully responsive, but other characters start glitching around the screen.

Also, note that 1.14 contained no changes that could have reduced your framerate or internet connection, so if you have problems since 1.14, then that is probably just coincidence and related to something else.

Ok so I found the"lag problem". It was dota 2 updating!! Also for one I dont even play the game, second I got it for free, and third they gave me 19 usless copies of that game.


ReplyDeleteIn conclusion I deleted dota 2 and the lag stoped. Thanks Joost for pointing out that it wasnt Awesomenaughts.

P.S. BEST GAME EVAR

Good to hear you found the cause! :) This is a nice example of number 4 in my Irritating Bugs list: random other programs interfering with the game... (http://joostdevblog.blogspot.nl/2013/01/my-favourite-bugs-top-7-7-to-4.html)

DeleteSo true. Lots of people have problems with lag in Awesomenauts. Typical in game latency is above 100ms so in my opinion pretty high for such a fast paced game. On my machine I actually just solved a problem with another program interfering with the game. Not long ago I installed Plex (a local media sharing server) which every 60 seconds was trying to send something to internet using UPnP in some weird which was causing my router to stop responding for 2-3 seconds. So every minute I had a 3 second lag in Awesomenauts. I've been playing like that for a month and thought these are other people that are lagging and not me simply as I have a very fast internet connection.


ReplyDeleteTook me couple hours research to track it to down and solve (I had to uninstall Plex as it apparently was flawed). I still think that standard lag in Awesomenauts is a bit too high but at least now its constant :)

That 100ms actually does not mean the lag is higher in Awesomenauts than in other games. Just the number is higher, not the actual lag. This is because our lag number includes the time between receiving a message and processing it, on both computers. Other games don't include that in their ping number, so this makes the number higher while the connection might be the same.


DeleteBecause of this, Awesomenauts plays perfectly fine when it reports 100ms, since in comparison to other games this is more similar to 60ms, which is fine.

Thank you, I'm the player with old laptop, and it was quite slow even at low, and now it's really fluent.


ReplyDeleteAnd really big thanks for sharing your gamedev experiens with us.

This comment has been removed by the author.

ReplyDeleteI remember I was struggling with fill-rate issues when we were working in Face-Plant Adventures for the Xbox360.




ReplyDeleteI fixed that by rendering the scene in multiple passes. First pass renders opaque geometry from front-to-back with z-read/write enabled. This will reject many pixels z-early, the game has 15 parallax layers. The second pass renders transparent geometry from back-to-front with z-read enabled only, which also helps to reject pixels. Our game contains much more opaque- than transparent geometry though.

Another step to boost performance was to merge geometry in a chunk-based-fashion on each layer. So rather than having 200 separate "image objects" on one screen per layer that need to get drawn, they get merged into vertexbuffer blocks during level start. This allows us to draw hundrets of images with one draw call.

Another trick is, rather than drawing rects, to generate geometry (in an offline build-step) that somehow matches the texture content. This generates more vertices per "object", but usually helps to reduce pixel fillrate issues.

Thanks for sharing, very interesting! :)



DeleteDuring development I looked into the solutions you mention here, but they each turned out to not be feasible with Awesomenauts:

-To get high quality anti-aliasing on the texture, we need transparency on practically all objects in Awesomenauts, making the z-buffer practically useless.

-Merging chunks requires texture atlassus, which would have been a lot of work to build because our editors are not set up with this in mind (so artists use tricks that work poorly with atlassus). Also, drawcalls are not really our limiting factor and merging objects does not help for fillrate.

-Generating geometry around actual texture content would have worked, but it would have been so much work to implement, especially since our artists have the possibility to animate texture coordinates. Definitely possible, definitely a good idea, but also just too much work for our small team...

I would have loved to try each of these and see how much could have been won there, but there just wasn't enough time for us to build them.