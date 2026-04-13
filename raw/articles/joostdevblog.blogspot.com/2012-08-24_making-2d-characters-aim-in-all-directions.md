---
title: Making 2D characters aim in all directions
url: http://joostdevblog.blogspot.com/2012/08/making-2d-characters-aim-in-all.html
author: Joost van Dongen
published: '2012-08-24'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)we have characters that can aim in all directions. How does that work? In a 3D game this would be quite straightforward: you just make animations in a couple of directions and blend those. Blending angles of bone-animations is a really simple thing. To make it easier, you might animate the upper body and the legs separately and blend those parts as well.

In 2D, however, this is a wholly different story. Awesomenauts characters don't have bones: the game simply gets a series of frames for each animation and shows those in order. So how to do this, then?

We started by having a look at several other games. An older game that solves this problem, is

[Abuse](http://en.wikipedia.org/wiki/Abuse_(video_game))(1996). Looking at footage from that game, I think what they did is that the upper and lower body are animated entirely separately and then combined in the game. The legs just do the walking and jumping and such, and totally ignore the aiming. The arms have been drawn for each aiming direction they support, which I think is as least 16 directions. I get the idea they did not actually animate the arms: they just drew one frame for each direction, and then move the entire frame up and down with the lower body to keep it from being too static. Not sure if this is actually the case, but that is what I think they did.

Another solution can be found in

[Capsized](http://www.capsizedgame.com/)(2011). Capsized also splits the body at the waist, but to get the aiming directions for the arms, they simply rotate the entire upper body. This is a pretty smart solution, I think, and it rotates very fluently. The character can aim in all directions with very little animation work involved. At the same time it doesn't look very natural, since the upper body very clearly just rotates as a whole, arms and head included.

*Aiming animations in Capsized. Note the smart trick they did with the lower body: it contains a bent back that becomes visible when the character looks down. It also glitches a bit at the front when the character looks up, though.*

Both Capsized and Abuse have in common that the character has been split at the waist. However, when we were working on this, we already had several characters that didn't have a clear waistline (like a belt or something like that), making it difficult to separate them easily. Since our artists had already rebuilt the first characters several times at that point (they were also exploring After Effects as an animation tool around that time), we decided to not do another redesign with a clear waistline, and to not rebuild the characters in After Effects for this.

![](../../assets/087213101808b52a.jpg)

By this time, for gameplay reasons we had already decided that characters could only aim in angles of 45 degrees, and could not aim backwards. So the player could aim in only 8 directions. This made the animation problem a lot simpler. We chose to simply animate the character in each of the directions. So for each animation (walk, idle, slide, jump, fall) our art team made animations in each direction. Since the player cannot aim backwards, and since some combinations cannot be done with our control scheme (like walking and aiming straight up), our art team had to make around three directions for each animation. This works great and looks very smooth, as you can see in the video below.

*Animations in different directions in Awesomenauts on console. Note how having completely separate animations allowed our artists to do cool stuff like showing Lonestar's teeth and eyes or Froggy's tongue under certain angles.*

![](../../assets/4abafe16c36df57d.gif)

However, when we got to porting for the PC version, this turned out to not work for that. On PC the player was to aim towards the cursor, and capping that to 45 degrees plays horribly. To solve this problem, our artists were forced to rebuild all animations in a different way. Since some of our characters still didn't have a clear waistline, the choice was made to make only the arms freely rotating. So on PC, the shooting arm always rotates towards the cursor.

Combining this with what we already had, turned out to look fantastic. There are a couple of reasons for this. First of all, our artists had drawn all characters somewhat from the side and with the shooting arm at the back. This means that the rotation point of the arm is always hidden behind the shoulders, thus nicely hiding the ugly rotation point of the arm. The other great thing is that the 45 degrees animations for the body combine well with this: while the arms rotate freely over 180 degrees, the body makes jumps every 45 degrees to follow that. This looks really slick, and makes sure that if the character is aiming upwards, he also

*looks*upwards. This is really important for making it look convincing.

Our art team did have to add the missing directions, though. So now we needed 5 directions for each animation (5, not 8, because our characters still cannot aim backwards).

*Aiming on PC is a combination of a freely rotating arm and the 45 degrees body animations from the console version.*

Making all of these animations was an enormous amount of work, and part of the reason why Awesomenauts took so long to make. However, seeing the end result, I am incredibly proud of what we achieved, and I think our art team really did a tremendous job.

For the next blogpost, I would like to discuss an important related topic that wasn't covered today: shooting. How to combine shoot animations with a moving character that needs consistent leg movement? We used a couple of quite clever tricks for that (or so I like to think), so I will explain how shooting was made in my next blogpost. See you then!

some things animation can be changed and still have effect like froggy g's tornado.if u start it then teleport it would still have effect but froggy would be walking and cant shoot

ReplyDeleteI love your blogspot

ReplyDeleteI'm actually kinda blown away you choose that option. The biggest point being extremely labour intensive, which cost time and money.


ReplyDeleteTo me animating limbs on planes with a simple skeleton looks like a viable option.

Could you elaborate on why you eliminated the 2D with rig and bones option?

I'm really curious about that.

A skeleton-system would also have been a lot of work. Then we would have needed to create a toolchain to set up those skeletons (including mapping characters in pieces to polygons to mark how parts are linked to the skeleton), exporting tools, and a system to animate those in realtime on all the different platforms we support.




DeleteAlso note that such a system would still need to allow a combination of frame-to-frame animation and skeletal animation. A 2D character cannot rotate towards the camera and things like facial animation really don't work with bones in 2D. That is a lot of extra work to get right in the toolchain.

So it would also have been a lot of work, except that the work would have partially moved from the art-team to the coding team. In general our coding team is always our bottleneck, so we try to avoid moving work there.

Note that in After Effects, our artists do use bone-like systems. "Puppet-pins" they are called there and they are more flexible than normal bones. They combine this with all kinds of other techniques, including frame-to-frame.

Nice article.



ReplyDeleteI just downloaded the demo on Xbox and kind of thought the new aiming would fit in there nicely too. But maybe you have already tried it?

After playing the first "level" and returning to the main menu I was a bit confused.

IS this an online only game? At least that is how the game looks in the trial version.

Plus I would love to have local multiplayer (possible even co-op) but then again maybe it there and the trial is limited? If so, then I would say some improvements could be made to communicate what the player is actually missing from the trial version. I at least did not get it. :-)

(hence I did not buy it)

There is local co-op, both in online matches and in offline practice matches. In the demo this is only available online, though, which is limited to 30 minutes. However, this is pretty much an online only game: Practice mode is there to practice before going online.

Delete@Joost: You're awesome man, thank you so much for sharing these techniques. Can't wait for the next blog post!

ReplyDeleteVery interesting post!

ReplyDeleteI absolutely love the art style of your team artists.

Why don’t make animation of shooting backwards while running?

ReplyDeleteThat was a gameplay decision, not an art decision. Awesomenauts would have been a pretty different game if characters would have been able to shoot backwards. Chasing an enemy is a very important part of Awesomenauts and chasing becomes totally different and much more difficult if the guy you are chasing can shoot at you while running away. We played around with this and felt the game was more fun when shooting backwards is not possible.

DeleteI think that melee attacks (or other 1-directional, like Bull) should be released in the face direction nevertheless of mouse position. E.g. D + Mouse 1 will always results as strike to the right.


DeleteWhat do you think of it?

We tried that, but most players found that scheme more confusing.

Delete