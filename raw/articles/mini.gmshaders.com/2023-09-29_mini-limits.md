---
title: 'Mini: Limits'
url: https://mini.gmshaders.com/p/limits
author: Xor
published: '2023-09-29'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Limits

### The limits of shaders

Hi folks,

Today is all about what you can’t or shouldn’t do with shaders.

If you’re new to shaders, it may be hard to tell what can or cannot be done with shaders. Perhaps you’ve seen procedural cloud generation/rendering, pixel sorting, procedural cities, flood filling, fluid/physics simulations or neural networks?

It’s hard to say what’s possible with shaders as new techniques are being discovered all the time. Instead, let’s look at what you can’t or shouldn’t do with shaders, so hopefully I can save you some time!

**Vertices and Fragments**

At the end of the day, shaders are just vertices and fragments. Compute shaders broaden the possibilities a bit, but in a GameMaker context we currently only have vertex shaders and fragment shaders.

**Vertex Shaders**

The vertex shader’s limitations are easier to define. In it, the only direct output you have is with `gl_Position`

which is the projection-space coordinates of the vertices on your screen. This allows you to move vertices around which can be used for effects like billboarding, fluid displacement, shockwave distortions and much more. The vertex shader also handles the data you pass via “varying” to the fragment shader from the inputs: attributes and uniforms. Usually you pass over the vertex color and texture coordinates, but you can pass any values you want over. I’ve even passed matrices and floats (like depth).

The vertex shader cannot however add or remove vertices. If you’re a bit clever, you might be able to remove certain triangles by moving all the vertices to (0,0,0), but it’s not the ideal solution.

*Note: My anecdotal experience is that moving vertices too far can result in performances hiccups. I assume it has something to do with the z-testing being out of order, but not sure exactly.*

### Fragment Shaders

There’s a reason that most people think of fragment shaders first. Firstly, it’s run on every single fragment/pixel which gives you finer control than with the vertex shader, but remember the fragment shader only runs on the output of the vertex shader. For example, if you’re running a blur shader on individual sprite, you cannot blur outside the vertex boundaries, often leading to harsh borders. This could be fixed by padding the sprite in the vertex shader or by padding the input texture.

In any case, you’re limited by vertices first. You cannot create fragments where there isn’t a vertex mesh already. Here’s an illustration with Mr. Juju:

The fragment shader is only run inside the yellow box, but it is run on the transparent pixels too.

Fragment shaders have a special trick up their sleeves though. They can be drawn to surfaces/buffers. This greatly expands what can be done with shaders because you can layer multiple effects, save the results or even read them in GML (albeit very slowly `surface_getpixel()`

or `buffer_get_surface()`

). So although fragment shaders are meant for purely visual uses, they can actually be used to build regular buffers and effect the gameplay mechanics directly. I once used shaders to generate an audio buffer far quicker than I could in GML sequentially.

And there’s one more thing: `discard`

. Discard, lets you completely throw out a fragment and skip the whole blending / depth testing part, which is very useful in 3D.

I think that just about covers it for frag shaders (unless you want to look up `gl_FragDepth`

).

### Soft Limits

While you technically can have resolutions up to 16,384x16,384 in GM, that doesn’t mean you should. Be aware of the impact that resolution has on performance. 1920x1080 may not be feasible on some machines if you have an expensive shader, so always consider drawing at a lower resolution on a surface and scaling up. Many effects like blur shaders can be done at half or even quarter resolution which will greatly expand the number of devices your code will run on. Also the size of textures you pass into the shader will have some effect on performance.

Finally, you have to be careful with the number of times you sample textures in your shaders. A blur shader that samples 500 times may run okay on midrange hardware, but will suffer on lower-end hardware. I don’t think there’s a magic formula for how many times you should sample in a shader since hardware is constantly evolving and it depends on factors like resolution. I think 32 samples is a pretty conservative limit, but you may need to go higher or lower. If possible doing more passes with fewer samples, can save a lot of performance cost!

**Version Limits**

