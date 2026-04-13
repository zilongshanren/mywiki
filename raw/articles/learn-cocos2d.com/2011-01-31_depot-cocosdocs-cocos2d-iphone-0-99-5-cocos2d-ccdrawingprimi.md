---
title: /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/CCDrawingPrimitives.h File Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_c_drawing_primitives_8h/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <Availability.h>`

`#import <Foundation/Foundation.h>`

`#import <CoreGraphics/CGGeometry.h>`

[Go to the source code of this file.](/)

Functions
|
| void | [ccDrawCircle](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#ga34d0ad7b8f0d0dbd5fb874d607d69f1d) (CGPoint center, float radius, float angle, NSUInteger segments, BOOL drawLineToCenter) |
| void | [ccDrawCubicBezier](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#ga5a391711c0aa611a06167bdd7637571f) (CGPoint origin, CGPoint control1, CGPoint control2, CGPoint destination, NSUInteger segments) |
| void | [ccDrawLine](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#ga26a514883252b7cd5461fa8472309416) (CGPoint origin, CGPoint destination) |
| void | [ccDrawPoint](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#ga049d8eec041179d6e70f2428d8ebf248) (CGPoint point) |
| void | [ccDrawPoints](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#gad545cd6e2e2350e278d8eeafcb8c3762) (const CGPoint *points, NSUInteger numberOfPoints) |
| void | [ccDrawPoly](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#gac0b6ec146da9061bfb0c29e3dd933c1a) (const CGPoint *vertices, NSUInteger numOfVertices, BOOL closePolygon) |
| void | [ccDrawQuadBezier](../../../unofficial-cocos2d-api-reference/html/group___drawing_primitives/#gae8eca0753e76b604d747dcb9f8c74cb4) (CGPoint origin, CGPoint control, CGPoint destination, NSUInteger segments) |


## Detailed Description

Drawing OpenGL ES primitives.

- ccDrawPoint
- ccDrawLine
- ccDrawPoly
- ccDrawCircle
- ccDrawQuadBezier
- ccDrawCubicBezier

You can change the color, width and other property by calling the glColor4ub(), glLineWitdh(), glPointSize().

**Warning:**- These functions draws the Line, Point, Polygon, immediately. They aren't batched. If you are going to make a game that depends on these primitives, I suggest creating a batch.