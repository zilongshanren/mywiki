---
title: Simonschreibt.
url: https://simonschreibt.de/gat/zelda-wind-waker-hyrule-travel-guide/
author: Simon
published: '2014-11-26'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Index

The World

Inhabitants

Activities

Thank you for choosing our Travel Guide! Now you own the perfect collection of stunning information about

**Hyrule** – the land where

[Zelda: The Wind Waker](http://www.zelda.com/windwaker/) is located in. Before you go out exploring, please read these safety-Nintendodructions:

**I.** The [first edition of this guide](http://www.polycount.com/forum/showthread.php?t=104415) was crafted by [Warby](http://www.warby.de/). I just extended it a bit and we’re both proud to present you this 2nd edition!

**II.** If you like what you see and want to support the experience, feel free to check out the new [Support Simon](http://simonschreibt.de/supportsimon/)-page.

**III.** It’s dangerous to go alone! Take this:

Now then, we wish you a great time reading through this guide and discovering some of the greatest secrets crafted by [Nintendo](http://en.wikipedia.org/wiki/Nintendo) – the ancient creators of Hyrule.




The shape of

*our* world has been seen as a disc and (since some years) is nowadays known as a sphere. The shape of the world where Hyrule is settled, has for form of a cube. The

[GameCube](http://en.wikipedia.org/wiki/GameCube).

![](../../assets/f982d662a3138a9b.jpg)

Different Worldshapes

The GameCube console was released 13 years ago (in 2001) which makes it even more respectful what Nintendo squeezed out of its hardware. We’re talking about cell-shading, cloth simulation, depth of field effects and more. The following pages will cover some of the greatest tricks and we hope you’ll be as impressed as we are.




Normally, 3D engines sort all objects and throw away what you can’t see. It might be surprising to you, but in our real world this isn’t the case. Stuff behind a wall stays there, even if you can’t see it. And so in the Zelda game! In this world, it seems that nothing gets culled. In any standard

[BSP scene](http://en.wikipedia.org/wiki/Binary_space_partitioning) nothing would be rendered behind this wall:

But as you see here, nothing gets culled. Note: Based on the changing draw call count while rotating the camera, there

*is* [view frustum culling](http://en.wikipedia.org/wiki/Frustum_culling)).

It seems that the GameCube was faster in just rendering everything instead of sorting what doesn’t need to be shown.




Hyrule is full of refreshing air and rich green grass bushes. You can cut down every single one of them and you might suspect that there surely must be some batching/instancing technique behind that amount of bushes. But if you look at the scene drawcall per drawcall, you’ll notice, that every bush is separately rendered.

Warbys observation brought up the question “What exactly is a draw call?” in Simons head and he then spent two month writing

[about rendering](http://simonschreibt.de/gat/renderhell/).

Below you can find an animation where drawcall after drawcall is shown – you can see that every plant is rendered separately.

The GameCube seems to crunch through those drawcalls very well and one reason for this is, that consoles have less clutter (driver, APIs, …) between the game and the hardware and the whole rendering process benefits from the less communication between software and hardware (read more about this in the

[mentioned article](http://simonschreibt.de/gat/renderhell/)).




One remarkable characteristic of the citizens is, that their eyes and eyebrows are always rendered **on top** of their hair (the mouth **isnt**). For some people it’s hard to get used to this “Manga Style” but you better do because the Hyrulians don’t like to get stared at.




The people in Hyrule love sport. Below you see one doing his morning exercises and he fits his feet in no-time to the stairs. Isn’t this impressive? The game is more than 12 years old and even today not every game has such a

[IK](http://www.euclideanspace.com/physics/kinematics/joints/ik/index.htm)-System implemented (but it’s worth noticing that Zelda was

**not** the first game with such a technology).

Additionally, the feet don’t only get fit to the height but also to the angle of the surface! A lovely detail in my eyes.




The residents in Hyrule love fashion! Even the monsters decorate their spears with beautiful moving streak-cloth-thingies. But simulating cloth is expensive and some skeptical tourists could think it is pre-calculated.

Today we know: It’s not! If it **would** be pre-calculated, it would **not** be able to adjust itself to various ground heights. Interestingly the cloth always assumes, that the ground it hits is flat (must be some kind of approximation / optimization. You can see this in the next picture, where the white line marks the actual orientation of the floor):

Another optimization seems to be, that characters and objects are ignored by the cloth. If you have eyes like an eagle you will spot that, in this example, the cloth doesn’t collide with the wall (the video-framerate was reduced to make it more visible):

Also non-static objects like this barrel (some Inhabitants use it as a hideout and sneak around) are excluded of the cloth simulation.

Last but not least: the fashion-piggy itself seems to be made of air from the perspective of the cloth system.

But all this is really nitpicking. It looks great and while wandering around in this beautiful world, nobody rally cares about those tiny details and we rate this sense of detail with 5 Warby & Simon stars.





Science is another big topic in Hyrule. Often executed is observing the universe by looking at the stars. If those would be based on textures, you would get pretty blurred results by looking at them with a telescope. But look at this:

The stars are made out of two triangles which makes sure that the edges always stay sharp! Another interesting detail can be observed by looking at the sky – but at daylight. By looking closely into the sun you get a nice lensflare and an even nicer HDR effect.

If you’re a professional archer, you can observe the HDR effect (and a red tint) by shooting a fire-arrow and enjoying the following explosion:

A small hint from our side: Look out for a clear sky when you want to observe the sun because clouds make the effect disappear.

Speaking of clouds: some foreigners think, that there is exactly “1” perfect swirl/whirl/twirl-cloud texture. Warby worked on multiple games where people tried to imitate that **perfect** Nintendo cartoon smoke cloud sprite texture. But newest discoveries tell us, that there are actually a whole bunch of different ones for all sorts of occasions:




Since the world of the game consists almost only of isles, driving around with a boat is kind of a forced hobby. It’s great but also dangerous if high waves push you around. The water in the game is basically one huge non-tessellated plane. So how is it possible that there are harmful waves you might ask? Well…as soon as you leave the secure waters an additional plane fades in (only visible in wireframe mode):

You can’t see this plane in-game yet, but as soon as the world decides to turn the water on, the plane fades slowly in and presents itself with a nice water-texture.

Several points shall be noticed: The plane is tessellated and therefore “real” waves can be produced. The center of the plane is always below the boat and moves with it (if you look closely you can see where the plane ends in the distance). To give the illusion of movement, the wave-texture is scrolled over the plane depending on your direction and speed.




Without Internet, the people in Hyrule have a lot free time, which some fill with catching fireflies. While running behind a shiny firefly, you may notice, that they seem to have dynamic light sources which could be kind of a performance hit.

The light tech was one of the most discussed topics, here’s an update. Thanks very much to Alex, Amandine Coget, Guillaume and James O’Hare for bumping me and [Crazy Butcher](http://www.polycount.com/forum/member.php?u=13945) and [alfalfasprossen](http://www.polycount.com/forum/member.php?u=45601) for taking the time to investigate and [think about how it was done](http://www.polycount.com/forum/showpost.php?p=2195385&postcount=382). Here are the results:
Instead of using

[Deferred lighting](http://en.wikipedia.org/wiki/Deferred_shading), they used a

[stencil buffer](http://en.wikipedia.org/wiki/Stencil_buffer) – which is a full resolution texture, masking out (using bright and black pixels), where the light actually needs to be rendered. To create this mask, they render 3 geometry spheres per light – their presence/intersection with the world create the final mask. THe following is speculation – for the 100%-truth you have to ask Nintendo.

![](../../assets/a170d3ad4ad2906b.jpg)

Only the

**back faces** are taken from the 1st sphere. And

**only its obstructed** geometry (behind the torch, wood, wall, ground) is rendered into the mask (which means that even light spheres behind walls are taken into account):


The 2nd sphere is rendered – this time the **front faces** are used when they are **not obstructed** (which means that this time hidden lights are **not** added to the mask). If you look **separately** at this draw call, it looks like this.

In the stencil buffer this mask is **overlayed** above the one which was rendered first. The result looks then like this. The areas where the first and this draw call overlap, get even brighter. This bright area is exactly what we want.


Last but not least, the 3rd sphere is added to the scene. And within its range, the **darker** values are **clamped** and only the brighter values stay in the buffer. This means, that hidden lights are clamped to black since they were **not** brightened up since they didn’t make it into the mask during the 2nd step.

After those 3 spheres, a fullscreen quad is rendered above the whole scene with the color of the light. Of course, you don’t want to have the whole scene lightened up! Therefore you render the light only where the just rendered stencil buffer mask has bright pixels.

Here’s an example of the whole process. Notice, that some lights “disappear” from the scene, since they are hidden by geometry. Like mentioned

[above](#culling), everything is rendered in Zelda. There’s no distance culling.




Games and Culture have a high standing in Hyrule and one way to live this is via shadow play. But it’s not too easy! In Zelda, only one light source at the time can influence the shading and shadow of a character. What happens when lights overlap? Well, the closest light wins the battle:

A nice detail: If a change happens, the light source seems to “jump/move” to the (now closer) light position. You can see, that the transition between old and new shadow **isn’t** happening within one frame but looks kind of smooth:

The shadows itself are really interesting too! In **our** world, everything casts a shadow. In the Zelda game only characters do! Every character in a scene gets its shadow rendered into a 128×128 texture. Only big monsters fill this texture to a major degree.

We can’t prove it, but it looks like that these shadow textures are put on an **extruded** version of the **collision** geometry. The “prove” can be found by a quick look at the shadow itself:

The shadow “cuts” the stairs. Exactly like Links feet do (which are placed on the collision geometry)! This leads to our heavy assumption, that the collision geometry is used for the shadow placement. Another clue is, that if we deactivate the drawcall where the collision geometry shows up, also the shadow is gone:

Interestingly, the collision geometry for that specific draw call doesn’t cover the whole level. It seems that somehow only special polygons/tris (near Link) are used. Here you can see Link while he runs with activated collision geometry drawcalls:

The vertices of this geometry don’t seem to be “stitched” together because you can clearly see gabs between differently oriented faces. This also supports our assumption, that the polygons were extruded to float above the surface.

Not yet enough details? Here’s something no common tourist guide would know: Carpets are geometry which “float” a bit above the ground. To avoid that your feet stick **in** the carpet, it has its own collision geometry (in addition to the ground below) which leads to a double shadow:

When a character stands in water, it looks all totally like it should. The shadow is on the water surface and all is perfect and how we would expect it:

But look how this impression changes when the major part of Links body is **below** the water surface (which doesn’t influence the shadow map generation since it was done as first render step without caring about the environment). It looks like the water is kind of transparent. Two effects by **not** changing the technique. Impressive!




Thank you for reading through the whole guide! We hope, that we could serve some useful information and we would be happy if you got motivated to start a nice tour to and through Hyrule.

For any further questions feel free to contact us! Below you can find additional sources for more information about Zelda, Hyrule and technical details.

![](../../assets/ba0680151067ebbc.png)

Update 2

[Jasper](https://twitter.com/JasperRLZ) created an amazing video about the game which is of course a must to add to this article. <3

![](../../assets/9446a06e9b7854ad.png)

![](../../assets/ba0680151067ebbc.png)

Update 3

[Robin Payot](https://twitter.com/RobinPayot) re-made a part of the game with JavaScript and ThreeJS! This is a very nice deep-dive how some of the effects can be created from scratch.

![](../../assets/1e1552035ee20ca5.jpg)

![](../../assets/ba0680151067ebbc.png)

Update 4

[Johan Peitz](https://twitter.com/johanpeitz/status/1287421324445528067?t=WTM1eO_ulI91cceBnnrqsw) re-made a scene of the game with Pico8! And he also made a nice breakdown in a Twitter-Thread. Check it out [here](https://twitter.com/johanpeitz/status/1287421324445528067?t=WTM1eO_ulI91cceBnnrqsw)!

![](../../assets/680d1e91cf4240f7.gif)

Hi!

This is a great article thank you for sharing! For a TV show project with a similar look we used a very similar technique with the water edging.

One correction I’d like to make. I don’t think deferred shading is being applied here for the fireflies. What it looks like is something similar to ‘depth-fail’ shadow volumes, but much simpler and doing an additive blend. So the trick is after you render the whole scene you disable depth writes and set your depth testing to ‘fail’ so when you issue a draw call of a sphere that overlaps a bit of ground or wall it will render fragments only if your geometry is less distance to the zbuffer, and you just make the sphere a yellow or white additive colour, and the sphere must have its normals face inwards and with backface culling enabled.

It explains why the light is a constant cut-out colour rather than having a smooth fall-off on the edges like a point light would normally have in deferred shading, but here it really suits the style of Wind Waker and it is very very cheap to render.

Thank you very much for the kind words! Oh, do you have a video of this show project? Would love to see you water edging :)

Regarding the lights: Yes, i’ve got a lot of feedback about that an will correct it asap. :)

I just added a small text to make this more clear. What do you think? It is OK or confusing, that i let the deferred rendering part in the article?

http://simonschreibt.de/gat/zelda-wind-waker-hyrule-travel-guide#update1

Yet another awesome post, shows just how much an API pays off in efficiency.

Thanks for making these, keep it up!

Thanks man :) Yeah .. it’s interesting how much communication between hardware can improve or decrease performance.

YES!

I’ve been waiting every day for a new article :)

Awww, thank you :) Sorry for making you wait so long. Took a long time again. :,(

Incredibile article, it’s hard to imagine what a man can learn from an old game.

Thank you for taking the time reading it and the kind words :) But i think it’s not totally uncommon that you can learn more from old stuff. Without many resources you have to be creative and that’s what they did :)

With the light spheres, isn’t it just a simple combination of ZTest, ZWrite and blending?

As in, you only render the light sphere geometry where it’s behind other geometry (and you render it with additive blending).

I don’t think there’s any kind of deferred lighting, not because it’s too complex, but because the light’s “halo” isn’t spherical.

Although it looks like I’ve been beaten to the punch with that one!

I completely reworked the Light-Section. Feel free to check it out :)

http://simonschreibt.de/gat/zelda-wind-waker-hyrule-travel-guide/#fireflying

Thanks for your comment! This topic is the most discussed one :) I just checked something which makes me confused. Independent of the used technology, the z-Buffer would be used for it. Right? What i already noticed is, that the z-Buffer in Zelda has only 1/2 the size of the actual resolution. So, if the z-Buffer is used for checking the “collision” with the wall, shouldn’t the edges of the light-spere not be less crisp? I’ve an example image which i would like to show. Left is the light and the edges look very sharp. The right side shows the z-Buffer which is pretty pixelated in comparison:

data.simonschreibt.de/gat050/lightcount_dephbuffer01.jpg

Ok, hoping you’re still reading replies here.

Thank you for the wonderful analysis! Found it through Warby’s post, and you really did manage to elaborate! I’ve sort of used it as my way into the more technical aspects of 3D game art, as well as a reference in a mini-thesis on techniques used to create a game with a cel-shaded visual style.

My question is; could you elaborate on the use of that 3rd sphere in the bit about stencil buffering? Reading it over and over again, I can’t figure out why it’s used, when I can imagine one could just have the engine ignore every light value beneath 100 per light source check, so speak. I’m sure this is how it’s done in the game, if you say so, but I want to better understand why. (Not pretending this is a clever question, just… Plez…)

Thank you for your time and consideration, and thanks again for this article!

Thanks, glad you like the post :) I’m not sure what you mean with “have the engine ignore every light value beneath 100 per light source check” but I think the important point is that they need a lot dynamic light sources (fireflies) and only want to render the light where the light-spheres intersect with the level-geometry so they must somehow find out what this intersection would be. Feel free to specifiy your question a bit more, I’m not sure if I understood 100% what you are looking for. :)

Hi Simon!

A friend just showed me your website, and now I am going to spend a lot of time here!

I wanted just to ask, if you have any clue of how the clouds are rendered in wind waker, they cannot be volumetrics, so I belive it’s some parallax/normal magic. Do you have any clue?

Thanks

LG

Pivetta

I hope you like the other articles :) Do you mean these clouds? http://i.imgur.com/Ig6nRZy.jpg

Hello Simon,

First of, awesome job on sharing the knowledge! It is very useful.

Now, I suppose you must have quite a few requests, but I was wondering if you could briefly show the way Windwaker setup the waterfalls/water. Just a few wireframe screenshots that would tell us more about how they set them up, if possible(I have no idea how much work making these screenshots represent). I have an idea, but I think they’ve been smarter than what I would except.

Thanks!

ben

In fact I was planning doing a small thing about the Zelda water but until that maybe this threads helps you: http://polycount.com/discussion/98578/udk-zelda-water-shader-help

You’re not alone with an interest in this style :)