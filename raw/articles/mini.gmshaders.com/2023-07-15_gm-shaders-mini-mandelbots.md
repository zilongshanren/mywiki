---
title: 'GM Shaders Mini: MandelBots'
url: https://mini.gmshaders.com/p/gm-shaders-mini-mandelbots
author: Xor
published: '2023-07-15'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: MandelBots

### A technical overview of raymarched, fractal game

Hi folks!


You may have noticed I’ve been gone for a little while. I haven’t forgotten you, but I have been quite busy working on an experimental game concept I had.

If you’ve been [following me on Twitter](https://twitter.com/XorDev/status/1671018259707985920), you probably know what I’m talking about, but in case you haven’t, I’ll summarize it briefly here.

I set out to make a First Person Shooter game in 10 days because I had a few ideas I wanted to try out (experimenting in a new genre for me, with infinite fractal worlds and procedurally-generated weapons).

I ended up spending a little over 10 days, and while it is still somewhat buggy, I’m quite happy with the results and particularly the lighting system. Here’s a screenshot for context:

Today I want to share some of the technical details I learned along the way!

## Technical Overview

For the first few hours, I experimented with vertex buffers, trying to generate fractals by starting with a plane mesh and subtracting cubes. This ended up being too complicated to solve in a timely manner and I decided to stick with what I know. I already knew how to generate [interesting fractals](https://www.shadertoy.com/view/cdG3Wd) using SDFs so I went with **raymarching **for rendering the buildings.

## Raymarching

I wrote about raymarching here if you want to learn more:

I was a bit worried about how I’d handle collisions but to my surprise, porting the GLSL SDF function to GML was easy, fast, and accurate. Fast enough that I could raymarch multiple times per frame in GML. This is useful for computing projectile collisions. For the player collisions, I sampled the distance field 6 times to compute the slope along each axis (x,y, and z), and from there, it’s as simple as shifting the player away from the slope when it gets too close!

## Deferred Rendering

Have you seen “Gbuffers” (geometry buffers) used in games sometimes? They are sometimes used in 3D games to reduce the lighting workload or for effects like SSAO. So instead of the shader having to loop through all the lights at once (which can get quite costly), they can be rendered onto a lighting surface, 1 at a time without strict limits!

Here’s what mine looks like:

In my case with split-screen multiplayer, it can actually render lights for all screens at once because all the necessary data is there! (I used world space coordinates so that all screens are in the same coordinate space).

Color and normals were regular 8-bit surfaces, but the world space was a 32-bit float and the lighting was a 16-bit float. This allows for proper HDR lighting. More on that later.

## Soft Shading and AO

I’m hoping you noticed the cool shading. This was achieved in two parts: shadow pass and ambient occlusion pass.

Shadows are done by sampling the distance field at a few points toward the light. The ratio of the sampled distance to the expected distance tells us roughly how occluded the sample is. Here’s how it looks with some dithering to smooth it out.

My code looked something like this:

```
float shadow(vec3 pos, vec3 dir, float start, float end)
{
float light = 1.0;
float iterations = 0.0;
for(float scale = start*(1.0+0.4*dither); scale<end; scale*=1.4)
{
light *= clamp(dist(pos+dir*scale)/scale*2.0, 0.002, 1.0);
iterations++;
}
return pow(light, 2.0/iterations);
}
```



Ambient occlusion follows the same principle, but instead of sampling toward the light, it samples along the surface normal. This pass only uses two samples!

## Line lights

One of the effects I’m quite proud of is the line lights used for projectiles and lasers.

For this, I computed the nearest point along the line and used that as the center for the light beam, which worked pretty well.

And to make the particles actually visible in the air, I used this [ShaderToy example](https://www.shadertoy.com/view/tslXRj) to project it in 2D space. This has the added benefit of giving us a bloom effect for free!

This part was quite difficult to solve because I kept getting strange artifacts at the endpoints. I ended up adding point lights at the endpoints to cover up these artifacts. Probably not the best solution, but it got me by for the challenge.

Performance was decent, but there was definitely a dip when rendering a bunch of lights. I found that batching the lights in groups of 8 was quite a bit faster, so that’s what I ended up with!

## HDR Tone Mapping

I started by using regular 8-bit lighting, but that resulted in clipping with too many lights:

See how as the light gets brighter, it goes from green to cyan to white? This is because the light color is something like `vec3(0.2, 1.0, 0.5)`

. If you add two of these lights together, you get `vec3(0.4, 2.0, 1.0),`

but since the color output is limited to the 0 - 1 range the color looks closer to cyan. The green tint is completely lost in the blue.

This can be fixed by using a floating-point surface (16-bit is enough) and using “[Tone Mapping](https://www.shadertoy.com/view/llXyWr)”. Here’s an illustration:

Basically, instead of using a linear function for light brightness, we can use an inverse exponential. With linear color grading, color is lost once one of the channels exceeds 1.0, but by using tone mapping, we can make the transition to white, much smoother and allow users to see brighter colors!


I ended up using this formula from Unreal 3, which also does gamma correction baked in!

```
float Tonemap_Unreal(vec3 x)
{
// Unreal 3, Documentation: "Color Grading"
// Adapted to be close to Tonemap_ACES, with similar range
// Gamma 2.2 correction is baked in, don't use with sRGB conversion!
return x / (x + 0.155) * 1.019;
}
```



## Instancing Attempt #1: Post-Render

The main benefit of using deferred rendering is that it lets you add lights in post-process, so you don’t have to include them in the main loop. I thought, why don’t I render my in-game objects like weapons or players this way?

So basically I can raymarch each object separately and layer it on top of the scene. Since the Gbuffer is in world space, I can render objects for all screens at once. Unfortunately, this ended up being too slow to be used practically. It needs 2x the surfaces for ping-ponging and has to be rendered across the entire screen. The rendered objects can cast shadows, but can’t receive shadows from anything drawn before it, which would look bad.

I needed a plan B.

## Instancing Attempt #2: Textures

I thought of placing weapons in grid cells across the map. Each cell’s data would be stored on a surface with each pixel representing one cell. Data could include weapon type and relative x, y, and z. This has a couple of drawbacks. Weapons must be spread across separate cells, so two weapons would have to be a minimum distance of separation. That was a trade-off I was willing to make, however, I ran into this error:

I’m still not precisely sure what caused it, but I tried many different variations, but no luck. It seemed that sampling the texture in the distance function caused this error no matter what I did with it. Odd because I’ve done this many times before.

In the end, I just ended up using forward rendering for weapon objects and limited it to 6 drop boxes at a time. Maybe I’ll solve this next time!

## Pre-Rendering Attempt

Another concept I wanted to try is called pre-rendering. Basically, I render the scene depth map at 1/8th resolution stopping the raymarching early when we get approximately within 1 pixel of the geometry. Then I can use this as a starting point for the full rendering pass, which should in theory render in far fewer steps.

Unfortunately, in practice, this barely seemed to make a difference in performance and it introduced a bunch of new artifacts. I will plan to revisit this concept next time I make a large raymarched game.

## Volumetric Radar

I’m nearing the file size limit, but [here’s a link](https://twitter.com/XorDev/status/1674657562405240838) if you want to see the volumetric radar in-game. I was thinking about different ways to display a mini-map and I realized I need to use the map SDF as well as the player/weapon positions. I thought, why not just make it 3D? Most games don’t have the luxury of volumetric data, but in this case, I do!

The process is to sample along the ray and only add points close to a surface. I made the color vary with z (height value) to help separate higher and lower objects. For players, I just used bright point lights that pulse with the radar.

I combined the radar code with the main render shader so that there’s no overdraw. Seemed to help with performance a little bit.

## Conclusion

So that was the gist of it! I hope you learned something interesting along the way. I know I sure did! Turns out that making raymarched games can be quite fun and with practice, fast to develop! It’s really quite handy to have a distance field for everything. It makes lighting, shading, and collisions much easier. I hope some of you are inspired to give it a go. If you do, please let me know how it goes!

At this point, I’m not planning to release this game as it has a very niche audience (split-screen multiplayer on high-end Windows hardware). If enough people shout at me, I might change my mind though. Tell me what you think!

In any case, thanks for reading. Stay tuned for more great stuff. I have some awesome guest writers that will be posting here in the near future!

This is awesome! I'm also working on a raymarcher game engine, and it feels super lonely. I would really like to read more about this project as you develop it further.