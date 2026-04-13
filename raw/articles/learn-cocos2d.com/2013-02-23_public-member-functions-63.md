---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation_frame/
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

`#import <CCAnimation.h>`


| (id) | -
|

[CCAnimationFrame](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation_frame/) A frame of the animation. It contains information like:

| - (id) initWithSpriteFrame: | (
|

initializes the animation frame with a spriteframe, number of delay units and a notification user info

A CCAnimationFrameDisplayedNotification notification will be broadcasted when the frame is displayed with this dictionary as UserInfo. If UserInfo is nil, then no notification will be broadcasted.