---
title: 'GM Shaders: MRT'
url: https://mini.gmshaders.com/p/mrt
author: Xor
published: '2024-01-06'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# MRT

### How to output to multiple surfaces simultaneously (Multiple Render Targets)

Hello there,

Happy New Year! Hope you had a great 2023, and I hope you have an even better 2024! Let’s start the year off by looking at Multiple Render Target (“MRT”) output.

It’s so simple, I can explain it in a single sentence:

By using `gl_FragData[0-3]`

instead of `gl_FragColor`

, you can actually output 4 separate fragment colors to up to 4 surfaces with one draw call!

That’s the gist of it, but let’s go over the setup, use-cases, and potential issues that can occur.

# Setup

For testing, create a shader and replace the gl_FragColor with this:

```
//Output 0 (red)
gl_FragData[0] = vec4(1,0,0,1);
//Output 1 (green)
gl_FragData[1] = vec4(0,1,0,1);
//Output 2 (blue)
gl_FragData[2] = vec4(0,0,1,1);
//Output 0 (white)
gl_FragData[3] = vec4(1,1,1,1);
```


This will output all red to the first surface, all green to the second, all blue to the third and white to the fourth. We can set each fragment output independently to any values, but for testing solid colors will do.

Now, when we draw with the shader, we can assign the surfaces using [surface_set_target_ext()](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Drawing/Surfaces/surface_set_target_ext.htm).

The first argument is the index number 0 to 3 and corresponds to the gl_FragData index. The second argument is the surface you’re assigning it to. Apply the shader should look something like this:

```
shader_set(shd_mrt);
surface_set_target_ext(0, surf0);
surface_set_target_ext(1, surf1);
surface_set_target_ext(2, surf2);
surface_set_target_ext(3, surf3);
draw_self();
surface_reset_target();
shader_reset();
```


I drew the 4 surfaces in each quadrant of the screen, and you can see the correct results:

I’ve put together a little demo project on [GitHub](https://github.com/XorDev/GM_MRT). You might be wondering how this can be used in games, and I was going to do a full normal mapping demo using this, but it went beyond the scope of this tutorial and my schedule. Perhaps this should be a future tutorial? Let’s look at some other applications where multiple outputs may be useful.

# Applications

Probably the most common usage for MRTs is for [deferred rendering](https://learnopengl.com/Advanced-Lighting/Deferred-Shading).

In deferred rendering, you store the normals, albedo/diffuse color and sometimes positions, specularity, roughness, metallic or emissive properties on separate surfaces. Then, when you need to draw a light, you sample these textures to use that data to compute the lighting. This has the benefit of allowing you to draw the geometry once and adding as many lights as you need one at a time. This works in 2D or 3D contexts and is greatly expandable. More details in the link above if you want to learn more.

### Object ID

For my idle game, [Constructor](https://gx.games/games/qrcxnd/constructor/), I had each object output a unique “ID” color to a separate ID surface. Then I had an outline shader which added outlines around the edges of any highlighted objects. See the center house below:

So the first object had an id color of `vec3(1,0,0) / 255.0`

, the second `vec3(2,0,0) / 255.0`

and so, each with their own unique color. Then, the outline shader can highlight and outline the desired ID. All this works in 2D or 3D with only drawing each object once!

### Depth Maps

Having depth information is crucial to many 3D effects (SSAO or shadow mapping just to name a couple). GM doesn’t yet give us access to the depth buffer, but we can always create one ourselves using the new surface formats and a second fragment output.

Basically, MRTs are useful anytime you need to store extra data beyond just a color output. They can be super useful in effects with multiple different stages, and they may save you from having to draw things multiple times. I should warn you about a couple of issues you may encounter, though.

# Concerns

Firstly, they aren’t compatible with all platforms. HTML5 outright does not support MRTs. Low-end devices will definitely struggle with MRTs and in some cases it might even be faster to do separate draw calls with separate shaders.

As I mentioned earlier, you are limited to 1 to 4 MRT outputs. Most of the time that is enough, but it’s a limitation to be aware of.

Remember, having lots of surfaces will require more VRAM (video memory). In 2D games, you can probably use `surface_depth_disable(true)`

to cut your surface VRAM usage about in half. But still, if you have a bunch of full HD surfaces on a lower-end device, it’s going to take a hit.

Surface formats are important too when it comes to VRAM usage. Don’t use `surface_rgba32float`

unless you absolutely have to. If you only need one color channel, `surface_r8unorm `

is one-quarter of the normal surface size!

Also, remember that you can only control the fragment outputs independently, so all the fragments must share the same vertices and camera view. If you `discard`

one fragment, you discard them all.

Please make sure your target hardware will run your game as early as possible. MRTs are best used on mid to high-end desktops and high-end consoles. Testing early will save you a ton of headache later!

# Conclusion

Multiple Render Targets are a great tool for making more advanced shader effects more efficient, especially when you have to draw a lot of objects. MRTs allow you to write color data to up to for different surfaces at the same time, which is perfect for applications like normal mapping. Sometimes you need a color output and additional outputs like normals, depth, object ID, etc. and there’s no better way than by using MRTs.

However, with this power comes great responsibility to manage your video memory carefully. You don’t want to have more surfaces than you need or more data than you need. Sometimes you can reduce the VRAM usage by reducing surface resolutions or changing surface formats.

That’s it for today’s topic, but in case that’s not enough, here are some extra great resources to consider checking out!

# Extras

["Low-level thinking in high level shading languages"](https://interplayoflight.wordpress.com/2023/12/29/low-level-thinking-in-high-level-shading-languages-2023/) by Kostas Anagnostou is well worth a read. There are lots of small optimizations that can be made when you understand what modern compilers do with high-level languages like GLSL.

[Eclipse Light Engine](https://badwrong.itch.io/eclipse-light-engine) is a powerful 2D lighting system which uses MRTs to render efficiently. It’s $16 at the time of writing, and well worth it for anyone who doesn’t want to create their own lighting systems from scratch. (No, I wasn’t sponsored, I just think it’s neat to see this sort of thing for GM users).

Also, FoxyOfJungle released a [2D water reflection shader](https://foxyofjungle.itch.io/water-reflective) which is currently on sale for $7. It’s a sweet effect that can be thrown into most projects in a pinch.


That’s it for now. Thanks again for reading and I wish you a great weekend!

Bye!

-Xor