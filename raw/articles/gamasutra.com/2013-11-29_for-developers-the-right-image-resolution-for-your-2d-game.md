---
title: 'For developers: the right image resolution for your 2D game'
url: https://www.gamedeveloper.com/art/for-developers-the-right-image-resolution-for-your-2d-game
author: Junxue Li
published: '2013-11-29'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# For developers: the right image resolution for your 2D game

This article is about how to choose graphic resolution for your 2D game art work production.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I think this article would be helpful not only to Hidden Object game developers and artists, it applies to all kinds of 2D games.

Many Hidden Object game developers often consult us, what is the right image resolution for the production of their background images. For it influences 2 aspects of the game:

Visual impact. Of course, bigger images can fit to bigger screens, which offers more details and visual impact.

Budget. Bigger resolution images have more details, so more budget in the art making.


And basically, what platform the game is for, is of upper importance. Here I list the physical resolution of some main stream devices/platforms: (in pixels)

iPad mini -1024 × 768

ipad mini 2 -2048 x 1536

ipad 4 -2048 x 1536

nexus 7 Gen2 -1920×1200

GALAXY Note 3 -1920x1080

PC

Bigfish Games: -1366x768

facebook full screen: -1284x800 (16:10)

facebook window mode: -756x473 (16:10)

Solution 1: Fill the screen

To get good graphic quality, the minimum development size of the art works should be as the same as the device resolution.

Solution 2: Future proof

Who can tell tomorrow would bring what new gaming devices? And one thing is certain, new devices always have higher resolution screens. So, to make the art works future proof, many developers choose to make the art works at 1.5~2 times the size of the current device resolution. There are true stories of developers spend money to retouch the art works to higher resolution, when port their old games(under 800x600) to ipad.

This solution takes more budget for today, but saves for tomorrow. If your game is not intended for future porting, you can disregard this solution.

Solution 3: Tolerably good

For example, you make a game for ipad4, for Solution 1, you should make art work at size 2048 x 1536; However, if the art work is made at 1600x1200, the picture quality still looks tolerably good on ipad, not as good as full size though.

If you want cut budget, you can use this tactics.

Tip: Stretch and Squash

If you want to make a cross platform game for iOS and Android, we can see from the list, that ipad 4 is 2048 x 1536, and nexus 7 Gen2 is 1920×1200. Their image ratio are different. You can make the art work at 1600x1000, when apply it to both devices, allow some stretch and squash. Chances are that the players won’t feel the nuisance. This trick would save you from the headache of making two sets of graphics, and adopt different ways of cutting the images, safe zones. So it saves budget, but certainly sacrifice graphic quality.