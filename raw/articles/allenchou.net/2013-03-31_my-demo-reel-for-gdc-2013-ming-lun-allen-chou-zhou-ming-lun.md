---
title: My Demo Reel for GDC 2013 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2013/03/my-demo-reel-for-gdc-2013/
author: Allen Chou
published: '2013-03-31'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of [My Career Series](http://allenchou.net/my-career/).

This is the demo reel I showed people on my tablet and phone at GDC 2013. I made it approximately one-minute-long and practiced talking while showing the video, explaining the technical details. I basically picked the features that are not commonly present in other people’s games.

So this is what generally said when I showed people this video:

Here’s a video of the three games I have worked on at DigiPen so far.

The first game ([Astrobunny](http://allenchou.net/astrobunny/)) is a freshman game project. Not every one knew programming at that point. Some of us came straight out of high schools, so we were asked to use an educational game engine built by the school faculty. I did all the programming and art of this game, and my teammates did the level design. This is a one-button puzzle game, where you have to use the mouse cursor to guide the ship to the exit of each level.

The second game ([Photon Bunny](http://allenchou.net/photon-bunny/)) was made in my second semester. This time we have to build the game engine from scratch, and we were restricted to using strict ANSI C. We still managed to implemented [object-oriented structures](http://allenchou.net/2012/01/object-oriented-structures-in-c/) by making our own version of virtual tables. For graphics, we were only provided with `getPixel()`

and `setPixel()`

and we were not allowed to use any other graphics API. The entire graphics engine was built from scratch using only these two functions, and I implemented blend modes, 2D dynamic shadows, pixel blitting, triangle rasterization, and normal mapping in the background, all in software. It was a very interesting challenge.

The third game (Flora Bunny) is our current project. This time we are allowed to use C++ and OpenGL or DirectX, so the graphics engine is finally hardware-accelerated. I built another game engine and graphics engine from scratch for this project. My recent responsibilities are mainly polishing up the game and make everything look visually smoother. This includes throwing in lots of particle effects and transition animations to cover up visual flaws. We are planning on finishing and submitting this game two weeks from now, so that we can enter the school’s student showcase and prepare for our finals.