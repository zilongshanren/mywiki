---
title: Simonschreibt.
url: https://simonschreibt.de/gat/company-of-heroes-flamethrower/
author: Simon
published: '2013-08-20'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This blog is about games, right? So let’s play a small text adventure:

You feel a bit tired so you need a small encouragement which lets you have a look into your mirror. What do you see?

[1] A good looking effect artist! (continue reading at

– 4 –)

[2] A creative & very smart person starring back! (continue reading at– 3 –)

** – 3 – **

You feel like you want to be an effect artist! That’s why you go into the basement and boot up your personality changer. (continue reading at **– 4 –**)

** – 4 – **

You’re an effect artist. What a coincidence!! Because this article could be interesting for you.

End.

[@TychoCelchuuu](https://twitter.com/TychoCelchuuu) asked me how this beautiful effect was done. Let’s lean back, relax and look at it for a while:

If you already know what a simple particle system does, [continue reading at – 5 –](http://simonschreibt.de/gat/company-of-heroes-flamethrower#readat5)

A particle is more or less a polygon which is (most times) always aligned to the camera:

![](https://data.simonschreibt.de/gat042/blog_particles_01.jpg)

![](../../assets/f22f491206fd4ac6.jpg)

![](../../assets/1a1237d9f55f8f35.jpg)

**– 5 –**

…I’m really stunned by the technology of the [Company of Heroes](http://www.companyofheroes.com/) engine! Because you need a lot more than a simple particle system to accomplish this effect:

![](../../assets/a98c389be7fed140.gif)


- The fire sparkles are
oriented randomly but into their moving direction!*not* - The fire sparkles are
*stretched*depending on their speed! - The fire sparkles burn where they hit the ground and create a new smoke effect. This means there’s a collision detection – and we don’t talk about GPU calculated PhysX here!
- Last but not least: The core of this effect is a fire stream which
built out of a massive amount of particles. This is awesome, because the stream never interrupts even when the tank would rotate very fast! But how is the stream done?*isn’t*

![]() |
Here you can see the stream and how it deforms when the stream source is moved. Looks really neat to me!No single particles are visible. Guess what the whole thing is made of? |
![]() |
It’s a geometry. At first i thought a texture is moved along it but a close look reveals that the geometry itself is moved (especially visible at the end then the whole thing stops).I’m not 100% sure but i guess they colorize it via vertex colors so that the upper part gets first reddish and then fades out. |

But how do they prevent the viewer from seeing the geometry from the side? Here you have the answer:

![](../../assets/ece0cecf3cb34f87.gif)

[Homeworld Trails article](https://simonschreibt.de/gat/homeworld-2-engines).

The Relic effect engine is very powerful and if you want to know more you should [have a look on this presentation](http://www.slideshare.net/proyZ/relics-fx-system).

If you want to see the flame thower in action you can use these videos:

![](../../assets/d3d8bab16dd6bb91.png)


![](../../assets/d3d8bab16dd6bb91.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/ae955af4ee841def.png)


![](../../assets/ae955af4ee841def.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Thanks at [Ryan Pool](http://www.youtube.com/user/rmp135) for his help, ansers to my questions and his really cool CoH World Builder tutorials.

![](../../assets/ba0680151067ebbc.png)

YAY! Thank you! This is a really great article! Relic has some tremendous effects in their games and it’s awesome to see how they do it.

You’re welcome :)

Hmm.. Well I think the CoH flamethrower effect is nice… but would easily been done way better!

* fire is not only additive! In the CoH fx I see no grime when the flames dissolve. Look here: youtube.com/D9DkciMTsLI black smoke coming immediately from the flames.

* the direction is only forward. But fire rises! And expanding gas decelerates! So there should be some rolling, slowing down and rising flame balls

Of course motion is always tricky to fake properly without fluid sim. But It always helps to just add some particles that fake movement like that.

That’s all right, but don’t forget that the game is pretty old. Sure, for actual high-end-fx you should offer more features like you said. But it’s the other way around, i don’t see brilliant particle tech (like in CoH) in many games and most engines just cover the basics of particle systems – without any/much advanced technology.

But awesome gifs as allways!! :D

and I ♥ trails!

fix the coh steam server!!! dumbass … coh2 really sucks

I didn’t try CoH2 and played CoH only a little. But hopefully i’ll find more time to spend into the games. :)

Mike Baks The effects of the original Company of Heroes are some of the best ever! Even today full blown modern first person shooters can’t come close to the quality that Relic Entertainment delivered way back in 2006…Such a shame that the effects took a nosedive in quality with it’s sequel, Company of Heroes 2. :( :(

Yes the guys of Relic can be really proud :)

Cool effect and article. :)

However I’d like to note that there is a clear distinction between how particle data is generated and the way those particles are represented in the game world.

The core of the particle system creates raw data for each particle: position, rotation, size, color and so on. That data can be then used by different kind of renderers to create the final effect. A renderer can produce a lot of things: it could create camera facing quads mentioned in the article but also meshes (like an asteroid field), sound sources or even a crowd of animated characters.

I have a hunch is that the body of the flame above is a particle system too using a quad strip renderer where each division of the strip is a particle: location and size based on the raw particle data.

Thank you for the compliment and the comment!

You’re right. I thought especially on speed-dependant particles where you need additional parameter like direction and speed, but in general the renderer can interpret the “simple” paramters in a more complicated way :) But i don’t see that very often in games. :(

Certain effects definitely need more data: as you said the velocity vector is an important one, acceleration helps to control motion, a counter for counting collisions, an extra vector to pass down to the shader to be used in whatever manner, and the list goes on. A great way to dissect particle effects is diving into UDK’s stock content, but a lot can be learned from it.

That’s right! The UDK Tools provide several awesome examples not only for effects but also for interesting shaders/materials :D Unfortunately i never used UDK in a professional way :,(

This comment has been removed by the author.

Hi Sharon, sad that you deleted your post :,( I read it in my mail (which i got from blogger) and was really happy about that you said hello to us :)