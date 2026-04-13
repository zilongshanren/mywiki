---
title: Combining Shaders
url: https://mini.gmshaders.com/p/combiningshaders
author: Xor
published: '2025-04-19'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Combining Shaders

### How and when to combine shaders into a single pass.

Howdy folks,

Hope you are doing well! Previously, I wrote about setting up “multi-pass” shaders as a way of layering shaders together (or repeating a shader multiple times):

This is commonly used for blurring because it can be more efficient to apply a large blur in separate passes (*for example, instead of a 9x9 Gaussian blur, you can do a 9x1 blur and 1x9 blur, 2*N samples instead of N^2*). However, multipass effects have downsides. They are more difficult to implement, requiring surfaces/canvases, additional draw calls, and more video memory usage. They will complicate your draw pipeline process, and in some cases, are unfeasible. The alternative is to combine two shaders together. So, when is it worth it to combine shaders?

# When To Combine Shaders

Here’s a quick checklist to go over when considering shader compatibility, roughly in order of most important to least important:

**Performance**: Are the effects expensive? Chances are, if both shaders being combined are expensive, the combined shader will be very expensive. Unless you can think of some clever optimizations that simplify it, it’s probably not going to work!**Sample Count**: Do these shaders require lots of texture samples? If you have an outline shader that uses 8 texture samples and a blur shader that uses 32 samples, you’ll likely have to do 8 outline samples for every blur sample, meaning you’ll be using`8*32`

or`256`

