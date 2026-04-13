---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/latest/cocos2d-iphone/html/interface_c_c_follow/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.koboldtouch.com developers
|

`#import <CCAction.h>`


| (id) | -
|

| (id) | +
|

|

| BOOL |
|

[CCFollow](http://www.learn-cocos2d.com/api-ref/KoboldTouch/latest/cocos2d-iphone/html/interface_c_c_follow/) is an action that "follows" a node.

Eg: [layer runAction: [[CCFollow](http://www.learn-cocos2d.com/api-ref/KoboldTouch/latest/cocos2d-iphone/html/interface_c_c_follow/) actionWithTarget:hero]];

Instead of using [CCCamera](http://www.learn-cocos2d.com/) as a "follower", use this action instead.

creates the action with a set boundary

initializes the action with a set boundary

|
readwritenonatomicassign |

alter behavior - turn on/off boundary