Now let’s take a look at shader version limitations, which affects what features we have access to. GameMaker currently uses GLSL 1.00. This means we’re missing many of the newer functions. I’ll compare this to [GLSL 3.00](https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf), which is more widely used (like with ShaderToy). Here’s a list of new features in 3.00 that we’re missing in 1.00:

**Operators:** `%, <<, >>, &, ^, |`


These are operators specifically for integers. In order we have mod for ints, bitshift left, bitshift right, bitwise AND, bitwise XOR and bitwise OR. These are frequently used in modern hash/noise functions, which are faster and more consistent!

**Data types:** `uint/uvec`


This is a new data type for unsigned integers (for values 0 or greater, no negatives). uints are good for bitwise math, where every bit counts.

**Texture functions:** `textureGrad, textureSize, textureOffset, textureGradOffset, textureProjLodOffset, textureProjGrad, texelFetch, texelFetchOffset`


The texture “grad” functions gives you direct control of the gradients (derivatives) that are used for mipmapping. A common issue you may experience with mipmaps, is if you repeat a texture by `fract(uv)`

, you get seams because the coordinates are discontinuous. This can be solved with `textureGrad`

by computing the derivatives independently: `dFdx(uv), dFdy(uv)`

. `textureSize`

is a convenient way to get the texture resolution with needing to pass it in via uniform. Offset functions add an offset to the uv coordinates (honestly never used it) and `texelFetch`

which samples specified texel without any filtering.

**Hyperbolic trig functions:** `sinh, cosh, tanh, asinh, acosh, atanh`


