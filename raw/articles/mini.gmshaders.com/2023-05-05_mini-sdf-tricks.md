---
title: 'Mini: SDF Tricks'
url: https://mini.gmshaders.com/p/gm-shaders-mini-sdf-tricks
author: Xor
published: '2023-05-05'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: SDF Tricks

### Some cool things you can do with Signed Distance Functions

Hi people!

A while back I wrote about Raymarching. I’d recommend reading this first before tackling this topic:

Today I want to cover some more cool things you can use SDFs for.

## Shapes

So we covered raymarching for rendering 3D objects inside a fragshader, but SDFs are also very useful in 2D. SDFs are often used to create shapes, like circles, boxes, or more complex shapes:

This is basically the main way to generate vector shapes in shaders manually. Once you learn these techniques, it makes it possible to do so much more like localize an effect to a certain area or even make shader art!

The easiest shape to learn is the circle SDF:

```
//Signed distance to circle using relative position and radius
float SDF_circle(vec2 p, float r)
{
return length(p) - r;
}
```


Give it a relative position and a radius in any units (pixels, texels, whatever) and it returns the distance to the nearest edge of the circle (negative if inside).

Here’s an example of how you might use it:

```
//If inside 100 pixel circle
if (SDF_circle(circle_pos - pixel, 100.0) <= 0.0)
{
//Output red color
color = vec4(1.0, 0.0, 0.0, 1.0);
}
```


Box SDFs are a little more interesting

```
//Signed distance to box using relative position and box size
float SDF_box(vec2 p, vec2 s)
{
//Mirroring the positive quadrant simplifes the math
//Here we are getting the distance along the x and y axes
vec2 b = abs(p) - s;
//Compute the length of the outside vector + inside vector
return length(max(b,0.0)) + min(max(b.x,b.y), 0.0);
}
```


I could go through all sorts of different shapes, but it’s best to start simple!

When you’re ready to go deeper, [Inigo Quilez has written formulas](https://iquilezles.org/articles/distfunctions2d/) for all sorts of shapes so you don’t have to! Also, [Juju has ported several of them](https://github.com/JujuAdams/Clean-Shapes/wiki) to GameMaker already.

One of the benefits you get with function-based shapes is you can easily make them tile at a minimal cost, just by repeating the input coordinates with mod or fract. You can’t draw an infinite number of sprites on the CPU because each sprite is drawn sequentially. On the GPU, if you tile the coordinates, each pixel may still be processing just one shape, but you can be rendering hundreds or thousands simultaneously! Perfect for snowflakes, rain, stars, or whatever!

Now let’s explore producing smoother shapes!

## Anti-Aliasing

In case you missed the [FXAA tutorial](https://mini.gmshaders.com/p/gm-shaders-mini-fxaa), the purpose of anti-aliasing is to show subpixel detail in the pixel output.

Unless you’re deliberately going for a pixel style, you probably want anti-aliasing. Real-life perception is not blocky, so it’s better to think of pixels in terms of the percentage covered.

Thankfully with SDFs, this is practically free to calculate! Just subtract the pixel function from 0.5 (the alpha midpoint) and divided it by our desired pixel spread:

```
//Distance to circle in pixel coordinates
float dist = SDF_circle(pixel - circle_pos, 64.0);
//Compute alpha from pixel distance function
float alpha = clamp(0.5 - dist / AA_SPREAD, 0.0, 1.0);
//Smoothly blend with existing color
color = mix(color, vec4(1.0, 0.0, 0.0, 1.0), alpha);
```


I typically like a spread of 2 pixels, but it’s up to you. I’d generally advise between 1 and 3.

Perhaps even more interestingly, you can add outlines to anything also for next to no performance cost!

You can compute the outline distance field, but just subtracting your outline thickness:

`float outline_dist = dist - outline_thickness;`


Which can then be blended just like the regular SDF above.

I also briefly mentioned in the [Lights tutorial](https://mini.gmshaders.com/p/gm-shaders-mini-lights) how SDFs can be used for a rich glow effect:

And with a little creativity, this can also be used for soft drop shadows!

## Conclusion

SDFs are everywhere in shaders and for good reason. It’s arguably the easiest way to define shapes with code! And as a side effect, it gives you AA practically for free, outlines, glows, and shadows.

This still only scratches the surface of what can be done with these formulas, but hopefully, that’s enough to get you started. SDFs become exponentially more powerful in 3D and can be used for direct lighting, soft shadows, ambient occlusion, and even has applications in collisions/physics! Perhaps I’ll do a part two if the interest is there.

Thanks for reading! Have a great weekend!

How to draw a perfect 1 pixel border ring? I tried but when resolution scales, the border scales too.