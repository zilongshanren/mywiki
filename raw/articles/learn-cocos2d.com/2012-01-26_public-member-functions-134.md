---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCSpriteFrame.h>`



[List of all members.](/)

Public Member Functions
|
| id | [initWithTexture:rect:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#af8bce98fcf5dcd354d65735687343cf5) ([CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) *texture,[rect] CGRect rect) |
| id | [initWithTexture:rectInPixels:rotated:offset:originalSize:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#adfdb63e74246965ef35f37b61a542cd4) ([CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) *texture,[rectInPixels] CGRect rect,[rotated] BOOL rotated,[offset] CGPoint offset,[originalSize] CGSize originalSize) |
Static Public Member Functions
|
| id | [frameWithTexture:rect:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a3d33a9ddece7caa8c8384575c6c8f549) ([CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) *texture,[rect] CGRect rect) |
| id | [frameWithTexture:rectInPixels:rotated:offset:originalSize:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a88111a9fc32cf1cb947d0e9e37b8feca) ([CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) *texture,[rectInPixels] CGRect rect,[rotated] BOOL rotated,[offset] CGPoint offset,[originalSize] CGSize originalSize) |
Protected Attributes
|
CGRect | **rect_** |
CGRect | **rectInPixels_** |
BOOL | **rotated_** |
CGPoint | **offsetInPixels_** |
CGSize | **originalSizeInPixels_** |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * | **texture_** |
Properties
|
| CGRect | [rect](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a7c5eb9c09bca5b2dac1a5d2c988affdb) |
| CGRect | [rectInPixels](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a0b1ba9e7d49cfa23b120828b8dc1dfea) |
| BOOL | [rotated](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a53892235ea1f843c39d9be3eaea3a05c) |
| CGPoint | [offsetInPixels](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#ac1b194686a75ffafffbc9ea2cc2a4f7c) |
| CGSize | [originalSizeInPixels](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a7ec8a93d1aa970d2b0f9574874e8df48) |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * | [texture](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/#a1111c858631cbe06f5197518424ff858) |


## Detailed Description

A [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) has:

You can modify the frame of a [CCSprite](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite/) by doing:

[CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) *frame = [[CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) frameWithTexture:texture rect:rect offset:offset]; [sprite setDisplayFrame:frame];


## Member Function Documentation

| id CCSpriteFrame::frameWithTexture:rect: |
( |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * |
*texture*, |
|
|
[rect] CGRect |
*rect* |
|
) |
| ` [static, virtual]` |

Create a [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect in points. It is assumed that the frame was not trimmed.

| id CCSpriteFrame::frameWithTexture:rectInPixels:rotated:offset:originalSize: |
( |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * |
*texture*, |
|
|
[rectInPixels] CGRect |
*rect*, |
|
|
[rotated] BOOL |
*rotated*, |
|
|
[offset] CGPoint |
*offset*, |
|
|
[originalSize] CGSize |
*originalSize* |
|
) |
| ` [static, virtual]` |

Create a [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect, rotated, offset and originalSize in pixels. The originalSize is the size in points of the frame before being trimmed.

| id CCSpriteFrame::initWithTexture:rect: |
( |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * |
*texture*, |
|
|
[rect] CGRect |
*rect* |
|
) |
| ` [virtual]` |

Initializes a [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect in points; It is assumed that the frame was not trimmed.

| id CCSpriteFrame::initWithTexture:rectInPixels:rotated:offset:originalSize: |
( |
[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) * |
*texture*, |
|
|
[rectInPixels] CGRect |
*rect*, |
|
|
[rotated] BOOL |
*rotated*, |
|
|
[offset] CGPoint |
*offset*, |
|
|
[originalSize] CGSize |
*originalSize* |
|
) |
| ` [virtual]` |

Initializes a [CCSpriteFrame](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_frame/) with a texture, rect, rotated, offset and originalSize in pixels. The originalSize is the size in points of the frame before being trimmed.


## Property Documentation

CGPoint CCSpriteFrame::offsetInPixels` [read, write, assign]` |

offset of the frame in pixels

CGSize CCSpriteFrame::originalSizeInPixels` [read, write, assign]` |

original size of the trimmed image in pixels

CGRect CCSpriteFrame::rect` [read, write, assign]` |

rect of the frame in points. If it is updated, then rectInPixels will be updated too.

CGRect CCSpriteFrame::rectInPixels` [read, write, assign]` |

rect of the frame in pixels. If it is updated, then rect (points) will be udpated too.

BOOL CCSpriteFrame::rotated` [read, write, assign]` |

whether or not the rect of the frame is rotated ( x = x+width, y = y+height, width = height, height = width )

[CCTexture2D](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/)* CCSpriteFrame::texture` [read, write, retain]` |


The documentation for this interface was generated from the following file: