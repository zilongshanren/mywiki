---
title: How To Bring A Puppet To Life (Without Satanic Rites)
url: https://www.gamedeveloper.com/art/how-to-bring-a-puppet-to-life-without-satanic-rites-
author: Giuseppe Navarria
published: '2011-02-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# How To Bring A Puppet To Life (Without Satanic Rites)

With this first of a series (I hope) of “techie-talk” posts, I’ll introduce you one of the most ancient digital necromancies: bringing an animated sprite to life. This is an extract from our devlog on www.dungeoncraftgame.com

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

With this first of a series (I hope) of “techie-talk” posts, I’ll introduce you one of the most ancient digital necromancies: bringing an animated sprite to life.

In this article I’ll use vector art, meaning that I’ll do my final 2d character using geometric shapes, but you can apply these concepts to any kind of sprite, from freehand-drawn to pixel art ones.

The animation that I’ll covecartr here is called run cycle or walk cycle in lingo, that depends if it represent a character sprinting or just walking.

Usually, in videogames, when you have a single animation for a character’s movement you try to do a sort of “fast paced walking”, something that doesn’t give the impression of someone constantly sprinting even when moving just few steps but at the same time something that’s also fast enough not to result in a sloppy and boring gameplay.

The walking animation pace in fact deeply influences gameplay: you really don’t want a character that slides around the screen so the animation pace is directly connected to the effective speed your character will move in the game. The programming-related saying fail early, fail often applies in this field too, don’t settle with the first thing you did just because you spent a lot of time making it. If you’re not an expert there’s a good chance your first tries will suck.

Now it’s time to introduce Bob, a dummy sprite I was using to make all the basic animations in the game before we switched to 3D (this is another story, I’ll cover it soon, promise!).

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/haiduds.png?width=1280&auto=webp&quality=80&disable=upscale)


A good way to “fail early” is to make rough and fast animation sketches instead of directly animating the game sprite. This will permit you to find weak spots and wrong poses in your animation even before making a single definitive sprite and adjust it before spending precious time in something that then you’ll have to scrap.

My favorite piece of software for this kind of job is an old thing called Jasc Paint Shop Pro 9 ([trial version here](http://www.oldversion.com/Paint_Shop_Pro.html)), but you can use whatever you want, from Photoshop to Flash.

If you decide to try Paint Shop Pro 9 be aware that’s now owned by Corel and the newer versions (X, X2 and so on) are totally different beasts with different purposes. You can still grab a copy of Jasc PSP9 cheaply on eBay, it should also include Animation Shop, a nice GIF animation editor, useful to test your spritesheets (Photoshop instead has this feature built-in).

We’ll make Bob run sideways, in a classic platform game style. To do so, we need to redraw him from the side, like it’s usually done in games like Super Mario Bros.

Drawing a character completely from a side usually don’t give good looking results, so we need to do some little perspective fixes to make him appear from a side but at the same time having him looking at the player:

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/platformdoodle.png?width=1280&auto=webp&quality=80&disable=upscale)


The fact that both eyes are visible is particularly important in cartoonish characters, also having the front torso showing permits to add details to the clothes that would be hard to represent in other ways.

After making this first rough sketch and happy of our result we can start to draw the frames of a whole walk cycle.

A walk or run animation is one of the easiest to make for who has a bit of experience over his shoulders thanks to the fact that a lot of studies were made about it, from [Eadweard Muybridge](http://en.wikipedia.org/wiki/Eadweard_Muybridge) work to today animation books.

At the same time this topic is also one of the hardest to get right if you’re just beginning or you still don’t know its basic concepts because in such actions every limb is in motion and in interaction with each other to preserve the equilibrium of the body.

In this case a glorious book called The Animator’s Survival Kit by Richard Williams comes to rescue us:

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/animatorsurvival.jpg?width=1280&auto=webp&quality=80&disable=upscale)


As you can see a walk cycle can be stripped down to four fundamental phases per leg: contact, down (or recoil), passing, and up (or high point).

The whole animation will consist of two of each poses, one for leg.

Still talking about legs, the movement we want to represent is the following one: one leg does contact with the ground, then slides back (in reality it stands still and it’s the rest that moves forward but we’re animating in place), contemporarily the other one goes up and forward, ready to make contact itself.

On the higher part of the body we have instead the exact opposite movement. The arm that advances is the one on the side of the leg that goes back.

Drawing all the frames one next to the other we’ll have something similar:

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/walkcycle.png?width=1280&auto=webp&quality=80&disable=upscale)


Once we do so it’s important to draw a grid to contain the frames in a more ordinated way, this will allow us to make an usable spritesheet easily and to align correctly each frame respect the others. A misaligned frame, even only by a single pixel, can really ruin your final animation as it will make your character flick a bit at each step of his walk cycle.

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/walkcycle2_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


It’s good practice to draw a cross over the character’s head to facilitate the sprite positioning inside the box, then the whole set needs to be animated and checked. I usually play it at a slow paced speed to check better eventually misaligned frames.

For this job I use Animation Shop, an utility bundled with PSP9. Adobe Photoshop instead has a built-in animation function that cycles between layers, without the need for external programs.

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/wobblywalk.gif?width=1280&auto=webp&quality=80&disable=upscale)


After finishing this fancy looking sketch, correcting wrong poses or frames, we can start to draw the actual character over it.

If you’re particularly skilled you can skip the whole sketch part, but remind that a single error during the later phases will make you waste much more time. This rough sketch purpose is in fact to show in the shortest time possible eventual errors in the animation design or in the single poses.

To draw Bob I used vector shapes, it’s a very useful method because the shapes are deformable just moving the vertices around and so it’s a good way to animate rapidly.

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/vectorart.png?width=1280&auto=webp&quality=80&disable=upscale)


I set the sketchy frames on half-opacity, then I start to copy and adapt my vector drawing to recreate the whole animation sequence:

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/walkcycle3_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


Lastly I align the drawings to the previous grid to fix eventually misaligned frames, the resulting animation is this one:

![](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2011/02/puppetwalk.gif?width=1280&auto=webp&quality=80&disable=upscale)


If you liked this techie-talk and want more articles like this one, let me know in the comments section or even better on my [main blog](http://www.dungeoncraftgame.com/blog/)! And stay tuned for news on DungeonCraft development at [http://www.dungeoncraftgame.com](http://www.dungeoncraftgame.com)!