---
title: When to go C++ in Godot
url: https://claire-blackshaw.com/blog/2024/05/when_c/
author: Claire Blackshaw
published: '2024-05-26'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

I'm working on a VR game in Godot 4.x and well it has been long since that I admitted I would need to hack open the engine and make changes. I am trying to keep that to a minimum I talk about that about why the last game was shelved in [this video](https://youtu.be/X-7HdH1Ovlg). Now as progress on the new game is going well I want to talk about -two things- when you should C++.

**Problem**: Cut a mesh in VR very fast

## GDSCript is Great

It's fast, you can live edit it and well when speed of iteration is king it is hard to beat a domain specific scripting language. Though that is all it is a scripting language. That is not a bad thing and one of my favourite things about GDScript is it doesn't try to overreach. So many game enginges I've worked on get really over complicated when really a bit of YAML or LUA would serve 99% of their needs. So that golden rule for me is, **build it in gdscript first whenever possible**. So I start out by building a simple slicer using ArrayMesh in GDScript.

## Why not use generic addon ect...

VR needs speed and general purpose mesh processing algos are really slow and have a tendency to get linear fast, which means it is hard to avoid frame hitches. 99/100 if your doing realtime mesh processing in a game you haven't spoken to your tech artist enough. Smoke and mirrors baby! Also only solving the problems you to is a huge boost.

## Fake the cut then delay the processing across several frames

- Not going to split the rigid body till the moment of the cut completion
- The cut is likely to occur over multiple frames
- Minimal change of graphics buffers


So the MVP is we need to...

- Take a mesh and a cut plane
- Determine if you are either side of the plane. Simple dot product per vert
- Show the cut in progress without changing the mesh
- Then write a mesh slicer that is possible to split over multiple frames and does minimal IO


Another thing is the set of preconditions

- We can preprocess the mesh to be easy to cut (avoid long triangles for example)
- We can use gameplay effects to slow the cut down
- We can hide the moment of the cut with visual feedback on top


## What can't we do in GDScript

**Honestly nothing in that list, we good** then the question is what *should we do* in gdscript. Looking at the docs for array mesh and the functions offered by the Render Server I noticed a few things. Any mesh processing or buffer management will be a lot more complex, indirect and hard to optimise in GDScript. This is because many functions are wrapped through layers of indirection which would be hard for compilers to optimised. Now if I wasn't working on a VR game where every drop of perf mattered this wouldn't be a huge issue, but it is for me. Another thing though is...

## Scripting is aweful for Cache

Writing code which is very robust to processing large chunks of data with minimal wasteage mostly comes down to caring about IO and cache friendly operations. People will often talk about Big O optimisation or some fancy way of making the code "cleaner" but the reality is the compiler needs to scan a bunch of data from one place, make a transformation using a small set of instructions on a tiny worktable (CPU/GPU registers). It has some shelves by the table it can each to, or turn around and reach which can hold a bit more (Cache). But every time the computer needs to walk away from that worktable to fetch something from another room like hard drive or ram, or worse go talk to the neighbour or drive to another city over a network connection things slow waaaaaaaay down.

So often **doing more work that involves less moving about** is faster than doing less work. Think about this like sorting the puzzle pieces before doing a jigsaw or sorting out the bits of pieces from a model kit, cutting all the sprus while having the cutters in your hand. So sometimes scanning through data and working on it as you come across it, even if it means scanning the data twice or three times is faster. These deep coding problems are when you should be reaching for C++.

Additionally looking at the scripting API for GDScript, rendering server and its multiple backend support for Vulkan and other renderers because I know I'm only on Vulkan I can make things work directly with that. And the calls which are exposed to scripting are often done so in a friendly easy to process way for human devs rather than what is nice for the computer.

## Final Solution

I'm still optimising and cleaning up the solution but currently here is the process

### Shader is given uniform cutplane data for current cut

- Cut effect is done in shader
- Updated by gdscript to keep iteration fast
- Only one cut at a time, assumed to be plane
- Avoids any IO except setting shader param (very small)


### C++ Module for Mesh Cutting

- Given Cut point, normal, direction
- Encode UV2 to store dist from plane and relative 1D position in the cut
- Iterate any faces which are split by the cut plane
- Generate two new vertices slightly apart from the cut plane, quantise them into int grid
- Merge any cut vertices in same grid point
- Define new faces in direction of the cut plane using grid surf gen
- Define two surfaces using the same underlying buffers to minimise GPU IO
- Each surface uses unique index buffer
- Directly update buffers


Wrap that C++ function in a custom module which is callable from GDScript.

## Conclusion

I hope that is useful for some people I'm happy to talk more specifics if people are interested just drop me a line on masto: [@kimau@mastodon.gamedev.place](https://mastodon.gamedev.place/@kimau) or twitter: [@EvilKimau](https://x.com/evilkimau)