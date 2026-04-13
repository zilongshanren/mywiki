---
title: Simonschreibt.
url: https://simonschreibt.de/gat/metal-gear-rising-slicing/
author: Simon
published: '2013-03-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

In [Metal Gear Rising](http://www.konami.jp/mgr/) you can slice objects into very small pieces. Of course, something like that was already implemented e.g. in [Tiny and Big](http://www.tinyandbig.com/), [Afro Samurai](http://en.wikipedia.org/wiki/Afro_Samurai) or [Crysis](http://www.crysis.com/). But Rising impressed me the most. It is real, free cutting. This is the tech demo:

![](../../assets/7dfb974f6693dcd9.png)


![](../../assets/7dfb974f6693dcd9.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

# Crysis

I had no idea how stuff like this is possible. So i searched in [polycount and found out](http://www.polycount.com/forum/showthread.php?t=74713) that it’s **maybe** called “[realtime cgs](http://en.wikipedia.org/wiki/Constructive_solid_geometry)“. I’m not 100% sure. And what do i do in this situation? I ask people. Crysis trees where shoot-able so i asked [Marcel](http://www.marcelschaika.com/) and he gave me an [interesting link how dynamic bool works](http://freesdk.crydev.net/display/SDKDOC3/Boolean+Destructibles) in the [CryEngine](http://www.mycryengine.com/). I installed my old Crysis version and looked at it by myself:

I’m impressed because normally if you bool something in 3Ds Max or Maya, the result is *one *object. Even if you create a gap in between, at the end it’s logically just one object. But here, the new object is independent and has its own phyisque. Cool! And that the bool object is then used to “gap” the broken surfaces is awesome:

# L4D2

Another thing mentioned by [Surfa](http://www.polycount.com/forum/member.php?u=27435) was the [Rendering Wounds in L4D2](http://www.valvesoftware.com/publications/2010/gdc2010_vlachos_l4d2wounds.pdf) technique which is also really impressive. The “just” don’t paint the pixels within a invisible sphere and fill the hole with a tasty looking wound model.

But i think this isn’t the tech which was used at Rising. Anyway, feel free to check out this [video where AirAardvark rebuilt the L4D2 wound system](http://www.youtube.com/watch?v=5_G79LJ_l2Y):

**Side note**: We don’t see these wounds in Germany because we have a strong “anti violence” politic. On the other hand, we don’t have too much problems with sex and nipples. :D

# Metal Gear Rising

We’re lucky! Because [Platinum Games](http://platinumgames.com/) (they did [MGR](http://www.konami.jp/mgr/)) not only make great games, they also [write a cool dev blog](https://www.platinumgames.com/official-blog/article/4748) (where you can download any posted video in HD, nice!). And there i found some interesting information about their slicing approach.

# Fact #1 “Slice Position”

They can define different inner surfaces “[for each part of the body.](https://data.simonschreibt.de/gat024/backup/A%20Cast%20of%20Cut-Ups.png)“. I don’t know if this means per “bone” or how they define their parts. But the picture of their blog explains what they mean:

# Fact #2 “Slice Orientation”

They can at least define what texture is used for horizontals and vertical slices: “[horizontal cuts give us an orange and vertical cuts give us a watermelon.](https://data.simonschreibt.de/gat024/backup/A%20Cast%20of%20Cut-Ups.png)“. This is pretty cool especially when it comes to cutting through android limbs.

# Fact #3 “Slice Reaction”

When you chop off parts of an enemy, they should react. Spontaneous i would say that a “dynamic” solution would be the best to avoid creating a huge amount of animation. But in Rising they weren’t satisfied with the procedural stuff and made one by one:

These are the three main facts i could collect from their blog. But i found more stuff during my observations of the game. But please remember: these i just guessing by me. Not knowing!

# Observation #1 “Dynamic Skeleton”

They not only can split the bone structure of the characters when they’re hit/dead. This special enemy shows, that it is possible every time. But in this case, with pre-defined slice points. I think this looks stunning!

# Observation #2 “Slice Depth”

It *seems*, that they also have something like a depth for their slices. Two points let me come to this point. First, the border of inner melon looks a bit low poly.


Second, a cut near the melon surface tangent shows *no *red melon flesh:

OK, you *could *use a spherical texture with border for the melon but then you would have a different border width depending how big you cut surface is and more important, it *wouldn’t* work on cube melons:

# Observation #3 “Hollow Objects”

This is nothing special but maybe worth mentioning: Objects doesn’t have to be “solid”. The can be hollow and only their solid structures are affected by the cut.

# Observation #4 “Only cut Cyborgs!”

Not every living object is cut-able. And in my books, this is better. At least i hope, that no one wants to see this sweet cat damaged! ♥

# Observation #5 “3rd Arm”

In most 3D RPGs the weapon “floats” when the character wears it at the back. This is a bit cheap i think and i was surprised that MGR does something at exactly this detail. Sure, here you don’t have a huge amount of armors and different weapons, but i like what they did very much. Maybe this inspires modern RPGs to try to avoid this floating weapon stuff with the help of a small “weapon arm”.

I also saw some “problems” or let’s say limitations. I want to underline here, that i * love* what they achieved in MGR! This is totally awesome and what i will write in some seconds is because of my interest and shall

*not*be understood as any blaming!

# Limitation #1 “Non-destructible Objects”

Before i had the game, i asked myself, if *every* object would be destroyable. Of course, this is not the case. And i think it’s better for level design and performance. But why some cars are destructible and some *aren’t*, that i don’t get.

# Limitation #2 “Balance Problem”

If you have a roof, standing on 4 columns, some games have the problem, that they don’t check the balance. So you can destroy three of the four colums and the roof would be stable until you destroy the last column. For me it seems, that MGR handles this problem in an “interesting” way:

# Limitation #3 “No Sub-Objects”

Normally you get only *two* objects when you slice one. But in some special cases, there are more then one “sub-objects” generated after a slice *without* any physical connection. But the game logic threats them as one:

# Limitation #4 “Fat Fade-Out”

Before i had the game i asked myself how they solve the problem, that after some time thousands of objects would lay around in the level. The answer: after ca. 10s the cut objects fade out:

# Limitation #5 “Inner Texture”

The definition of the inner texture has its problems when it comes to more detailed objects like this couch. You would be very surprised when you sit down on this one, because the pillows are made out of wood. ;)

# Limitation #6 “Cut Count”

When you have a lot cut objects lay around it seems that the engine doesn’t cut new parts until the engine decreases the amount of objects (by fading them out). I’m not 100% sure if this is true, but it felt like this and would make sense from a performance standpoint.

Darn you’re putting the finger on really interesting topics!! :D much appreciated! *bow*

Glad to hear you like it. Especially this article didn’t get too much attention so i’m happy that at least one person thinks it’s interesting. Ok…2 because i think that too :)

I created a demo with a similar slicing effect a while back. It had some technical information that you might find interesting:

http://www.codercorner.com/blog/?p=258

Wow! Thank you for sharing! I’ll play around with it later but the video looks very like Metal Gear :)

very nice analysis thanks for sharing

Thanks for the kind words :) I’m happy that you found it useful.

Nice article I loved this game and especially the dynamic skeleton too. Just crazy stuff. For observation #2 about the cut depth, I don’t think that is what’s going on. I think what’s happening here is there is another sphere or melon shape inside the melon that is the pink part. That would explain how the effect is achieved and how it has less geometry around the inner circumference.

Thank for your comment :) I already added this text passage, but maybe i should re-write it, so that it’s more clear. I think you are right, a 2nd geometry seems more reasonable. Since the game is now available on steam, i might get the PC version someday. Or a fellow sponsor buys it from by steam wishlist :D Anyway, then i might be able to check it out in more detail. Here is my original text passage:

“After thinking about that I’m mostly sure, that this isn’t a procedural depth. Probably they just have two geometries here: The hull of the melon (with a green cut tiling texture) and of course the inner part.”

Interesting method used in Unity:

http://danni.foxesgames.com/2015/03/29/mesh-splitting-going-open-source/#.V0I-aJErKM8

Thanks for the link! Looks interesting!

Woah, thank you doing all these research and laying it out like this. This all is super interesting and easy to understand to get an idea of how the implementation would be properly done.