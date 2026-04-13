---
title: Simonschreibt.
url: https://simonschreibt.de/gat/homeworld-2-engines/
author: Simon
published: '2013-04-06'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/73b2487539acb354.jpg)

[Homeworld](http://www.relic.com/games/homeworld/): The trails. But the engine effects don’t *only* consist of trails.

Engine Glow

The engine glows i know, are crossed planes which maybe fade out if you look in a narrow angle at them. But Homeworld has two interesting approaches how to do engine glows.

![](../../assets/8495046dc8d67cae.gif)

*not* that strong in the game! I hope you can see, that these are three slightly animated “spheres” sticked into each other. So they get a nice volume for their engine glows for the big ships. Here you can see the geometries:

![](../../assets/1c1483a86ce7093d.gif)


The effect for smaller ships is a bit simpler. They seem to use several round sprites and scaling them down to create kind of a “tail” (move up and down if you can’t see it, maybe you’re in a bad spot of your flat screen):

In [this Wiki](http://hw2wiki.net/wiki.hw2.info/FunctionsetEngineBurn.html) you can read about a “iSparksPerPath” parameter which is described as “This graphic seems to be accomplished entirely out of one round effect repeated in the below fashon.”

It was really interesting to see this, because i saw this idea (to use several sprites for an volumetric effect) for example in [StarForge](http://www.starforge.com/):

At the “peak” of the spotlight effect you can clearly see the circles. The color bending in the wider base of the spotlight effect comes from the GIF – it looks fine in the original video! Anyway, i think it’s an interesting approach and besides of the “peak” it looks good to me.

Engine Trails

Homeworld “hides” this by covering their peak with the trail. I would have thought, that the trail is a dynamically generated crossed plane to make sure you see it from any angle. But i was wrong:

![](../../assets/7a23f4680d9cefe2.gif)

*one* plane and it looks perfect if you don’t do what i did here. That’s a really good solution in my eyes because you avoid to double the polycount. Of course, it depends of how expensive it is to align the trail to the camera of the player.

And trails aren’t the only thing they handle like that. Bullets and muzzle flashes are also “just” planes:

![](../../assets/3b98bdc8d2c535cb.gif)

![](../../assets/93d19a697948f873.gif)


![](../../assets/2ba36756096e8fe0.gif)

[define the width of them in a script file](http://hw2wiki.net/wiki.hw2.info/FunctionsetEngineTrail.html). And even if the 2 outer shapes have a function, what’s up with the one in the middle? I can’t see anything in the game:

![](../../assets/013972b254eda7c2.jpg)


Youre doing great job. Keep it up.

Thx man! I will do more as long as I have stuff to talk about :)

I don’t have any proper feedback, just wanted to let you know that highlight of any of my days is seeing more of these tricks and tips. Really good read. Thumbs up :)

Thanks man! Comments like this (and of course cool trick) make my days :)

Really interesting blog dude! I Enjoy your analysis a lot!

Thanks man! Really pushes motivation to hear that :)

The square in the middle may be used to define a 2nd LOD for the trails in order to half them when seen from afar. It’s in the very middle, simple-shaped and thick as the trail should be seen from the distance. Anyway, I’m just guessing.

An amazing blog, by the way.

Thank you very much.

Thank you for your comment and the compliment! I’m really happy to hear that you like the blog! :) But why would you half the trail? I mean it’s already only “one plane” which orients to the camera (and not e.g. a non-orienting plane model made of 2 crossed planes).

Hello.

The orientation of the trail planes and projectiles referred to in section “Engine Trails” is most likely given by vector math, so they always face the camera in the best (as in, the most frontal) way possible.

The calculation used for this finds the vector that you can use to position the vertices of your trail mesh.

The calculation should be done for each trail and is as follows:

– You know the source (or start) and destination (or end) points of the trail.

– Consider the vector ‘A’ as the vector from the start of the trail to its end ( ‘A = trail.dst – trail.src’ ).

– Consider the vector ‘B’ as the vector from the start of the trail to the position of the camera ( ‘B = camera.position – trail.src’ ).

– Calculate the vector ‘C’, which is the cross-product of vectors ‘A’ and ‘B’ ( ‘C = CrossProduct( A, B )’ ).

– You can now use ‘C’ along with the start and end points of the trail to position the four vertices that make your trail mesh:

1) trail.src + C

2) trail.src – C

3) trail.dst – C

4) trail.dst + C

With this the plane mesh will be built to face the camera in the most frontal way.

You need to disable ‘backface culling’ when rendering your trail mesh, or it might disappear depending on the position of the camera.

Although the steps may seem complicated, this procedure is quite fast. You can use it for laser-beam effects, flamethrowers etc.

Thx Kryzon! Sounds like you did such things more often in the past. Thank you for sharing your knowledge! Soon there will be a new article a bit related to this topic :) stay tuned!

Hello.

A small correction on the final step:

To find the four ideal vertex positions for the trail, the ‘C’ vector needs to be ‘normalized’ and ‘multiplied by half the width’ that you want your trail to have.

Therefore, the four vertices are positioned based on the start and end points of the trail like this:

offset = Normalize( C ) * ( trail.width / 2 )

1) trail.src + offset

2) trail.dst + offset

3) trail.dst – offset

4) trail.src – offset

The rest of the post is correct.

Thank you again :) I wish you a happy new year 2014!

I am looking for the transparency shader for Unity (I’m not a programing guy…) which does the same thing as the first engine glow so the transparency of each face at narrow angle fades to create a soften edge of the mesh, but no luck at all…

Hm sadly i can’t help since i have no clue about Unity. But maybe someone will see your post and can help :)