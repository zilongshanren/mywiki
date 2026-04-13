---
title: Dive into the depths of the fog
url: https://www.gamedeveloper.com/art/dive-into-the-depths-of-the-fog
author: Jussi-Petteri Kemppainen
published: '2019-04-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

As a great fan of old-school adventure games. I wanted to achieve some of that aesthetic in our game as well. For me, the clear style choice those games utilized was the black void around the scene.

![](https://irondanger.com/wp-content/uploads/2019/04/dott.0.0-1024x683.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Image copyright LucasArts

So, the ways we used to achieve that iconic look, was to create a way for us to dim the foreground and add black to the background. This is how we built that look.

## Foreground

The first thing we did was to add an inverted fog to our game view. A fog, that makes the foreground completely black. We also animate the depth of that fog based on camera distance from the player character in order to control it's effectiveness more.

![](https://irondanger.com/wp-content/uploads/2019/04/FGfog_off.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Game view without foreground fog.


![](https://irondanger.com/wp-content/uploads/2019/04/FGfog_on.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The same view with the fog dimming out foreground objects.

## Background

![](https://irondanger.com/wp-content/uploads/2019/04/fog_base.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The "unfogged" base image.

Our base render of the game is pretty contrasty. This is by design as the post effect we will lay on top will affect the look a lot.

### Distance fog

![](https://irondanger.com/wp-content/uploads/2019/04/fog_war.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Fog-of-war applied. This further makes the image dark and even empty. Wait for it.

Instead of creating the background with a distance based fog, we opted to go with fog of war. A dark area that will be cleared when the player moves into it. To me, this feels like uncovering a mystery. Like exploration. It has no game-play value for us, the fog of war has no effect on aiming or AI functionality. It is purely a stylistic choice and I just love how it feels. I think it reminds me of the original UFO: Enemy Unknown.

The black fog of war alone is not a good look though. It makes the game look super dark and low quality. So we need something to counter that look.

### Volumetric lighting

![](https://irondanger.com/wp-content/uploads/2019/04/fog_volume.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Boom! The final image with all layers of fog applied on top of each other.

Volumetric lighting simulates the humidity and dust in the air. We can add a really nice layer of depth and really boost the look of the lighting by adding volumetrics to the mix. The solution we are using is called Aura 2 and it is really really good! It allows us to precisely control the look of our dark backgrounds and the dusty / humid illusion in the atmosphere. Our look highly relies on the atmosphere being visualized as you can see in these screenshots.

So there you have it. Our method of creating the look of Iron Danger!

Original post: [https://irondanger.com/blog/friday-rewind-5/](https://irondanger.com/blog/friday-rewind-5/)