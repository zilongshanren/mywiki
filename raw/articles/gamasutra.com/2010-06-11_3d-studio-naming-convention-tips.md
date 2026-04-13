---
title: '3D Studio: Naming Convention Tips'
url: https://www.gamedeveloper.com/art/3d-studio-naming-convention-tips
author: Cathy Pyle
published: '2010-06-11'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I have been using 3D Studio since the DOS version in the 90’s. I have developed some time saving, and sometimes project saving procedures I would like to pass along here. Now I do currently use an older version of 3D Studio so improvements in performance and crashing issues have more than likely improved, but just the same these tips are good to implement.![](../../assets/16bdc8a5033e0ca2.jpg)


1. When saving a project, do your own incremental saves.

Incremental saves have saved my ass a number of times. I can’t tell you how many times I have worked on something, saved it, added something else and the program crash on me. Yeah it saves a recovery project, but more than likely it won’t be usable and will just reproduce the crash again.

I don’t use the incremental save built in; here’s why. It wants to tag a number on the “end” on the filename. This convention makes it a bitch to find the latest version when you are browsing in file explorer because of the alphabetical sorting of file names. So what I do is put my own number on the front end of the filename, and give a description afterwards like so.

00 Started Desert Scene.max

01 Built Desert ground.max

02 Added yucca plants.max

The file browser will then incrementally sort your projects by number :) I you have a really huge project, and expect more than 99 increments, just use three digits instead of two.


2. Name items using Hungarian notation.

As a software engineer, this is natural for me, but for an artist they might not be familiar with it. So here it is in a nutshell. Prefix items you construct with a lowercase letter indicating its type. For example if you make a shape for a loft, prefix it with “p” for path. If you make a mesh object, prefix it with “o”, Like this:

pTrainTrack – (A shape used as a path for the train track)

sTrainTrack – (The cross section shape of a loft)

oTrainTrack – (The lofted track resulting from the two)

Some of the common prefixes I use are as follows:

p = path

s = shape

o = object

h = helper

b = boolean object

l = light

c = camera

You get the idea…

Another ad-hoc notation I use is to add a relative indicator to the name. Say for example, you have a robot that is humanoid with two arms and two legs. So it is common to build one arm, and mirror an instance of it for the other. So for the objects on the right I add an “_R” to the end of the name, “_L” for the left, “_F” for the front, and “_B” for the back. For example

oRobotShoulder_R – (Right shoulder of robot)

oRobotShoulder_L – (Left shoulder of robot)

I personally always build the right side, front side, and top side of items as the main object and make the left side, backside, and bottom be the reference objects. This way on something like the robot, I always know that the right side of the robot is the controlling object and all parts on the left are instance or reference objects.

I realize the when you press “H” in 3DS to select an item you can turn off shapes and lights and all that sort of thing, but it is much quicker to just type “o” in the name field and it will just to all the objects or “s” for all the shapes

Well I hope this helps you out and saves you some time with your 3D modeling projects :)

You can read more and follow me and [Neuron Games, Inc.](http://www.neurongames.com/) here:![](../../assets/d49cc957e2457055.png)

![](../../assets/a4fe289f01a51ad9.png)

![](../../assets/04cbd197fdf46cd4.png)

![](../../assets/92ad448a914f2de6.png)

![](../../assets/110b447ea5e26ca8.png)