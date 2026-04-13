---
title: Simonschreibt.
url: https://simonschreibt.de/gat/doom-3-volumetric-glow/
author: Simon
published: '2013-05-01'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Doom 3 is known for its shadows but in the last days something different got my interest: the volumetric effects around lights.

Before we start, let me point something out: The aura around light is called many things. Here’s some terminology (please correct me if got this wrong):

** Glare** occurs when light is too bright and disables seeing sharp. Disappears when the light source isn’t seen directly.

** Haze** is basically fog and in our case lit by some light. You can see this even the light source isn’t visible!

** Lens flare** is an effect caused by the imperfection of the camera lens. And it’s an

Photoshop effect which was heavily overused after it was

implemented.

![](../../assets/0c7b361a6fa79fcf.jpg)

[ID](http://www.idsoftware.com/)calls them “flare” in their materials.

I alread knew three ways of doing these light effect.

- Render every glow of the frame into a big texture, blur it and overlay it with the the current frame. This costs memory but no special setup by artists. The glow is reduced automatically if the visible light area gets smaller or disappears (like glare).
- Place planes with a glowtexture around the light (the planes would have to fade out if you look in a narrow angle at them). This costs not much more memory but the effect stays even you don’t see the source of the light (like haze). Also it takes some time for artist to create these planes around every glowing area.
- Place a big glowing sprite which rotates always to the camera. But this wouldn’t work well at rectangular light areas which you find very often in Doom 3.

I created a test object with just a polygon like said in the [documentation of D3](http://www.iddevnet.com/doom3/materials.php) and added a material you find e.g. on the Doom 3 desk lamps:

The effect behaves a bit “weird”, because when you walk near a light source there’s some movement in the aura. Another artifact cen be seen in the first image (orange lights): the lower light cuts into the wall and this cut “moves”. This wouldn’t happen if you place the planes by hand (because they don’t rotate to the camera).

How did [ID](http://www.idsoftware.com/) this effect? I have no idea and also the Internet does know too much. Only one other guys [asked himself the same question](http://www.gamedev.net/topic/331826-doom-3-light-glow-effect/) but the answers weren’t satisfying. We can at least look at the wireframe:

Isn’t that beautiful? They fold and unfold a (i think) vertex colored mesh in a way, that you always get a volumetric look. I love it!

They draw this geometry only when you’re in front of the light source. If you lose direct sight, it disappears:

Depending on the angle they fade out the light by turning down the vertex colors. At least i think it’s done via vertex color. Anyway, they fade the effect out in a smooth way – i like it!

If you don’t have much graphic memory and you don’t want to let artist spend a lot of time in creating this effect by hand, i think this technique is awesome. You only have to create a polygon (quad) and add a predefined material to it. Also you can set the parameters right in the material which gives you a good control.

Have a nice day!

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

Well the source code is out now, you can check it out.

He he, that’s right. But I’m just a small artist and don’t understand the code. But maybe we get lucky and a programmer will have a look on it :)

You understand the way the algorithms and problem solving works.

Most importantly you understand the aspect of what kind of property you want to be able to represent, and that you need to abstract it in order to render it with a GPU.

It’s a small step from there to actual code.

I haven’t looked at the source but from what I can see on those images, basically what it does is calculated the silhouette (ie a list of all the edges that don’t have a visible face on both sides from the POV of the player) and are thus the borders of the drawn object, and then “expand” them, drawing a polygon strip around them.

Normally determining the silhouette and dynamically creating that strip would be somewhat complex and developers wouldn’t implement it just for the sake of that effect, but for Doom 3 it wasn’t a problem because it *already* uses silhouettes with polygon strips for its shadowing system (same principle, but from the POV of the light that’s casting a shadow), so they just recycled the algorithm for an extra effect.

That sounds logic to me but i think they must have extended the tech a bit because the base geometry for the light plane is just a quad. But the generated glow geometry is “round” at its corners. A shadow volume if the plane would be “hard-cornered” if you know what i mean.

But i really like the idea that they used their shadow tech for doing these volumes.

True. Actually, as long as the polygon is flat you can precompute the silhouette (all edges are always gonna be visible if the poly is) and if it’s convex you know you need the extra two triangles for each corner, so you can precompute the mesh for all convex shapes and then it’s just a bit of vertex shader tinkering to get the effect (all lines orientations for a corner mesh are just dependent on the screen space positions of the two segments that form the corner. The two “exterior” lines are each perpendicular to a segment, the “interior” line is at the halfway angle between them)

Maybe you’re interested that some guy implemented it into this engine:

http://www.reddit.com/r/gamedev/comments/1djnql/doom_3_volumetric_glow/

simply beautifull.

I love ID just because they solve usual and common problems just in their very own way. This use to make them very creative and technically alternative.

Anyway I should recognize that sometimes they’re right and sometimes not so…

Yeah, i’m looking forward to Doom 4 :)

Thanks for the great article – I really like this blog. There’s some discussion on Reddit if you’re interested http://www.reddit.com/r/gamedev/comments/1djnql/doom_3_volumetric_glow/

Thanks man! I saw some clicks coming from reddit in my statistics and found it :) But it’s very nice that you gave me the link! :)

This is one of Doom 3’s effects that i also paid attention too since it provides “clean” results even without HDR.

I haven’t implemented it yet, but i think the idea is very simple: the polygon edges are projected in screen space and then they’re extruded with a constant (screen space) distance from the (2D projected) center with one additional vertex for each corner (so they’re round).

Since Doom 3 does that only for visible “light” surfaces which face the camera (which is a very cheap test) and those lights are convex shapes, the geometry for this can be calculated at realtime).

~badsector

I saw you post on reddit and answered there :)

Addendum to above:

So i decided to try and implement this. Here it is running in RobGetOut’s forward render path:

http://badsector.minus.com/lbnqk1Rovw2adt

and in the deferred render path:

http://badsector.minus.com/lbgZeGZMVviPKX

The forward path looks more like Doom 3’s while the deferred looks more as if there was some blur pass with HDR (the light “bleeds” out thanks to the contrast filter).

As an extra note, i had to bring the vertices back to camera space in order to do depth testing. Which makes me wonder if it would be easier to simply calculate scale from the projection matrix and do everything in world space.

wonder if it would look better with pixel vs vertex interpolation.

Sure – or maybe with some more intersections in the “light mesh”…

Like the Haze effect, it sounds real amazing with a perfect glow behind the object. This would be a great while in capturing images and in specific in regards to photography.

Hi Viz apparel

Not sure if your link is really related to my article…

Hey Simon, I implemented this effect using C++ and OpenGL for my game, Yzer. I hope it’s okay that I used some of your gif files?

Of course, no problem! :) I added your link to the article as Update #2. I hope that’s ok for you :) Really cool to have a code example (which i can’t understand since i’m not a coder) but i’m sure this will help a lot if other programmers try to implement this tech.

Thanks for sharing!

Hey there, I implemented a very basic version of this algorithm in WebGL. Here’s the URL: https://webgl-doom-glare.vercel.app/

Source: https://github.com/michaeldll/webgl-doom-glare

Currently looking for help in improving it, if anyone’s interested.

Have a good one and thanks for the wonderfully inspiring article

Love this site!

Recently made a few enhancements to the Unity version of DoomGlow for distance based fade in and out and the ability to follow moving objects. While minor, these updates help extend this effect a bit further, especially in areas where image effects aren’t viable options at this time (mobile VR). Hopeful they’re useful to someone!

https://github.com/SuperWhimsy/DoomGlowUnity/

That’s super cool! Thanks for sharing <3