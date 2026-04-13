---
title: 'Mini: ShaderToy'
url: https://mini.gmshaders.com/p/gm-shaders-mini-shadertoy-1392217
author: Xor
published: '2022-10-07'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: ShaderToy

### Understanding ShaderToy's format and porting shaders to GM

Good day, friends,

[ShaderToy](https://www.shadertoy.com) is a web platform for testing and sharing GLSL shaders more easily. Today, I want to show how these shaders can be ported to GameMaker.

First, I should mention that there is an [awesome tool](https://iarri.github.io/Shadertoy2GM/) for automatically porting ShaderToy shaders to GameMaker. This is good enough for basic shaders, but today, we'll go over the entire process so that you know how to fix any issues that may arise and become a better coder.

## Format

The first thing you may notice on ShaderToy is that there are no vertex shaders, only pixel shaders (AKA fragment shaders). ShaderToy shaders are applied to a quad with no important data, like vertex color or vertex texture coordinates, to be passed into the fragment shader.

In GM, you have some extra data to work with (including vertex color/alpha, texture coordinates, and possibly more). The default vertex shader is fine for ShaderToy shaders. In the fragment shader, you can copy the ShaderToy "Image" code over first. Next, you should add your varying vectors to the top of the shader:

```
varying vec2 v_vTexcoord;
varying vec4 v_vColour;
```



Then you have to replace the `void mainImage(...`

line with this:

`void main()`



*ShaderToy uses 'mainImage' instead of 'main' simply because internally, it has different main functions for different use cases like VR and cubemaps (using mainVR, mainCubemap). We don't need this in GM, so we use main.*

Finally, you **must **replace "fragColor" with "`gl_FragColor`

" and "fragCoord" with "`gl_FragCoord.xy`

".

Note: ShaderToy does not do alpha blending, so make sure you set the fragcolor alpha intentionally. Some shaders ignore alpha because it has no visible effect on ShaderToy.

## Uniforms

The next step is to make sure you set all the uniforms that the shader uses. On ShaderToy, you can click the little arrow by "Shader Inputs" to see all the uniforms that ShaderToy supports:

In the create event, I'll pre-define all the uniforms that the shader uses, starting with the "u_*" prefix. For example:

`u_iResolution = shader_get_uniform(SHADER_NAME, "iResolution");`



You only need to set the uniforms that the shader actually uses. Here's a quick guide on the values that the shader is expecting:

**iResolution:**

Almost every shader uses iResolution, which is the resolution of the shader canvas. For some reason, this is vec3, but the z-component is always 1.0. Some shaders use this, so make sure to include that third component.

When we're drawing with the shader, set the uniforms like so:

`shader_set_uniform_f(u_iResolution, WIDTH, HEIGHT, 1);`



Where "WIDTH" and "HEIGHT" are the dimensions of whatever we're drawing. If it's the application surface, use the surface's dimensions.

**iTime:**

This can be the time in seconds since the game. `get_timer()`

in GML, returns the time in microseconds (*1,000,000 microseconds = 1 second*).

`shader_set_uniform_f(u_iTime, get_timer() / 1000000);`



**iTimeDelta:**

This can be the time in seconds since the last frame. GM actually already has a variable for this called "delta_time" so we can just use that (*delta_time also is in microseconds*):

`shader_set_uniform_f(u_iTime, delta_time / 1000000);`



**iChannel0..3:**

****These are the extra textures that some ShaderToy shaders use:

If the shader only uses one texture, you could replace it with "`gm_BaseTexture`

" which could save some work.

Otherwise, these can be initialized as uniform samplers along with their respective settings:

```
u_iChannel0 = shader_get_sampler_index(SHADER_NAME, "iChannel0");
gpu_set_tex_filter_ext(u_iChannel0, true);
gpu_set_tex_repeat_ext(u_iChannel0, true);
gpu_set_tex_mip_filter_ext(u_iChannel0, false);
```



I like to use the "t_*" prefix for my texture variables:

`t_iChannel0 = sprite_get_texture(spr_texture0, 0);`



ShaderToy shaders expect every texture to be on a separate texture page, so if you haven't done that, you need to [follow my last tutorial](https://www.getrevue.co/profile/xordev/issues/gm-shaders-mini-two-textures-1376349).

Note: GM Only supports 2D textures, so you will have to find substitutes for 3D textures or other texture formats.

**iChannelResolution[]:**

This is an array of the resolutions of the textures for iChannel0 to iChannel3. You can initialize an array of the resolutions like so:

```
iChannelResolution[0] = texture_get_width(t_iChannel0);
iChannelResolution[1] = texture_get_height(t_iChannel0);
iChannelResolution[2] = 1;
...
```



And when it's time to draw:

`shader_set_uniform_f_array(u_iChannelResolution, iChannelResolution);`



**iMouse**:

It is a vec4 with the xy components containing the current mouse xy position and the zw components containing the last pressed position (*negative when the mouse is released*).

For most shaders, just the x and y will do:

`shader_set_uniform_f(u_iMouse, window_mouse_get_x(), window_mouse_get_y(), 0, 0);`



If the shader uses z or w, though, you'll need a GML variable for the last pressed mouse position. Something like:

```
if (mouse_check_button_pressed(mb_left))
{
press_x = window_mouse_get_x();
press_y = window_mouse_get_y();
}
var _sign = mouse_check_button(mb_left)*2 - 1;
shader_set_uniform_f(u_iMouse, window_mouse_get_y(), _sign*press_x, _sign*press_y);
```



**iFrame**:

Simply the number of frames since the shader started. It can be done with a local "frames" variable like so:

`shader_set_uniform_f(u_iFrame, frames++);`



The other uniforms are rarely used, so I won't cover them here. The basic descriptions are in the "Shader Inputs" tab on ShaderToy.

## Substitutions

ShaderToy moved to WebGL 2.0 while GM is still on the equivalent of WebGL 1.0. That means some things have to be changed for compatibility.

The most obvious change is to replace all instances of "`texture`

" with "`texture2D`

"

GM does **NOT** support bitwise operations (&, |, ^, <<, >>, %), switch statements, dynamic arrays (*you'll have to predefine the size*), non-square matrices (e.g. mat2x4), and lacks some math/matrix functions.

If you come across `round(x)`

you can replace it with `floor(x+0.5)`

.

## Buffer Tabs

If you see multiple tabs at the top of the shader, that effect is composed of multiple separate shaders. Each "Buffer" tab is a separate shader. If not, you can skip this section!

These can be a bit more time-consuming to port, but often produce the most impressive results. The output of each pass can then be used as a texture in the next shader.

In GM, each buffer should be drawn to a surface so that it can be used in the next shader. On ShaderToy, these buffer textures are stored as floating-point textures instead of 8-bit ints like in GM. This means on ShaderToy, you can output a color outside of the 0 to 1 range, while in GM, you can't!

**So, make sure these buffer outputs range from 0 to 1 before attempting to port this!**

The Common tab is just code shared across all the shaders. In GM, you can just copy-paste that code on top of each buffer shader.

## Licenses and Attributions

Please make sure to credit the original author every time you use someone's code, even for personal projects! You never know when this information could come in handy if you forget how something works.

If there is a license on top of the shader, you **MUST **include it in your shader and make sure to read all the conditions of the license.

If you are releasing the shader in a commercial game or open-source resource, please contact the original author first and get their permission before doing so. It's not nice to steal code (or sometimes even the ideas)!

Who knows, maybe this could save you some legal headaches down the line!

## Conclusion

ShaderToy is an excellent resource for learning about code or quickly prototyping ideas. Understanding how shaders work in a game setting can unlock many new possibilities, and it's way more fun, too. I've learned so much from working on hundreds of different shaders for a variety of games.

Hopefully, by this point, you'll have felt like you unlocked a new superpower and can use it responsibly to make better games!

If you found this useful, please consider supporting my work on [Ko-fi](https://ko-fi.com/xor). Thanks!