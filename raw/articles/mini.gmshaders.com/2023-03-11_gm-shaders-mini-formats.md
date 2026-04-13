---
title: 'GM Shaders Mini: Formats'
url: https://mini.gmshaders.com/p/mini-formats
author: Xor
published: '2023-03-11'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Formats

### Let's talk about texture formats

Hello folks! It’s been a while, but I’m back!

GameMaker recently added new “surface formats”. If you’re wondering what this is, you’ve come to the right place.

Today, I want to cover what all this means and how you can use it!

## Formats

Until now, GM has only supported one texture format: RGBA8unorm.

This has 4 channels (red, green, blue, and alpha), 8-bits per channel (0-255), and is unsigned and normalized (meaning it ranges from 0 to 1 in 1/255th units).

We now have 8 formats we can choose from:

`surface_rgba8unorm`

`surface_rg8unorm`

`surface_r8unorm`

`surface_rgba4unorm`

`surface_rgba16float`

`surface_r16float`

`surface_rgba32float`

`surface_r32float`


The “rg” and “r” have only two and one channels respectively. This means that there is no alpha channel and blue channel. This saves memory usage and should be slightly faster.

“4unorm” is a format that only has 4-bits per channel so 1/16th increments. This saves 50% of the memory usage but is only supported on some hardware.

“16float” and “32float” store color as floats in 16 and 32 bits respectively. This is huge when it comes to shaders! You can now output values greater than 1 or even negative values and it’s more precise than 1/255ths. 16 bits are enough for HDR effects or depth maps and 32 is for high-precision at the cost of higher memory usage.

You can check if a format is supported on your hardware using this function:

`surface_format_is_supported()`


Now let’s go over some cool ways to use this!

## Simple Lighting

In my [Lights tutorial](https://xordev.substack.com/p/gm-shaders-mini-lights), I mentioned the challenge of using 8-bit surfaces for doing lighting. Now it’s possible to do this without shaders!

**1: Create a light surface**:

I'm calling mine "surf_light" and initialize it at -1 so I can create it later. In the Draw GUI Event, I create the surface. This also recreates the surface if it gets destroyed. We can use the new "surface_rgba16float" so that we can have light values greater than 1.

```
//Make sure the light surface exists!
if surface_exists(surf_light)
{
//Match the width and height of the application surface
var _w,_h;
_w = surface_get_width(application_surface);
_h = surface_get_height(application_surface);
surf_light = surface_create(_w,_h, surface_rgba16float);
}
```


**2: Draw Lights:**

Next, we need to draw the lights on our surface. This could be ambient lights, sprites, gradients, or anything. camera_apply here means we can draw in room coordinates instead of surface coordinates. Use an add blendmode to draw lights properly!

```
//Draw lights to light surface
surface_set_target(surf_light);
//Start with ambient light color
draw_clear(light_ambient_color);
//Apply view coordinates
camera_apply(view_camera[0]);
Additive blending for lights
gpu_set_blendmode(bm_add);
//
//DRAW LIGHTS HERE
//
//Finish
surface_reset_target();
```


**3: Blend with application surface:**

Now we can create using a multiply blendmode to blend the light surface with the application surface. We're multiplying the destination color (app surface) by the source color (surf_light). Finally, we can just draw the results and we're done!

```
//Finally, blend it with the application surface
surface_set_target(surf_light);
gpu_set_blendmode_ext(bm_dest_color, bm_zero);
draw_surface(application_surface,0,0);
gpu_set_blendmode(bm_normal);
surface_reset_target();
Draw blended result
draw_surface(surf_light,0,0);
```


And that’s it!

You can download my example project [here](https://github.com/XorDev/BasicLighting).

## Other Uses

There are many cases where 8-bits RGBA isn’t ideal. Here are some ideas:

**HDR Bloom/Blur:**When you do bloom on large scale, 8-bits often isn’t enough precision and causes visible banding (especially in multipass shaders). By using float16, you can have higher precision and better results**Depthmaps/shadowmaps:**Many shaders require storing the screen depth onto a surface. Now you can do it efficiently using`surface_r16float or surface_r32float (no more bit packing!).`

**Jump Flood Algorithm**: JFAs are multipass shaders, used to compute the distance field around arbitrary shapes. They only need x and y channels, so`surface_rg8unorm is ideal.`

**Fluid/Particle Simulation**: Floating point textures allow for precise simulations of velocity which previously was difficult or messy.

Those are just a few of the many possibilities! Can’t wait to play around with these further to see what else can be achieved.

## Conclusion

So to summarize, the new surface formats give us greater control of our VRAM and open some doors. We no longer need to use workarounds like bit-packing for depthmaps!

It’s a good time to explore shaders with GameMaker, especially with compute shaders on the way.

Anyway, that’s all I got for today. Thanks for reading!

Thank you so much!

Can you explain the connection between a surface and a particle simulation? I saw examples on Twitter where GM users are happy that they have the high precision surfaces to create particle simulations but I don't see the connection.