These are the [hyperbolic trigonometry functions](https://en.wikipedia.org/wiki/Hyperbolic_functions). I think I’ve only ever used tanh because it maps a value between -∞ and +∞ to the -1 and +1 range which can be useful.

**General math:** `round, roundEven, trunc, modf,`


`round(x)`

rounds toward the nearest whole number. round(0.5) will return either 0.0 or 1.0 depending on the implementation, so if you need predictable behavior, use `floor(x+0.5)`

, `ceil(x-0.5)`

or `roundEven(x)`

. roundEven rounds to the nearest even number, so 1.5 and 2.5 both round to 2. `trunc`

rounds towards 0.0, so -0.5 and +0.5 both round to 0. `modf(x,y)`

returns `fract(x)`

with “y” being set to floor(x).

**Matrices:** `determinant, outerProduct, inverse, transpose`


These are some advanced matrix functions. This goes beyond the scope of this guide, but if you have to do a lot with matrices, these are a must-have. If you need these in GLSL 1.00, you can always just [calculate it manually](https://github.com/glslify/glsl-inverse/blob/master/index.glsl).

**Data and bits:** `isnan, isinf, intBitsToFloat, uintBitsToFloat, floatBitsToInt, floatBitsToUint, packSnorm2x16, packUnorm2x16, unpackSnorm2x16, unpackUnorm2x16`


`isnan(x)`

returns true if “x” is “Not a Number” and `isinf(x)`

returns true if x is positive or negative infinity (for example, 1e50 is large enough in high float precision to be considered positive infinity). The rest of the functions are used for converting bits to floats, floats to bits, vec2s to uints and vice versa.

These are just the differences between 1.00 and 3.00. There are more functions, datatypes, doubles, atomics and much more. I couldn’t include all the details, but I’ll leave a [link to the docs here](https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf).

# Constant Limits

GLSL has a few built-in constants which can tell you the maximum number of things like uniforms, that are supported on your target hardware. I’ll include my tested values on my RTX 2060 for comparison.

**Sampler limits**

There are three constants relating to textures and samplers.

`gl_MaxTextureImageUnits`

is an `int`

that gives us that max number of supported textures/samplers in the fragments shader. On my machine this is set to 16, but GM caps this at 8 (including `gm_BaseTexture`

) presumably for compatibility.

`gl_MaxVertexTextureImageUnits`

tells the maximum number of textures/samplers you can have in the vertex shader, but as of writing you can only sample textures in the vertex shader on the Web export, so not super useful here.

`gl_MaxCombinedTextureImageUnits`

tells us the maximum number of textures/samplers total that can be used in the vertex and fragment shaders (32 in my case).

**Uniform limits**

As you can imagine, there is a maximum number of uniforms you can have in a given shader. This also depends on the shader implementation and hardware.

`gl_MaxFragmentUniformVectors`

gives you the maximum number of floats or vectors you can pass into a fragment shader. On my hardware, it is 1024, but it can vary as low as 16. I’d recommend using at most 256 uniforms if you want to be compatible with older machines and even lower if you need to support older mobile devices.

`gl_MaxVertexUniformVectors`

gives you the maximum number of floats or vectors you can pass into a vertex shader. This is also 1024 on my machine, however you’re guaranteed [at least 128](https://shaderific.com/glsl/constants.html) even on low end hardware.

**Attributes and Varyings**

There is also a limit to the number of attributes and varying vectors you can have.

*You should be somewhat careful with how much data you pass into your shaders anyway. Having lots of attribute data can slow your drawing down especially with larger scenes. In some cases, you can calculate values like tangents, which may be faster than passing them in*!

`gl_MaxVertexAttribs`

for the maximum vertex attributes you can have. You’re guaranteed at least 8 and my case 16.

`gl_MaxVaryingVectors`

is the number of varying vectors, floats or matrices you can have in your vertex and fragment shaders. You’re guaranteed at least 8 and I get 32.

**Multiple Render Targets**

MRT deserves a full tutorial by itself (soon?), but to briefly summarize `gl_FragData[]`

allows you to output to up to 4 surfaces simultaneously. Especially useful with deferred rendering.

`gl_MaxDrawBuffers`

is the number of supported render targets (4 in my case).

# Precision Limits

Maybe you want to generate a super detailed fractal in your shader. Unfortunately we don’t have doubles, so we have to aware of our precision limitations.

On mobile devices, precision qualifiers make a huge difference for performance and quality. For example, here’s a typical noise function in highp vs lowp.

This is because the precision of the floats will vary from device to device. These are minimum qualities you can expect.

So in other words:

**lowp:**Float's range goes up to 2 (positive and negative) with a relative precision of 1/256.

Integers can range up to 256 (including positive and negative).

Lowp floats are adequate for colors, but may not be precise enough for other purposes.**mediump:**Float's range goes up to 16,384 with a relative precision of*1/1,024*.

Integers can range up to 1,024.

Mediump floats are usually adequate for texture coordinates and normals.**highp:**Float's range goes up to**4,611,686,018,427,387,904! with a relative precision of 1/65536.

Integers can range up to 65536.

Highp floats are best used for positions.

Technically, the precision could be higher on new hardware, but these are minimum specs.

# Conclusion

So to recap, the vertex shader can only move vertices and the fragment shader can only set colors or discard itself. When you pair the fragment shader with surfaces and buffers, you greatly expand the power of shaders!

Be careful with resolution and texture samples, especially on mobile hardware.

Working with GLSL 1.00 makes bitwise operations extremely slow and cumbersome unfortunately, but many of the other convenience functions can be recreated.

Hopefully you’ll never run into them, but there are some constants like `gl_MaxFragmentUniformVectors`

which limit how many uniforms you can have.

And finally, shader precision is only so good and it varies with different hardware.

So that just about summarizes it. I tried to be somewhat rigorous, but without covering too many niche details. Hopefully this was a good balance between detail and readability. Let me know how I did below! I’m constantly trying to refine my process.

# Extras

[Xygthop3](https://github.com/xygthop3) is a GM veteran who’s examples helped teach me shaders 10 years ago.

He’s back with updated version of his [free shaders pack](https://github.com/xygthop3/Free-Shaders/tree/main)!

[Here’s a little guide](http://www.davetech.co.uk/gamemakerdistortscreen) on creating a screen distortion effect in GM.

Here’s a good video by Gaming Engineer about building 3D games in GameMaker:

Anyway, I gotta get going now. Have a great weekend!

-Xor