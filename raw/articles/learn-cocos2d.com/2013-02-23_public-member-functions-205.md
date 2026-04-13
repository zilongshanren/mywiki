---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_targeted_touch_handler/
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

`#import <CCTouchHandler.h>`


| (id) | -
|

[CCTargetedTouchHandler](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_targeted_touch_handler/) Object than contains the claimed touches and if it swallows touches. Used internally by TouchDispatcher

| + (id) handlerWithDelegate: | (id) | aDelegate |
|
| priority: | (int) | priority |
|
| swallowsTouches: | (BOOL) | swallowsTouches |
|

allocates a TargetedTouchHandler with a delegate, a priority and whether or not it swallows touches or not

| - (id) initWithDelegate: | (id) | aDelegate |
|
| priority: | (int) | priority |
|
| swallowsTouches: | (BOOL) | swallowsTouches |
|

initializes a TargetedTouchHandler with a delegate, a priority and whether or not it swallows touches or not