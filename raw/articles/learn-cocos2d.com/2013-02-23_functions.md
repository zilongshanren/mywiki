---
title: Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/_c_c_drawing_primitives_8h/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <Foundation/Foundation.h>`

`#import "`[ccTypes.h](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/cc_types_8h/)"

`#import "`[ccMacros.h](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/cc_macros_8h/)"

`#import <CoreGraphics/CGGeometry.h>`

| void |
|

Drawing OpenGL ES primitives.

You can change the color, point size, width by calling:

draws a Cardinal Spline path.

draws a Catmull Rom path.

| void
|

draws a circle given the center, radius and number of segments measured in points

set the drawing color with 4 unsigned bytes

set the drawing color with 4 floats

| void
|

draws a cubic bezier path measured in points.

draws a line given the origin and destination point measured in points.

draws an array of points.

draws a polygon given a pointer to CGPoint coordinates and the number of vertices measured in points. The polygon can be closed or open

draws a quad bezier path measured in points.

draws a rectangle given the origin and destination point measured in points.

draws a solid polygon given a pointer to CGPoint coordinates, the number of vertices measured in points, and a color.

draws a solid rectangle given the origin and destination point measured in points.