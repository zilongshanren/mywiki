---
title: Stereoscopic 3D
url: http://joostdevblog.blogspot.com/2010/11/stereoscopic-3d.html
author: Joost van Dongen
published: '2010-11-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com)for the Playstation 3 and

[Proun](http://www.proun-game.com)for the PC. The latter will be playable in 3D in a few weeks at the

[STRP festival](http://www.strp.nl)in Eindhoven.

I won't bother you with the technical aspects and the weird camera math of stereoscopic 3D, since I think the implications of stereoscopic 3D for graphics are a lot more interesting and not as straightforward as one might think.

The first thing to realize is that you should really consider the monitor to be a window into another world. Things may come out from this world, through the monitor towards the player, but if this happens, then these objects should not be cut-off by the edges of the screen. If an object is behind the screen in the 3D space, then the viewer's brain easily accepts that it is partially behind the monitor's edge. However, if the object is in front of the screen, yet is cut-off by the edge of the screen, then that is really weird to watch: how can an object be hidden behind something that is further away? This is called a

*window violation*. A design implication of this is that in a first person shooter, the gun cannot be in front of the monitor and thus cannot be really close to the player.

![](http://www.proun-game.com/Oogst3D/BLOG/Stereo3D%20Proun.jpg )

However, it is a lot of fun to have objects fly towards you. This looks so real, that as a player, you will want to duck to evade that coconut that is being thrown at you. So it is a good idea to put some of these effects in the game. Unfortunately, both Proun and Swords & Soldiers lack such effects, because I didn't have the time to add additional special effects just for 3D.

For pure realism, one could argue that the distance between the left and right eye in the game world should be the same as on a real person. However, as a programmer, you have control over this. Moving the virtual eyes further away from each other essentially makes the depth effect stronger. The stronger, the more spectacular, but making it too strong causes headaches.

![](../../assets/4525245a5ff63295.jpg)

A difficulty of 3D is that your eyes always focus on the screen, even though your brain thinks you are seeing objects that are behind the screen or in front of it. Because of this difference between your brain and your eyes, switching from where you are looking takes longer for stereo 3D than it does in the real world. Even worse: doing it a lot causes headaches, especially with certain people who are sensitive to this (like myself).

![](http://www.proun-game.com/Oogst3D/BLOG/Stereo3D%20focus%20distance.gif )

This is especially important to think about for the GUI. For example, in Swords & Soldiers, the healthbars are deliberately placed at the same distance as the soldiers. I would have liked to also position the map and the player's gold at this same distance, but because we also have foreground graphics, I had to place the interface in front of the foreground graphics.

![](http://www.proun-game.com/Oogst3D/BLOG/Stereo3D%20SwordsAndSoldiers.jpg )

A very cool effect in Swords & Soldiers is that because all the objects are themselves 2D, making the entire scene 3D means that all objects look like cardboard cut-outs. In a normal game that wouldn't be cool, but it works really well with the cartoony art style of Swords & Soldiers and looks awesome!

Finally, stereoscopic 3D means that certain cheap tricks cannot be used any more. Many games create rain by simple placing a rain texture on the screen, instead of having actual rain in the 3D world. With stereoscopic 3D, this trick becomes very obvious, so you need to somehow do better rain.

So, even though it is pretty easy to get 3D to work at all, it definitely takes some extra design work to make a game that works really well with stereoscopic 3D!

## No comments:

## Post a Comment