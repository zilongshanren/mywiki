---
title: Dragon Mania
url: https://www.elopezr.com/dragon-mania/
author: Redorav
published: '2014-03-09'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Dragon Mania is a game about taking care of dragons on a remote island that belongs to you. The tycoon part of the game has simple mechanics – buildings to grow dragon food, habitats where you keep and grow them, and a breeding den to breed different types of dragons. The main attraction of the game is the sheer variety of dragons at the player’s disposal, from the easy to obtain through breeding to the almost impossible. There is also a combat system to battle your friends, and several single player castle raids.

I worked on the game during the final months of development, and all through the QA process. I was involved in several tasks of the game such as:

**Sound and localization bug fixing****Performance optimizations****Dithering algorithm to reduce image size with little quality loss**

##### Performance

Optimizations in the game deserve special mention, due to the fact that this game was using a very old engine designed back in the MIDP days, and later ported to Android. Because of that, the image quality suffered (only **256 colors per texture**), and performance also suffered (texture packing was very inefficient, many **draw calls** and too many **textures** ~900). All dragon textures had to be loaded throughout the game (to avoid loading them at runtime when breeding a new dragon, and allow for online combat), and with very tight time constraints, we had to make sure the game would run at a reasonable speed.

The game underwent several profiling sessions, **trimming textures, reducing OpenGL calls, packing textures where available**, creating a **dithering algorithm** to mask the very tight color palette, etc. The biggest problem were the dragons themselves: composed of many parts, the system did not allow packing the same dragon into a single texture, so every part of the dragon had a separate render call. In the end, the game went from running at 3-4 fps to running at 14-15 fps on the worst phone in our benchmark (the Galaxy Ace), which was deemed playable enough.