---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_call_func_n_d/
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

`#import <CCActionInstant.h>`


| (id) | -
|

Calls a 'callback' with the node as the first argument and the 2nd argument is data. ND means: Node and Data. Data is void *, so it could be anything.

| + (id) actionWithTarget: | (id) | t |
|
| selector: | (SEL) | s |
|
| data: | (void *) | d |
|

creates the action with the callback and the data to pass as an argument

| - (id) initWithTarget: | (id) | t |
|
| selector: | (SEL) | s |
|
| data: | (void *) | d |
|

initializes the action with the callback and the data to pass as an argument

Invocation object that has the target::selector and the parameters