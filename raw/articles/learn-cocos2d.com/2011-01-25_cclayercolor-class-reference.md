---
title: CCLayerColor Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer_color/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[CCLayer.h](../../../unofficial-cocos2d-api-reference/html/_c_c_layer_8h_source/)"


Inherits [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/), [CCRGBAProtocol-p](../../../unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/), and [CCBlendProtocol-p](/).

Inherited by [CCColorLayer](/), and [CCLayerGradient](/).

[List of all members.](/)


## Detailed Description

[CCLayerColor](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer_color/) is a subclass of [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) that implements the [CCRGBAProtocol](../../../unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/) protocol.

All features from [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) are valid, plus the following new features:


## Member Function Documentation

| - (void) changeHeight: |
|
(GLfloat) |
*h* |
|
|

| - (void) changeWidth: |
|
(GLfloat) |
*w* |
|
|

| - (void) changeWidth: |
|
(GLfloat) |
*w* |
| height: |
|
(GLfloat) |
*h* | |
|
|
| | |

change width and height in Points

**Since:**- v0.8

initializes a [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) with color. Width and height are the window size.

| - (id) initWithColor: |
|
([ccColor4B](../../../unofficial-cocos2d-api-reference/html/structcc_color4_b/)) |
*color* |
| width: |
|
(GLfloat) |
*w* |
| height: |
|
(GLfloat) |
*h* | |
|
|
| | |

initializes a [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) with color, width and height in Points

creates a [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) with color. Width and height are the window size.

| + (id) layerWithColor: |
|
([ccColor4B](../../../unofficial-cocos2d-api-reference/html/structcc_color4_b/)) |
*color* |
| width: |
|
(GLfloat) |
*w* |
| height: |
|
(GLfloat) |
*h* | |
|
|
| | |

creates a [CCLayer](../../../unofficial-cocos2d-api-reference/html/interface_c_c_layer/) with color, width and height in Points


## Property Documentation

- (GLubyte) opacity` [read, assign]` |


The documentation for this class was generated from the following file:

- /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/
[CCLayer.h](../../../unofficial-cocos2d-api-reference/html/_c_c_layer_8h_source/)