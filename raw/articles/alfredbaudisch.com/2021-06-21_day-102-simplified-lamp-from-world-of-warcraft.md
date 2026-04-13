---
title: 'Day 102: Simplified Lamp from World of Warcraft'
url: https://alfredbaudisch.com/dailies/day-102-simplified-lamp/
author: Alfred Reinold Baudisch
published: '2021-06-21'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

I wanted to create a World of Warcraft lamp (a type of item for the "Off-Hand" slot) and I decided to make the geometry as simple as I could, where I set the details via the UV mapping and with texture alpha. I managed to accomplish that (the cut-off rectangles come from the texture, not from the geometry).

I modeled only 1/4 of the geometry and then added a mirror modifier on 2 axis, as it can be seen in the process screenshot below.

Now it's a matter of creating the final texture for it, and then I'll add the fire with Godot. But this will be the subject of another daily.