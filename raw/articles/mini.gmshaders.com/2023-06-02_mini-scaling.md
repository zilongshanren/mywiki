---
title: 'Mini: Scaling'
url: https://mini.gmshaders.com/p/gm-shaders-mini-scaling
author: Xor
published: '2023-06-02'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Scaling

### How to handle scaling, aspect ratios and centering

Greetings,

Early in my shader journey, I struggled with scaling or layout issues. I might get the scale correct, but only to have stretching or incorrect centering. Take for example these common issues when attempting to center a circle:

If ever tried to center your shader without stretching, you’ve probably seen these configurations. My goal for tonight is to go over a few common scaling arrangements so that you can understand them once and for all! Don’t worry, they are fairly easy to learn and remember for future reference!

## Pixel Scaling

Last year, I wrote about the relationship between texture coordinates and pixels. Well worth a read if you haven’t yet:

The first step here is to make sure you know how to convert between texture coordinates and pixel coordinates. You can convert [normalized texture coordinates](https://mini.gmshaders.com/i/91667868/normalized-coordinates) to pixel coordinates by multiplying them with the texture or screen resolution (u_res).

`vec2 pixel = v_vTexcoord * u_res;`


Or for shaders that don’t have texture coordinates (like ShaderToy shaders), `gl_FragCoord.xy`

would also work for screen pixel coordinates.

It’s worth noting that if we sample a texture using the pixel coordinates divided by 100.0, the texture will stretch across (0, 0) to (100, 100) pixels.

If you divided by 256.0, it stretches from (0,0) to (256, 256). This may seem unintuitive at first. Why does dividing texture coordinates by a larger number result in a larger texture? Well the reason we’re dividing the size instead of multiplying, is because we’re scaling the input coordinates, not the size of the texture. For example, if we have texture coordinates that range from 0 to 1 and we divide them by 2, we get a range of 0 to 0.5. That means instead of showing the whole texture, we’re only showing the bottom-left quarter across the whole screen, doubling its x and y scales by 2!

In short to scale texture coordinates we divide by the scale, not multiply!

`vec2 uv_scaled = uv / scale;`


This is was a bit of a mystery to me when I first approached it, so hopefully my explanation can save you some trouble!

## Stretching

Most of the time, you’ll want to do any scaling, offsets, and rotations using pixel coordinates. Then you may need to convert these modified pixel coordinates back to uv (texture) coordinates either for sampling a texture or any effect that should scale with the screen size.

Here’s the simplest way to compute uv coordinates stretched across the screen:

`vec2 stretched_uv = pixel / u_res;`


However, if we don’t want to keep the uv coordinates nice and square, we have to divide both axes by the same values:

```
//UV coordinates range from 0 to at least 1 (cropping excess)
vec2 fill_uv = pixel / min(u_res.x, u_res.y);
//UV coordinates range from 0 to at most 1 (including empty space)
vec2 fit_uv = pixel / max(u_res.x, u_res.y);
```


These are just like the settings you have when setting your Desktop wallpaper on Windows:

I personally use “fit” most often in my shaders because it doesn’t crop anything out, but knowing and understanding both is a good idea!

## Centering

So using fit or fill fixes the stretching issues when dealing with different screen/window sizes, but what about centering?

Thankfully it’s very straightforward. Just center the pixel coordinates so they range from -res/2 to +res/2, do your uv coordinates stretching/scaling, and then add 0.5 to put it back to the 0 to 1 range!

```
//Pixel coordinates relative to the screen center
vec2 center_pixel = pixel - u_res*0.5;
//Compute uv coordinates using centered coordinates and add 0.5
vec2 fill_uv = center_pixel / min(u_res.x, u_res.y) + 0.5;
vec2 fit_uv = center_pixel / max(u_res.x, u_res.y) + 0.5;
```


The neat part about this method is it works with any sort of layout. If I want to center around the middle-bottom side, I could do so like so:

```
//Put the scaling origin on the middle-bottom side (0 to 1 range)
vec2 origin = vec2(0.5, 1.0);
//Compute scaled uv coordinates using this origin
vec2 center_pixel = pixel - u_res * origin;
vec2 fill_uv = center_pixel / min(u_res.x, u_res.y) + origin;
```



I don’t use other origins often, but I thought I’d share it here just in case it ends up being useful!

## Ratios

So far, I’ve been assuming that you want to map square uv coordinates to the screen, but what if you need to map 2x1 texture to any screen dimensions with no cropping (fit scaling)?

Well, to do so we need to do two things: stretch the output uv coordinates using this ratio, and account for it while finding the fit scale. Both can be done like so:

```
//Texture aspect ratio (could be passed in via uniform)
vec2 ratio = vec2(2, 1);
//Correct resolution with texture ratio
vec2 res_ratio = u_res / ratio;
//Center origin
vec2 origin = vec2(0.5, 0.5);
//Pixel coordinates relative to the screen center
vec2 center_pixel = pixel - u_res * origin;
//Compute centered uv coordinates with desired aspect ratio.
vec2 fit_uv = center_pixel / max(ratio_res.x, ratio_res.y) / ratio + origin;
```



Hopefully, you won’t need all of this, but if you do, this is how you do it!

## Conclusion

To recap, if you want to scale elements with the screen, you should first center the pixel coordinates, scale them to the desired fit or scale, optionally stretch with aspect ratio, and remap back to the UV coordinates (with 0.5 being the center). Doing anything in the wrong order or multiplying by a scale when you should be dividing, are very common problems.

This is meant as a clear blue print you can follow if you ever get stuck in the future. Consider bookmarking this if you think you’ll need it.

Thanks a lot! Have a great weekend!