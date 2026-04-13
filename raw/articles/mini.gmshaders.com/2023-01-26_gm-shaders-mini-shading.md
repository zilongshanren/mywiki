---
title: 'GM Shaders Mini: Shading'
url: https://mini.gmshaders.com/p/gm-shaders-mini-shading
author: Xor
published: '2023-01-26'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Shading

### All about diffuse shading

Good evening, people,

Last week, we covered some basic lighting shaders and attenuation. Read here if you missed it:

The next step is shading. That’s what shaders were designed for after all! To understand shading, we’ll need to go over some basic light physics

## Diffusion

We’ve all heard that light bounces off of objects and lands in our retinas, but what does this actually mean? What is the difference between shiny chrome and a piece of paper?

Well, there are two main types of light interactions to consider here: Specular and diffuse. Take a look at this 2D illustration:

Here you see white light rays coming from the upper left, reflecting off a surface. Specular materials behave a bit like mirrors, with simple reflections. Diffuse materials, however, have a more chaotic structure such that light rays are reflected in unpredictable directions.

This also illustrates how color is transferred. The surface here absorbs red light, only reflecting the teal light to our eyes (or camera).

Today, we’ll just focus on the diffuse interactions (perhaps I’ll do a “Physically-Based Rendering” tutorial later).

## Shading

So what does this mean for shading? Well, it shows that light direction and the surface direction, “normal”, are important when approximating how much light reaches our eyes.

Thankfully, Johann Heinrich Lambert discovered the “[cosine law](https://en.wikipedia.org/wiki/Lambert%27s_cosine_law)” so we can easily compute this light value. *Essentially, it calculates the percentage of all possible light rays that reflect out.*


In shader terms, it looks something like this:

`float light = max(cos(theta), 0.0);`


Theta here is the angle between the light direction and surface normal. Negative light values don’t make sense, so that’s why we max it to at least 0.

The most important bit to understand is that when the light and normal are perpendicular to each other, no light is reflected (0.0), but when they are facing each other, all the light is reflected (1.0). It’s easier to understand in action, so I’ll go over a simple application.

## Bump Mapping

[Bump mapping](https://en.wikipedia.org/wiki/Bump_mapping) is probably the easiest way to implement simple shading in your games, which gives them a sense of depth.

All you need is a bump map or a height map (grayscale image representing depth), and you can compute the shading in real-time with the fragment shader.

The method I used here is rather simple. Sample the heightmap at the current pixel, and again one pixel toward the light source. Then you can calculate the normal using the two sampled height values:

`float normal = atan(texel.y, (height0 - height1) * depth);`


Now we can compute light value like so:

`float lambert = max(cos(normal - light_pitch), 0.0);`


Try my [full example ShaderToy here](https://www.shadertoy.com/view/mlfSzn).

## Conclusion

Welp, I planned to include normal mapping, but this tutorial is long enough already. To summarize the most important bits, diffuse reflections are the reason that objects appear shaded. It’s helpful to imagine a zillion photons bouncing in all different directions. When you get enough photons together, it can produce smooth shading despite the fact that it’s a product of trillions of little interactions.

And with the power of Lambert’s cosine law, you can compute lighting using the angle between the light direction and the surface normal. There are many different methods of doing diffuse lighting, but they all hinge on this simple principle, so it’s important to understand.

Hopefully, you learned something new about lighting, computing normals, or something in between. Best of luck on your shading endeavors.

Thanks for reading,

-Xor