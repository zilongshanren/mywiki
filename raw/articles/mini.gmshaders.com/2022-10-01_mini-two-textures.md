---
title: 'Mini: Two Textures'
url: https://mini.gmshaders.com/p/gm-shaders-mini-two-textures-1376349
author: Xor
published: '2022-10-01'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Two Textures

### How to sample two textures together (with texture pages)

Hi folks,

Today we're gonna talk about texture pages and how to deal with them in shaders. I've written about [texture pages before](https://gmshaders.com/tutorials/gamemaker/), however, this will be a more complete and specific guide.

## What Are Texture Pages?

Texture pages are how GameMaker stores your sprites, fonts, tiles, and other textures on a single texture sheet. Here's a real example from my GM Shaders project:

Here you can see that when we draw sprites in a room (like the chair on the right), it is actually pulling from a page of textures (like shown on the left).

Texture pages are typically 2048x2048, but it depends on the number/size of sprites and can be configured for each platform. In any case, the texture page is always a power-of-two size (...128, 256, 512, etc).

You may have noticed the stretched pixels at the borders of each sprite. This is so that if you have texture interpolation enabled, it doesn't blend into other nearby sprites.

GM lets you control how texture pages are formed. You can put a sprite on its own texture page using the "Separate Texture Page" box, or you can group textures together using texture groups:

**Note:** if you put a sprite on a separate texture page, GM will not clip the empty space around sprites and will even add padding to make the sprite a power-of-2 size. This option will be useful to understand later.

## What Are UVs?

UVs are the x and y coordinates of a texture and this is what the "v_vTexcoord" varying vector is for. So (0,0) is the top-left of a texture and (1,1) is the bottom-right. Here's what it looks like on the same texture page:

So you can see why the chair coordinates have a smaller range than 0 to 1. If I were to guess, something like (0.4, 0.2) to (0.7, 0.6).

If you put the chair sprite on a separate texture page though, the texture coordinates, then you'll have the full 0-1 range which can be helpful for effects that use gradients. For example, a wind or wave shader that uses the texture coordinates to determine wave intensity (0 effect at the bottom, full effect at the top). It can also be used for [calculating pixel coordinates](https://www.getrevue.co/profile/xordev/issues/gm-shaders-mini-texels-and-pixels-1308242).

The problem with using separate texture pages is that it can be cumbersome to set up, negatively affects performance (because we have to swap through more texture pages), and turns all sprites to power-of-2 sizes, which can mess with our coordinate range.

There is a better way! By "normalizing" our texture coordinates for any sprite.

## Normalized Coordinates

Normalizing in this context simply means we convert the sprite UV range to a 0-1 range for any sprite.

To do this, we need to pass in the sprite UVs to our shader via uniform:

`uniform`

` `

`vec4`

```
sprite_uvs; //uvs [x, y, w, h]
//Use sprite_get_uvs() to get the coordinates of the top-left and bottom-right corners:
//Example: var uvs = sprite_get_uvs(sprite_index, image_index);
//You can get the texture coordinate range as the difference between them:
//Example: shader_set_uniform_f(uni_uvs, uvs[0], uvs[1], uvs[2]-uvs[0], uvs[3]-uvs[1]);
```



Now with this one uniform, we can convert our texture coordinates to a 0 - 1 range. Here's my conversion function:

`vec2`

` texcoord_normalize(`

`vec2`

` coord, `

```
vec4 uvs)
{
```

```
return (coord-uvs.xy)/uvs.zw;
}
```



We can use these normalized texture coordinates for whatever we need. For this example, let's just flip the texture coordinates:

`vec2 flip_coords = 1.0 - texcoord_normalize(v_vTexcoord, sprite_uvs);`



Then we'll have to convert this back to the original range. We can use this:

`vec2`

` texcoord_unnormalize(`

`vec2`

` coord, `

```
vec4 uvs)
{
return
```

```
coord*uvs.zw + uvs.xy;
}
```



Now let's complete our example:

```
vec2 new_coord = texcoord_unnormalize(flip_coords, sprite_uvs);
vec4 color = texture2D(gm_BaseTexture, new_coord);
```



## Multiple Samplers

Let's solve one more problem! Suppose we want to map two textures together (perhaps for masking, bumpmapping, normal mapping, texture splatting, etc).

If these textures are on texture pages, they will probably be in different places on the texture page, so we'll need to convert from one sampler's range to the other's range.

Here's an example where we want to blend a diffuse texture with an ambient occlusion texture:

Thankfully, we don't need anything new to solve this. We can just normalize the first texture's coordinates like so:

`vec2 norm_coord = texcoord_normalize(v_vTexcoord, diffuse_uvs);`



And then “unnormalize” it using the second texture's UVs.

`vec2 ao_coord = texture_unnormalize(norm_coord, ao_uvs);`



Now we can sample the second texture and do whatever we need with it!

## Conclusion

If you need to manipulate texture coordinates in any way, it's important to understand how they work. This explains what the purpose of "separate texture pages" is and the other way to handle texture coordinates.

Knowing how to map two or more textures over the same coordinates is crucial for more advanced effects like normal mapping.

Hope you learned something interesting. Thanks for reading!