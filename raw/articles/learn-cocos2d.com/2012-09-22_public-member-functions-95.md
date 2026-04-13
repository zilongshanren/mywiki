---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCSpriteFrame.h>`



[List of all members.](/)


## Detailed Description

A [CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) has:

You can modify the frame of a [CCSprite](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite/) by doing:

[CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) *frame = [[CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) frameWithTexture:texture rect:rect offset:offset]; [sprite setDisplayFrame:frame];


## Member Function Documentation

| + (id) frameWithTexture: |
|
([CCTexture2D](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_texture2_d/) *) |
*texture* |
| rect: |
|
(CGRect) |
*rect* |
|
|
| |

Create a [CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect in points. It is assumed that the frame was not trimmed.

| + (id) frameWithTexture: |
|
([CCTexture2D](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_texture2_d/) *) |
*texture* |
| rectInPixels: |
|
(CGRect) |
*rect* |
| rotated: |
|
(BOOL) |
*rotated* |
| offset: |
|
(CGPoint) |
*offset* |
| originalSize: |
|
(CGSize) |
*originalSize* |
|
|
| |

Create a [CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect, rotated, offset and originalSize in pixels. The originalSize is the size in points of the frame before being trimmed.

| - (id) initWithTexture: |
|
([CCTexture2D](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_texture2_d/) *) |
*texture* |
| rect: |
|
(CGRect) |
*rect* |
|
|
| |

Initializes a [CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect in points; It is assumed that the frame was not trimmed.

| - (id) initWithTexture: |
|
([CCTexture2D](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_texture2_d/) *) |
*texture* |
| rectInPixels: |
|
(CGRect) |
*rect* |
| rotated: |
|
(BOOL) |
*rotated* |
| offset: |
|
(CGPoint) |
*offset* |
| originalSize: |
|
(CGSize) |
*originalSize* |
|
|
| |

Initializes a [CCSpriteFrame](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect, rotated, offset and originalSize in pixels. The originalSize is the size in points of the frame before being trimmed.


## Property Documentation

offset of the frame in pixels

original size of the trimmed image in pixels

- (CGRect) [rect](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/#a7c5eb9c09bca5b2dac1a5d2c988affdb)` [read, write, assign]` |

rect of the frame in points. If it is updated, then rectInPixels will be updated too.

rect of the frame in pixels. If it is updated, then rect (points) will be udpated too.

- (BOOL) [rotated](../../../../../api-ref/latest/cocos2d-iphone/html/interface_c_c_sprite_frame/#a53892235ea1f843c39d9be3eaea3a05c)` [read, write, assign]` |

whether or not the rect of the frame is rotated ( x = x+width, y = y+height, width = height, height = width )


The documentation for this class was generated from the following file: