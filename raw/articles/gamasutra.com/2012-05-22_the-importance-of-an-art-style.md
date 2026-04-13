---
title: The importance of an art-style
url: https://www.gamedeveloper.com/art/the-importance-of-an-art-style
author: Giuseppe Navarria
published: '2012-05-22'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# The importance of an art-style

People have a very wide range of tastes, something that’s undoubtedly beautiful for someone can be really horrid for someone else. Because of that, you cannot please everybody with your artistic direction, but what you can, is having an art-style.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

People have a very wide range of tastes, something that’s undoubtedly beautiful for someone can be really horrid for someone else.

Because of that, when making a game, you clearly cannot please everybody with your artistic direction. And that’s more true when we talk about games that doesn't aim to be realistically rendered and try to mimic real materials and lighting.

But what you can, and you should, is having an artistic style.

This sound stupid doesn’t it? How can you even do graphics without an art-style?

Of course my game has an art-style! It’s already fixed in the meaning of the words themselves: if you do graphics, you automatically do them in a style right?

No. Or… not quite!

While everything can be summarized in a style or another, having a meaningful, constant art style in your whole game isn’t quite as easy.

Let’s start with a definition for artistic style itself:

“[style is] any distinctive, and therefore recognizable, way in which an act is performed or an artifact made or ought to be performed and made.” Ernst Gombrich, The Art of Art History: A Critical Anthology.

The keyword there is distinctive, your game needs to have a recognizable mood in his graphics (and in music and sound of course, but we’ll talk about that another time) for it to have a proper art-style.

![goblin_style goblin_style](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/goblin_style_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


goblin_style

![](http://www.dungeoncraftgame.com/blog/wp-includes/js/tinymce/plugins/wordpress/img/trans.gif?width=1280&auto=webp&quality=80&disable=upscale)


More...

Choosing a well thought style and sticking to it is a first step in the right direction, but the path is full of pits very easy to fall into: over used and “cheap” styles.Standing on top of currently over used styles for indie developers, proudly showing his blocky figure, is the retro 8-bit style.

While pixel art per se isn’t really a style, but it’s more a way of working with graphics (you can have very different styles even doing pixel art), games that mimic the 8-bit classics look and feel are really a lot, and still on the rise.

Personally, I love pixel art, and I love a good “8-bit” look. [Dark Void Zero](http://www.youtube.com/watch?v=XdJ5nt_BmNw) and [Retro City Rampage](http://www.youtube.com/watch?v=_6sMr-qKmD4) are good examples for that.

Those titles show carefully selected palette and resolution and a cohesive style along all the game parts. Maybe they’re not really following 8-bit platforms limitations but that’s not the point. There’s a mood going on, and the game conveys that.

Choosing retro pixel art is not only a matter of what’s cool at the moment, it’s also a quick way to do art and everybody (with different results of course) can put some pixels together.

That also means that’s very easy to do uninspired pixel art, or just copycat other games, using stock-art can be another problem too, and will make your game just look lazily done (in the graphical department at least).

Just check this out:

![MadLegendOfLoot MadLegendOfLoot](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/MadLegendOfLoot_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


MadLegendOfLoot

Now, I literally LOVE these three games, but the authors definitely could spend a day (that’s kind of graphics you can definitely do in a single day), to do some original art.

[Oryx tileset](http://forums.tigsource.com/index.php?topic=8970.0) is nice and all, but your players will easily get a sense of deja-vu and maybe confusion playing another game that uses it.

In Dungeoncraft, we’re trying very hard to find and maintain an unique look, when I started, the game was using 2D vector based art, the very one you can see in this site basically, for both environment tiles and characters.

For example, this is how our “cave” tileset looked like:

![caveTileset2d caveTileset2d](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/caveTileset2d_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


caveTileset2d

I tried to find a balance between flat colors and gradients, to obtain a look that kind of reminds me of some illustrations in children’s storybooks.

I did that not only to find a compelling and not overused art style for my game, but also because I needed a way to be able to make TONS of assets quickly, and within the realm of my current skills.

When new people joined [Moonloop](http://moonloop.vg), our software house, and we decided to focus on this project again, we had to carefully think about the right way to go, I am going to do a lot more code than art now, and our character artists and animator are more confident with 3D.

3D graphics also allows us to better use our coding skills in an effort to actually enhance the style I had in mind, with the style of dynamic lighting via pixel shaders for example.

Last but not least, we’ll be able to do a lot more things that would have been way harder to achieve with 2D graphics, gameplay wise.

One thing I didn’t want to lose going for 3d models instead of sprites was that look made of abstract shapes and carefully placed gradients, so I took a day to experiment and try to go as closer as possible to my 2D art, but in 3D.

This is how a 3D tile compare against a 2D one, as you can see, perspective correction aside, it’s basically the same:

![tile2Dto3D tile2Dto3D](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/tile2Dto3D_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


tile2Dto3D

My vector was quickly replaced by a fully 3d model made of triangles:

![tile3Dwireframe tile3Dwireframe](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/tile3Dwireframe_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


tile3Dwireframe

After that, I tried to do the same with the old bearded warrior you can see on [dungeoncraftgame.com](http://www.dungeoncraftgame.com) and this was the result:

![dwarf3d dwarf3d](http://www.dungeoncraftgame.com/blog/wp-content/uploads/2012/05/dwarf3d_thumb.png?width=1280&auto=webp&quality=80&disable=upscale)


dwarf3d

This model took me way more time than drawing the original sprite of course, but animating a sprite in 8 directions, in the end, was quite more time consuming than doing a skeletal animation for our brave Giovanni, our animator.

In the end, finding a good art style for our game was way more elaborate than I thought: I had not only to think of something cool looking and suitable for our game, but also something that can actually be done in sustainable times for a small team and that make use of our existing strengths.

I think this style fits both us and our game very well now, but more than once, especially looking at other games, the thought of adding cooler graphical effects, like rim-lighting or proper ambient occlusion haunted me.

Now I always remind myself that a cohesive look that can stand out is way more important, in the end, than any fancy graphical trick.

So remember, you probably won’t find a working style for a new game under a rock or just wishing for it. You need hard work and dedication, but it’s totally worth it!

Stay tuned for more sneak peeks in our game development and more articles\rants like this one! We really cannot wait to show you more and more about [Dungeoncraft](http://www.dungeoncraftgame.com)!