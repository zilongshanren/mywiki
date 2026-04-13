---
title: Astrobunny! | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/12/astrobunny/
author: Allen Chou
published: '2011-12-12'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Here it is! Our game project for the first semester at [DigiPen](https://www.digipen.edu/). We used a game editor provided by the school called [ProjectFUN](https://projectfun.digipen.edu/). I coded in C++.

I basically only used ProjectFUN as a render engine, since I pretty much ported the Easing Equations from ActionScript 3.0, built a tweening engine, created a command framework based [on one of my articles](http://active.tutsplus.com/tutorials/actionscript/thinking-in-commands-part-1-of-2/), and put together a baby version of [Stardust](https://allenchou.net/stardust-particle-engine.googlecode.com), called StarLite. ProjectFUN provides a built-in physics engine, but I found it’s collision detection system for circles quite buggy, so I implemented one my own.

I built the template levels in the editor, so that we could create new levels just by drag-and-drop. All the planet-orbit linking, orb position correction, initial velocity based on object orientations are all taken care of by my code automatically.

Something very special about this game is the Credits level. We actually made the Credits screen into a fully playable level, where all the information are shown on planets and speech bubbles.

And here’s a dedicated planet to one of my classmates, Justin. He is such an annoying play-tester (i.e. he play-tested a lot, so I couldn’t use my laptop) that I thought he deserved his own planet 🙂

So this is Astrobunny. I really enjoyed making it, and I hope you enjoy Astrobunny’s journey through space. Be sure to check out the awesome Credits level, too!

hey! Cj!

Every time I tried to open the game, it tells me that “The “wglCreateContext” function failed with error 2000:

Try placing the folder in an English-character-only path, such as “D:/games/Astrobunny”. I’ve heard people are having problems running the game if the path includes Chinese characters. If that doesn’t work, then I really don’t know what’s going wrong. So far I’ve been able to run the game on all Windows computers I’ve used.

I’m putting it here, which is “D:\Astrobunny”

And bad thing still happens, like this:

http://tinyurl.com/d6sxaey

Or should I change the language settings of the Windows?

For more info, my laptop and desktop both have the same problem, and my roommate have the same problem also.

Even the Error line 898 is the same.

I’m not sure what’s causing this problem, but I’m guessing that has something to do with your graphics card’s driver support for OpenGL. I found some online forum posts with similar issues, and people usually suggest updating the graphics card driver. Besides that, I really don’t know what to do. Sorry.

I go to this page

http://sites.amd.com/us/game/downloads/Pages/radeon_win7-64.aspx

and download the “Catalyst Software Suite” and install it, and now the game run correctly!

I’m not sure what exactly the problem is, but that package solve my problem =)

Wow! This is so awesome! That was a great game, I loved how simple it was but still really fun! Congratulations 🙂