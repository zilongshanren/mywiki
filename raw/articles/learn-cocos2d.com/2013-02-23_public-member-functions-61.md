---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation/
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

A [CCAnimation](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation/) object is used to perform animations on the [CCSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/) objects.

The [CCAnimation](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation/) object contains [CCAnimationFrame](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation_frame/) objects, and a possible delay between the frames. You can animate a [CCAnimation](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animation/) object by using the [CCAnimate](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animate/) action. Example:

[sprite runAction:[[CCAnimate](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_animate/) actionWithAnimation:animation]];

Adds a frame with a texture and a rect. Internally it will create a [CCSpriteFrame](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_frame/) and it will add it. The frame will be added with one "delay unit". Added to facilitate the migration from v0.8 to v0.9.

duration in seconds of the whole animation. It is the result of totalDelayUnits * delayPerUnit

how many times the animation is going to loop. 0 means animation is not animated. 1, animation is executed one time, ...

whether or not it shall restore the original frame when the animation finishes