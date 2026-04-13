---
title: GameBackground Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_background/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Provides the background image/animations of the scene.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[GameBackground.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_background_8h_source/)>

| (id) | -
|

` [implementation]`

Provides the background image/animations of the scene.

Why is this a seperate class? For one, you might want to animate certain parts of the background. A seperate class that handles all the background animations makes it easier to do that. Then you might want to change the background depending on the game state or if certain events happen. Finally, you might want to have several overlapping backgrounds with transparent areas. That is also easier to do if you have your own class for that. Background is drawn at, well, the background level at the very "bottom".

| + (id) background |

initializes class and returns an autoreleased instance of the class

| - (void) dealloc | ` [implementation]` |

| - (id) init |

initializes class and returns an instance of the class, you must take care of allocating the object yourself