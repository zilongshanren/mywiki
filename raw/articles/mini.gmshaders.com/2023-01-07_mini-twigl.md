---
title: 'Mini: Twigl'
url: https://mini.gmshaders.com/p/gm-shaders-mini-twigl
author: Xor
published: '2023-01-07'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Twigl

### Porting tweet shaders to GameMaker

Howdy folks,

First off, hello from Substack! As mentioned in the last email, Revue, my previous newsletter host, is shutting down, so I’ve made a move to Substack. Now you can leave comments below on these articles! Feel free to ask questions or just say hi.

## What is Twigl?

[Twigl.app](https://twigl.app) is an [open-source](https://github.com/doxas/twigl) mini shader editor. A bit like a minimal ShaderToy, specifically for those tiny shaders that fit in a tweet (280 characters). If you’re following me on [Twitter](https://twitter.com/XorDev), you’ve probably seen some of these shaders. It’s crazy what can be done in just 280 chars.

## Twigl Formats

Twigl has a few different regulation options, which can change the shader formats a bit:

I typically use “geekest (300 es)” because it allows for the most compact shaders, but I occasionally use geekest MRT as well.

In classic, you have to define every uniform, float precision, and the main function, while geekest handles that internally:

I’ll focus on geekest (300 es) because it’s the hardest to understand, but the most powerful. Classic is quite similar to ShaderToy. In geekest mode, you don’t need to worry about the main function, just set the output color, and twigl handles the rest.

As you can probably guess, the “300 es” indicates OpenGL ES 3.0, which is a newer shader version (where you don’t need to use gl_FragColor).

## Variables and functions

Here are the uniform variables that twigl supports:

**t**: a float for the time elapsed in seconds.**r**: the vec2 resolution of the shader window in pixels.**m**: normalized vec2 mouse coordinates, ranging from 0 to 1. Multiply by “r” to get the pixel coordinates**b**: a sampler2D “backbuffer” texture from the last frame.**f**: a float frame counter starting at 0, 1, 2…**o**: fragment/output color.FC: fragment or pixel coordinates relative to the screen.


And if you’re in MRT mode, you get **o0**, **o1**, **b0**, and **b1** for separate buffers.

Twigl also adds some common functions that you’ll need to add to your ported shaders manually. You can just copy and paste [the function’s source code](https://github.com/doxas/twigl/blob/master/src/shader_snippet/noise.glsl) into your shaders.

**Note:** Please make sure to respect the MIT license for this code! MIT license is super flexible for private or commercial projects. Just make sure to include it if you intend to release it.

In case you’re curious, here’s what the most common functions do:

**snoise2D,snoise3D,snoise4D**: 2D, 3D, and 4D implementations of Simplex noise. This is similar to Perlin noise but designed to be faster in higher dimensions (I have my doubts about it in 2D or 3D).**fsnoise**: a classic white noise hash function.**hsv**: computes an RGB vec3 from a hue, saturation, and value (all ranging from 0 to 1).**rotate2D,rotate3D**: Returns 2D and 3D rotation matrices using a rotation angle argument. In 3D, you also need to specify the axis of rotation as the second argument.

Hope that helped demystify some of the code! This is partly why ShaderToy versions of twigl shaders are often longer.

## GML Uniforms

Let’s set up our uniforms so we can use these variables in GameMaker! Thankfully, they are all quite intuitive, so it should be easy to follow along here:

```
//Initialize shader uniforms (Create Event)
u_time = shader_get_uniform(SHADER_NAME, "u_time");
u_res = shader_get_uniform(SHADER_NAME, "u_res");
u_mouse = shader_get_uniform(SHADER_NAME, "u_mouse");
//Setting the shader uniforms (Draw Event)
//Get resolution and mouse (normalized) coordinates
var _ww,_wh,_mx,_my;
_ww = window_get_width();
_wh = window_get_height();
_mx = window_mouse_get_x() / _ww;
_my = window_mouse_get_y() / _wh;
//Apply the shader
shader_set(SHADER_NAME);
//Set the uniforms
shader_set_uniform_f(u_time , get_timer()/1000000);
shader_set_uniform_f(u_res , _ww, _wh);
shader_set_uniform_f(u_time , _mx, _my);
//Draw the things here
shader_reset();
```


In this case, we don’t need the mouse coordinates, so we can remove that part!

**Note**: if you’re using backbuffers or MRT, you’ll need to set up a surface and sampler texture. I’d recommend reading my [Recursive Shaders tutorial](https://xordev.substack.com/p/gm-shaders-mini-recursive-shaders-1308459) first!

## Shader Porting

Let’s try porting this shader:

```
vec3 d=vec3(FC.xy*2.-r,r)/r.x,p;
for(float i,s;i++<2e2;p+=d*(p.y+.2-.2*snoise2D((p.xz*.6+t*.2)*s))/s)
s=exp(mod(i,5.));
o.grb=.5*d+.03*++d/length(d.xy-1.3)-.7/++p.z-min(.2+p+p,0.).y;
```


**Step 1, Reformat**: We need to put this code in a main function and replace “o” with “gl_FragColor” and “FC” with “gl_FragCoord”.

```
void main()
{
vec3 d = vec3(gl_FragCoord.xy*2.-r,r)/r.x,
p = vec3(0);
for(float i = 0.0, s = 0.0; i++<2e2; p += d*(p.y+.2 - .2 * snoise2D((p.xz*.6+t*.2)*s))/s)
s = exp(mod(i,5.));
gl_FragColor.grb=.5*d+.03*++d/length(d.xy-1.3)-.7/++p.z-min(.2+p+p,0.).y;
}
```



While you’re at it, make sure every variable is properly initialized!

**Step 2, Twigl functions**: Here, we just need to copy the snoise2D function and the functions it uses. To make matters simple, we’ll just copy the twigl whole code, but you’re welcome to clean up the unused functions and variables if you like!

**Step 3, Uniforms**: We’ll add the required uniforms: “r” and “t”. We’re not worried about size constraints in GameMaker, so I’m gonna give them a more descriptive name:

```
/*
snoise2D code goes here
*/
uniform vec2 u_res; //Room or window resolution in pixels
uniform float u_time; //Time in seconds
void main()
{
vec3 d = vec3(gl_FragCoord.xy*2.-u_res,u_res)/u_res.x,
p = vec3(0);
for(float i = 0.0, s = 0.0 ; i++<2e2; p += d*(p.y+.2 - .2 * snoise2D((p.xz*.6+u_time*.2)*s))/s)
s = exp(mod(i,5.));
gl_FragColor.grb=.5*d+.03*++d/length(d.xy-1.3)-.7/++p.z-min(.2+p+p,0.).y;
}
```



**Step 4, Fixes (optional):** And finally, there are a few issues that you might run into:

**Flipped Image**: GameMaker’s frag coordinates start at 0,0 with the top-right, while twigl and ShaderToy start in the bottom-right. This means you’ll have to flip the coordinates like so: ‘`flipped_y = res.y-y;’`

or our case, we can just do ‘`d.y = -d.y;’`

**Blank or Holey**: twigl doesn’t care about the alpha channel, but GameMaker does! Just set the alpha to 1 at the end of your shader like so: ‘`gl_FragColor.a = 1.0;’`

**Black or White Spots**: Check for code that could lead to undefined values. Division by zero, undefined variables,`sqrt()`

or`pow()`

on negative numbers. It’s wise to look for these in any shader, as it may work on your hardware, but not elsewhere.

And we’re done! This particular shader should look something like this!

Not bad for a shader that can fit in a tweet!

## Shaders to try

Want to try more shaders? Well, I’ve posted dozens of shaders like these on my Twitter:

Check out this thread to see some of my personal favorites! All of these are free to use in any projects (*just don’t sue me if your computer burns down or something!). I would love to see some of these shaders put to good use in your games and projects! Feel free to tag me if you do!

You can also search “#つぶやきGLSL” for some amazing works by the talented coders of the internet. But please, if you use someone else’s code, ask for their permission first! It’s the right thing to do.

Thanks! Anyway, that’s all for this week. Have a great weekend!

-Xor

Hi Xor! Thanks for bringing attention to twigl.app, I like it too! BTW, you can also use `f` uniform in geekest mode to access a frame number