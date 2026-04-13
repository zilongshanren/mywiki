---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCSpriteBatchNode.h>`


| (id) | -
|

[CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) is like a batch node: if it contains children, it will draw them in 1 single OpenGL call (often known as "batch draw").

A [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) can reference one and only one texture (one image file, one texture atlas). Only the CCSprites that are contained in that texture can be added to the [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/). All CCSprites added to a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) are drawn in one OpenGL ES draw call. If the CCSprites are not added to a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) then an OpenGL ES draw call will be needed for each one, which is less efficient.

Limitations:

creates a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) with a default capacity of 29 children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

creates a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| - (id) initWithFile: | (NSString *) | fileImage |
|
| capacity: | (NSUInteger) | capacity |
|

initializes a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and a capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

Inserts a quad at a certain index into the texture atlas. The [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) won't be added into the children array. This method should be called only when you are dealing with very big AtlasSrite and when most of the [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) won't be updated. For example: a tile map (CCTMXMap) or a label with lots of characters ([CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_label_b_m_font/))

| - (void) removeChildAtIndex: | (NSUInteger) | index |
|
| cleanup: | (BOOL) | doCleanup |
|

Updates a quad at a certain index into the texture atlas. The [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) won't be added into the children array. This method should be called only when you are dealing with very big AtlasSrite and when most of the [CCSprite](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_sprite/) won't be updated. For example: a tile map (CCTMXMap) or a label with lots of characters ([CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_label_b_m_font/))