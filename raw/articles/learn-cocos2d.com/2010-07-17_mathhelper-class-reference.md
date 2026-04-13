---
title: MathHelper Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_math_helper/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Helpful Math routines and commonly used calculations.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[MathHelper.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_math_helper_8h_source/)>

| (CGPoint) | +
|

Helpful Math routines and commonly used calculations.

| + (CCNode *) getClosestNode: | (CCNode*) | node1 |
||
| otherNode: | (CCNode*) | node2 |
||
| location: | (CGPoint) | location | ||

returns the CCNode that is closer to the given location

| + (float) getDirectionFromPoint: | (CGPoint) | point1 |
||
| toPoint: | (CGPoint) | point2 | ||

Returns the rotation angle (in degrees) to have an object at point1 rotate to and face point2.

Requires your object's image to be drawn so that they point to the right when they aren't rotated. If your images have the object point upwards then you need to add +90 to the angle.

| + (CGPoint) getDistantPointInDirection: | (float) | direction |
||
| fromLocation: | (CGPoint) | location | ||

Returns a point on the line defined by location and direction (angle in degrees) which is far away.

The intention being that the returned point is guaranteed to be outside of the screen, even if the location itself is somewhat outside the screen.

| + (float) getFixedSpeedDurationBetweenPoint: | (CGPoint) | point1 |
||
| andPoint: | (CGPoint) | point2 |
||
| forSpeed: | (float) | speed | ||

| + (CGPoint) getNormalizedDirectionVector: | (float) | direction |

returns the normalized direction vector from a rotation angle (direction)

| + (CGPoint) getTouchesLocation: | (NSSet*) | touches |

Returns the location on screen (converted to GL coordinates) of any of the touches.

| + (CGPoint) getTouchLocation: | (UITouch*) | touch |

Returns the location on screen (converted to GL coordinates) of the touch.

| + (bool) isDistanceBetweenPoint: | (CGPoint) | point1 |
||
| andPoint: | (CGPoint) | point2 |
||
| greaterThan: | (float) | distance | ||

Returns true if the distance between the two points is greater than the given distance.

| + (bool) isDistanceBetweenPoint: | (CGPoint) | point1 |
||
| andPoint: | (CGPoint) | point2 |
||
| smallerThan: | (float) | distance | ||

Returns true if the distance between the two points is smaller than the given distance.