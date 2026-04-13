---
title: Simonschreibt.
url: https://simonschreibt.de/gat/assassins-creed-3-lod-blending/
author: Simon
published: '2013-01-28'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

During my colleague Matthias captured the scenes for the [AC3 windows article](http://simonschreibt.de/gat/assassins-creed-3-windows/) we had to turn down the graphic settings because the frame rate was a bit low. But this gave us the opportunity to see an interesting effect. Normally you can’t see it because with higher settings they do it far away, barely noticeable.

It’s how they blend in/out the Level of Detail (LoD) versions of their objects. Do you see it? The have a noise texture which gets more grainy over time until the object is blended in completely. For me it looks like alpha1/alphatest.

So why is this awesome? Because, as far as I know, there’re two (now three) techniques how you can change level of detail stuff.

- Blend nothing. Just let the new object *plopp* in (and the old out)
- Blend smoothly via alpha8
- Blend grainy via alpha1/alphatest (seen above)

The *plopping* takes less performance because you have to render only one LoD version at a time. When you do blending, you have to render two objects (new and old version) for at least the blending time. But the switching between the versions (depending on the distance) is very noticeable and ugly.

Number two gives you the most beautiful effect but *can *have problems when it comes to foggy regions. Depending on your engine it can happen, that it’s not possible to have fog on alpha8 objects. This means, during the blending you would see the new LoD object rendered without fog and when the blending is over it would *plopp* “into” the fog because now the engine is able to lay the fog over the object. See the picture below as an example. This picture is taken from the Internet and they solved the problem, but it shows what I mean.

So the solution in Assassins Creed impressed me, because they have combined the beauty of blending and avoided the problems with fog. I’m not saying, that they would have problems with fog! But maybe that’s the point why they choose this blending solution.

Just Cause 2 did the same for their vegetation LOD.

It’s a very old trick used in Win 3.11/95/DOS games to do transparency (i.e. 50% transparency is emulated using one discard one pixel, show one pixel)

A trick also useful (to certain extent) when doing Deferred Shading in DX 9.0 hardware.

You can choose a dithered noise pattern, or an even, homogeneous pattern.

Also, you forgot to mention the “tesselation” lod method (swap the distant model for the closer one, and start displacing some vertices from an edge to the actual location as you move closer).

This is hard to do, because it requires a lot of work to determine the best edge to put the vertex into; and also dealing with blend shape-like animation. In other words, it’s rarely worth the effort (except when doing terrain lod).

It also implies that LOD1 is just LOD0 with fewer vertices, thus this technique doesn’t work with hand-made Lod models (well it’s not impossible, but it becomes looooot harder).

Of course, that’s assuming you don’t have access to hull & domain shaders.

Oops! Forgot something: As for the alpha8 vs Fog problem, this is really really outdated.

It was a problem when the fixed function pipeline did vertex-colour fog. But calculating per-pixel fog (which btw. enables more advanced fog) solves the fog bug while doing alpha blending.

The biggest problem w/ alpha8 though (besides bandwidth consumption & ROP limit), is that it doesn’t play nice with some techniques (i.e. deferred shader, some postprocessing effects, including depth-based godrays or fog as a postprocess as the problem you mention comes back)

Hola Matias, qué tal?

Thank you very much for the time you spent to write these comments! Unfortunately i understood only 50% because i’m just an artist :D

One of the transparency fakes i already mentioned in this article: http://simonschreibt.blogspot.de/2013/02/1943-retro-shadows.html

I thought about to write about the tesselation LoD but i never saw it in a game (maybe thats a good sign :D because than it was very well implemented). For terrain i saw it of course – I noticed it in Battlefield2 the first time. But for characters and props i didn’t noticed it in any game.

Hm i’m not sure if i understood everything of your 2nd post but i totally think you’re right. Maybe i think about this from another way: sure the tech is there, i mean we see what’s possible in UDK, Cryengine or Frostbyte. But sometimes i have the feeling that something is wrong implemented or just a bug which results in fog/alpha problems. I saw it the last time in Dead Space 3. And that some engines have problems to mirror UVs and render the normal map correctly shouldn’t be too hard but sometimes this effect is also visible.

I made a small GIF for you to see what i mean. This is from Dead Space 3 (sorry for bad quality) and it shows some…heavy dirt stuff hanging from the top of the room. It looks totally ok if you’re near, but if fog is behind the pipe where this stuff is hangning from, then it gets very transparent.

http://i.minus.com/ibbUSdgYKBU2Dj.gif

Oh by the way: your blog looks awesome! Have to check it out in detail!

Hallo Simon,

I thought you were a tech artist. Sorry for the confussion.

Ok, I’ll proceed to explain.

In the old days (pre Shader Model 2.0, which is circa before 2002) a lot of math was done per vertex instead of per pixel. Fog was one of them. Because of this, fog would not only affect the opaque pixels, but also the transparent ones; making them visible with the colour of the fog (i.e. point sprites like particle fx suddenly become very obvious that they’re a quad it’s a grey rectangle with colour in the middle).

So we either render the alpha-blended stuff without fog, or don’t render the alpha blended stuff.

When decent pixel shaders came into play, we could move the fog math to the pixel shader, and by the nature of how it work, it’s almost automatic that the fog is only applied to non-transparent pixels, removing most artifacts. If there’s artifacts left, pixel shaders allow us to tune some formula to reduce them (i.e. lighten fog based on transparency level).

However, in the present day; we face another problem: Postprocessing and deferred shaders.

The problem with Alpha blending is that even fully transparent pixels write their depth values to the depth buffer. This often results in serious artifacts (the “rectangle nature” of many sprites becomes aparent because they avoid anything behind them to be rendered, as if they were a fully opaque quad). Imagine the lens of truth from Ocarina Of Time, but on reverse: everything that is inside the lens isn’t rendered, even though it’s fully transparent!

There is no direct solution to that problem. We *can* prevent filling the depth buffer when transparency is 0%, but what about 1%? Does it mean we should write 1% of the depth value? That makes no sense, more transparency doesn’t mean it’s closer to the camera. And what about 50%?

The quick ‘n dirty solution that everyone does is to disable depth writes for alpha blended objects while still keep depth reads. In other words, no sorting *at all* between transparent objects, but transparent objects overlapping already-rendered-non-transparent geometry are sorted correctly.

Transparent vs Transparent = Potentially incorrectly rendered (if they overlap).

Transparent vs Opaque = Correctly rendered.

This trick also requires the transparent stuff to be rendered last, because it leaves no trace in the depth buffer AND HERE LIES THE PROBLEM. If you render opaque geometry behind a particle effect in the wrong order, it will overwrite the particle, because there was no depth there to compare with.

If the particle is rendered after the opaque house, it will compare the depth from the house and see the particle is in front of it. The reverse is not possible, the house won’t see the particle’s depth and think it is in front of it.

Many postprocessing effects need the depth buffer data: God rays, Depth of Field (focus), SSAO, Fog as a postprocess, etc. And surprise! There’s no information about the alpha-blended’s depth. We could enable depth writes, but artifacts are horrible and obvious.

The three alternatives are:

* Render alpha stuff after all depth-based postprocessing: (i.e.) Particles won’t receive proper god rays/sun shafts, won’t be fogged at all, won’t be out of focus.

* Do the postprocessing anyway on alpha stuff: Quality depends on WHAT’S BEHIND the particles. If there was a wall very close to it, quality will be a close match (correct focus & fog). If there is a wall behind but is very far away, the particles will be postprocessed as if they were far away too, even though they could be close. I’m not sure if I understand your picture of Dead Space 3, but it looks like the dirt rendering is depending on what’s behind it. Sounds familiar? I wouldn’t be surprised they chose this alternative, as it is the most common one. Often the geometry behind transparent stuff is not far away, which leads to “good enough” results. Particularly in close environments. It’s a lot better than method 1 (who doesn’t nottice a piece of coloured glass in the distance outstanding in the middle of fully saturated grey fog??? or fully sharp glass in the middle of fully out of focus environment?). In fact we do this for Distant Souls & The Dead Linger.

* Emulate post processing in the alpha blended shader: This is an insane option. It requires to do all the the compositor stuff during the render pass, per object. It sounds nice in theory, but you already know some compositor chains can get quite complex and becomes absurd to try to emulate them by a technical artist. It gets even worse if the game options allow to selectively switch postprocessing fxs, as the shader has to be modified & recompiled to account for that. If someone manages to do this alternative, rendering should be 99.99% accurate. But the effort is not worth the improvement IMHO (unless the game core mechanics rely on transparency too much?).

And then there’s deferred rendering, which in it’s basic form doesn’t play well with alpha blending. I won’t go into detail on why in this one, there’s a lot of material out there in the web, but it’s enough to say that for that reason, many games often resort to the same: Render alpha blended stuff *after* deferred pass (called the “forward pass”). Thus Normal data (GBuffer) is not available which is also used by many compositors. And here we go again into the same problem.

Alpha1 / Alpha testing doesn’t have this problem, because there are two choices: To be or not to be (rendered). This poses no problem, transparent pixels write no depth, opaque pixels write depth. It also plays nice with deferred shading. The problem only arises when there are degrees of transparency.

Hope this sheds light into the dark

And I’m glad you find my blog attractive. Your’s is awesome too :-) Tschüss

