---
title: Bringing Warmth to Deep Space in Lovers in a Dangerous Spacetime
url: https://www.gamedeveloper.com/art/bringing-warmth-to-deep-space-in-lovers-in-a-dangerous-spacetime
author: Matt Hammill
published: '2014-05-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Bringing Warmth to Deep Space in Lovers in a Dangerous Spacetime

How we're making our space backgrounds feel alive in Lovers in a Dangerous Spacetime.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![Bringing warmth to deep space Bringing warmth to deep space](http://www.asteroidbase.com/devlog-images/d10_bgs_titlegraphic_600.jpg?width=1280&auto=webp&quality=80&disable=upscale)


When we showed Lovers in a Dangerous Spacetime at PAX East last month, we got asked a few times about how we were handling our space backgrounds, so I thought I'd go into a bit of detail. We're aiming for a rich, 2.5D neon fantasy look, and we wanted our backgrounds to fit this world and feel alive. We ended up combining a few different elements for the effect we wanted.

![Ship flying through background Ship flying through background](http://www.asteroidbase.com/devlog-images/d10_bgs_shipflying.gif?width=1280&auto=webp&quality=80&disable=upscale)


Element 1 - Far BG plane

The farthest background layer is a big plane with a 1024 x 1024 texture on it. I used some of the sky photos at [CGTextures.com](http://www.cgtextures.com) to get started, and the painted texture contains some colourful nebula cloudiness, but doesn't have much fine detail. The image tiles perfectly, thanks to Photoshop's good old Filter → Other → Offset.

One early problem with implementing the background was that the procedurally generated levels in Lovers can get fairly big, yet we wanted to avoid dealing with ridiculously large background planes. We decided that instead of having the player's ship travel past a stationary background, the background plane would be just large enough to fill the camera, and actually travel around the level with the ship. It only appears that the ship is moving past the background because the texture itself scrolls across the background plane in the opposite speed that the ship is moving in (using SetTextureOffset in Unity). The result is that the background plane works sort of like a window moving around the level, revealing a space background only where the player happens to be.

![Far bg tile Far bg tile](http://www.asteroidbase.com/devlog-images/d10_bgs_bgtile.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![The view in Unity The view in Unity](http://www.asteroidbase.com/devlog-images/d10_bgs_unityflying.gif?width=1280&auto=webp&quality=80&disable=upscale)


The far BG tile texture, and the far BG plane in Unity

Element 2 - Stars and space plankton

The next element we needed was a star field. We're using Unity particles for our stars, and we have one main particle system emitting sub-emitters which in turn emit the actual stars. This gives us some subtle clumping, rather than a perfectly even distribution. We also set them to twinkle and fade over time.

The particle stars are created within a box emitter shape, and this emitter travels around the level with the ship emitting stars around the ship as it goes. Stars appear and disappear slowly, so the player doesn't notice them being generated. Because we also wanted some parallax to the environment, we're shooting the BG plane and these particles from a perspective camera, while all the foreground gameplay elements are shot with an orthographic camera. We occasionally have planets or other doodads show up in the background too; these are generated with additional particle systems. We also threw in some super-subtle foreground particles (think the blurry plankton bits in flOw) which might seem strange for outer space, but they add some weird glowy nebula ambience and give the sense that you're moving through the space clouds, rather than just in front of them.

(As an aside, before we started using particles for stars, we used to use have several huge layered planes with transparent star textures on them. This wasn't very efficient because the there was lots of unnecessary overdraw, as most of the pixels in the star textures were completely transparent. On our middling laptops we saved 5 - 10 fps after switching to particle stars.)

Element 3 - Foreground Glow

For the sake of framerate we're trying to avoid post-processing effects, and for all the other blooms and glows in the game we're using baked-in textures, which we can get away with because everything is shot from one camera angle. So to help stitch the gameplay and background elements together with some overall glowiness, we added one additional plane with some really faint colour glow blobs painted on it. This plane appears in front of the ship and enemies, and its material is a Flare type so it overlays on top of everything else. The texture on this plane scrolls similarly to the far BG plane, but faster, so that as you fly the ship around the colours on the FG glow blobs and the BG clouds mix and shift against each other. This just makes the environment feel deeper and more alive. ![Bg assembly diagram Bg assembly diagram](http://www.asteroidbase.com/devlog-images/d10_bgs_assembly.gif?width=1280&auto=webp&quality=80&disable=upscale)


The different background elements layered together

Element 4 - Location-based elements

Now that we have a solid base background, we can add some variations to different areas of the level by layering on some location-based elements, like this green electron storm. An additional particle system behind the electro orbs is emitting some large green blobby particles.

![Flying through electro balls Flying through electro balls](http://www.asteroidbase.com/devlog-images/d10_bgs_electroballs.gif?width=1280&auto=webp&quality=80&disable=upscale)


Final notes

While we were assembling this system, there were a couple of things we noticed. Because there's a lot of foreground action in our game, we found we had to keep the background fairly subdued so as not to compete with the gameplay elements. We also learned not to overdo the parallax effect--while it's great for adding depth, if you're flying around in space, your eye needs a consistent reference point to judge your speed. If you can't tell what "depth" you're flying at, then you can't tell how fast you're going.

In any case, using this system, it's pretty easy to modify the different elements to suit different environments, while keeping a consistent overall feel to the environments.

--

Matt Hammill ([@matthammill](http://twitter.com/matthammill)) is an artist/designer/co-founder at [Asteroid Base](http://www.asteroidbase.com/). This article was originally posted at [http://www.asteroidbase.com/devlog/bringing-warmth-to-deep-space/](http://www.asteroidbase.com/devlog/bringing-warmth-to-deep-space/)