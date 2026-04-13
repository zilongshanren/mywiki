---
title: Simonschreibt.
url: https://simonschreibt.de/gat/lego-studs/
author: Simon
published: '2013-06-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/69687205139533c1.jpg)


Once upon a time there were three types of [Lego](http://www.lego.com/de-de/default.aspx) studs and every had his special character… ![](../../assets/6282fb86bd761061.jpg)


The classic was shaped exactly like in the real world. For that, he was well known by the folks but also a bit boring – he didn’t care because he got real geometry. He hung around with only *some* – but very close – friends:

![](../../assets/275296b738de407c.jpg)

*many* other studs. But you can’t tell the story fluently when you mention every stud with its full shape. That’s why they’re just “painted” on a flat surface when there are very much in one place:

![](../../assets/da4e861ed90d2e66.jpg)


Well stranger, you’re still listening? Then let me tell you some of my thoughts. But be warned: these *weren’t* made in the Lego game! Maybe they will, maybe not. I just had fun in thinking about other ways to visualize the Lego studs:

Parallax Mapping

To give the studs a more outstanding shape, you can’t just use a normal map. It doesn’t look good from more flat angles:

![](../../assets/777566bf7e41ea0e.gif)

[Bump Offset Mappig](http://udn.epicgames.com/Three/DevelopmentKitGemsParallaxOccludedMapping.html#Bump%20Offset%20mapping) or even better: [Parallax Occlusion Mapping](http://udn.epicgames.com/Three/DevelopmentKitGemsParallaxOccludedMapping.html#Parallax%20Occlusion%20mapping). For these techniques you’ll need a height map and here comes the problem: a height map of a Lego stud looks pretty “boring” and isn’t perfect since you have more or less just black and white colors and no transition inbetween:

![](../../assets/d4b74d08ca3b94e8.jpg)

[UDK](http://www.unrealengine.com/udk/), i observed something interesting:

![](../../assets/fedad5ddef9b5233.gif)


![](../../assets/7d8524ff27008597.gif)

[parallax way](http://en.wikipedia.org/wiki/Parallax_scrolling) like the in old jump ‘n run games. To make sure you don’t misunderstand: this artifacts happens because the height map doesn’t have much transitions between black and white!

The effect gets even more pronounced when you use the Parallax Occlusion Mapping:

![](../../assets/1aa35407e0961af9.gif)

![](../../assets/e7092f9475d567fc.gif)


My point is, that i found it very “likeable” that the low quality stud rendering in Lego Batman looks like the next gen rendering techniques (if you use a bad height map). I just liked that. :)

Voxel

You could also use Voxel! Forgive me if i’m wrong, but for me voxels are more or less lines which are created by pushing pixels upwards based on a height map. [The Wikipedia articles](http://en.wikipedia.org/wiki/Voxel) says something different but the base information is: real pushed geometry! This would give a nice silhouette:

![](../../assets/a4961689eff8c598.gif)

Note: Since i don’t know any voxel engine, i had to fake this effect in 3Ds Max.

One of the most famous use of voxels can be seen on Outcast. The environment looked (and in my opinion *still* looks) very organic and nice:

Tesselation

Instead of having the voxel detail all the time, you could create it dynamically with [tesselation](http://en.wikipedia.org/wiki/Tessellation_%28computer_graphics%29). It’s height map based. Distance dependent and computed on the graphic card. In real time. I would love it! So the studs near to you would pop out and be real detailed geometry.

![](../../assets/dcc9b5656ca0eb06.jpg)

Note: I don’t own a DX11 graphic card so i had to fake the effect in 3Ds Max.

Imposters

This technique fascinates me since [Neox](https://simonschreibt.de/polyphobia.de) told me about it. But i never saw it used in a game. Maybe that’s a good sign, because then it would work perfectly.

[Imposters](http://www.gamasutra.com/view/feature/2501/dynamic_2d_imposters_a_simple_.php?page=2) are basically a render of a detailed geometry placed to a plane which always points to the viewer. And you update this rendering more often the nearer it is to the viewer.

![](../../assets/d73e2ef8df53baa5.jpg)


![](../../assets/9d6b3e4bd82f7462.gif)

Note: Again, it’s a fake. I don’t know an imposter engine.

That’s it. I hope you enjoyed this article even it wasn’t about a very unique trick. I just liked the small workaround the Lego game did and thought about other solutions to render the studs.

Feel free to leave me a comment, write a [tweet](https://twitter.com/simonschreibt) or a [mail](mailto:simon@simonschreibt.de). This is what brings me the greatest joy: hearing from you guys!

**Thank you very much for reading!**

For the pixel displacement you could also use cone step mapping, which doesn’t have stairstepping effects.

Thanks for the hint! I never heard about the cone step mapping. Sounds interesting! But i think the future lies in tesselation. So you get things right (shadow, silhouette, deformation) without any artifacts. But i really like to know what else is possible. Thanks for your comment!

cone step meapping is very ineffective pipeline-wise because of its enormous pre-calculation time and the increased memory footprint is not the best solution either.

what the unreal docs describe seems to be a simple Steep Parallax Mapping (only a primary linear stepping pass) and not a real Parallax Occlusion Mapping (which would use a secant-method as the second pass to smooth out stepping artifacts)

the problem all of these fake-displacement techniques have in common is the lack of real silhouette, the surface is flat nonetheless and you will get artifacts at grazing view angles.

the future might be tesselation, but not necessarily in the form of a heightfield displacement. instead use the “classic” method and make the pins round by tesselation or stuff like that

These authors devised a way that precomputes in milliseconds.

http://www.csie.ntu.edu.tw/~cyy/publications/papers/apsipa2009.pdf

also cone map can be used as replacement for normal etc

Thank you for sharing the link! This looks really promissing!

It’s so interesting to see, how important a silhouette is. :) At the end of the UDK docs is a small experiment with parallax+silhouette but you’re right, faking isn’t the future…i guess :D

Voxels are 3D grid. You can make overhang with them, unlike heightmap. And make hole easily, without retessellating the mesh.

The sprite method is nice; remind me of Warcraft 3.

What if we had a 3D texture, the third dimension being the orientation from the camera? And what if we had a normal map to shadow the stud, like this: http://www.youtube.com/watch?v=-Q6ISVaM5Ww

Interesting. When i was getting the first knowledge about voxels it was about Outcast and there you could not have overhangs or anything like this.

Maybe the voxel tech developed more than i thought :)

Warcraft 3? They did imposters? Or do you just mean sprites?

Oh interesting video! Remembers me of the engine for the kickstarter project “Project Eternity”. A classic 2D game but with enhanced tech like normalmaps and stuff like this :)

Voxel literally means “volumetric pixel”. Saying voxels can’t do overhangs is like saying pixels are a line that curves.

An example of a popular game that uses voxels is Minecraft, it uses very large voxels that are not smoothed. Another example is Atomontage engine https://www.youtube.com/watch?v=VYfBrNOi9VM

You’re right…thanks man! :)

Outcast only used height-map information for the voxel terrain, so this technique is not able to render caves and the like. It’s a reduction of a hell of a lot of information you would need to keep in memory if you really use the third dimension in your voxel grid.

so each voxel in outcast has a location on the 2d grid and a height. you never have two or more voxels on top of each other

Thanks for clearing out. Now it’s clear to me. Voxel CAN be “3D” but for optimization purposes they did it only “2D”.

Hi Simon !

First, thanks for your curiosity and sharing all this with us :)

On the Imposters method :

From my understanding, one of the limitations lies in the view angle. As long as the view angle of the imposter billboard is about the same as the view angle that was used to bake the texture, it’s fine. But when the difference between these view angles is too extreme, the trick is revealed.

How would you takle that issue ?

Does a billboard angle controlled shader could fade in-between 3 texture “states” (top, mid, side) ? or would that just feel super weird ?

Lighting, as it is baked and always faces the camera, is another issue as well, though you could still cheaply “light” these billboards in real time with some tricks, but “stylistically” there should be constraints when rendering the texture so it adapts visually :)

The lighting issue doesn’t show in your example as the light is frontal and not moving, only the object is.

I believe LOD could also be an option :

– Closer studs are geometry

– Further are billboards/imposters (you still have silouhettes)

– Even further are flat texture

This means that all level geometry should be cut into pieces to allow proper LOD swapping. What do you think about that ?

When talking about these options, I have in mind mobile as well. For next gen, tessellation feels like the future, it’s powerful, optimized and flexible.

Thanks again for your work !

ben

Hi Ben, thank you very much for your long post! :)

To be honest, my presentation isn’t 100% correct: you would render one imposter for every of these sprites. This means: when you’re near to them, it doesn’t make sense at all!

But: you don’t update them in real time a soon as they are a bit more far away. So for far away objects you could see you update them when the camera angle changed 5° and maybe for further objets only when it changed 10° or something like this.

In my GIF i used the same stud-rendering for all sprites because it’s just a tiny fake and not a real imposter :D i just tried to present the way of using renderd textures on sprites.

If you want to know more about this, feel free to read the linked article (i linked the “Imposters” word to it) where this tech is explained very well. They bake even the shadow in the texture! Awesome :)

