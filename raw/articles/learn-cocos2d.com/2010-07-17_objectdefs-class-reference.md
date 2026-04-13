---
title: ObjectDefs Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_object_defs/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Singleton that gives you access to all Object Definitions and is the central class for creating [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) types.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[ObjectDefs.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_object_defs_8h_source/)>

| (
|

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

Singleton that gives you access to all Object Definitions and is the central class for creating [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) types.

It doubles as a factory for creating [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) instances by calling createMovingObjectOfType: - you should not create [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) objects yourself but route it through this class instead by extending it as needed. That way you keep definitions central as well as error handling.

| + (id) alloc | ` [implementation]` |

| - (void) dealloc | ` [implementation]` |

| - (void) initAllObjects | ` [implementation]` |