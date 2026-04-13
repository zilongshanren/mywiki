---
title: GameObjects Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_objects/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Contains all moving game objects which can be given a [Path](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_path/).
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[GameObjects.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_objects_8h_source/)>

| (id) | -
|

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

Contains all moving game objects which can be given a [Path](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_path/).

Determines if touch was on a [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) and if so, returns that object. Updates each [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/), schedules collision checks via ObjectCollisionTest and spawning of new objects via ObjectSpawn. Moving objects are drawn just above [GamePaths](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_paths/) and below the [GameUI](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_u_i/).

| - (void) collisionTest | ` [implementation]` |

| - (void) crashDetectedBetweenObject: | (
|

` [implementation]`

two objects have crashed, do what's necessary to stop the game

| - (void) createObjectAt: | (CGPoint) | spawnLocation |
` [implementation]` |

| - (void) dealloc | ` [implementation]` |

Returns the [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) at the location, taking into account the object collisionRadius.

get the object at a specific screen location, usually used to find which object was touched

Returns nil if no object is in the vicinity of the location.

| - (void) increaseSpawnInterval | ` [implementation]` |

| - (id) init |

initializes class and returns an instance of the class, you must take care of allocating the object yourself

| - (void) initSpawnLocations | ` [implementation]` |

| - (bool) isPositionCollisionFree: | (CGPoint) | point |
||
| collisionRadius: | (float) | radius | ||
` [implementation]` |

check if the given point is free of collisions with other objects in the given radius

| + (id) objects |

initializes class and returns an autoreleased instance of the class

| - (void) spawnObject | ` [implementation]` |

| - (void) update: | (ccTime) | delta |
` [implementation]` |

| - (void) updateObjectSpawn: | (ccTime) | delta |
` [implementation]` |