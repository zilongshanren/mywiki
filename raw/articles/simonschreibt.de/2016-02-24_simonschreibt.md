---
title: Simonschreibt.
url: https://simonschreibt.de/gat/darkmaus-topdown-trees/
author: Simon
published: '2016-02-24'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/93fc878889ce2c15.png)


![](../../assets/93fc878889ce2c15.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

I noticed a very interesting way how [Dark Maus](http://www.darkmaus.com) handles trees and vegetation. If you would give this assignment to me…

You’re allowed to use TWO sprites.

…I think my initial reaction would be to just use two sprites as frame animation (**left**) or maybe to separate trunk and tree and animate it (**right**):

From top … this is a bit harder. Following my first thought this might look like below … not the most convincing animation I must confess.

Now we’re on the same page when it comes to how my mind was working when I saw the vegetation in Dark Maus:

As you can see, the wind moves the two sprites around **but** they stay aligned and the parallax effect creates perspective and depth (of course it could also be two textures on planes but as far as I know the game is pure 2D).

**My** first impression was that it looks like leaf-layers visualizing a slightly bending tree. Here’s an example for what I mean:

You might state that the lower sprite is “just” the shadow of the tree which of course is another view on the things. I like that it’s a bit open for interpretation.

Either way the smaller plants show this clearer because there the upper and lower layer look sometimes very different:

I think it’s a very nice idea and it’s fascinating how much depth is achieved by using **two** sprites instead of only one (see the example below).

The parallax effect sells it soooo much.

Another really nice trick: If you have a big tree and look from top-down, its leafs would **occlude** the player as he walks nearby. The obvious solution is to remove the leafs and just render a trunk but this would make the tree look dried out … or you do it like in the game:

Isn’t that nice? Just the leaf-shadows are enough to tell the story of a leafy tree but by not showing them directly you avoid that the player gets occluded. Nicely done! :)

Speaking of leaf-shadows: Some time ago [Kosmonautblog](https://kosmonautblog.wordpress.com/) revealed [in this great article](https://kosmonautblog.wordpress.com/2014/03/04/tomb-raider-static-shadows-trick/) that you can **turn off all shadows** in Tomb Raider you **still** see leaf shadows!

It seems that these are “just” projected textures and not “real” shadows.

I hope you like these little tricks as I much as I do. If not, take the assignment and show us how you would go for it. :)

Have a nice day!

![](../../assets/ba0680151067ebbc.png)

[Nicolae Berbece](https://twitter.com/xelubest)mentioned the great looking

[Future Unfolding](http://www.futureunfolding.com/)where the trees seem to be made out of separately moving sprites similary to what I described above:

In fact, reading the [dev blog](http://www.spacesofplay.com/blog/why-we-built-our-own-tech-for-future-unfolding/) of this game: everything is made via particles. Crazy! :D

![](../../assets/ba0680151067ebbc.png)

I think Darkwood do this a lot better. Dark Maus is kinda ugly in some places ;)

Darkwood is in Unity so it may have 3D trees. I don’t know. As always great post Simon. Thanks!

Oh I didn’t know Darkwood – looks nice! Thanks for the hint, your comment and the kind words. :)

Really nice effect.

So, as I can see, it seems they used two textures with lowered opacity, so when they overlap creates this darkening effect where they’re one on another, if I got it right.