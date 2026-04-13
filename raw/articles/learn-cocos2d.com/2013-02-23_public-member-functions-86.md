---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_draw_node/
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

`#import <CCDrawNode.h>`


| (void) | -
|

[CCDrawNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_draw_node/) Node that draws dots, segments and polygons. Faster than the "drawing primitives" since they it draws everything in one single batch.

draw a dot at a position, with a given radius and color

| - (void) drawPolyWithVerts: | (CGPoint *) | verts |
|
| count: | (NSUInteger) | count |
|
| fillColor: | (
|

draw a polygon with a fill color and line color

| - (void) drawSegmentFrom: | (CGPoint) | a |
|
| to: | (CGPoint) | b |
|
| radius: | (CGFloat) | radius |
|
| color: | (
|

draw a segment with a radius and color