---
title: How to make graphic list for adventure/hidden object games
url: https://www.gamedeveloper.com/art/how-to-make-graphic-list-for-adventure-hidden-object-games
author: Junxue Li
published: '2013-07-03'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# How to make graphic list for adventure/hidden object games

This article is about how to make an organized art assets list for adventure/hidden object games.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

If you are making a point&click game, adventure game or hidden object game, for each location in the game, it is essential for the game designer to make a clear graphic list. This list can communication the game design ideas across many departments. The concept artist would understand how many elements need to be drawn, the production art team may produce the graphics with nothing missing, keeping graphics in good order to manage, and the dev team may have clear idea of what to do.

The graphic list should be well organized, clearly state how many graphics for each element/object.

Part I: Graphic Categories:

We can put the graphics into the following categories:

Background;

Lighting condition change;

Story objects;

Multiple state objects;

Animations;

Hidden objects;


Let us go to details one by one:


1.Background

like this example, the background need to be made in 5 layers. ![](../../assets/283ce5ec05083de7.jpg)

![](../../assets/0d1a1daf97d97009.jpg)


On the list, write down all the layers needed. It would be better to attach a thumb nail. Make note which layers need to be complete, for parallax; And which layers need not.


2.Lighting condition change

Often in a scene, the players would lit a candle, or switch on a light. Like the following sample, there are 2 graphics needed.


![](../../assets/449d98443007929c.gif)


The lighting condition change in a scene may be global or areal. For example a small candle may only hit a small area. Generally one light source would bring one additional graphics.


3. Story objects

Story objects are key items, usually one single graphic, like keys. The item can be picked from the scene by one click.

In fact our team put all the removable single graphic objects into the story objects category, not only key items. For example, a slide door can be moved by code; Drawings on the wall, which can be erased later.


4.Multiple state objects;

The same object, which would move or change in multiple states(in discrete manner), that need multiple graphics. The most common examples are open/close of door, chest. Like this example:


![](../../assets/6635bd6042da78d4.gif)


2 graphics needed. If you need 3~5 frame inbetween for the smooth door open transition, you’d better list this graphics to “Animation” category.

Sometimes, for complicated multiple states objects, write more details, that will help the artists to better understand it. For example, 3 parts of a machine monkey scatter in the scene, the player would first pick up the parts, assemble the parts to the body, then the monkey moves in a idle cycle. You may list the graphics in this way:

(1)Monkey body with 3 parts missing;

(2)3 parts placed randomly in the scene;

(3)3 parts put on the body, one after another in certain order;

(4)Idle move (animation)


5. Animations;

Animation is usually for an object would change and move in a smooth manner, which usually demands more frames than “multiple state objects”. Make detailed description for each animation, and the frames needed. For example:


6 frames needed, loopable animation.

![](../../assets/ef3385cc5871452e.gif)


4 frames for the process of damaging a window

![](../../assets/318486ee862c0487.gif)


6 frame, loopable animation for a fish, the space movement would be handled by code;

![](../../assets/cd0d74b2f082f20c.gif)


Often the subject of animation need well textured as the background, it would be labor saving and accurate to create the animation in 3D.

![](../../assets/cfa837d7a138faa1.gif)


6. Hidden object games

For hidden object game, it needs to put many object in the picture. Write down how many objects are needed, and the Yes/No rule for the selection of objects.

![](../../assets/bb24f2d5bf07edd5.gif)



Part II, Graphic Listing

You may use a spread sheet to make the list. For each graphic, there would be the following entries:

(1)Graphic Code; For example, in our team, we use “D##” to represent background graphics, “S##” for story objects, “M##” for multiple states objects, etc.

and for the team to find each graphic on the picture easily, we put markers on the draft, like these:


![](../../assets/e64c390c892d996e.jpg)


![](../../assets/712edacd46a44d98.jpg)


(2)Graphic Name;

(3)Graphic Description;

(4)Number of graphics/frames. For multiple states objects and animations, write down the number of graphics/frames needed.


Example 1:

Code | Name | Graphic Description |
|---|---|---|
S1 | Golden Key | A luxury golden key, with skull shape deco on the head, and blue gems; |


Example 2:

Code | Name | Graphic Description | Number of graphics |
|---|---|---|---|
M3 | Machine Monkey | A machine monkey on the table, 3 parts of its body missing, which scatter in the scene. The player would first pick up the parts, assemble the parts to the body. | 7 graphics 1)Monkey body with 3 parts missing; 2)3 parts placed randomly in the scene; 3) 3 parts put on the body, one after another in certain order; |


Example 3:

Code | Name | Graphic Description | Number of graphics |
|---|---|---|---|
A2 | Mouse running | A mouse running animation in place, loopable; The movement in space will be handled by code. | 6 frames |