---
title: 'Mini: Texels and Pixels'
url: https://mini.gmshaders.com/p/gm-shaders-mini-texels-and-pixels-1308242
author: Xor
published: '2022-08-12'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Texels and Pixels

### The relationship between "texels" and pixels

Hello people!

Hope you all are doing well. I'm beginning a [new weekly series](https://twitter.com/XorDev/status/1555689666153783296) of mini shader tutorials for my newsletter subscribers! These will be little bite-sized guides on a variety of topics for beginners and advanced users alike.

Today, we're going to learn about texels, pixels, and conversion between the two!

## What are Texels?

You already know what [pixels](https://en.wikipedia.org/wiki/Pixel) are, but what are [Texels](https://en.wikipedia.org/wiki/Texel_(graphics))? As the name implies, it's a pixel unit of a texture (not the screen). So while the pixel unit represents 1 pixel on the screen, the texel unit can be stretched across multiple pixels or any other transformations.

In technical terms, pixels are screen-space units and texels are texture-space units. This may be useful to know down the line!

## Texel Uniforms

So, suppose you are making a magnifying post-process shader and you want to distort a texture at the mouse position. The mouse position will be relative to the screen size, but the texture coordinates always range from 0 to 1.

This means we need to convert the texture coordinates to pixels so that we can do the pixel distortion and then convert them back to texture coordinates. Since we're converting from the room size to a 0-1 range, the texel size is simply 1.0 / room_width and 1.0 / room_height.

So we need two uniforms: a vec2 for the mouse position relative to the screen (mouse_x, mouse_y), and a vec2 for the texel unit size. I'll call this u_mouse and u_texel, respectively.

Note: if you're using views, then replace mouse_x/y with windows_mouse_get_x/y and room_width/height with window_get_width/height.

## Magnifying Example

Now in the shader, we can compute the pixel coordinates from texture coordinates by dividing the texture coordinates by the texel size:

`vec2 pixel = v_vTexcoord / u_texel;`



Now we can apply our magnifying effect, for example:

First, we'll find the difference from the pixel to the mouse:

`vec2 to_mouse = pixel - u_mouse.xy;`



Then we can make the effect fade out (attenuate) to 0 at 100 pixels from the mouse:

`float attenuation = max(1.0 - length(to_mouse) / 100.0, 0.);`



Finally, we'll add our mouse offset with attenuation:

`pixel -= to_mouse * attenuation * 0.5;`



Now that part is not too important. It could be any sort of effect where pixel coordinates are relevant. Maybe you want to randomly offset every 10 pixels? Maybe you want to invert colors around the mouse? Either way, you can do that with pixel coordinates!

In order to use our new pixel coordinates, we'll have to convert them back to texture coordinates, and it's as easy as multiplying by our texel size:

`vec2 new_coords = pixel * u_texel;`



And of course, we must sample the base texture using our new coordinates:

`gl_FragColor = v_vColour * texture2D(gm_BaseTexture, new_coords);`



And we're done! We took a journey from texture coordinates to pixels, applied distortion, and returned to texture coordinates so we can see the results!

## Complex Cases

This tutorial is assuming the simplest case scenario: You're drawing a surface that extends across the entire screen, your texture is its own [texture page](https://gmshaders.com/tutorials/gamemaker/#texturepages) (so it ranges from 0 to 1 and not something weird: see the [Texture Coordinates section](https://gmshaders.com/tutorials/tips_and_tricks/#useful)), and you have mouse coordinates relative to the screen.

Unfortunately, these conversions can become quite complicated if you have rotations, skewing, or stretching of either the view or the texture. These scenarios go a bit beyond the scope of this tutorial, but if they can't be avoided, you'll need to look into matrices and inverse matrices.

Perhaps I'll cover this in a future tutorial!

## Conclusion

Hopefully, you found this useful. There are a lot of terms that can be confusing, so with this series, I hope to clarify them in small steps.

Thanks for reading

-@XorDev