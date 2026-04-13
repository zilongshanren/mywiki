---
title: Simonschreibt.
url: https://simonschreibt.de/gat/alien-vs-wolfenstein-cutting-torch/
author: Simon
published: '2016-03-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](https://data.simonschreibt.de/gat062/thumbnail_youtube_01_forward.png)


![](../../assets/0d45f605a2524137.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/1d084db60d100ed5.png)

![](../../assets/e620bef718d2a96d.png)

Today we’ll compare the cutting torch of Alien Isolation with the one in Wolfenstein. At first let’s see which one can cut a better shape.

![](../../assets/f7a53db2afff1c69.png)

In Alien Isolation you can weld on special prepared places. It looks gorgeous but it happens on a **pre-defined** path! The player can choose going left or right but that’s all freedom you get. On first look it looks almost like an interactive animation.

Like in Alien, you can also only weld on some exclusive areas in Wolfenstein (special metal plates). But in comparison you’re **free** to weld any shape you want and you’re **not** bound to a default path.

![](../../assets/e620bef718d2a96d.png)

But careful! There **is** a limitation! Yes, the mesh is divided **dynamically** but for performance reasons there’s a restriction in precision so that you can **not** cut the metal into too tiny pieces (unfortunately I wasn’t able to capture a wireframe to visualize the dynamic splitting of the metal plate).

Here’s an example. On the **left** you can see that the cut begins at the first hole in the plate. On the **right** you can see that I’m not able to make a cut **at the exact same place** because another cut was already made really near to it.

That’s the limitation – you **can’t** set the cuts too close to eachother.

![](../../assets/e620bef718d2a96d.png)

![](../../assets/1d084db60d100ed5.png)

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/09700ea733e2269d.png)

In both games poly-stripes are rendered along the way which make the edge glow very nicely.

In addition to all the stunning detail effects in the curves are pretty wide so there’s **no** problem creating a perfect poly-stripe.

By the way: the small flames are animated via a flipbook texture.

The created stripe in Wolfenstein looks awesome too but seeing it side by side I must say that Ripley wins the race in this case.

Especially at the corners you can see some interruptions which seem to be the price for the freedom of cutting whatever form you want.

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/191dc50baf588231.png)

In the Alien game this is pretty straight forward: As soon as you “close” the welding cut, the poly-stripe disappears and the formerly un-damaged door gets **exchanged** with a new geometry. This time the geometry is already divided into parts so that Ripley can pull the inner part out:

Within **one frame** the poly-stripe gets removed (the particles stay) and the new door geometry comes in. You can see that the welding edge still exists in the “new” door but is “cold” for one frame. You can see the bare metal. One frame later, it starts glowing again to act like it’s the welding edge from before.

If you look very careful you can see this happen even in motion (video is in slow motion):

In Wolfenstein it’s similar **and** different at the same time. Here the part falls down dynamically as soon as the cut is finished. Notice the the newly created metal has **no** glowing edge anymore.

Similar to the Alien game you can see that for **one frame** the original geometry disappears and is **exchanged** (now not having a glowing edge anymore). But here it is a **dynamically** created model and not pre-defined by an artist:

But that’s not the end of the story! Let’s have a close look on the glowing edge. If you have a poly-stripe around the cut it may look like that:

![](../../assets/786f5a10b300682c.png)


As you can see the polygons reach outwards and inwards to cover both sides of the cut. Not a problem until the inner metal plate falls down. Now you end up with a poly-stripe which “hangs” over the inner area:

The obvious solution might be to divide the stripe in two parts and delete the inner one:

But I’ve another theory how Wolfenstein did this and will show you the proof later.

I guess you guys know soft-particles, right? You can avoid having hard cuts at intersecting geometries (**left**) by fading it out **the closer it gets** to other geometries (**right**):

You can also **invert** this to only show geometry which is **near** to another surface. On the right you can see that my example cloud is only rendered when it’s near to the ground:

What this means is, that if you have a plane with a nice glow texture and you apply this trick, you see it only if it’s near to other surfaces and gets invisible when nothing is in close distance (the black area on the right is just empty space):

And if we apply this to our poly-stripe it looks like this:

