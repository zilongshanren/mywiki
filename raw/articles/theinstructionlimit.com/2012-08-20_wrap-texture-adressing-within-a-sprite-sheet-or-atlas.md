---
title: Wrap texture adressing within a sprite sheet or atlas
url: https://theinstructionlimit.com/wrap-spritesheet-atlas
author: Author Renaud Bédard
published: '2012-08-20'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

[FEZ](http://fezgame.com) shipped with volume textures (aka 3D textures) for all the sprite animations in the game. Gomez, NPCs and other animated pixel art were all done using those. This was a tech call that I made way back in 2008 and kept with it because it makes more sense than you might think :

- No need to do texture packing and keeping track of where frames are in the sheet; a volume texture is an ordered list of 3D textures, every frame is a slice!
- The pixel shader just does a
`tex3D()`

call with the Z component of the texture coordinates being the step of the animation between 0 and 1. - Cool side-effect : hardware linear interpolation between animation frames! This wasn’t very useful for me (except for one thing, water caustic overlays), but it’s a nice bonus.
- Mip-mapping with 3D textures is problematic because it downsizes in X, Y and Z, meaning that each mip level halves the number of frames. However, I didn’t need mip mapping at all (for sprites), I never undersample pixel art.
- Same limitation when making a volume texture power-of-two, it also goes power-of-two in the Z axis which means a lot of blank frames, which is wasteful but not a huge problem to deal with.

But while I haven’t done real testing, one can assume that they’re slower than a regular 2D sprite sheet, and they imply that you have one texture by animation, which restricts how much you can pack things together. Creating a volume texture at load-time with XNA `Texture2D.SetData()`

calls means one call per animation frame, which is noticeably slow. Also, volume textures are not currently supported by [MonoGame](http://monogame.codeplex.com/), and I assume some integrated graphics hardware would have trouble dealing with them.

So the more traditional alternative is using a sprite sheet, which is easy to make using tools like the [Sprite Sheet Packer](http://spritesheetpacker.codeplex.com/).

But then what if you need to use wrap texture addressing on it, to have horizontally and/or vertically repeating textures?

If you only repeat on one axis, have relatively small textures and a small number of frames, you can force the texture packer to layout the sprites on a single row or column, which allows wrapping on the other axis.

This worked for some animations, but some were just too big or had too many frames to fit it in under 4096 pixels. In that case, there’s one final option : pixel shaders to the rescue!

When addressing the texture in your shader, you’re likely to use a 3×3 texture matrix, or a 4D vector if you’re short on input parameters. Either way, you have four components : UV offset and UV scale. You can use those to manually wrap the texture coordinates on a per-pixel basis. In the sample below, I extract the data from a texture matrix.

**Vertex Shader**

Out.TextureCoordinates = mul(float3(In.TextureCoordinates, 1), Matrices_Texture).xy; Out.UVMinimum = Matrices_Texture[2].xy; Out.UVScale = float2(Matrices_Texture[0][0], Matrices_Texture[1][1]);

**Pixel Shader**

float2 tc = In.TextureCoordinates; tc = frac((tc - In.UVMinimum) / In.UVScale) * In.UVScale + In.UVMinimum; float4 sample = tex2D(AnimatedSampler, tc);

The `frac()`

HLSL intrinsic retains the decimal part of its input, which gives the normalized portion of the texture that the coordinates are supposed to show. Then I remap that to the sprite’s area in the atlas, and sample using those.

I ended up only needing wrapping on one axis for that big texture/animation, but this code does both just in case. This is WAY simpler than customizing the vertex texture coordinates to allow wrapping.

One caveat though, this won’t play well with linear filtering. Since FEZ is pixel art, I could get away with point sampling and had no artifacts there.

P.S. A simple fix to enable usage of linear filtering : pad the sprites with 1 pixel column and rows of the opposite side of the texture! (and don’t include those in the sampled area; it only gets sampled by the interpolator)

Now that fish canceled the fez 2 game, ask him to do good to the indie world and release the trixel engine as an opensource project so we can all contribute to create a legacy with your ideas

You can fix the linear filtering issue by placing a single border of pixels around the tile in the atlas, where the pixels are copied from the opposite side of the tile.

Yep, see the “P.S.” at the bottom of the post. :)

Would you mind explaining in greater detail each steps so that it can be understood by someone that have no experience with HLSL? I have been trying to reproduce this effect for a simple shader that will allow tiling sprites with little success regardless of the amount of documentation I read on the subject.

You can see what I achieved so far over stackexchange :

https://gamedev.stackexchange.com/questions/165514/texture-atlas-and-hlsl-shader-for-sprite-tiling

If you have any tips when creating shaders, it would also probably be great. I just found out about FX Composer 2.5, this has been great but there’s still seem to be a lots of things that I might be missing. Also it doesn’t seem like a shader that works in FX Composer 2.5 necessarily work with XNA.