---
title: 'Write-up: Magical Marbles'
url: https://halisavakis.com/write-up-magical-marbles/
published: '2019-04-17'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

I guess this is the first entry to this category, since I never had such a demand for a write-up before. So here goes!

The different between this format and regular “My take on shaders” post is that this is a more direct format, just going through a particular effect that I find too specific to write a complete tutorial about. Also, in some cases, like this one, I won’t be providing the completed code but I will be writing about the general idea and the process behind the specific effect.

In [my tweet](https://twitter.com/HarryAlisavakis/status/1118434598957006848) I mentioned it being a form of “raymarching” though I might be using the term loosely here. While I use a loop to move towards a certain direction, the technique doesn’t really resemble traditional raymarching. So keep that in mind.

## The core idea

I’ve been constantly thinking about how to take advantage of past effects, and in this case I had an idea concerning the “layered parallax” effect that I demonstrated in [an older post](https://halisavakis.com/my-take-on-shaders-parallax-effect-part-ii/).

With that technique, you could sample a texture using coordinates that had been offset “inwards” of the object, by using the camera’s view direction in tangent space. The effect is super useful for adding some depth to materials like ice, or tiles or basically anything you want to make it look like “there’s something underneath the surface”. The result looked something like this:

![](https://i0.wp.com/halisavakis.com/wp-content/uploads/2019/04/layered_parallax.gif?resize=600%2C450&ssl=1)

My thoughts going from this effect were these:

- Let’s ditch the main texture, don’t need it for now
- What if in every “layer” of this effect, I performed a “step” function on a 2D noise texture, where the cutoff value ranges from 0 to 1 based on the “index” of the layer?

The “stepping” (that’s what I’ll call “using the “step” function” from now on) was inspired by the concept of using grayscale textures as heightmaps, with their value representing depth. Adjusting the cutoff value of a simple texture with a radial gradient looks like this:

![](https://i0.wp.com/halisavakis.com/wp-content/uploads/2019/04/cone_sdf.gif?resize=600%2C450&ssl=1)

As if the texture actually represents a cone and when I’m using “step” I’m cutting slices into it which decrease in size as I get to the top. Basically I’m super-over-explaining SDFs here, but that representation really helped clear things in my head.

So, if I were to assign 1 to the cutoff value of the out-most layer, 0 to the value of the deepest layer and the inbetween values to the inbetween layers, each parallax layer would have a differently sized “slice” of the texture.

If we add that “stepping” to each layer, with the same radial gradient texture, we end up with something like this (the texture is tiled 5 times so just pay attention to the middle one):

![](../../assets/bfa53dab2e378829.gif)

Turn up the iterations/number of layers (here it’s something 128) and you have ｓｍｏｏｔｈｎｅｓｓ:

![](../../assets/321ff9d48cba67cf.gif)

Add a somewhat more complex texture, like a simple cloud texture and you have this:

![](../../assets/c45f7154784a7d85.gif)

Trying out random textures and noises is super fun with this one btw.

Add the material on a sphere and you have the ＯＲＢ:

![](../../assets/ac5190a65b52df89.gif)

Add 2 HDR colors, and lerp between them based on the layer “index” instead of just lerping the intensity from 0 to 1 (also some Post-processing for the looks):

![](../../assets/dedccf93c54668a0.gif)

Add some [waving displacement](https://halisavakis.com/my-take-on-shaders-waving-displacement/) when sampling the texture in each layer for some extra variation and *magic*:

![](../../assets/cc1a4452a5816078.gif)

And that’s it! I hope that was helpful and I hope there will be many more write-ups in the future, especially as I’m easing into VFX stuff at the moment of writing. So, I’ll see you in the next one! 😉

## Comments

Great job, That was really inspiring for me

Cool idea!