Of course **I don’t know for sure** if it was done this way but here’s why I think I’m right: When you get near to the edge with your hands in the game, the stripe gets visible again:

My guess is that the hands write into the depth buffer and therefore the stripe thinks “Oh…something is near to me. I better show up!”

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/0bfd4d8d4cb4c4ec.png)

When you cut a hole into the two polygons (the front and the back of a metal plate) you’ll run into problems because then you can see “into” the model. It’s necessary to create new polygons to close the gap:

![](../../assets/3726a6c10a60dae1.png)


In the Alien game this is relatively easy because an artist can close the gap manually since the mesh **isn’t** created dynamically. But in exchange the edge looks nicely frayed:

Wolfenstein creates these bridge-polygons on the fly with the help of awesome code magic:

But they are **not** created immediately! As you can see here I cut the surface a bit (**left**) but while I glitch through the surface (**right**) there is no polygon visible…

…until you set the last cut which closes the welding edge. Now all necessary polygons are created:

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/efca4dd2dafc3a9b.png)

![](../../assets/51d6710f3fd7a9fd.png)

![](../../assets/1d084db60d100ed5.png)

![](../../assets/e620bef718d2a96d.png)

(Unfortunately I’ve no idea how the Rainbow Six programmers did this but there will be a [talk about it on GDC this year](http://schedule.gdconf.com/session/the-art-of-destruction-in-rainbow-six-siege)! I hope we’ll see a wireframe rendering! :)

If you want to read more about geometry destruction you may findmy [article about slicing/destruction in Metal Gear and other games](http://simonschreibt.de/gat/metal-gear-rising-slicing/) interesting.)

Thanks for reading and feel free to drop me some feedback in the comments!

![](../../assets/ba0680151067ebbc.png)

Hey! Just wanted to thank you for these great articles! Found this blog not long ago, have read everything. I find it very exciting to see developers find creative solutions to different problems. Have a great day! -Martch

Thank you for the nice comment! Yeah it’s awesome what the coders and artists come up with. Do you prefer reading or watching the content?

Reading. ‘Cause then I can go through at my own pace and it’s easier to go back and forth through the content. TBH I am yet to watch the video from this article. :) Gonna do that now. -Martch

Hey Simon! Awesome comparison!! Thanks a lot for this! :D

I was pretty fond of the Wolfenstein cutting but never thought so much about it. They also do it on wire!!

In my opinion a little more resolution would have hurt the performance too much. This way now the dynamic pieces look a little oldschool. Interesting that when a piece is detached it actually DISAPPEARS for one frame!! :]

For the depth check shader on the glow borders: I think it would have been better to put a separate stripe on the pieces themselves. So you have automatically gone on the static parts. One could have made a softer border as well. (What I also don’t like is that these borders glow forever)

Thank you very much :) Yeah I forgot to wait some minutes and see if the borders stop glowing … but to be honest, normal players will pass these areas in 30s so no need for less glow over time :D

Yea there are some underground train areas where you spend some time and you see the borders even glowing through the dark. You’d need some age value fed into the shader instance. But might be you can do it with a 1px multiply-texture strip as well.

Anyway: I just thought about the mesh wire fence again: Of course on this thing you get okish looking glowing wire ends for free with the depth test shader!! ;]

Lol, nice comparison!!! When I played Wolfenstein, I thought it used alpha testing because of hard edges, didn’t know these were true polygons.

Love your blog man! brilliant!

Really great that you continue posting your investigations! I often visit this page to find inspiration for my job. And even re-reading older articles brings a lot of pleasure to me! Thanks for that!

As for Rainbow Six. I can assume that it’s made by dynamically created mask texture, adjusted by shader (you can see the strange edges of the cut), saving holes positions and calculating closing shapes, then, when the shape is closed, creating piece of wall, that uses the same texture that original wall, but with calculated UV offset. Maybe the wall is still solid, just with transparency mask. Guess wireframe display can help resolve this magic :)

Your guess sounds great. When the game is on sale I might look into that. Or maybe someone else does? Actually there should be a GDC talk somewhere but I didn’t see it yet. Maybe it’s only availiable in the closed GDC Vault :,(

Some real life reference:

http://i.imgur.com/Sn0lFK7.mp4