---
title: 'Linkvent Calendar, Day 3: MVC with Cocos2D'
url: http://www.learn-cocos2d.com/2010/12/linkvent-calendar-day-3-mvc-cocos2d/
published: '2010-12-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Today’s link is about the Model-View-Controller (MVC) design pattern and how to implement it in Cocos2D. Bartek Wilczyński from Poland has written a two-part tutorial about how to implement this design pattern, and explains why this is a good design choice:

While I was reading that, I remembered that Jeremy Flores had created a github repository with his implementation of a MVC pattern in Cocos2D. He dubbed his project Cocos2D-MNC, as in Model-Node-Controller. The code is published under the MIT license.

The MVC pattern is somewhat similar to a game object component system that I described here. For both systems, the general idea is not to subclass CCSprite and put your game logic in there. CCSprite already is a complete visual representation class for your player, enemy, and what not. But in some cases, you need more than one sprite, or a combination of a sprite and particle effects. Once you get there, it’s much better to have a CCNode containing (aggregating) all the visual elements of your game object, while handling all the game logic of that object and updating the visual elements. The CCNode becomes the controller, controlling the views. As the views (sprites, effects, GL drawings, etc.) move on screen, the controller node polls the visual nodes for state information and runs the game logic code, which in turn may update the views.

In very simple terms, this is my pragmatic approach of the MVC pattern that also works quite well. It’s definitely already a big leap forward compared to extensively subclassing the CCSprite class. If you notice that you’re doing that a lot, you should do yourself a favor and read up on the MVC design pattern.

Add your link to the Cocos2D Linkvent Calendar

Do you have something to share with the Cocos2D community? I haven’t received enough submissions to fill all the days until Xmas, although I do have enough links to post one each day, I’d rather post a link to your website or blog post.

I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. Help me help you by browsing the products in the Learn Cocos2D Store.

TilemapKit is the complete solution for tilemap game developers. Click an image to learn more!

Iso Map rendered by TilemapKit

Ortho Map rendered by TilemapKit

Hex Map rendered by TilemapKit

Steffen's Books

The iOS Action RPG Engine

Rapidly create your own RPG or action-adventure game with this complete starter kit. Includes an ebook, game source code and a royalty-free art package. More Affiliate Products …