---
title: How to make art assets list for an iOS game
url: https://www.gamedeveloper.com/art/how-to-make-art-assets-list-for-an-ios-game
author: Junxue Li
published: '2013-07-03'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This article is about how to make a complete art assets list of an iOS game. This list is for the art team to work out things, and for calculating the art budget.

Think about a simple alien-shooting game, it has a start screen, which have these buttons: “play game”, “option”, etc. And a single game play screen, a top-down view in which a soldier shoots aliens. And of course, some “achievement” and “credit” screens.

The basic idea is to break down the whole game to elements, and then make a complete list.

First have a look at the start screen, it has background image, game logo, “play game”, “options”, “Credit”, “More games…”, perhaps some animations.

Make a spreadsheet, for each item, we have those entries:

1. Item code; 2. Item name; 3. Asset category; 4. Specification; 5. Pixel size; 6. Price;

For example：

“Play game” button:

1. Item code: BN01-playGame (code should reflect the item category and info)

2.Item name: “Play game” button

3. Asset category: button

4. Specification: graphic has 2 states: normal/pressed

5. Pixel size: 200x80

6. Price: $xx

Background image:

1. Item code: BG01-start

2.Item name: Start screen background

3. Asset category: background

4. Specification: full screen, static image

5. Pixel size: 960x640

6. Price: $xx

And let us see the game play screen, we may need a background, some foreground graphics, the soldier with 5 animations(walk, idle, fire, hurt, die), a few types of aliens also with some animations, a few interactive objects, like wood crate, garbage cans, and some VFX for blast, blood splash, bullets…

As we’ve dealt with the game start screen, list every item in the spreadsheet. For example:

Soldier walking animation:

1. Item code: Ani-SD01-walk

2.Item name: soldier-walk

3. Asset category: animation

4. Specification: 32 frames, loopable, FPS=16

5. Pixel size: 120x120

6. Price: $xx

Continue, until you have listed all the items in all the game screens. To this point, congratulations! You’ve got a full list of art assets for your game!

If you hire an art contractor to do all the assets, you can leave the Price entry of every item for him to fill.