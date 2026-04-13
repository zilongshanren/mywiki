---
title: TargetObjects Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_target_objects/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[TargetObjects](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_target_objects/) manages the landing pads, docks or whatever you choose.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[TargetObjects.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_target_objects_8h_source/)>

| (id) | -
|

` [implementation]`

[TargetObjects](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_target_objects/) manages the landing pads, docks or whatever you choose.

It tests if a path drawn to one of the Targets counts as an endpoint.

| - (void) dealloc | ` [implementation]` |

| - (id) init |

| - (bool) isPointCloseToTarget: | (CGPoint) | point |
||
| previousPoint: | (CGPoint) | prevPoint |
||
| targetType: | (
|

Checks each target location and returns true if the point is close enough to the target to land/dock there.

Previous point can be used to determine incoming angle which may be needed for some targets (for example: airstrip). TargetType determines which types of targets should be evaluated, since not all objects should be able to land/dock/etc on every target.

| + (id) targetObjects |