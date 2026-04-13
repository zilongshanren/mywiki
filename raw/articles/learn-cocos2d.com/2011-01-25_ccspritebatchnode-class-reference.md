---
title: CCSpriteBatchNode Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCSpriteBatchNode.h](/)"


Inherits [CCNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_node/), and [CCTextureProtocol-p](../../../unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/).

Inherited by [CCLabelBMFont](../../../unofficial-cocos2d-api-reference/html/interface_c_c_label_b_m_font/), CCSpriteSheetInternalOnly, and [CCTMXLayer](/).

[List of all members.](/)


## Detailed Description

[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) is like a batch node: if it contains children, it will draw them in 1 single OpenGL call (often known as "batch draw").

A [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) can reference one and only one texture (one image file, one texture atlas). Only the CCSprites that are contained in that texture can be added to the [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/). All CCSprites added to a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) are drawn in one OpenGL ES draw call. If the CCSprites are not added to a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) then an OpenGL ES draw call will be needed for each one, which is less efficient.

Limitations:

- The only object that is accepted as child (or grandchild, grand-grandchild, etc...) is
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) or any subclass of [CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/). eg: particles, labels and layer can't be added to a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/).
- Either all its children are Aliased or Antialiased. It can't be a mix. This is because "alias" is a property of the texture, and all the sprites share the same texture.

**Since:**- v0.7.1


## Member Function Documentation

| + (id) batchNodeWithFile: |
|
(NSString *) |
*fileImage* |
|
|

creates a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) with a default capacity of 29 children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| + (id) batchNodeWithFile: |
|
(NSString *) |
*fileImage* |
| capacity: |
|
(NSUInteger) |
*capacity* | |
|
|
| | |

creates a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

creates a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a texture2d and a default capacity of 29 children. The capacity will be increased in 33% in runtime if it run out of space.

| + (id) batchNodeWithTexture: |
|
([CCTexture2D](../../../unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) *) |
*tex* |
| capacity: |
|
(NSUInteger) |
*capacity* | |
|
|
| | |

creates a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a texture2d and capacity of children. The capacity will be increased in 33% in runtime if it run out of space.

- ([CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/)*) createSpriteWithRect: |
|
(CGRect) |
*DEPRECATED_ATTRIBUTE* |
|
|

creates an sprite with a rect in the [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/). It's the same as:

- create an standard CCSsprite
- set the usingSpriteSheet = YES
- set the textureAtlas to the same texture Atlas as the
[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) [Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000020)- Use [
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) spriteWithBatchNode:rect:] instead;


| - (void) initSprite: |
|
([CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) *) |
*sprite* |
| rect: |
|
(CGRect) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

initializes a previously created sprite with a rect. This sprite will have the same texture as the [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/). It's the same as:

- initialize an standard CCSsprite
- set the usingBatchNode = YES
- set the textureAtlas to the same texture Atlas as the
[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) **Since:**- v0.99.0

[Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000021)- Use [
[CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) initWithBatchNode:rect:] instead;


| - (id) initWithFile: |
|
(NSString *) |
*fileImage* |
| capacity: |
|
(NSUInteger) |
*capacity* | |
|
|
| | |

initializes a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a file image (.png, .jpeg, .pvr, etc) and a capacity of children. The capacity will be increased in 33% in runtime if it run out of space. The file will be loaded using the TextureMgr.

| - (id) initWithTexture: |
|
([CCTexture2D](../../../unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) *) |
*tex* |
| capacity: |
|
(NSUInteger) |
*capacity* | |
|
|
| | |

initializes a [CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) with a texture2d and capacity of children. The capacity will be increased in 33% in runtime if it run out of space.

| - (void) removeChild: |
|
([CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) *) |
*sprite* |
| cleanup: |
|
(BOOL) |
*doCleanup* | |
|
|
| | |

removes a child given a reference. It will also cleanup the running actions depending on the cleanup parameter.

**Warning:**- Removing a child from a
[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) is very slow

| - (void) removeChildAtIndex: |
|
(NSUInteger) |
*index* |
| cleanup: |
|
(BOOL) |
*doCleanup* | |
|
|
| | |

removes a child given a certain index. It will also cleanup the running actions depending on the cleanup parameter.

**Warning:**- Removing a child from a
[CCSpriteBatchNode](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/) is very slow


## Property Documentation

- ([CCArray](../../../unofficial-cocos2d-api-reference/html/interface_c_c_array/)*) descendants` [read, assign]` |

descendants (children, gran children, etc)

returns the TextureAtlas that is used


The documentation for this class was generated from the following file: