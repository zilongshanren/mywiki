---
title: Solid Motion
url: http://joostdevblog.blogspot.com/2011/07/solid-motion.html
author: Joost van Dongen
published: '2011-07-30'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/43f5a61e7adaa09b.jpg)


![](../../assets/43f5a61e7adaa09b.jpg)

"Solid Motion O" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20O%20-%20high.jpg)or download

[ultra high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20O%20-%20ultra%20high.jpg)

What you see here, is the

*Solid Motion*of a teapot falling down and bouncing off the ground.

*Solid Motion*is a word I made up for these kinds of shapes. So what does it mean? The idea is that when an object moves from point A to point B, there is an amount of space in between that it moves through. All this space together is what I call a Solid Motion. It is a solid object that covers that entire space.

![](../../assets/e94ecfd91a25fd23.gif)

So to generate a Solid Motion, I need an animated model. This is the animation that created the teapot image at the start of this post:

![](../../assets/292341d2f110ab1b.gif)

When you compare the two, you can see all the motions in the Solid Motion. Especially the ending position of the teapot at the bottom of the image is pretty easy to distinguish.

What I find absolutely fascinating in this technique, is that the shapes it creates are at a strange middle ground between abstract and figurative. The image above shows a falling teapot, which is totally figurative. Just a teapot falling down. However, once the Solid Motion has been generated, the teapot is hardly visible any more and the new shape is this weird, abstract thing with lots of interesting curves and spikes in its surface. So the figurative teapot became an abstract Solid Motion!

Another beautiful example is this temple being destroyed by a ball crashing into it. I especially love the curves of the pillars falling down.

![](../../assets/d82d9de2c9b6fd09.jpg)


![](../../assets/d82d9de2c9b6fd09.jpg)

"Solid Motion M" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20M%20-%20high.jpg)

![](../../assets/54ac6611a7872727.gif)

I cam up with the idea for Solid Motion after reading a book about Futurism. Futurism is an Italian art movement from the early 20th century. Futurists were fascinated by movement, especially in the new technology of the machines, planes and fast cars of the time. They did lots of artistic experiments, including theatre with strange angular costumes and even cooking, which apparently resulted in absolutely horrible meals...

The futurists were a strange bunch: they loved modern technology so much, that they were very eager to go into the Great War and play with all this speed and technology. Several of them died during World War I, including Boccioni, their most talented artist (just check

[this painting](http://masterpieceart.net/wp-content/uploads/2011/06/Umberto-Boccioni-Charge-of-the-Lancers-GC-1024x731.jpg)and

[this famous sculpture](http://digilander.libero.it/debibliotheca/Arte/boccioni/00740100.jpg)for an idea of his awesome work).

Futurism resulted in lots of interesting artworks, and their history has so many strange aspects that I could talk about them all day, but lets ignore the story of them trying to become friends with the Italian fascists (Mussolini!), and lets not turn this blog into an art history thing (although I have to admit I would enjoy that quite a lot...). The point here is that one of the things the Futurists tried to do, was to capture movement and speed in a single painting or sculpture. This made me think about modern methods to do that, which resulted in my Solid Motion script.

Enough talk, though! Here are some more Solid Motions, plus the animations that were used to generate them. I had a lot of fun playing around with some really weird materials for these, and I personally think that resulted in some pretty strong and unique images. ^_^ Be sure to check out the high resolution images as well, since they look a lot better when viewed full screen!

![](../../assets/4ce03aa95338da34.jpg)


![](../../assets/4ce03aa95338da34.jpg)

"Solid Motion I" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20I%20-%20high.jpg)or download

[ultra high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20I%20-%20ultra%20high.jpg)

![](../../assets/6a811e85e3e72a7c.gif)

![](../../assets/110aa5be044b8a79.jpg)


![](../../assets/110aa5be044b8a79.jpg)

"Solid Motion E" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20E%20-%20high.jpg)

![](../../assets/b6c5eea098e49078.gif)

![](../../assets/f25fe1f6b51d6f14.jpg)


![](../../assets/f25fe1f6b51d6f14.jpg)

"Solid Motion J" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20J%20-%20high.jpg)or download

[ultra high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20J%20-%20ultra%20high.jpg)

![](../../assets/18d371e6aca836f8.gif)

