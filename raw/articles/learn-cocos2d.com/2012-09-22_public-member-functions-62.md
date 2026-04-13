---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone-mac/html/interface_c_c_animation_frame/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-mac
2.0
Improved Cocos2D API Reference (Mac OS X version) for www.kobold2d.com developers
|

`#import <CCAnimation.h>`


| (id) | -
|

[CCAnimationFrame](http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone-mac/html/interface_c_c_animation_frame/) A frame of the animation. It contains information like:

| - (id) initWithSpriteFrame: | (
|

initializes the animation frame with a spriteframe, number of delay units and a notification user info

A CCAnimationFrameDisplayedNotification notification will be broadcasted when the frame is displayed with this dictionary as UserInfo. If UserInfo is nil, then no notification will be broadcasted.