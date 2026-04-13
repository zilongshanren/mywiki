---
title: Protected Attributes
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_physics_sprite/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCPhysicsSprite.h>`




[List of all members.](/)


## Detailed Description

A [CCSprite](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/) subclass that is bound to a physics body. It works with:

- Chipmunk: Preprocessor macro CC_ENABLE_CHIPMUNK_INTEGRATION should be defined
- Objective-Chipmunk: Preprocessor macro CC_ENABLE_CHIPMUNK_INTEGRATION should be defined
- Box2d: Preprocessor macro CC_ENABLE_BOX2D_INTEGRATION should be defined

Features and Limitations:

- Scale and Skew properties are ignored.
- Position and rotation are going to updated from the physics body
- If you update the rotation or position manually, the physics body will be updated
- You can't eble both Chipmunk support and Box2d support at the same time. Only one can be enabled at compile time


## Property Documentation

Keep the sprite's rotation separate from the body.


The documentation for this class was generated from the following file: