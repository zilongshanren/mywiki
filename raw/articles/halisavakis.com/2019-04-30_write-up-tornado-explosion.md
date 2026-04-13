---
title: 'Write-up: Tornado & Explosion'
url: https://halisavakis.com/write-up-tornado-explosion/
published: '2019-04-30'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Recently I started experimenting with VFX and my 2 first entries on the field were 2 pretty standard concepts: a tornado and an explosion. Actually the whole idea of getting into VFX dawned on me after watching an awesome [VFX tornado by Spyro](https://realtimevfx.com/t/spyro-sketch-12/4802). So I tried approaching VFX my own way, with my existing assets/shaders and knowledge, and started with these 2 simple concepts, with a style I had in mind which was similar to the [waterfall shader I covered before](https://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-1/).

## Tornado

In case you missed it, the tornado turned out something like this:

![](../../assets/e3e8ee8a47e9c774.gif)

By now, you’ve probably figured out that it’s all about layering stuff, and this effect was no exception. It’s a combination of 3 distinct effects (4 if you include the clouds, which I won’t cover here): the tornado core (which consists of 4 meshes using the same shader), the top and bottom spiraling planes (can’t think of a better description) and the particle system on the bottom.

### Tornado core

The only custom mesh I used, looks something like this:

![](../../assets/47482f4d0f7cb5b6.png)

It’s nothing special, I did however make sure the UVs cover the whole square, so that the noise texture tiles as it pans on it.

I made a custom shader for the tornado which does the following effects:

- Takes a noise texture and pans it in both axes according to a given speed.
- Takes 2 HDR colors and, after rounding the texture’s values (like in the waterfall), lerps between them based on the banded value.
- Displaces the vertices of the model based on the noise texture (white = outwards, black = inwards).
- Uses a cutoff value to clip the pixels according to the texture’s grayscale value (without the rounding, for more values).

To get a better idea, each of the 4 layers of the core look like this:

![](../../assets/40a1b9a100c499f1.gif)

Each layer has a different material with different colors, amount of clipping, scaling and vertex displacement power.

An important factor to get this look was the noise texture, created in substance designer:

![](../../assets/6baa925e6d3d7e50.png)

Since I pan the texture in both axes, having a noise texture that was tilted 45 degrees like that was imperative to having the tornado swirling look.

### Spiraling planes

The planes on the top and bottom of the tornado, while not fitting without a context (and the sky is not really fitting to the scene), contribute significantly to the impression of the sucking power of the tornado. They use a shader which is more or less the exact same as the tornado core, but with one big difference: they sample the noise texture in **polar coordinates**. That way, they give the impression of the texture being sucked towards the center, like a portal. That’s obviously why using polar coordinates is common to portal effects.

![](../../assets/57be0c78ff5594a2.gif)

### The particles

The more keen-eyed of you might have seen the shader before; it’s the one from that waterfall shader I mentioned above. The shader for them is explained and written in [the second part of the tutorial](https://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-2/) so you can check it there!

![](../../assets/7655146ce53f50d8.gif)

## Explosion

Following the same style as the tornado, I wanted to make an explosion effect, as it’d probably be way more commonly used than the tornado. Because I was following the same style and the principles were more or less the same, I ended up using pretty much the same exact shaders with different parameters. The end result was something like this:

![](../../assets/d4874080fac7a737.gif)

Just to see it a bit better, here’s the effect without the animations:

![](../../assets/f0dcecc0b8fed5e0.gif)

You probably guessed it already: it’s a bunch of layers. No more than the tornado too. Here there are 3.5 distinct effects (3.5 because there are just 3 different shaders but one is used differently and on a separate mesh): The inner core of the explosion, the outer layers, the bottom spiraling plane and the outer air layers.

### Inner core

While this was a separate shader, the principle was the same: Noise texture that pans with some speed, used for both coloring by lerping between 2 HDR colors (no banding here though) and for displacing the vertices.

Without the extra layers, it looks like this:

![](../../assets/0aa336325933f9dd.gif)

With a noise texture that looked like this:

![](../../assets/c803e6f3a54f8d06.png)

### Outer layers

There are 2 outer layers, using the exact same shader and setup as the tornado layers. Easy to figure out when you see them away from each other:

![](../../assets/5188a8eb322c8a2c.gif)

Having them pan the opposite way really contributes to the chaos of the explosion, at least for me.

FYI, all these meshes are spheres, they just have a plane hiding the rest of the mesh.

### Bottom spiraling plane

No surprises here, it’s the exact same thing as before.

![](../../assets/e83424dd81a0c3ad.gif)

### Air layers

Just for this one, I’ll remove the ground plane to see what’s going on:

![](../../assets/cdad71ad00b53b18.gif)

Yes, it’s the tornado mesh with the same shader. I’m **that** lazy.

### The animation

Clearly most of the work went into animating the thing, to have a somewhat nice feeling on the impact and the timing. Lucky for me, I have a custom tool I made that takes care of simple “programmer” animations, using coroutines and such.

With that tool I can move, scale, rotate transforms, but I can also change the color of sprites/UI elements and (the more underutilized feature which I loved for this effect) change the property of a material. I can also sequence the aforementioned animations, delay them and make them use specific easing curves (or custom ones). It’s a handy tool, but right now it needs a massive refactoring and major UI/UX improvement cause this is an editor that only I can love:

![](../../assets/0af411270663f02c.png)

The good thing is that all the aforementioned shaders have a “_Cutoff” property, so it was easy to dissolve the effect over time, while also scaling it.

### Radial blur

To give more of an impact during the explosion, I used a custom shader for radial blur, for which I also happen to have a tutorial with the code [right here](https://halisavakis.com/my-take-on-shaders-radial-blur/). Lucky you! I do have to note that I’ve added a slight chromatic aberration effect on the existing shader though.

Here’s a comparison of a screenshot with and without the radial blur:

![](https://i1.wp.com/halisavakis.com/wp-content/uploads/2019/04/explosion_no_blur000.png?fit=1024%2C576&ssl=1)

![](../../assets/7ab896d228b4ce46.png)

## Conclusion

And that’s it! Hopefully this breakdown gives you a good idea about how to achieve similar effects! For me these little experiments are super fun and I want to explore what else I can do with these simple techniques and shaders. Until then, see you in the next one!

## Comments

Hi, thanks for sharing this shader. I’m trying to recreate the tornado for practice purposes. Everything works so far, but I can’t get the vertex displacement working. Can you share how you did this?

Author

To my surprise, I don’t have a tutorial for that kind of vertex displacement ._. The concept, however, is not too different from the vertex displacement shown in the butterfly/fish shader tutorial ( https://halisavakis.com/my-take-on-shaders-butterflies-and-fish-shader/ ). In the vertex shader I basically sample the noise texture, map the value to a [-1,1] range use this along with a property to displace the model’s vertices along their normal vector, before transferring the vertex position to clip space. The code for that looks like this:

float vertDispl = tex2Dlod(_MainTex, float4(o.uv – _Time.y * _Speed, 1, 1)).x;

vertDispl = -((vertDispl * 2) – 1) * _VertexDisplacement;

v.vertex.xyz += vertDispl * v.normal;

Thanks for the quick reply, wasn’t expecting to get a reply from these kind of blogs! Nice!

I’ll see if I can recreate something similar myself since I’m not really experienced in Shader language. I’m using Unity’s shader graph. I hope I can convert your code to the graphs.