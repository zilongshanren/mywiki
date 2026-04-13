---
title: Simonschreibt.
url: https://simonschreibt.de/gat/teleglitch-viewcones/
author: Simon
published: '2013-01-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

[ Nox](http://en.wikipedia.org/wiki/Nox_%28video_game%29) had a very nice feature: dynamic view cones! When the player moved, they were updated in real time. What an eye catcher!

The indie game [Teleglitch](http://teleglitch.com/) also has this feature. “Awesome Simon, thank you for pointing this out. Next!”. Not so fast, little Padawan! I mention this, because they fake the view cones in a very interesting way! At first I also thought “Oh ok, they have this Nox-Effect nice.” but after a while i noticed, that they move a bit differently. And then i saw how it works.

No I didn’t! Twice. I was corrected via mail and also now via a comment from johann and i have no idea why i didn’t updated the article… but better later then never, right? *correct mode on*

~~The code extrudes black “walls” above some objects and the walls upwards to the camera. Simple but awesome. But they don’t let the black walls start directly at the top of the objects. There’s a small gap in between so you can still see the top areas of the objects/walls. I love it.~~

Here’s the quote of the mail i got:

Actually, the line of sight shadows aren’t done with perspective. They are just black polygons extruded from the walls away from the player. The math is similar to black 3d walls extruding towards the camera, but if you really look at them, they aren’t.


Since my originally thoughts are at least *similar* to the actual technique, i think i can let the following stay in the article:


Because i have no idea about math and coding, and it’s hard for me to imagine things which i can’t see. So i checked the difference of “real” view cones vs. extruded walls (which isn’t what they actualy did, but at least it’s similar). What i saw was, that the columns aren’t 100% correct, but definitely good enough. Have a look Mr. Bond:

![](../../assets/b72bbb47fef4d48a.gif)


I can only speak for myself but this impressed me a lot. This is a great idea to save the time which would be necessary to code “real” view cones. Oh and if you’re a coder and interested, one of the developers sent me a link to [the code](http://pastebin.com/x7LV33Ft).

![](../../assets/ba0680151067ebbc.png)

[Diablo 2](http://eu.blizzard.com/de-de/games/d2/)one day and they had also some of these view cones. Really interesting because they don’t have any 3D information to calculate these.

![](../../assets/ba0680151067ebbc.png)

The problem with teleglitch pseudo view cones system is that I can’t help but see them as giant black 3D geometry hovering above the play field.

Which is like it is…but i think it’s a cool work around because implementing “real” view cones could be more complicated.

But you’re right! It looks…weird :D

I never saw teleglitch “walls” as view cones… But just as.. well, black super high walls.

And it’s super fine by me, makes the small areas much more interesting.

Hehe ok, that’s another way of seeing it. But totally fine for me :)

You say D2 didn’t have 3D info, but it did. Remember there was a “3D mode” you could enable, where it used the GPU to do a perspective “bend” of the world, as though you were on a very small planet with visible curvature.

From some angles, it gave you greater view distance, from others: less. I remember flipping it on and off between different levels. It looked nicer, but sometimes was lethal :)

Yes you’re right and i just wait for the right time to do a small article about D2-Perspective-Mode. It was a bit…”wobbly” but still impressive :) Do you know more about it? Just wonder how the interpreted the 2D-Data…

This is what a Diablo 2 map editor looks like to implement the light blocking tiles.

http://bhfiles.com/files/Diablo%20II/!Modding/Knowledge%20Base/Diablo%20II%20Map%20Editor%20-%20DS1%20Editor%20Documentation/Images/walkinfo2b_big.gif

http://bhfiles.com/files/Diablo%20II/!Modding/Knowledge%20Base/Diablo%20II%20Map%20Editor%20-%20DS1%20Editor%20Documentation/Images/bitfieldv2b_big.gif

Yeah, i saw this on the website from Paul and it’s crazy. It would be really interesting to see the original tools which where used by Blizzard.

In Droid Assault we use a similar technique but we only cast the shadow over objects within rooms – including enemies – and not over the walls and floor texture. This means you can still see the basic layout of the adjacent areas but you simply can’t see what’s in them until you go look.

Awwww i love the style of your games! These droids are sooo cool :) Thanks for mentioning your tech – but unfortunately i wasn’t able to see it too well in your trailer because all moves soooo fast :) Do you have some dev papers or examples?

This article is incorrect. If you actually try to extrude walls upward you’ll end up with something a bit different.

What exactly do you find incorrect? At this GIF i tried it and yes, it looks different but comes near to the “real” viewcones: http://data.simonschreibt.de/gat002/cone_vergleich.gif

teleglitch doesn’t extrude the shadows upwards, it extrudes them away from the player.

this makes them look a bit more uneven and organic

You’re right. I corrected the article, is it better now or would you still change things?

http://simonschreibt.de/gat/teleglitch-viewcones/#update2

Hi. There no need 3d dimension to calculate this shadows. Because they are have infinite length. And you can create finite length, if you add some height value for objects to calculate length of shadow.

Nox, I think, uses a raycast technique. But not a realy honest raycast, only on “visible” (visible by PC) verticles.

In teleglitch likely used a GPU shader, which calculate a shadow on some shader standart techniques. I read article about something like this, but on russian.

From my modest exploration of Teleglitch it seems they did use 3d geometry for extruding the walls. Here’s a screenshot with the length of the extrusion toned down significantly.

That’s a great shot, but how did you reduce the extrusion? Would be awesome to know so i can update my article.

I attached a debugger to the game and edited the shader in real-time. Alternatively you can change it in the application data directory, where the shaders are in text-form (shadow_v.glsl).

Thanks for the hint! Have to try it out as soon as i find some time – currently the Render Hell Update sucks in all my spare time :D The coolest thing would be to modify the camera in teleglitch. But i guess this isn’t easily done :(

To me the Teleglitch lighting effect always seemed like they almost nailed it but missed a few tricks. The extrusions clearly look like black geometry, with a case of “once you see it, you can’t unsee it”. They also bend away from the player in an effort to show the tops of things which unfortunately gives the trick away.

I feel they should have extruded black areas vertically up from the obstructing geometry, and then rendered the black areas inverted, so they appear inside-out. This would match shadows better and also hide the structure of the black stuff (inside-out geometry is always difficult for the brain to work out). It would also allow the tops of things to be seen.

I would also make it render the light results in an offscreen buffer and be mixed in with the render so the camera could be moved away from the player slightly, that would help seal the deal. Other lighting could be mixed in, like a slight darkening for distance from player, perhaps weighted by vertical height. Mixing multiple light sources could also be an option.

thanks, these are very interesting thoughts! one could argue that from the perspective of the character the upper parts of the walls would be invisible but yes, seeing the could be a nice addition :)

I think Diablo’s way is like that, Every property in map, like wall, box, post, they have a different render layer from BG. And every property has a “shadow map” which could be stretched by the view vector from character to the property. By doing this, the property draw in the top layer, shadow draw to the middle layer, and BG draw on the base layer. The effect finished. I don’t know if it’s correct. I think it should work.