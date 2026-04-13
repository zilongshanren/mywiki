---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_touch_dispatcher/
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

`#import <CCTouchDispatcher.h>`


| (void) | -
|

[CCTouchDispatcher](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_touch_dispatcher/). Object that handles all the touch events. The dispatcher dispatches events to the registered TouchHandlers. There are 2 different type of touch handlers:

The Standard Touch Handlers work like the CocoaTouch touch handler: a set of touches is passed to the delegate. On the other hand, the Targeted Touch Handlers only receive 1 touch at the time, and they can "swallow" touches (avoid the propagation of the event).

Firstly, the dispatcher sends the received touches to the targeted touches. These touches can be swallowed by the Targeted Touch Handlers. If there are still remaining touches, then the remaining touches will be sent to the Standard Touch Handlers.

Adds a standard touch delegate to the dispatcher's list. See StandardTouchDelegate description. IMPORTANT: The delegate will be retained.

| - (void) addTargetedDelegate: | (id<
|

Adds a targeted touch delegate to the dispatcher's list. See TargetedTouchDelegate description. IMPORTANT: The delegate will be retained.

| - (void) setPriority: | (int) | priority |
|
| forDelegate: | (id) | delegate |
|

Changes the priority of a previously added delegate. The lower the number, the higher the priority

Whether or not the events are going to be dispatched. Default: YES