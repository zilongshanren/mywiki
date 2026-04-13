---
title: How we made the Awesomenauts level art
url: http://joostdevblog.blogspot.com/2012/03/how-we-made-awesomenauts-level-art.html
author: Joost van Dongen
published: '2012-03-15'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), one of the first issues we had a good look at was how to create the graphics for our world. In

[Swords & Soldiers](http://www.swordsandsoldiers.com)all the levels were mainly randomly generated from a construction set. This looks good, but the result is rather repetitive and it is difficult to really make unique places. Also, we had quite a few people who saw screenshots of Swords & Soldiers and concluded it should be a free Flash game. Some gamers totally ignored the size and quality of the game, just because the graphical style could also be achieved in Flash. So for Awesomenauts, we wanted to step up our game and create something more painterly.

But how to go about that? Most 2D games build their levels out of square construction elements. This is very fast, but it results in rather blocky graphics, no matter how good the construction set. The ultimate example of this is of course the classic Mario games. Square construction sets can of course be a lot more free-form than this, but they remain limited nevertheless.

![](../../assets/2d40981a6d38cce4.gif)

Two games that we thought did their level graphics really well, were Wario Land: Shake It and Braid. Especially Braid achieves graphics that don't really show any patters and look gorgeous. It turned out the artist of Braid had actually written several really interesting blogpost about how the art was made, like

[this one](http://www.davidhellman.net/blog/archives/85)and

[this one](http://www.davidhellman.net/blog/archives/84).

![](../../assets/241d2da0253c28e9.jpg)

Even though Wario Land: Shake It has straighter outlines, the insides still don't really show any seams. Somehow Wario Land: Shake It uses a construction set in which repetitive elements can be spotted, but there seams cannot. At least not in the images below.

![](../../assets/7ed081a863825c35.jpg)

We didn't want to paint entire levels by hand, so we concluded that our ideal workflow would be to still have a construction set, but with completely free shapes in it. These shapes can then be put next to each other and on top of each other to together form solid shapes that make up the levels. So our artists set out creating lots of basic shapes of various sizes:

![](../../assets/c7b1a722a26b1af9.jpg)

The big question, though, is how to put these together. Our artists immediately knew that they wanted to be able to paint this over. Since the construction set elements need to be rotatable, there can hardly be any lighting in them. This would make the levels really bland, so they wanted to paint the lighting and shadows and maybe extra details on top of that.

The most obvious method to do this seems to be to just use Photoshop to piece together the elements, and then paint over that. In theory, that might work, but it has several major drawbacks. For of all, each element would become a layer, making Photoshop unworkable with thousands of layers per level. Also, Photoshop is not fast enough to handle textures with resolutions like 20,000 by 40,000 pixels. Since the levels contain really long and winding pieces of continuous art, splitting them in separate Photoshop file would make the seams between files difficult to handle.

So we concluded that Photoshop was not the right tool for this. Now since I was already building a level editor for the Ronitech (our multi-platform 2D engine), we decided to add some tools of our own to this. The scheme below shows the complete workflow that we used in the end. Note that this was used

*only*for the static geometry that the player walks over,

*not*for the backgrounds, the foregrounds or the animations in the levels.

![](../../assets/d6a7581426628c30.jpg)

How important lighting is, becomes obvious when looking at these comparisons of just the construction set elements and the painted over versions. At their core, these images might look the same, but the painted over versions just work so much more beautifully:

![](../../assets/987c00342f8efe70.jpg)

The method we used has two big drawbacks. The first is of course that it takes an enormous amount of handwork. We have all the tools to make it work from a technical standpoint, but our artists still need to paint over the entire level. This can be done relatively quickly, because the construction set elements are already there and mostly only the lighting needs to be added. Also, to save time we did mirror most of the graphics for the left and right half of the levels. But creating new levels does take way longer this way than it would have with other methods.

The other big drawback of this method is that once the level art has been finished, it is relatively cumbersome to move things around. With a design team that was constantly tweaking details in the levels really late in production, fixing the art every time cost quite a bit of time.

So for future games, we are going to use faster methods and just accept that we cannot always have the incredible hand-painted look of Awesomenauts everywhere. Making games efficiently requires having some repetition in the artwork. However, for Awesomenauts I definitely don't regret the way we approached this. I think the game looks absolutely gorgeous and part of that is because our art team painted all these beautiful lighting effects over the art, and did this uniquely everywhere in the levels. I think the end-result speaks for itself and makes the effort totally worth it!

![](../../assets/20fc246154903e92.jpg)

That's an awesome toolset! Any thoughts of commercializing it?

ReplyDeleteThose artist are awesome! Using that toolset definitely makes a huge difference. Lookin great!

ReplyDelete@Unknown: As far as I know, there are no multiplatform 2D engines available that do console games, so yes, we are actually considering commercializing this somehow at some point. :) So an interesting question there: are there indeed no multiplatform 2D console engines available right now?

ReplyDeleteIt seems UbiSoft is doing something with their UbiArt framework, are they not?

DeleteI was looking for that, but I couldn't find anything about that except some one or two years old blogposts by them. Also, I couldn't even find whether it was a complete multiplatform engine, or just a toolset that you need to plug into your own engine. Have you seen anything from them more recently?

DeleteThere was a publicity blitz related to Rayman Origins, but I haven't seen anything concrete, no. It's a shame, but it certainly opens up a very interesting avenue for you guys. Most "2d engines" are very low-level libraries (for Flash, typically), all reinventing the wheel, and something more high-level and artist focused could really work wonders.

DeleteAwesomenauts looks, well, awesome! The cartoonish graphics and crazy gameplay definitely looks like something I would like to buy. Unfortunately, I'll be sitting this one out, as I don't have a 360 or PS3. If there's a PC release at a later date, though, it's a must-buy for me.

ReplyDeleteI've been hunting for a 2d engine lately. Would definitely be interested in the awesomenauts engine. I think torque x or whatever the new iteration of torque 2d is called is multiplatform. I love the look and feel of awesomenauts though.

ReplyDeleteThe Ronitech is not available for licensing at the moment...


DeleteFrom what I have heard from other developers who used it, Torque is horrible for 2D. Unity is supposedly by itself also not very good for 2D, but there are plugins for it that make it quite a good option for 2D games. I haven't used either, though, so this is just what others tell me about them.