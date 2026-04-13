---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer_color/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCLayer.h>`




[List of all members.](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer_color-members/)


## Detailed Description

[CCLayerColor](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer_color/) is a subclass of [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) that implements the [CCRGBAProtocol](../../../../../api-ref/1.0/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/) protocol.

All features from [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) are valid, plus the following new features:


## Member Function Documentation

| void CCLayerColor::changeHeight: |
( |
GLfloat |
*h* | ) |
` [virtual]` |

| void CCLayerColor::changeWidth: |
( |
GLfloat |
*w* | ) |
` [virtual]` |

| void CCLayerColor::changeWidth:height: |
( |
GLfloat |
*w*, |
|
|
[height] GLfloat |
*h* |
|
) |
| ` [virtual]` |

change width and height in Points

**Since:**- v0.8

| id CCLayerColor::initWithColor: |
( |
[ccColor4B](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_color4_b/) |
*color* | ) |
` [virtual]` |

initializes a [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) with color. Width and height are the window size.

| id CCLayerColor::initWithColor:width:height: |
( |
[ccColor4B](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_color4_b/) |
*color*, |
|
|
[width] GLfloat |
*w*, |
|
|
[height] GLfloat |
*h* |
|
) |
| ` [virtual]` |

initializes a [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) with color, width and height in Points

| id CCLayerColor::layerWithColor: |
( |
[ccColor4B](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_color4_b/) |
*color* | ) |
` [static, virtual]` |

creates a [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) with color. Width and height are the window size.

| id CCLayerColor::layerWithColor:width:height: |
( |
[ccColor4B](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_color4_b/) |
*color*, |
|
|
[width] GLfloat |
*w*, |
|
|
[height] GLfloat |
*h* |
|
) |
| ` [static, virtual]` |

creates a [CCLayer](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_layer/) with color, width and height in Points


## Property Documentation

[ccBlendFunc](../../../../../api-ref/1.0/cocos2d-iphone/html/structcc_blend_func/) CCLayerColor::blendFunc` [read, write, assign]` |

GLubyte CCLayerColor::opacity` [read, assign]` |


The documentation for this interface was generated from the following file: