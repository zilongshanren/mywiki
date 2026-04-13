---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_point_array/
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

`#import <CCActionCatmullRom.h>`


| (id) | -
|

An Array that contain control points. Used by [CCCardinalSplineTo](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_cardinal_spline_to/) and (By) and [CCCatmullRomTo](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_catmull_rom_to/) (and By) actions.

creates and initializes a Points array with capacity

get the value of a controlPoint at a given index

initializes a Catmull Rom config with a capacity hint

| - (void) insertControlPoint: | (CGPoint) | controlPoint |
|
| atIndex: | (NSUInteger) | index |
|

inserts a controlPoint at index

| - (void) replaceControlPoint: | (CGPoint) | controlPoint |
|
| atIndex: | (NSUInteger) | index |
|

replaces an existing controlPoint at index

returns a new copy of the array reversed. User is responsible for releasing this copy