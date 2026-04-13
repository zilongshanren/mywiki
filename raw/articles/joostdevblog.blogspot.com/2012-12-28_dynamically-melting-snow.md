---
title: Dynamically melting snow
url: http://joostdevblog.blogspot.com/2012/12/dynamically-melting-snow.html
author: Joost van Dongen
published: '2012-12-28'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Snowball Earth](http://joostdevblog.blogspot.nl/2012/10/the-history-of-snowball-earth-now.html)is without a doubt the snow. As the player walks around and heats up the area around him, the snow melts, forms puddles and finally becomes grass. This is completely dynamic: the player can turn his heating on and off at any point, and the snow reacts correctly to that. The snow even has little piles around trees and rock walls, and these piles lower and disappear when the snow melts. So how did we make this?

*A slow motion video of how the snow melts around the player.*

Before I continue, I would like to mention once more that Snowball Earth is

[Ronimo](http://www.ronimo-games.com)'s cancelled game from 2008, and that the complete prototype can be downloaded here:

![](../../assets/85f5e307f2df2e00.jpg)


Download Snowball Earth prototype

![](../../assets/85f5e307f2df2e00.jpg)

Download Snowball Earth prototype

So how did I implement this melting effect? The basic trick is that for every vertex, I store the 'meltness': to what extend the ground at that vertex has already been melted. A value of 0 means snow, 0.5 means water and 1 means grass. The pixel shader then takes this value and uses it to simply choose between three textures, for grass, water and snow.

To store the correct value in each vertex, the code simply updates all vertices for which the value has been changed. This is done every frame. This would not be very efficient if the vertex count were very high, but it works well enough here. Especially since this is only a prototype and performance isn't as much of an issue as it would be in a released game.

A nice property of storing this value at the vertex, is that the value gets interpolated before it gets to the pixel shader. So if two vertices are next to each other, and one has value 1 (grass) and the other 0 (snow), then a pixel in the middle would get value 0.5 (water). This means that if I smoothly increase the value at the snow vertex during the melting, then the edge of the snow in between the two vertices smoothly moves towards the snow vertex, which looks like the snow is melting at the edges.

![](../../assets/3cf713e872de2fa2.jpg)

The water automatically always becomes a thin edge of water in between snow and grass, because vertices usually rather quickly go from 0 (snow) to 1 (grass).

So far the edges between snow and water and between water and grass would still be straight lines, since they are simply based on interpolated vertex values. This looks kind of okay, but it is still too geometrical to be really convincing. I would like to break up the border and add patterns to it, so I have a special greyscale texture that contains puddle-like patters. This texture is used to offset the 'meltness' value: I simply add the texture's value to it. The effect this has, is that wherever the offset-texture contains white, the water will disappear into grass earlier, while wherever the offset-texture contains black, the water will remain longer.

Our artist Ralph jumped on this and created two offset-textures: one for the water and one for the snow. He made the offset-texture for the water so that it contains roundish, puddle-like patterns, while the offset-texture for the snow contains long curves. This works really well in the actual game.

![](../../assets/9b051987235b4476.jpg)

In practice, the grass, water and snow are all a little bit more complex than simply 'a texture'. The snow has noisy specular reflections, the water reflects the sky a bit, etc. So instead of choosing which texture I use, I choose which material to use: snow, water or grass.

I wanted this to run on shader model 2 videocards (pretty ancient these days), so I couldn't use an if/else statement to choose the material, since if/else is not supported in shader model 2. Instead, I used the

*step(a, b)*function, which returns 0 if

*a*is larger and 1 otherwise. With some puzzling, most math that needs if/else-statements can be replaced by

*step*-functions, allowing quite complex things to be done on ancient shader model 2 videocards. This is also how I got the snow/water/grass choice working. Just look at this tiny bit of shader code for how that could be done (note that the final line could be replaced by a

*lerp(a, b, c)*call instead):

float4 grassColour = tex2D(grassTexture, uv); float4 snowColour = tex2D(snowTexture, uv); float choice = step(0.5f, meltness); float4 final = (1 - choice) * grassColour + choice * snowColour;

For a complete look at the shaders described above, you can check them out in the file

*Data\Assets\Shaders\Snow.cg*in the Snowball Earth prototype.

![](../../assets/78b15d4d17723745.jpg)

The final element to the snow effect is that the snow has little piles around trees and such, and when it melts, it lowers and the piles disappear. This was done with a simple morph: our artists made two versions of the ground meshes: one low one for the grass, and a slightly higher one for the snow. As the ground melts, the two positions for each vertex are simply interpolated to get the final position. Every snow-pile in the game was made by hand by our art-team, who raised the vertices around trees and next to walls.

![](../../assets/cbeb610b59cefb33.jpg)

Only one of the two meshes for the ground is used to handle physics and collisions. This is the lower grass-mesh. A nice added benefit of that is that all characters walk

*in*the snow and

*on*the grass/sand, giving the snow just that little bit extra.

![](../../assets/72c8754644a773a1.jpg)

To add to the atmosphere, there are also two different sets of lightmaps in Snowball Earth, each with different colours. This way I was able to give the snowy world a colder, more blueish lighting than the unfrozen world.

Having two sets of lightmaps also has an added benefit. There are no real-time shadows in Snowball Earth, so normally there would be the problem that objects that appear dynamically (like leafs and smaller plants) cannot cast shadows. Having separate shadow maps for the frozen and melted versions makes it possible to calculate these shadows into the melted world only.

This solution is not completely correct, though. If you look closely, you can sometimes see that if an area near a big plant is already melted while the plant itself is still frozen, it already contains the shadow of that plant, even though the plant itself has not appeared yet. However, this visual error only happens at the transition from frozen to unfrozen and is hardly visible (unless you look for it), so I never really considered that a problem.

That's it for Snowball Earth for the moment! Let me know if there are any further topics about Snowball Earth you would want to read more about! In the coming weeks I'll be getting back to posting about

[Awesomenauts](http://www.awesomenauts.com),

[Cello Fortress](http://www.cellofortress.com), and hopefully also about some exciting graphics experiments I have been doing!

Love this, not in the least for the SM 2.0 love. Real men only need 64 instructions :)

ReplyDeletefloat4 final = (1 - choice) * grassColour + choice * snowColour;



ReplyDeleteis:

f = (1 - a) * G + a * S (1 sub, 2 mul, 1 add)

f = a(S - G) + G (1 sub, 1 mul, 1 add)

Hehe, nice! Depending on whether the compiler actually compiles these two differently, though... ;)

DeleteI love these blogs, including the bits of code that are there for programmers to obsess over :) The melting effect of SE was indeed quite impressive. I love it when worlds dynamically change, it adds such a huge layer of interactivity. It reminds me of Starcraft, where my aim would always be to cover as much of the map with Zerg creep as possible. Except in SE I'd remove as much snow as I could!

ReplyDeleteYeah, changing the world is always fun! I also loved it in that Prince of Persia reboot. Did you see Giana Sisters? There you can constantly switch the whole world between two states, with everything morphing in reaction, pretty impressive!

DeleteI heard about that, but haven't seen it. Oh, and Animal Crossing has some spiffy things with plants running wild if you don't maintain the area. I bet my village look like a jungle right now, after years of neglect.

DeleteCapital article! Thanks for writing that down for us.

ReplyDeleteI'd imagine having two meshes to add snow piles adds a lot more vertices and causes a drop in performance. isn't it possible to raise the snow of the lowest mesh around trees and rocks automatically? When the snow melts, first de-extrapolate the vertices, then apply the melting shader trick. Or are trees and rocks also part of the ground mesh and not separate models? You would only loose the walk-in-snow effect though.

I guess this could indeed be optimised. :) To do so, the vertex shader would somehow need to know how high the snow is in a specific spot. This could be stored in a single extra float per vertex, while my current method has three three extra floats per vertex (for the extra position). However, to get proper normals for lighting (which isn't very relevant here, since most lighting in Snowball Earth is pre-calculated), some extra data would have to stored, since otherwise the normal would not change with the modified height relative to neighbouring vertices.

Delete