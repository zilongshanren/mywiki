---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_timer_target_selector/
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

| (id) | -
|

| - (id) initWithTarget: | (id) | t |
|
| selector: | (SEL) | s |
|

Initializes a timer with a target and a selector.

| - (id) initWithTarget: | (id) | t |
|
| selector: | (SEL) | s |
|
| interval: | (
|

Initializes a timer with a target, a selector, an interval in seconds, repeat in number of times to repeat, delay in seconds

| + (id) timerWithTarget: | (id) | t |
|
| selector: | (SEL) | s |
|

Allocates a timer with a target and a selector.

Allocates a timer with a target, a selector and an interval in seconds.