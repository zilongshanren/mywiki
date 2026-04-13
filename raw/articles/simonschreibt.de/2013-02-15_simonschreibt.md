---
title: Simonschreibt.
url: https://simonschreibt.de/gat/sacred-2-burning-map/
author: Simon
published: '2013-02-15'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The world map in Sacred 2 not just opened up. It burned in and out! How this looks, is proudly presented by this little GIF animation:

So how is such an effect possible? I can’t tell you the deep technical details, because i didn’t understand them. But let me try to explain it in artist words.

First you paint a height map. There should be one dominant spike in it, depending how you want the map to burn in/out. And now imagine how this map would look like in geometry:

![](../../assets/3690e47b7527c961.jpg)


![](../../assets/ad6b517a6d2a5d8f.gif)


If you now raise your hand and ask “But where comes the burning border from?”, then you’re a A+ pupil. As before i can’t explain how it really works, but there’s just one small gradient texture which is “wrapped” around the borders of the generated alpha mask:

![](../../assets/ba0680151067ebbc.png)

If I had to guess, I’d say that they have a heightmap, and rotate the gradient texture. So lets say your height map goes from 1.0 to 0.0 and you start with a variable X of 0.99

Anything at X gets painted yellow, and the lower you go towards 0.0, the more you move to the right of yellow on the alpha mask. Anything above X (to a max of 1.0) gets painted to the left (which is clear).

So you draw the screen from the camera, but you draw the map whenever you have alpha pixels. Move X down gradually, from 0.99 to 0.0 and then everything will be alpha (in otherwords, map). Because you’re scaling down X, everything that WAS X before is now clear, and the new X is yellow.

Thank for your comment!

The embarrassing fact is, that i worked on the game and asked the coder who did this effect. But after years some things get forgotten and so he couldn’t say exactly how he did it. :D

may i ask what part of the game did you worked on game designer perhaps ?

Sure. I was an artist and produced some assets. My portfolio shows some of them. :)

Hi,

I just found your blog and there is a lot of interesting stuff, keep up the good work.

I hope it wont be seen as advertising, but I made an Fx like this few weeks ago (but in 3D) with unity’s surface shader. This is not a big deal, but the source is available if you want to check it out: http://florian-noirbent.com/blog/en/disappear-objects-shader/ .

By the way, the idea of a ramp instead of a plain color for transitions is awesome, maybe I’ll update mine.

Hi good to hear that you like my articles :) Thank you!

In fact i love it when people share their stuff in the comments. It’s awesome to get in contact with other guys and their work. But for me the link wasn’t working so here’s the correct one:

http://florian-noirbent.com/blog/shader-disparition-dobjets/

Really nice effect!

http://kylehalladay.com/blog/tutorial/2015/11/10/Dissolve-Shader-Redux.html

Burning Paper Shader of Kyle Halladay

Oh that’s surprisingly easy, thx for explaining!

And it can be derivated for a variety of effects, hope to use it some day :)