samples! That is a lot of texture samples for moderately-sized textures! Generally, it’s safe to combine a multi-sample shader with a single sample shader, but be careful if both shaders use a lot of samples. The shader order does matter, though. If you have an expensive 1-sample shader before a cheap 8-sample blur, you have to do the expensive code 8 times! If the blurring occurs first, you’d only have to do the expensive part once.**Coordinates**: Check if the shaders are operating in the same coordinates. You might have one shader that is a screenspace effect applied to pixel coordinates on the screen, another might be[world-space coordinates](https://mini.gmshaders.com/p/vector-spaces), or[texel coordinates](https://mini.gmshaders.com/p/gm-shaders-mini-texels-and-pixels-1308242). That doesn’t necessarily mean they are incompatible, but it will take some unit conversion and may add some complications.**Textures**: Do your shaders require specific texture sizes? What about texture filtering (*e.g., linear interpolation vs nearest neighbor*)? How about texture boundaries? Distortion effects, outlines, or blurs may sample outside of the texture boundary, so you’ll have to consider how you handle these cases. Sometimes it may be texture repeat, texture clamping, or discarding outside fragments. Make sure they can be adapted to work together! You’ll also want to consider the GPU settings: mainly blend modes and alpha testing.**Uniforms and Inputs**: When combining shaders, you’ll need all the uniforms from both of the shaders. While the limits are pretty high,[shaders do have limits](https://mini.gmshaders.com/p/limits), especially when it comes to having lots of large textures or uniform arrays. You also want to make sure the shader inputs and outputs match (attributes and varyings in old-school GLSL). The good news is that sometimes you can reduce shader complexity by reusing uniforms for both effects (like resolution or time).

If you’ve made it past that, then you’re probably ready to start combining!

# Merging Shader Code

That checklist also hints a bit about how shaders are combined. The first step is to turn your shaders into functions. Let’s start with a sample grayscale shader like this:

```
//Saturation macro (0.0 = gray, 1.0 = full color)
#define SATURATION 0.0
varying vec2 v_vTexcoord;
void main()
{
vec2 uv = v_vTexcoord;
//Sample base texture.
vec4 tex = texture2D(gm_BaseTexture, uv);
//Output color and alpha
vec4 col = tex;
//Grayscale luma
//https://GMshaders.com/tutorials/tips_and_tricks/#useful
float gray = dot(tex, vec4(0.299, 0.587, 0.114, 0.0));
//Mix between gray and color with saturation
col.rgb = gray + (col.rgb - gray) * SATURATION;
}
```


We can rewrite this as a function, with fragment shader inputs as the arguments. In this case, we just have the UV coordinates:

```
//Simple saturation shader:
vec4 saturation(vec2 uv)
{
//Sample base texture.
vec4 tex = texture2D(gm_BaseTexture, uv);
//Output color and alpha
vec4 col = tex;
//Grayscale luma
//https://GMshaders.com/tutorials/tips_and_tricks/#useful
float gray = dot(tex, vec4(0.299, 0.587, 0.114, 0.0));
//Mix between gray and color with saturation
col.rgb = gray + (col.rgb - gray) * SATURATION;
return col;
}
```


Uniforms and macros can be directly referenced in the function, so they do not need to be added as arguments. This is a fairly light-weight function. It doesn’t require a bunch of texture samples, for-loops, branching, or lots of math. Now let’s say you want to combine it with this chromatic aberration shader:

Following a similar process, we end up with this function for radial CA:

```
//From GM Shaders Chromatic Aberration:
//shadertoy.com/view/DtGSRt
//Chromatic blur intensity
#define BLUR 0.05
//Chromatic constrast
#define CONTRAST 2.0
//Must be an even number
#define SAMPLES 20.0
vec4 chromatic(vec2 uv)
{
//Color output starts at 0.
vec4 color_sum = vec4(0);
vec4 weight_sum = vec4(0);
//Iterate 20 times from 0 to 1
for(float i = 0.0; i<=1.0; i+=1.0/SAMPLES)
{
//Add a texture sample approaching the center (0.5, 0.5)
//This center could moved to change how the direction of aberation
//The mix amount determines the intensity of the aberration smearing
vec2 coord = mix(uv, vec2(0.5), BLUR*(i-0.5));
vec4 weight = vec4(i,1.0 - abs(i+i-1.0), 1.0-i, 0.5);
weight = mix(vec4(0.5), weight, CONTRAST);
//Here we use the saturation effect as input
vec4 color = texture2D(gm_BaseTexture, coord);
color_sum += color * color * weight;
//Shift sample tint color from red to green to blue
//The total should be multiplied by the 2/number of samples, (e.g. 0.1)
weight_sum += weight;
}
//Output the resulting color
return sqrt(clamp(color_sum / weight_sum, 0.0, 1.0));
}
```


Now that we have both shaders as functions, we can put them together in one fragment shader. While we’re doing that, we should combine the uniforms, macros, functions, and shader inputs. This is a good time to remove any redundancies you find along the way and share functions and uniforms if possible.

### Order of Effects

Now is the point where you can actually combine the two functions as needed. In this case, I want to apply the desaturation first and then apply the chromatic aberration. To do this, I need to replace the texture2D in the “`chromatic`

” function with my “`saturation`

” function. If I wanted to apply the chromatic aberration first and desaturate after, I would put the `chromatic`

function inside the `saturation`

function. This way would be faster because it wouldn’t require executing the saturation function within a for-loop, but we don’t want to desaturate after applying a color effect.

# Newsletter Update

Just a heads-up, the cost for paid subscriptions is going up to $8/mo or $80/yr soon. This will help me keep a consistent schedule and take fewer contracts. If you’ve ever wanted to join, now is the last chance to get it for $50/yr!

Thank you for the support!

# Conclusion

Thankfully, the process for combining shaders is intuitive most of the time. It can be summed up be turning your shaders into functions and feeding one function into another as needed. The inner function is applied first. It’s preferable to do the most samples first because shader costs can compound quickly.

To recap, before you consider combining, you should look at:

**Performance** - Expensive shader + expensive shader ≈ very expensive!

**Sample Count** - Avoid combining shaders that use a lot of texture samples.

**Coordinates** - Make sure the type of coordinates matches up correctly.

**Textures** - They should share texture settings and formats.

**Inputs** - Vertex formats, uniforms, and varying will have to match up.

If you pass that test, then it may be worth trying.

# Extras

Here are my 3 examples of one-pass blur shaders

[1 Pass Blur](https://github.com/XorDev/1PassBlur/wiki) - A simple, cheap disk blur based on the [golden angle](https://mini.gmshaders.com/p/phi).

[Mip Blur](https://github.com/XorDev/GM_MipBlur) - An efficient blur that makes use of mipmapping.

[Bokeh](https://github.com/XorDev/Bokeh/wiki) - A rich Depth of Field effect that is good for backgrounds.

That’s all for today. Thank you for reading and have a great night!

-Xor

Thank you for the tutorial! My question is, is there any tool I can use to parse GLSL codes to do this automatically?

Shader beginner here - great tutorial.

Let's say I wanted to combine two shaders with both moving elements, one in the background that does moving color gradients, and one in the foreground that applies a circular ripple/shockwave effect on top of it.

How would you approach this conceptually? The mental challenge for me is that both are moving unlike a static photo background texture which I can just read.