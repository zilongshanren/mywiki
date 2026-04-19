---
title: PIX is great but...
url: https://c0de517e.blogspot.com/2010/03/pix-is-great-but.html
published: '2010-03-19'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

...sometimes using colors on the screen is actually better. The trick is all in the iteration time. PIX gives you accurate numbers and step-by-step execution of a shader. But if you can easily change/compile/reload shaders and quicky arrange dedicated views on screen of some render passes, then you might actually find your bugs better, even if all you have are colors.

I just finished debugging a very nasty bug involving coordinates in different spaces and decoding of the z-buffer. I worked a lot in PIX but I managed to find the problem only when I abandoned it and started comparing the data I recovered z-buffer view with the ground truth I had from the main rendering pass.

I quickly arranged a debug view of the data I recovered from the Z-buffer, by displaying it on a corner of the screen. Then I changed the main shaders to output the data I needed. A few changes later, I fixed the problem.

That was only possible thanks to the fact that our rendering is scripted (so it's easy to add such debug-views and stuff like that) and that I can modify the shaders and they get automatically updated in game.

I guess that's not surprising to anyone that worked with scripting languages as well. Most of the times if you can live-edit your code, you end up not using the debugger but just inserting print statements to see "live" what's happening.

The next step, for shader debugging would be for me to create some more live debugging visualization stuff. At the moment I can easily just render things, it would be cool if I could place on the rendered images some "color pickers" that also display an accurate numeric reading, or that are capable of interpreting colors as normals and so on...

## 1 comment:

I am also a huge fan of FBO debug by displaying them at screen corners. One day, that was not enough, so I ended up writting my FBO data into HDR image (to keep floating point precision). Then, I was able to read pixels values in photoshop. :)

Post a Comment