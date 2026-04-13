---
title: How to make the graphics for Star Driller Ultra
url: https://www.gamedeveloper.com/art/how-to-make-the-graphics-for-star-driller-ultra
author: Taro Omiya
published: '2015-04-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# How to make the graphics for Star Driller Ultra

So a lot of praises has been made about the graphics in our Ludum Dare game, Star Driller Ultra. How did we make such beautiful graphics in a short amount of time?

Well, actually, it’s a lot easier than you think.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/5b11ae25809e5cdc.img)


So a lot of praises has been made about the graphics in our Ludum Dare game [Star Driller Ultra](http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=20557). How did we make such beautiful graphics in a short amount of time?

Well, actually, it’s a lot easier than you think.

## Part 1: Making the model in Blender

First, open Blender.

![Easy enough... Easy enough...](../../assets/79b33ee91c2a8deb.png)


Select that shape with the right mouse button, then go to the right pane and click on the gear tab (called Modifier).

![Modifier selected Modifier selected](../../assets/7bf2bd586df42d8c.png)


Click on “Add Modifier”, and select “Wireframe.”

![And this is where the magic is about to start! And this is where the magic is about to start!](../../assets/bb6a0355f50ea600.png)


Now your shape is a wireframe!

![It doesn't look that nice, though. It doesn't look that nice, though.](../../assets/8adc9800ce3665d6.png)


After that, it’s just a matter of adjusting the thickness value on the modifier.

![That's more like it! That's more like it!](../../assets/4ed77db6bceeba57.png)


Now you can save this model in your Unity project’s Assets folder, and let the game engine do the rest.

## Part 2: Toon shading in Unity

Next, we need to import some toon shaders in Unity. Open Unity, then click on “Assets” under the menu bar, and select “Import Package -> Effects.”

![It's a poorly-worded location to put toon shaders into. It's a poorly-worded location to put toon shaders into.](../../assets/cd30f4a4a07504a7.png)


Open the Unity project, and drag your new model into the Scene.

![Wait a minute...that's not toon shading! Wait a minute...that's not toon shading!](../../assets/65bd46981d4c08a1.png)


On the Inspector panel, there’s the Material component properties displayed on the bottom. Scroll down there, and change it’s shader to “Toon -> Lit”

![Ooooh! So many shaders! Ooooh! So many shaders!](../../assets/bcff06abbfa3f71b.png)


The cube will still look a bit ugly because it doesn’t have a ramp set. Change the ramp to a horizontal monochrome gradient that’s 2 pixel tall, and 256 pixels wide. This will act as the gradient applied to the object in response to the lighting.

![A very sharp gradient as a toon ramp. A very sharp gradient as a toon ramp.](../../assets/186b42a8069bed29.png)


For [Star Driller Ultra](http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=20557), we used the ramp below:

![](https://bytebucket.org/OmiyaGames/ludum-dare-32/raw/bc3ff9fa600b3d7c2bc37ed9caddd1d945f82ed0/Assets/Images/UtilToonGradient.png?width=1280&auto=webp&quality=80&disable=upscale)


After that, just change the Main Color on the material to whatever you want it to be.

![Let's make it unoffensive green. Let's make it unoffensive green.](../../assets/92c00d51bbffa828.png)


## Part 3: Image effects (bloom!)

But wait! If you switch from Scene pane to Game pane, you’ll notice the graphics isn’t as awesome as [Star Driller Ultra](http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=20557).

![Not awesome enough. Not awesome enough.](../../assets/d2b4532792bb70b3.png)


That’s because we’re missing some image effects; specifically, bloom. Fortunately, we’ve already imported it, remember?

![Again, poorly worded. Again, poorly worded.](../../assets/cd30f4a4a07504a7.png)


Click on your camera, and in the inspector pane, use Add Component to add the following three image effects, in order.

Image Effects -> Camera -> Vignette and Chromatic Aberration

(Adds darker, blurry parts at the corner of the screen)

![Bloom2 Bloom2](../../assets/7031b407a1e67a1e.png)

Image Effects -> Bloom and Glow -> BloomAndFlares

(Adds blooming light effect)

![Bloom3 Bloom3](../../assets/23b5ee9a9e54c293.png)

Image Effects -> Other -> Antialiasing

(Soften shapes with jaggy edges)

![Bloom4 Bloom4](../../assets/25945d29d52d1fb8.png)


Furthermore, for [Star Driller Ultra](http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=20557), We’ve adjusted the values in each of these image effects under the inspector as follows:

![Lots of numbers. Lots of numbers.](../../assets/f36309e06e15bb17.png)


And that’s about it. You can see the results for yourself.

![A true work of art. A true work of art.](../../assets/b4ac7bcfb70fc76e.png)