![](../../assets/5e1fb6fb757cf6d5.jpg)


![](../../assets/5e1fb6fb757cf6d5.jpg)

"Solid Motion Q" - view

[high resolution](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20Q%20-%20high.jpg)

![](../../assets/8da5466145167d7b.gif)

I made a bunch more, but the others didn't turn out as well as these. You can see the rest

[here](http://solidmotion.oogst3d.net).

So, how did I actually create these Solid Motions? Since this is a new concept (as far as I know), I had to write my own script for 3D Studio MAX to generate them. Technically, it is quite simple. It starts by copying the animating object at every frame of the animation. This gives a good basic shape. To also create a smooth outside surface, I continue to create a polygon from every edge of the model to the same edge in the next frame. And that's basically it!

![](../../assets/9ce83922aa5cdcfd.jpg)

This does create an insane amount of polygons, though. For example, "Solid Motion J" (the black and white image above) has over four million polygons! Generating that using the always slow MAXScript programming language took a looooooong time! However, since this is only intended to create images, I don't really care about efficiency here anyway.

The first version of this script is already from 2006, and I have to admit that these images were mainly made in 2009, so quite a while ago. I will post some new ones in the near future, but in the meanwhile you can also give it a try yourself! You can download the MAXScript here:

[SolidMotion.ms](http://www.proun-game.com/Oogst3D/3DHI/SolidMotion/SolidMotion%20v13.ms)

To use it, animate some objects in 3D Studio MAX, select them, then click

*MAXScript*at the top of the screen, select

*Run Script*and select the script. Be sure to bring some patience, though, since generating them may take a while! The script generates Solid Motions for all selected objects for the entire timeline. Be sure to start out with just a couple of cubes and a hundred frames, though, before trying more complex things. Long animations of objects with lots of polygons are quite likely to crash 3D Studio MAX, so start out simple!

If you make some Solid Motions of your own, then please comment below to show your results! I would love to see what kind of animations and shapes you come up with! ^_^

This must be how Tralfamadorians see the world. I love the kind of work that condenses 4D space into 3D or 2D.



ReplyDeleteAlso, it is like a modern take on the PoV-Ray "sphere sweep" object:

http://www.povray.org/documentation/view/3.6.1/63/

Good job!

Shwing! Nice pictures :-)



ReplyDeleteSome thoughts: looking at "Solid Motion O", I find it hard to see what motion makes what extrusion in the smooth motion. Perhaps it's just because the animation is so quick. Maybe another cool idea would be to generate an animation of the smooth surface growing with the movement?

Also I wonder what makes the "reptile-scales" at the peak of the bounce, and the distinct angles on the bottom of the bounce curves, the teapot is quite smooth. Could this be an effect of subsampling? This is also very visible in the second picture "Solid Motion M" on the pillar to the left and the ball after the collision, I would expect smooth surfaces.

If these are artifacts, perhaps you could fix them by doing some form of adaptive sampling: more frames when stuff goes fast. Stretching time shouldn't change the theoretical object.

Awesome idea! Looks good. I like the spiky ball one.

ReplyDeleteThere are some "scales" visible, though. What happens if an object is both rotating and moving - it seems to me like the extruding may produce undesirable results in that case.

Wow, this is really cool!


ReplyDeleteSolid Motion E is my favourite, it's strangely beautiful :)

@Bdh and Anonymous:




ReplyDeleteThe scales come indeed from combining rotation and movement. They get less when the polygon count of the original object is higher, and when the number of frames in the animation is higher.

Solving them is really difficult and complex, but to me they are not a problem: they add patterns to the surface that make them way more interesting to look at. To me, Solid Motion is not a science, but a technique that helps me create cool images. Especially the teapot image at the top would be way less pretty without the scales.

Feel free to suggest or even implement improvements, though! I don't actually know any way of fixing those scales without needing at least 10 million polygons, so I'd be interested to know a solution. :)

@Eli:

Jup, pretty similar to Povray's sphere sweep technique, although Solid Motion is way more advanced. :)

I know this is a very late comment, but I am curious to know how you made the grass effect on Solid Motion Q?

ReplyDeleteIt is just a normal object, but with a VRay Displacement Modifier and a texture that I made based on regular noise. VRay Displacement Modifier essentially turns this into real 3D, so this takes an insane amount of time to render...

Delete