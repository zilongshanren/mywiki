---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_rot/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Rotation.
[More...](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#details)

`#include <b2Math.h>`


[List of all members.](/)

Public Member Functions
|
| | [b2Rot](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#aa40dda6d390a2f54c793c63027a9b46e) (float32 angle) |
| | Initialize from an angle in radians.
|
| void | [Set](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#acde9186de0a4a7397bf8ef714408ad60) (float32 angle) |
| | Set using an angle in radians.
|
| void | [SetIdentity](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#a7f534cb7ece8d325662d7d0e27d4f617) () |
| | Set to the identity rotation.
|
| float32 | [GetAngle](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#a67a6c08812c009654f00800256c8bfdc) () const |
| | Get the angle in radians.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetXAxis](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#ac4ab7f262adb99f161775314852723d8) () const |
| | Get the x-axis.
|
[b2Vec2](../../../../../api-ref/2.0/Box2D/html/structb2_vec2/) | [GetYAxis](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#ae731c7434fe1754114ee70149df36c7f) () const |
| | Get the u-axis.
|
Public Attributes
|
| float32 | [s](../../../../../api-ref/2.0/Box2D/html/structb2_rot/#a15725ce0a89cc735ad90687b4c0f4dce) |
| | Sine and cosine.
|
float32 | **c** |


## Detailed Description


## Constructor & Destructor Documentation

| b2Rot::b2Rot |
( |
float32 |
*angle* | ) |
` [inline, explicit]` |

Initialize from an angle in radians.

TODO_ERIN optimize


## Member Function Documentation

Get the angle in radians.

Set using an angle in radians.

TODO_ERIN optimize

Set to the identity rotation.


## Member Data Documentation


The documentation for this struct was generated from the following file: