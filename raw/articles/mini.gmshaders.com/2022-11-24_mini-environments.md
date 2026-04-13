---
title: 'Mini: Environments'
url: https://mini.gmshaders.com/p/gm-shaders-mini-environments-1475397
author: Xor
published: '2022-11-24'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Environments

### How to use HDRI textures in GM

Hi people!

Today, let's talk about environment mapping! It's actually surprisingly simple to set up. Let's explore how to use it.

## What Is An Environment Map?

An environment map is a panorama texture that gives a complete 360-degree view of the surrounding environment. GameMaker doesn't support cubemaps for environments, but that's okay. We can use equirectangular or HDRI textures as a common alternative:

*Fun fact: This is the same projection used on most world maps (only external instead of internal)!*

These can be used to texture skyboxes, for reflections, and much more.

## Texture Coordinates

In order to use these, we need to convert a vec3 direction vector to vec2 texture coordinates. It's important to understand how these textures are formatted. The texture's x-coordinate represents the horizontal direction (yaw) from 0 to 360 degrees. And the y-coordinate represents the pitch from -90 to 90 degrees. *For trig fans, this is just the spherical polar coordinates!*

We can calculate this yaw-direction like so:

`float `

`yaw = `

`atan`

`(direction.y, direction.x);`



**Note**: `atan`

`(y,x)`

* is short for arctangent, or in other words, it computes the direction of our vector (in radians). It's very similar to *`point_direction(0,0,x,y)`

* or *

`arctan2`

`(y,x)`

*in GML. If you want to learn more, I wrote about*

[it in detail here](https://gmshaders.com/glossary/?load=atan)!Now we can compute the pitch direction:

`float `

`pitch = `

`asin`

`(`

`clamp`

`(direction.z, -1.0, 1.0));`



So `asin`

`(x)`

is just the inverse of sine. It takes the ratio of the opposite side and the hypotenuse and returns the angle (in radians).

Now, to use these coordinates, we need to map them to the 0-1 range. Since we're using radians, `atan`

ranges from -pi to +p,i and `asin `

from -pi/2 to pi/2. Just some simple math to normalize them:

`#define `

```
PI 3.1415926
```

`vec2 `

`sphere_uv = `

`vec2`

`(yaw/PI*0.5+0.5, pitch/PI+0.5);`



You can use these UV coordinates to sample your texture!

## Skybox and Reflections!

For starters, this can be used to texture your skybox in a shader. Just compute the direction from the camera to the skybox like so:

`vec3 `

`direction = `

`normalize`

`(v_world_pos.xyz - u_camera);`



Here we're using the world-space coordinate from the vertex shader:

`v_world_pos = gm_Matrices[MATRIX_WORLD] * vec4(in_Position, 1.0);`



**Note:** *The world space parts are optional. They're just for when you rotate, scale or translate a model using the world matrix!*

And `u_camera `

which should be a uniform 3D camera's position.

This direction can then be converted to texture coordinates and used to sample the sky texture!

If you want to do reflective objects, copy the skybox shader, but add this:

`vec3 `

`ref_direction = `

`reflect`

`(direction, v_world_normal);`



This uses our view direction to reflect off of world-space normals.

I compute my world-space normals like this (vertex shader):

`v_world_normal= `

`normalize`

`((gm_Matrices[MATRIX_WORLD] * `

`vec4`

`(in_Normal, 0.0)).xyz);`



Let's test it on a sphere! Looks beautiful

You can also try refracting or sampling for directional lighting using environment textures! I'll leave those experiments up to you to try.

I've put together a little example on [ShaderToy ](https://www.shadertoy.com/view/cdsXzf)with all the code we've covered so far!

## How to Find Them

So you may be wondering how you can get a texture like this? Well, my favorite place is [PolyHaven HDRI](https://polyhaven.com/hdris). PolyHaven has tons of high-quality textures that are free to use even in commercial projects (licensed under CC0). They include HDR data, which GM doesn't currently support, but you can convert them to PNGs using a photo editor like GIMP.

Or you can search Google for "environment maps", "reflection maps", or "HDRI". Just make sure you have permission to use them if you plan on releasing anything with them!

## Conclusion

By now, you have a new tool at your disposal! I've used this just recently in jam game called Haven:

There are a lot of effects going on here, but one of the greatest additions was the subtle reflections on the blocks. I hope you can find some cool uses for this technique in your own games (maybe even in 2D?).

Anyway, Happy Thanksgiving to all who celebrate it, and thanks for reading.

Have a great night!