Yeah, tesselation is maybe the best way of doing it. And on mobile maybe doing it without geometry and only flat textures since the displays are pretty small :D

LoD would surely be possible, but then for the whole LEGO plate and not for every single stud i guess.

Thanks for all your thinking and questioning :) Really cool to “meet” people asking a lot like me :)

rendering the impostors for such small things which always look the same would be a waste of rendering time.

you know beforehand all the variations that this thingy can look. it looks the same from all left-right variations of view, so you only need to capture the variation of looking more from top or below. which would be 360 degree

you don’t need the below part, because you never will see it, halfing it to a hemisphere, 180 degree.

again, each half of it might look the same, you might only need to flip the texture on the height axis, reducing the required coverage to 90 degree.

setting a variation of 5 degree as the angle that requires a new texture, you would end up with 90/5=18 textures.

so you could pre render a flipbook texture with the about 18 texture to cover (nearly) every possible view you will ever have of such a pin.

lighting could be done using some fancy converting-the-normal-into-wordl-space stuff, if you don’t use deferred shading anyway.

definitely an interesting idea, using impostors for this ;)

-alfalfasprossen

Thank’s for the comment! Yeah…pre-rendering the stuff would also be an idea, that’s right! I just mentioned imposters because i wanted to drop some “next-gen-stud”-ideas :D pre-rendered stuff is totally usefull but i thought in my case felt a bit last-gen. hehe.

of course that’s not true, especially on the effect side (e.g. explosions) there’s pre-rendered stuff used all the time :)

You might want to try Iterative Parallax Mapping. It’s not as good (but cheaper) as POM/Relief/Cone Step Mapping and more convincing than simple Parallax / Bump Offset Mapping. You can also add some cheap fake self shadowing to the shader.

http://www.cescg.org/CESCG-2006/papers/TUBudapest-Premecz-Matyas.pdf

http://www.abload.de/img/iterativplxlego016mere.png

Thank for the links! Really interesting! By the way, you’ve a nice blog!

I cant for my life find the original article, but Sim City 4 Impostered all of its buildings. Take mesh, add decals, render, add to world and presto!

And it works delightfully well, with the whole isometric view they had!

Oh that’s a nice hint! But as far as I remember you never could rotate the camera freely in the older SimCities, right? It was always bound to 90° angles, or to I recall that wrong?