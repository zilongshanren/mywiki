---
title: 'GM Shaders Mini: Blendmodes'
url: https://mini.gmshaders.com/p/mini-blendmodes
author: Xor
published: '2023-02-11'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Blendmodes

### Recreating photoshop blendmodes with shaders

Hey friends,

Today I want to cover some photoshop blendmodes and how to recreate them using shaders. Blend modes are a great way to enrich your games graphically and can be used for lighting, shading, fog, and more.

If you’re unfamiliar with blendmodes in GameMaker, I’d recommend starting [here](https://gamemaker.io/en/blog/explaining-blend-modes-part-1).

These blendmodes are neat, but sometimes you need a few more options.

Here’s a neat one from Photoshop:

In order to recreate this, you’ll need to use shaders.

## Setup

So to use a blendmode, you need to know the two colors that are being blended.

**Source/target** = what you’re drawing on top

**Destination/blend** = what is already there (under the source)

In the shader, we’ll have to use two separate textures. The source can just be `gm_BaseTexture`

, but we’ll need a uniform `sampler2D`

for the destination.

For simplicity, I’m gonna use the application_surface for the destination and apply my blendmode shader in the Draw GUI event.

Here’s a neat trick for computing the screen uv coordinates in the vertex shader using gl_Position.

```
//0 to 1 uv coordinates relative to the screen
v_screen = gl_Position.xy*0.5 + 0.5;
```


You can pass this as a varying vec2 to the frag shader which is used for sampling the destination texture.

In the frag shader, you’ll want something like:

```
//Sample the source and destination textures
vec4 src = texture2D(gm_BaseTexture, v_coord);
vec4 dst = texture2D(u_destination, v_screen);
//Here's an additive blendmode for example:
gl_FragColor = src + dst;
```


## Photoshop

Rogelio Bernal Andreo recreated the formulas for common photoshop blendmodes, making these blendmodes easy to replicate!

I’ll do a couple of examples to show how this could look in GLSL:

```
//Darken blendmode
vec4 darken = min(src, dst);
//Screen blendmode
vec4 screen = 1.0 - (1.0-src)*(1.0-dst);
//Soft Light blendmode (reduced)
vec4 screen = mix(2.0*src*dst, 1.0-(2.0-2.0*src) * (1.0-dst), step(0.5,src));
```


Here I used mix and [step](https://gmshaders.com/glossary/?load=step) for the conditionals, but you could do if statements for each component if you prefer.

Note: these blendmodes are applied to the alpha channels as well! Sometimes this isn’t desired, so make sure to set the alpha as you intended.

EDIT: [Here’s another set of blendmodes](https://github.com/jamieowen/glsl-blend) already converted to GLSL under the MIT license.

## Conclusion

That’s all for tonight! Now you can bookmark this page for any time you need a specific blendmode or you can even try making your own! I hope this saves you some time and headaches!

I’m going to take a break from writing tuts for the next couple of weeks so I can spend some time with family. Until then, I’m letting my paid subscribers help pick the next tutorial topics!