---
title: The Beauty of Restriction
url: https://claire-blackshaw.com/blog/2011/04/the-beauty-of-restriction/
author: Claire Blackshaw
published: '2011-04-12'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![The Beauty of Restriction](../../assets/7ffe04df04627045.png)

When I first started to enjoy games on my C64 alongside the board games and role-playing games one thing was king, limitations of the medium. Shortly afterwards I learnt BASIC then C, and started making my own games some on paper, and I fell in love with the grid.

Now originally working in mostly text or simple 2D systems the grid was a joy, and the games were so great. Some of my favourite games, such as X-Com, were on the grid. The reason as a programmer I loved the grid is it made things simple. Collision detection, map editing, path-finding all was made simpler by the grid.

Then as I advanced as a programmer, learning new languages and then writing my own game engines. Learning about BSP, Object Models, Raycasting, Vistor patterns... and entering the industry, well I noticed a trend. More and more of my hobby projects in high-school and later were going unfinished mostly due to frustrating technical barriers.

Now I should mention recently in a professional capacity I’ve moved from a programmer role to a design role, though I still code in my free time and do not dismiss the option of flowing back and forth. Well my biggest hobby project over the last year has been “reset” several times. Recently I had a flash of inspiration.

So many of my unfinished projects were grid based (or using some similar arbitrary restriction) but were built on more advanced tech. The trend of technical hair pulling had started when I started using more my more sophisticated engines, in which these technical shortcuts of old like grids were actually MUCH MUCH harder to implement because they went against the grain of the renderer, physics or similar system. I was kidding myself about the technical benefit of these old style short-cuts.

Now if you had actually sat me down at any point and asked me, “Is a grid system optimal in a modern 3D engine” well obviously I would have said NO! So why did I keep pursuing the grid, and similar systems. The truth is love of the Design.

Now I won’t go into a rant about the awesomeness of the grid and its effect on game design, but let us just say it makes a much more interesting game design in many cases. This can be said for many technical limitations, at the time they were done because they were optimal but what many people don’t appreciate is they have value and facets of complexity to be explored. The closest parallels that come to mind are Monochrome Photography or Mosaic Tiles.

Now the lesson I learnt was, “Know the why before addressing the how”. In the example of the grid system once I acknowledge that the only reason I wanted it in-game was the game design benefit and not a technical one, well then my approach completely changed.

My object model became clear and clean without the mess of grids and my render graph all the sudden lost all its mess and clutter. Maps no longer need to be tile based but can be built with geometry in the style of grids and then a “game grid” can be generated offline using a series of collision objects. My lighting system could be broken into an abstract high-level effect and well let’s just say the hair pulling stopped.

It took me around 8 years to realise why I loved the things I loved. Strange but true.