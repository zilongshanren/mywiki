---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_batch_node/
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

`#import <CCParticleBatchNode.h>`


| (id) | -
|

[CCParticleBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_batch_node/) is like a batch node: if it contains children, it will draw them in 1 single OpenGL call (often known as "batch draw").

A [CCParticleBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_batch_node/) can reference one and only one texture (one image file, one texture atlas). Only the CCParticleSystems that are contained in that texture can be added to the [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_batch_node/). All CCParticleSystems added to a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) are drawn in one OpenGL ES draw call. If the CCParticleSystems are not added to a [CCParticleBatchNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_batch_node/) then an OpenGL ES draw call will be needed for each one, which is less efficient.

Limitations:

Most efficient usage

disables a particle by inserting a 0'd quad into the texture atlas

| - (id) initWithFile: | (NSString *) | fileImage |
|
| capacity: | (NSUInteger) | capacity |
|