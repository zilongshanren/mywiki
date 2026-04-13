---
title: Some ideas for Tokap
url: http://raytracey.blogspot.com/2011/02/some-ideas-for-tokap.html
author: Sam Lapere
published: '2011-02-24'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

While thinking about ways to make the ray traced Pong game more fun, some other ideas came to mind. If you think about it, there are a lot of simple games that can be built using just a few spheres. Some ideas:

- cube and pyramid of spheres. Shoot a sphere to see it collapse!

![](../../assets/1a2928769a0a7d42.jpg)

![](http://static-p3.fotolia.com/jpg/00/11/77/50/400_F_11775070_SJUweWvzaKP2fKJvmRjrywCC5GGyK0yc.jpg)

Newton's Cradle:

- Amiga juggler:

[http://www.youtube.com/watch?v=-yJNGwIcLtw](http://www.youtube.com/watch?v=-yJNGwIcLtw)The character is entirely made out of spheres.- A cool real-time path traced physics animation like this:

[http://www.youtube.com/watch?v=33rU1axSKhQ](http://www.youtube.com/watch?v=33rU1axSKhQ), originally developed by Chiaroscuro from Luxrender running on SmallptGPU.As long as the number of spheres remains modest, these scenes could be path traced in real-time (with tokaspt) on a high end GPU and provide very realistic looking graphics with nice physics. Since the geometry of the "physics world" is decoupled from that of the "graphics world", the sphere-only limitation of tokaspt doesn't apply to the physics simulation, which can actually use real planes and boxes. These planes and boxes can then be approximated with spheres in tokap, while still producing 100% accurate physics as if the ball is rolling on a real plane, so even a snooker game should be possible!

There is also an amazing real-time raytraced game called "AntiPlanet" which is running on CPU but also has a version running on CUDA (

[http://www.virtualray.ru/eng/download.html](http://www.virtualray.ru/eng/download.html)). It's a first person shooter game where the entire scene is made out of spheres, including the weapons and monsters, and has been in development since 2001 (see[http://www.virtualray.ru/eng/news.html](http://www.virtualray.ru/eng/news.html))Videos of AntiPlanet:

"AntiPlanet2 - indie game with real time ray tracing 3D engine which only does spheres. It has multi core and CUDA versions. The game is "doom"-style 3D shooter. The sperical graphics design is inspired by abstractionism and cubism genres of fine arts. Program download page www.virtualray.ru/eng/download.htmlNight-time scene. Video was rendered in 1920x1200 resolution, system Core Duo 1860 + GeForceGTX 280"

Screenshot of AntiPlanet:

It would be awesome if the CUDA ray tracing engine of AntiPlanet could be upgraded to use path tracing. 'Tokaspt' could be used as a base framework, but it doesn't have acceleration structures (such as BVH) which are a must if you want to raytrace the thousands of spheres in AntiPlanet at acceptable frame rates. The video shows that 30 fps at 1920x1200 resolution is possible on a GTX280 with 'plain' ray tracing, very impressive numbers due to the fact that ray-sphere intersections are much cheaper than ray-triangle intersections. If the ray tracing engine would be extended to path tracing, I'm pretty sure that real-time GI (coming from a HDR skydome) would be possible at 960x600 resolution on a GTX580 with this game.

## 2 comments:

Hi,




I am currently working in my spare time on a raytraced game (cuda accelerated) with spheres as only primitive featuring advanced Monte Carlo rendering (including MIS). Antiplanet is actually one of my main inspirations. The scale of the game world is a lot smaller though. And your pong game has been quite useful as well :)

Anyway thanks for stealing my idea! ;)

All the best

Hi Anonymous! That's amazing news!! Can you please provide some more details such as what kind of rendering method you're using (path tracing, bidirectional path tracing, two-way path tracing, mlt, erpt, ...)? Do you have any plans to release your game once it's finished?


Huge thanks in advance!

Post a Comment