---
title: CCAnimation Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_animation/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCAnimation.h](/)"


[List of all members.](/)


## Detailed Description

A [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) object is used to perform animations on the [CCSprite](../../../unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) objects.

The [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) object contains [CCSpriteFrame](/) objects, and a possible delay between the frames. You can animate a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) object by using the [CCAnimate](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animate/) action. Example:

[sprite runAction:[[CCAnimate](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animate/) actionWithAnimation:animation]];


## Member Function Documentation

| - (void) addFrameWithFilename: |
|
(NSString *) |
*filename* |
|
|

Adds a frame with an image filename. Internally it will create a [CCSpriteFrame](/) and it will add it. Added to facilitate the migration from v0.8 to v0.9.

| - (void) addFrameWithTexture: |
|
([CCTexture2D](../../../unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) *) |
*texture* |
| rect: |
|
(CGRect) |
*rect* | |
|
|
| | |

Adds a frame with a texture and a rect. Internally it will create a [CCSpriteFrame](/) and it will add it. Added to facilitate the migration from v0.8 to v0.9.

Creates an animation

**Since:**- v0.99.5

| + (id) animationWithFrames: |
|
(NSArray *) |
*frames* |
|
|

Creates an animation with frames.

**Since:**- v0.99.5

| + (id) animationWithName: |
|
(NSString *) |
*DEPRECATED_ATTRIBUTE* |
|
|

| + (id) animationWithName: |
|
(NSString *) |
*name* |
| delay: |
|
(float) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Creates a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name and delay between frames.

| + (id) animationWithName: |
|
(NSString *) |
*name* |
| delay: |
|
(float) |
*delay* |
| frames: |
|
(NSArray *) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Creates a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name, delay and an array of CCSpriteFrames.

| + (id) animationWithName: |
|
(NSString *) |
*name* |
| frames: |
|
(NSArray *) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Creates a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name and frames

**Since:**- v0.99.3

[Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000003)- Will be removed in 1.0.1. Use "animationWithFrames" instead.

| - (id) initWithFrames: |
|
(NSArray *) |
*frames* |
|
|

| - (id) initWithFrames: |
|
(NSArray *) |
*frames* |
| delay: |
|
(float) |
*delay* | |
|
|
| | |

Initializes a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with frames and a delay between frames

**Since:**- v0.99.5

| - (id) initWithName: |
|
(NSString *) |
*DEPRECATED_ATTRIBUTE* |
|
|

| - (id) initWithName: |
|
(NSString *) |
*name* |
| delay: |
|
(float) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Initializes a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name and delay between frames.

[Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000006)- Will be removed in 1.0.1. Use "initWithFrames:nil delay:delay" instead.

| - (id) initWithName: |
|
(NSString *) |
*name* |
| delay: |
|
(float) |
*delay* |
| frames: |
|
(NSArray *) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Initializes a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name, delay and an array of CCSpriteFrames.

[Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000007)- Will be removed in 1.0.1. Use "initWithFrames:frames delay:delay" instead.

| - (id) initWithName: |
|
(NSString *) |
*name* |
| frames: |
|
(NSArray *) |
*DEPRECATED_ATTRIBUTE* | |
|
|
| | |

Initializes a [CCAnimation](../../../unofficial-cocos2d-api-reference/html/interface_c_c_animation/) with a name and frames

**Since:**- v0.99.3

[Deprecated:](../../../unofficial-cocos2d-api-reference/html/deprecated/#_deprecated000005)- Will be removed in 1.0.1. Use "initWithFrames" instead.


## Property Documentation

- (float) delay` [read, write, assign]` |

delay between frames in seconds.

- (NSMutableArray*) frames` [read, write, retain]` |

- (NSString*) name` [read, write, retain]` |


The documentation for this class was generated from the following file: