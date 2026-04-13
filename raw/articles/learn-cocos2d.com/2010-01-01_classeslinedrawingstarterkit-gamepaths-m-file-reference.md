---
title: ClassesLineDrawingStarterkit/GamePaths.m File Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_paths_8m/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[GamePaths.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_paths_8m/)"

`#import "cocos2d.h"`

`#import "`[MathHelper.h](http://www.learn-cocos2d.com/_math_helper_8h_source.html)"

`#import "`[MovingObject.h](http://www.learn-cocos2d.com/_moving_object_8h_source.html)"

## Classes | |
| class | GamePaths(Private) |
## Variables | |
| static const float |
|

We need to limit the number of path points that will be drawn per path.

This is that number. Cool, ey?

Defines how many pixels two points must be apart before the new point gets added to the [Path](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_path/).

This avoids using too much memory by adding too many points but most of all it avoids the [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/) to flip around wildly if the player's finger moved in place.