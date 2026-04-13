---
title: Using 2D daylight assets to create a night level
url: http://joostdevblog.blogspot.com/2014/11/using-2d-daylight-assets-to-create.html
author: Joost van Dongen
published: '2014-11-08'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers II](http://www.swordsandsoldiers2.com/)all the level assets have their lighting drawn in. Of course you can ask the artist the redraw the image with different lighting, but that costs a lot of additional time and texture memory. We managed to re-use our daylight textures to create convincing nighttime levels, so today I would like to explain the tricks used to achieve that goal.

Today's post is all about the artistry of

[Ronimo](http://www.ronimo-games.com)artist Ralph Rademakers. He uses images drawn by Adam Daroszewski* and Gijs Hermans to decorate the levels in Swords & Soldiers II. Ralph keeps surprising me with the unexpected tricks he manages to pull off with our

[internal tools](http://joostdevblog.blogspot.nl/2012/11/introducing-editors-of-ronitech.html).

**By the way, note that Adam works as a freelancer these days. He drew most of the level props in this post and you can see some more of his amazing work*

[here](http://adamdaroszewski.tumblr.com/).There is basically a whole series of tricks that Ralph uses to turn day into night. I'll let the images do most of the talking today:

![](../../assets/33033758a30b2a16.jpg)

![](../../assets/83e8a9e37ca893f4.jpg)

![](../../assets/e011ce3d9c28f128.jpg)

Even in the night a form of atmospheric perspective can be used: in the video below the smoke in the foreground is much brighter than the smoke in the background to suggest additional depth. When I built the recolouring shaders and tools I never expected them to be used on almost every object in the levels. Also, note how the stars have been made using particles to make them blink and appear in random places for a more lively look.

![](../../assets/ae525fe606527cca.jpg)

As a starting point Ralph usually chooses one colour multiplier for all objects in the level. He tweaks the colour per object to make it look exactly right. In the end few objects use the same colour multiplier, but they all started from the same point.

![](../../assets/8599cdd29cfd61e8.jpg)

![](../../assets/2b0f199baa89bc64.jpg)

It surprises me how often these gradients are reused. From fog to lights to lens-flares and even just for hiding objects that should not be visible from certain viewpoints. The big downside of this approach is that it results in a lot of overdraw, which is also the main performance bottleneck in

[Awesomenauts](http://www.awesomenauts.com). Good thing modern videocards are so insanely fast...

![](../../assets/e6f979f85baaa1c0.jpg)

![](../../assets/502b13ddf0a01fa7.jpg)

The lights in the bar below blink to make the scene more dynamic. However, blinking lights attract the eye too much while the focus should be on the gameplay. Therefore the blinking is not between on and off, but between the more subtle slightly-bright and extra-bright. Also note how the blinking lights illuminate the barmaid's arm.

This bar is also a great example of Ralph adding tons of little animating details, like the drunk guy on the roof. Many of those details will likely not be seen by most players, but the total effect of having such a detailed world is very strong, even for players who don't look at it specifically.

![](../../assets/8483f5d403cd1f5e.jpg)

As a programmer when thinking about lighting in 2D games I immediately start considering technical solutions. I would look at things like normal maps (very possible in 2D) or automatic rim lighting. However, more creative, art-driven solutions often work much better, especially when creating a visual style with such a painterly look as in Swords & Soldiers II. The simple yet clever techniques Ralph used to create this nighttime level are a great example of this.

I like how you present your articles, very informative and easy to understand. What I particularly found interesting was the extensive use of gradient textures. Haven't given them much thought before.


ReplyDeleteThanks for sharing!

Great post! We're doing similar things with fogging and colorizing normal assets.



ReplyDeleteWe also render lighting information from a separate camera to a render texture that then gets set as a global texture property, so shaders that require it can access it without us having to send to each one.

I was amazed how little performance we lost (it works on phones just fine too) when we did direct GL calls to the RT at quarter resolution. All it really does is render an ambient color and additive sprites.

The game you are talking about is 2D, right? What method are you using to light that in real-time?

DeleteGreat post! Amazing and elucidatory - as always ;)

ReplyDelete