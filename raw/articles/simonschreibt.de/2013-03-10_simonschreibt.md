---
title: Simonschreibt.
url: https://simonschreibt.de/gat/dead-space-3-diffuse-reflections/
author: Simon
published: '2013-03-10'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The reflections in [Dead Space 3](http://www.deadspace.com/) got my interest because they “fade out” the “deeper” they reach into the ground. This is an effect i already tried to understand in [reality](http://en.wikipedia.org/wiki/Reality) and if you have knowledge or links about it, feel free to contact me! I would love to learn more about it.

As far a i know (pls correct me if I’m wrong) this is called [diffuse reflection](http://en.wikipedia.org/wiki/Diffuse_reflection) in the real world.

[e-freak](http://www.polycount.com/forum/member.php?u=22223) mentioned, that this is maybe a tech they call Screenspace-/Real Time Local Reflections in the [CryEngine 3](http://www.mycryengine.com/). Feel free to checkout the [presentation slides](http://www.crytek.com/download/S2011_SecretsCryENGINE3Tech.ppt) (slide 29) about this topic on [their website](http://www.crytek.com/cryengine/presentations).

It’s the opposite of a “perfect” reflection which you can see in a real mirror or [Deus Ex 1](http://en.wikipedia.org/wiki/Deus_Ex):

I would love to know how exactly they did it, but for now i can only guess. For me it seems like a “last rendered frame” fake (i wrote about this [here](http://simonschreibt.blogspot.de/2013/02/sacred-2-crystal-reflexion.html)) because of two points:

* #1 *Look at the chair to the right. The reflection looks like the image was stretched “down”. This works perfect on objects with mostly vertical edges, but these concave forms say to me “Simon, I’m not raytraced”.

* #2 *You (not you, but Isaac Clarke, the guy on the picture) has a weird influence on the reflection. It looks like he is also “stretched” into the reflection.

For the real world, I already could collect two interesting information about diffuse reflections:

* #1 *They are angle depended. The smaller the angle between the viewer and the reflecting surface, the stronger the reflection. This is why the reflection fades out. It’s called

[Fresnel equation](http://en.wikipedia.org/wiki/Fresnel_equations). By the way: the “s” in Fresnel is

*not*spoken because this guy was French. So just say “Frenel”.

![](../../assets/f5ca971f1d2901c9.jpg)

This effect is visible very well in the game when you see it in movement. For that, they get a “Fox Point” because of their smartness. Look how the reflections get stronger the more the camera decreases its angle to the ground:

* #2 *They get blurred

**.**I’m not sure if this is true, but for me it seems that the reflection is not only faded in their intensity but also blurred the “deeper” it goes. But this isn’t made in Dead Space as far as i see.

I really like that the developers invested time into this effect because i liked it already in reality and to see this in a game makes me happy. I hope for more stuff like this on the upcoming next gen consoles.

[Local Image-based Lighting With Parallax-corrected Cubemap](http://seblagarde.wordpress.com/2012/11/28/siggraph-2012-talk/)

[James made a tech demo of diffuse reflections](http://lightway3d.blogspot.de/2012/05/glossy-screen-space-reflections.html)

[Litheon does some experiments with real time local reflections](http://www.gamedev.net/blog/1323/entry-2254101-real-time-local-reflections/)

[Physical Based Lighting of the new Killzone (PS4)](http://www.youtube.com/watch?v=_29M8F-sRsU&feature=youtu.be)

![](../../assets/ba0680151067ebbc.png)

[Nicolae](https://twitter.com/xelubest)recorded this video for us and shows how the reflections in Deus Ex were made! The classic mirrored-geometry trick! <3

By the way, he also shared the console command to actually enable the wireframe:

In order to get this effect set launch option on the game on steam **“-hax0r”** then in-game, press **“Y”** for chat, and press **backspace** until you delete the **“TeamSay”** and then just enter the command after the the ones you need are:

**“ghost”**for noclip**“set DeusEx.JCDentonMale Airspeed 10”**for better movement control**“rmode 1”**to make wireframes visible

And to get rid of the **HUD**:

togglecrosshair

togglehitdisplay

togglecompass

toggleaugdisplay

toggleobjectbelt

toggleammodisplay

And he provided this video from a game, we’re not exactly sure about how it is named. If you know the name, let us know!

![](../../assets/ba0680151067ebbc.png)

This comment has been removed by a blog administrator.

Yes those are screenspace reflections. Some kind of limited raytracing inside the g-buffer afaik. I’m not sure about the technical bits, but I know the ‘leaking’ of foreground elements into the reflection is a limitation of doing things in screenspace. (the way i understand (i could be wrong, I only understand these things at a fairly high level), if a reflection vector points to a pixel that is occluded by a foreground pixel it will be forced to take that foreground pixel)

The parallax corrected cubemap approach seems to be the most promising, since it’s more cheap and doesn’t suffer from the 2.5d screenspace limitation — although it has the 2.5d cubemap limitation :) but it seems to look plausible enough most of the time.

Re-rendering the scene to a reflection plane is more accurate, but much more expensive. Games likes Half Life 2 do that, they also have the animated normalmaps to nicely hide the resolution limits of the render-to-texture approach. In the Deus Ex shot they seem to use a BSP portal mirror technique. This is one of those cool features of the first Unreal engine. There’s custom maps which show non Euclidean maps. It also did coronas (first that did it?) and even had heightmapped fog. UE was really ahead of it’s time back in the late nineties. Id also introduced mirrors like that since Quake3 I think — though I’ve read a programmer state they are fairly trivial to add into Q1. Q3 pioneered texture shaders and all around the same time. Seems like stuff that’s for given now, but was really amazing at the time.

The Build engine also used portals to fake room-above-room, since it’s raycasting pseudo-3D.

Hehe yeah, the good old times. I remember also that i was really impressed by the graphics uf the Unreal 1 Engine :,)

I added a link about phyical based lighting of the new killzone (ps4). You can find it at the end of the article.

The Deus Ex screenshot reminds me of the days before shaders (like NBA on the first Playstation), where you would make a reflective floor by simply modelling the reflected parts of the room flipped upside-down under the floor, and make the floor transparent so the “mirror image” shows through. The limit of how much geometry you could render gave extra reason to simulate a “diffuse reflection” — only model the parts of the set that touch the floor or are really bright. For example, only the legs of the players, the courtside billboards, and stadium lights were “reflected”. Google Image Search for “NBA Live PSX” to see.

Thanks for mentioning! Another nice trick was to give the mipmaps of the floor texture different transparency values. If for example the further away mimaps where more transparent, you got some kind of total reflection :)

what a great article, love the comments about old tech… trip down memory lane… wonder what people will look back at from 2034 saying “can’t believe they had that stuff in 2014”!

also, never heard of animated normal maps in half-life 2 will have to look that up

Thanks man! Good to hear! Yeah, maybe they will be impressed that we already do physical based rendering :D

Sorry for not going into the screenspace thing: I think we did the “reflections” the same way Deus Ex did in “Sportfischen Professional” some ages ago:

https://duckduckgo.com/?q=Sportfischen+Professional&t=ffab&iax=1&ia=images

Its treacherously calm on the water all the times ;]

I’ll ask some peeps for more insight.

Bit late to the party, but that last video is from Wii Sports Resort

Thank you! I’ve added a link to the game :)