Sorry for my late answer but i was slapping myself because i didn’t player ocarina of time :,( Just kidding, i was a bit busy with the new D3 article. Anyway, i want to say: Thank you very much for writing that much text. It’s just awesome that you took the time to explain all that stuff.

In conclusion it sounds for me like what i tried to express: transparency stuff is complicated. Because – as far as i understood – there’s no perfect realtime solution. That’s something i hope we can solve with the next Gen consoles: make perfect transparency :D

Hasta pronto!

I know this is an old thread, don’t want to necro etc, but figure it might be useful.

The vertex/tesselation LOD you were discussing is often called “Multi-resolution mesh” and involves doing a collapse function on a high-poly mesh, by choosing edges/vertices that don’t sit on the silhouette and collapsing them down. Eventually you get a collapse-list that takes you from high to low poly (and in reverse).

I believe it was first talked about by a graphics tech guy called Hughes-Hoppes.

It was used for characters in the HL2 engine at some point (I remember they were using it for the soldier-version of Team Fortress 2).

There’s even a directx version of it in the old DirectX sdk’s (around dx 4-5 I think?). It was a funky technique, used on terrains a lot too. But I think it isn’t used much anymore because it was generally a CPU-only thing.

Great blog btw.

It’s the other way around, i’m really thankful when people writing comments even to “old” themes. I mean, the whole blog project is about collecting stuff to collect the awesome knowledge :)

I heard of this LoD tech too. But never saw it in games. Battlefield 2 had some “movement” in the terrain but i couldn’t see exactly what was going on.

There’s also another trick to this, to alleviate the stipple pattern effect that you get from alpha test/discard, you can enable anti-aliasing and apply alpha to coverage. That way you can get a nicer transition and not have issues with sorting.

Nice thought! I didn’t think about it, but now it seems pretty obvious to me. If i get AC3 on my PC i’ll try it out.

I noticed this too on the PS3 version of AS3. It seems that the dissolve effect doesn’t quite move with the camera, at least for some bits of scenery. I found it a bit too noticeable at times, especially for big rocks and cliffs.

In the previous Assassin games they DID slowly blend in and out of LOD. Wonder what caused the change?

Just found your blog today and it’s great following you through all the little things you find in games! I’ve been fascinated by a lot of the same stuff. :)

Thx for your comment! I think MAYBE the noticed then the dissolve effect costs less performance or produces less problems with fog?

Glad you like the blog! Feel free to drop a hint if you also saw some nice details in games :)

I noticed that the stipple-based lod blending is used in the example engine PS3 devs get, so perhaps its just performant on PS3 hardware (which has some quirks).

Interesting info Phil! Thanks for sharing!