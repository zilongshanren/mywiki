---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_progress_timer/
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

`#import <CCProgressTimer.h>`


| (id) | -
|

CCProgresstimer is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/). It renders the inner sprite according to the percentage. The progress can be Radial, Horizontal or vertical.

Initializes a progress timer with the sprite as the shape the timer goes through

Creates a progress timer with the sprite as the shape the timer goes through

This allows the bar type to move the component at a specific rate Set the component to 0 to make sure it stays at 100%. For example you want a left to right bar but not have the height stay 100% Set the rate to be ccp(0,1); and set the midpoint to = ccp(0,.5f);

Midpoint is used to modify the progress start position. If you're using radials type then the midpoint changes the center point If you're using bar type the the midpoint changes the bar growth it expands from the center but clamps to the sprites edge so: you want a left to right then set the midpoint all the way to ccp(0,y) you want a right to left then set the midpoint all the way to ccp(1,y) you want a bottom to top then set the midpoint all the way to ccp(x,0) you want a top to bottom then set the midpoint all the way to ccp(x,1)