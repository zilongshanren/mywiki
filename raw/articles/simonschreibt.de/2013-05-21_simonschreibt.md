---
title: Simonschreibt.
url: https://simonschreibt.de/gat/lego-batman-crawler/
author: Simon
published: '2013-05-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

LEGO is awesome. LEGO games are awesome. And – at least for me – this trick is awesome. It’s about the crawler “chains”. You know, the things around the wheel rims.

Let me explain, why i think this looks really good: If you wanna do such a “conveyor” animation in 3D, you need to animate some geometry. And depending on your engine you can do this in different ways:

**Way #1 “Texture Animation”**

You could use a texture animation where you let a texture slide over a geometry. This is very easy to setup but the silhouette of the whole thing isn’t that stunning:

![](../../assets/50f4cdafe53baea2.gif)


**Way #2 “Geometry Animation”**

If your engine doesn’t support texture animation and/or you want a nice silhouette you can make a conveyor out of separate geometries. This costs a lot more animation effort and of course more drawcalls since you get more separate objects. The plus side: the silhouette looks more interesting.

![](../../assets/9a13cdd18d0eb107.gif)


![](../../assets/a8bf44a1b4883e77.gif)


**The LEGO Way**

Let’s look again at the LEGO thingie. Am i the only one who thinks, that this looks like they bent a rubber geometry around the wheel rims? I really like it!

At first i thought about crazy bend-modify-programmer-stuff but then i checked out the drawcalls/wireframes. I bet you already guessed how they did it. If not, here’s a clue:

It’s kind of a mixture of both ways.

There’s a big geometry as a base (without crazy silhouette) and in addition several moving smaller parts (which create a great silhouette). Of course you don’t need a texture animation on the base geometry because there’s no visible texture/structure but it gives the whole thing a good shape.

![](../../assets/72a90f169004cb8a.gif)

![](../../assets/f2b4e69c07139463.gif)


![](../../assets/ba0680151067ebbc.png)

[these very good looking tools](http://www.norman3d.com/MaxScriptPack1/). With that it seems to be possible, to have only

*one*geometry but with different sub-geometries/elements/parts and everyone of those has it’s own pivot point which would save some draw calls if you would use it on stuff like the crawler.

![](../../assets/ba0680151067ebbc.png)

[Evgen Zaitsev](https://www.artstation.com/artwork/X12Ygy)showed how such tracks would be done with modern technology:

*“I made a shader, which moves/rotates vertices of the static mesh. Using this shader we implemented metal/rubber caterpillar treads. I also made tool for Maya, which generates all necessary data from spline, and exports it into the GIANTS Engine.”*

I don’t think drawcalls are what you think they are.

Isn’t a draw call a “call” do draw/render something? And every model/texture produces at least one of it if you don’t instance anything?

Don’t hesitate to correct me :)

A model can have gaps, e.g.: cluster of trees can be one draw call. In the above, both left and right tracks can be drawn in one call.

– Different Anonym

That’s right. But the Intel GPA Programm (which makes me able to show the wireframe) splits up the scene into drawcalls. You’re able to activate drawcall by drawcall which i did for the image with the wireframe of the chain parts. So every step you can see in the GIF is a single drawcall.

Having so many drawcalls is an absolute nono in almost any ambitious game. So, have a look at Norman3D’s Maxscript pack. It has just the tool you need for this trick: Sub Pivot Point Baker.

http://www.norman3d.com/MaxScriptPack1/

Enjoy!

Thanks for the link! I didn’t know about that tech – really fascinating. Have to pack this link into the article. :)