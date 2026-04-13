---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCSpriteBatchNode.h>`


| id |
|

[CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) is like a batch node: if it contains children, it will draw them in 1 single OpenGL call (often known as "batch draw").

A [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) can reference one and only one texture (one image file, one texture atlas). Only the CCSprites that are contained in that texture can be added to the [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/). All CCSprites added to a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) are drawn in one OpenGL ES draw call. If the CCSprites are not added to a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) then an OpenGL ES draw call will be needed for each one, which is less efficient.

Limitations:

| id CCSpriteBatchNode::batchNodeWithFile: | ( | NSString * | fileImage | ) | ` [static, virtual]` |

creates a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) with a default capacity of 29 children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| id CCSpriteBatchNode::batchNodeWithFile:capacity: | ( | NSString * | fileImage, |
| [capacity] NSUInteger | capacity |
||
| ) | ` [static, virtual]` |

creates a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| id CCSpriteBatchNode::initWithFile:capacity: | ( | NSString * | fileImage, |
| [capacity] NSUInteger | capacity |
||
| ) | ` [virtual]` |

initializes a [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and a capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| void CCSpriteBatchNode::removeChildAtIndex:cleanup: | ( | NSUInteger | index, |
| [cleanup] BOOL | doCleanup |
||
| ) | ` [virtual]` |

returns the TextureAtlas that is used