---
title: Simonschreibt.
url: https://simonschreibt.de/gat/deus-ex-3-folds/
author: Simon
published: '2013-01-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This shader wasn’t really impressive to anyone but me i guess. Together with the sound, Deus Ex creates a really strong atmosphere. And i really like how it looks. I only can assume how they did this. I think they animate the UVs for the distortion and also move a tiled normalmap from top right to bottom left.

I don’t think that there is any vertex animation, because on the one hand, i can’t see any movement when looking at it from the side. On the other hand they would have to “lock” the border verts and this seems a bit too complicated to me.

After reading this text my friend [Falk](http://www.fa-so.de/) mentioned, that this trick is pretty easy to do via UDK. Ok….anyway i really like it and i didn’t noticed it in other games. He also confirmed my thoughts: it is UV animation plus a “overlayed” and moved tile able normalmap.

**Update #1**

I found a tool which is able to give me a wireframe. You can clearly see, that there are not much UV intersections which made my theory of animated UVs worthless. But how did they move the fabric? An animated normal map would only have pushed/pulled out the folds.

I didn’t found any interesting texture in the memory. But then i went through all the options of the debug tool and found “Disable Texture Filtering”. And this is how it looked like. At first i thought it’s maybe a bug…

…but then i checked the textures again and found a small nice noise texture. And in combination with the picture above it’s pretty clear. They don’t use any normal map or UV distortion. They use parallax mapping (like said by [JacqueChoi](http://www.polycount.com/forum/showpost.php?p=1763419&postcount=36)). I wasn’t sure because i thought an “animated” parallax map would mean an complete bake of a high resolution folding simulation. But now it’s more clear.

![](../../assets/8993d193002f0e03.jpg)


Of course the base for the folds is this. I’m not sure..looks like an object space normal map…i’m not sure if the b/w texture is used.

![](../../assets/cc53b92ef1914ae6.jpg)


And instead of heaving a higher resolution texture with round half spheres (like I thought first), the scale this small noise texture and let the texture filtering do the work. Foxes!

![](../../assets/ba0680151067ebbc.png)

[Batman: Arkham City](http://rocksteadyltd.com/#arkham-city)has similar cloth-fold-stuff like Deus Ex:

Looks really nice and even the **silhouette is moving**! Works perfect for the pennants I would say. At least if you look towards at them. Seen from the side there’s no movement (like in Deus Ex):

Here’s the wireframe. Even if the banner looks really tesselated, the vertices **aren’t** moving in the game. I guess they’re used to mask areas where the silhouette moves a lot (at the bottom of the banner) or less (at the top/side of the banner):

It seems (but I can’t prove it) that in Batman they used normal maps for displacing the texture (while in Deus Ex it was a small grey-scale-texture). Like I said, I can’t prove it but these wavy normal maps look perfect for such use:

![](../../assets/ba0680151067ebbc.png)

Here is another nice example for a “oh look a moving mesh – no wait, only the texture wiggles!”-effect:

As you can see from the side, the mesh is static. But here the surrounding metal-structures (which hold the cloth in place) help to hide the trick while in deus ex the borders of the fabric were exposed.

This one is really impressive, best use of normal maps i’ve seen since blending for cloths.

That’s also how they do water ripples in the UDK

First time i remember this effect in

Mirrors Edge on “scaffolding cover fabric”

(in some different variations)

http://i.imgur.com/Ga6PwWO.png

Mirrors Edge have unstable (UE3) editor

(which funs inserted back)

it allows you open and see game content

including packages and maps by DICE

i jump in and catch scaffold material for you

http://www.imagetoo.com/images/clothnorma.png

I forgot to mention that this effect

works only Without PhysX

if PhysX swiched on – then scaffolding cover

swiched in PhysX Cloth material

http://www.youtube.com/watch?v=uFio7wMTQ2k

@ Félix Arsenault

Seems it’s not normal maps :) I was wrong.

@ ScorpyX

Thanks for the links :) Yeah the ME nVidia PhysiX is aewsome :)

nice update Simon, thx

The texture on the left seems like a normal map with just the R and G channels… B is probably reconstructed in realtime. The one on the right puzzles me though…

Yes it’s most likely that the left NMap is just 2 channels. The right one is a map for Bump Offset as far as i can tell. The brigher the color, the more the pixels will get “moved” to another position.

Thanks for you comment :)

Best I can tell, we have an animated parallax map tree, plus a (yup) reconstructed normal map. The parallax map probably starts with the b&w side as a base heightmap, then multiplies or is otherwise moded by the noise – at large scale as we can see the pixels with the debugger on – but animated down-left, and then the parallax tree is blended/blurred. The normal map is very light in the final render, but it isn’t animated, so we retain hints of the original shape of the pinned fabric folds, and the detail of the cloth after the blur happens to the rest of the shader.

Great site. -><-

Thank you very much! :)

Hey Simon,

this is one of my favorite articles on your site. ;-) Can you tell me which tool you used to display the wireframe?

Sure :) I used Intel GPA but it might be that there are better tools for this.

Oh, nice, thanks! Great tool, the one I found was heavily outdated and didn’t work.

Just wanted to share one nice effect I’ve made using this technique. It’s really amazing approach! Also used this to make super-fast animated water.

http://i.imgur.com/UOOkcK6.gif

Looks really nice, thank you for sharing :)