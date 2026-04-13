---
title: My upcoming GDC 2014 presentation
url: https://bartwronski.com/2014/03/09/my-upcoming-gdc-2014-presentation/
published: '2014-03-09'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

Ok, so GDC 2014 is coming up next week, are you excited? Because I am. 🙂

Thanks to the GDC Committee I will be giving a talk this year [http://schedule.gdconf.com/sessi](http://schedule.gdconf.com/session-id/826051)[on-id/826051](http://schedule.gdconf.com/session-id/826051) named “Assassin’s Creed IV – Road to Next-Gen Graphics”. As I’m +/- finished with the contents of my presentations and after many iterations on it, I wanted to give you a small sneak-peek of its contents so you can decide if it’s worth to come and see it.

As the presentation title suggests, it will be mostly about various next-gen techniques we developed to next-genify our game. Don’t expect any “we upped the texture and screen resolution and increased geometric LOD” boring and common stuff, I will talk only about novel and newly developed techniques and next-gen console experience from a developer point of view. 🙂

## Global Illumination

This section will be a bit different from the other ones, as I will briefly describe a partially baked GI solution we used on both next gen as well as **current gen**.

In over one month a small strike team consisting of Mickael Gilabert, John Huelin, Benjamin Rouveyrol and me created, iterated on and deployed a solution that uses around ~600kB VRAM, almost zero main memory RAM, adds around under 1ms of GPU overhead on PS3 and is compatible with dynamic time of day and various weather presets. I think it was a huge and important addition and improvement over previous AC games rendering.

## Volumetric Fog

I will do a small introduction to various atmospheric-scattering related effects and how we tried to unify them in a single, coherent system (so no more separate volume shadows, fog, light-shafts, god-rays and post-effect based hacks!). Developed Volumetric Fog algorithm uses small resolution volumetric textures to both estimate (procedural animations) participating media density, estimate in-scattered lighting (from many and any light sources!) and then in a second step create a lookup texture for final in- and out- scattering to be applied during shading. It can be applied it in either deferred or forward manner using one tex3D operation and one MAD instruction as it is totally decoupled from scene geometric information and z-buffer. Final performance is a fixed cost of around 1.1ms on both Sony PlayStation 4 and Microsoft Xbox One including “common” engine operations like shadowmap downsampling / ESM generation from depth-based shadow maps and applying the effect in a separate fullscreen pass.

Please note that on this screenshot showed effect uses custom, art-driven (not physically based!) phase functions and uses exaggerated (but in-engine) settings.

## Screen-space Reflections

I will talk briefly about the reasons why it is beneficial to sometimes use screen-space reflections (see my [previous blog post](https://bartwronski.com/2014/01/25/the-future-of-screenspace-reflections/)), describe how the algorithm should work in general and then details of our implementation and performance optimizations for next gen consoles. I will show achieved results and talk how we got performance of this effect down to 1-2ms (depending on a scene).

## Next-gen console GPU architecture, its impact on performance and optimizations

Definitely the most technical part of my presentation, but potentially most useful for other graphics programmers who are still to ship a next-gen title. I will describe what we have learned about the GCN architecture of PS4 and X1 GPUs and how we applied this knowledge in practice.

You can expect me to describe GCN compute unit architecture and explain basic terms related to it like:

- vector/scalar registers and difference between them
- register pressure
- wave occupancy
- SIMD lanes
- Latency hiding
- “Superscalar-like” architecture

…and how all of them affect the performance of your shaders and GPU code. It won’t be a section only about theory – I will try to show some code snippets and talk about actual numbers.

## Bonus content and summary

I planned lots of bonus content that I probably won’t be able to describe in the talk itself. However, I will post the presentation on my blog after the conference with all the slides – and will be available to answer your questions – during and after the conference. Bonus content includes our efficient Parallax Occlusion Mapping implementation and code, SSAO algorithm we used and reasoning behind it, possible next-gen only extensions to our GI technique, fully GPU simulated procedural rain.

I hope to see you there! 🙂

You must be logged in to post a comment.