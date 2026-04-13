---
title: 'GM Shaders: Gamma'
url: https://mini.gmshaders.com/p/gamma
author: Xor
published: '2025-01-24'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Gamma

### How computers handle lighting

Hi there!

Today, we’re tackling gamma correction inside shaders. Many have written about gamma correction, but I haven’t found any that satisfy my teaching goals, so I thought I’d write my own quick overview. Your time is precious, so I’ll save you trouble and start with why you should care about gamma.

You may know of Gamma as a brightness slider in games, but there’s much more to it than that. Color, specifically luminance, is often stored and displayed differently to how light behaves in real life. There are two main formats: linear color (as in real life) and Standard RGB or “sRGB” (encoded light). Images are stored in sRGB because it’s a more efficient use of bits, but it’s incorrect to do our lighting operations in sRGB, so we need to know how to convert back and forth.

[Even common shader effects like blurs are often done incorrectly](https://iquilezles.org/articles/gamma), by not accounting for gamma correction. Here’s how gamma can affect blurring:

So, gamma is not about the overall brightness of an image. Black is still black, and white is still white, but it does affect the distribution of brightness. Doing it correctly can make a big difference in the look and feel of your game!

# Encoding and Decoding

You’ve probably heard of Gamma 2.2 before. It’s been the standard in most displays for a while now, but what does the “2.2” mean? Well, the gamma number is the exponent used to map the RGB back to the linear color. Some rare monitors might have a gamma of 2.0 or 2.4, but 2.2 is the general standard to assume.

Here’s an illustration of what that looks like:

The red line represents how colors are stored (black being on the left end of the spectrum and white being on the right). You can see that the gray values in the middle are shifted downward towards darker shades. If you want to reverse this curve, you need to apply the green decoding curve, which gets us back to linear color.

With linear color, you can do any color transformations you want (like additive blending), but then, when you’re done, you need to convert the output back to sRGB.

Here are my little approximate functions to do these conversions:

```
//Standard gamma exponent
#define GAMMA 2.2
//Decode sRGB to linear color //Note: this is a standard approximation vec3 gamma_decode(vec3 srgb)
{
return pow(srgb, vec3(GAMMA));
}
//Encode linear color to sRGB
vec3 gamma_encode(vec3 lrgb)
{
return pow(lrgb, vec3(1.0/GAMMA));
}
```


[I’ve put together a simple example](https://www.shadertoy.com/view/XXyBRR) using two point lights:

```
//Screen coordinates from -1 to +1 (aspect ratio corrected)
vec2 suv = (gl_FragCoord*2.0 - u_resolution.xy) / u_resolution.y;
//2.2 gamma on the right
//Light source positions
vec2 pos = 0.4 * sin(u_time+vec2(0,11)) * cos(u_time*0.618);
//Red light
vec3 light1 = 1.0 / (1.0 + length(suv+pos) * vec3(1,5,9));
//Blue Light
vec3 light2 = 1.0 / (1.0 + length(suv-pos) * vec3(9,5,1));
//Linear color values
vec3 lin1 = gamma_decode(light1);
vec3 lin2 = gamma_decode(light2);
//Add light sources together
vec3 col = lin1+lin2;
//Convert back to sRGB
gl_FragColor = vec4(gamma_encode(col), 1.0);
```


You can see the image is overexposed on the right and does not blend as cleanly. Anything that has to do with color blending or light should be done in linear color space! If you sample a texture, it will be in sRGB, so you’ll need to convert that to linear color, do your operations, and then finally convert the results back to sRGB.

# Exact sRGB

Okay, I must admit I simplified a little bit. sRGB is a bit more complicated than gamma 2.2, but gamma 2.2 is a good approximation.

Here’s the real formula with a lot more magic numbers:

```
//Decode sRGB to linear
vec3 SRGB_decode(vec3 srgb)
{
return mix(
srgb / 12.92,
pow((srgb + 0.055) / 1.055, vec3(2.4)),
step(0.04045, srgb)
);
}
//Encode linear to sRGB
vec3 SRGB_encode(vec3 lrgb)
{
return mix(
12.92 * lrgb,
1.055 * pow(lrgb, vec3(1.0 / 2.4)) - 0.055,
step(0.0031308, lrgb)
);
}
```


[The difference is quite subtle](https://www.shadertoy.com/view/M3KBR3), but it does make a difference with darker shades and the upper middle:

In professional contexts where precision is essential, you’ll want to use the exact sRGB formula, but in most contexts, gamma 2.2 is a good, cheaper approximation. It’s way better than nothing!

# Gamma Origins

Now that we covered the basics, here’s a little background context.

The sRGB format originated because the old Cathode-Ray Tube displays had a non-linear relationship between the input voltage and the output pixel brightness (usually a gamma of 2.2 to 2.5). This was convenient because our eyes do not perceive lightness linearly either, and we are more sensitive to changes in darker shades than lighter ones, so if we have a limited number of bits to store colors, we should store more darker shades.

Camera sensors capture light in linear color but store their images with gamma encoding for image storage efficiency. This is why it’s crucial to convert images back to linear color before you do anything with them!

# Conclusion

As with many topics, gamma correction can be quite complicated, and this tutorial only scratches the surface. I hope that this will make the concepts more approachable so that you can do further experimenting and learning as you go, just with a bit more context about how computers handle colors.

If I could reduce this tutorial down to one point, it’d be that computers store colors at the power of 1/2.2 (sRGB), and if you want to do any math with your colors, you should convert to linear first and then finally convert the end results back to sRGB. This one lesson is actually super important, and not enough shader people do this, so it’s best to start now! As always, I’m including some additional resources below

# Extras

John Novak has an [excellent and thorough guide on everything about gamma](https://blog.johnnovak.net/2016/09/21/what-every-coder-should-know-about-gamma/)! If you need a little more clarity on anything, I’d check here first!

Kostas Anagnostou wrote about the [hidden cost of shader instruction,s](https://interplayoflight.wordpress.com/2025/01/19/the-hidden-cost-of-shader-instructions/) which explains why some functions are much slower than others. Avoid the arc trigonometry functions like atan and aco,s particularly!

Thanks for reading! Have a great night!

-Xor