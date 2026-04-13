---
title: Public Types
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_debug_draw/
published: '2011-09-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2WorldCallbacks.h>`


[List of all members.](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw-members/)

Public Types
|
| enum | {
[e_shapeBit](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3aadd3dbc2b9c41b1ecb1d002d97a210d7) = 0x0001,
[e_jointBit](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a97122a80af0336c5f2dee36e305b2efb) = 0x0002,
[e_aabbBit](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a1c925b159b060d11a34b08e2a3a108e2) = 0x0004,
[e_pairBit](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a2e9fbd0b7ea527c986f880f8e6021086) = 0x0008,
[e_centerOfMassBit](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3aea9f5f85554f8e08b01a6eb0ad8dba7c) = 0x0010
} |
Public Member Functions
|
| void | [SetFlags](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#ad16f3929a7ae1db79a946aa0cfb97690) (uint32 flags) |
| | Set the drawing flags.
|
| uint32 | [GetFlags](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a2cfd95c027fd25e12e9a28dc1b84683d) () const |
| | Get the drawing flags.
|
| void | [AppendFlags](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a45d471e1e7f42ee05a6d7768786b91d7) (uint32 flags) |
| | Append flags to the current flags.
|
| void | [ClearFlags](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a3a95e31c1c33f9532ec1a703c2b5a475) (uint32 flags) |
| | Clear flags from the current flags.
|
| virtual void | [DrawPolygon](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a6b34d94add9fe6e237efbd63cac9ff1e) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) *vertices, int32 vertexCount, const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) &color)=0 |
| | Draw a closed polygon provided in CCW order.
|
| virtual void | [DrawSolidPolygon](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a96f94aef4083fb8492547aa1d04318b4) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) *vertices, int32 vertexCount, const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) &color)=0 |
| | Draw a solid closed polygon provided in CCW order.
|
| virtual void | [DrawCircle](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a80bb5da763af96f8216612726b9026d4) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) ¢er, float32 radius, const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) &color)=0 |
| | Draw a circle.
|
| virtual void | [DrawSolidCircle](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a79c7226c17fa669f034e4322b8670961) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) ¢er, float32 radius, const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &axis, const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) &color)=0 |
| | Draw a solid circle.
|
| virtual void | [DrawSegment](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#a8099b5a99a5f643578b5c5d60c5d3946) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &p1, const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &p2, const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) &color)=0 |
| | Draw a line segment.
|
| virtual void | [DrawTransform](../../../../../api-ref/1.0/Box2D/html/classb2_debug_draw/#ad8ae0c5bdde1cddf18746b091923387e) (const [b2Transform](../../../../../api-ref/1.0/Box2D/html/structb2_transform/) &xf)=0 |
Protected Attributes
|
uint32 | **m_drawFlags** |


## Detailed Description

Implement and register this class with a [b2World](../../../../../api-ref/1.0/Box2D/html/classb2_world/) to provide debug drawing of physics entities in your game.


## Member Enumeration Documentation

**Enumerator: **
e_shapeBit |
draw shapes
|
e_jointBit |
draw joint connections
|
e_aabbBit |
draw axis aligned bounding boxes
|
e_pairBit |
draw broad-phase pairs
|
e_centerOfMassBit |
draw center of mass frame
|



## Member Function Documentation

| void b2DebugDraw::AppendFlags |
( |
uint32 |
*flags* | ) |
|

Append flags to the current flags.

| void b2DebugDraw::ClearFlags |
( |
uint32 |
*flags* | ) |
|

Clear flags from the current flags.

| virtual void b2DebugDraw::DrawCircle |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*center*, |
|
|
float32 |
*radius*, |
|
|
const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) & |
*color* |
|
) |
| ` [pure virtual]` |

| virtual void b2DebugDraw::DrawPolygon |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) * |
*vertices*, |
|
|
int32 |
*vertexCount*, |
|
|
const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) & |
*color* |
|
) |
| ` [pure virtual]` |

Draw a closed polygon provided in CCW order.

| virtual void b2DebugDraw::DrawSegment |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*p1*, |
|
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*p2*, |
|
|
const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) & |
*color* |
|
) |
| ` [pure virtual]` |

| virtual void b2DebugDraw::DrawSolidCircle |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*center*, |
|
|
float32 |
*radius*, |
|
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*axis*, |
|
|
const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) & |
*color* |
|
) |
| ` [pure virtual]` |

| virtual void b2DebugDraw::DrawSolidPolygon |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) * |
*vertices*, |
|
|
int32 |
*vertexCount*, |
|
|
const [b2Color](../../../../../api-ref/1.0/Box2D/html/structb2_color/) & |
*color* |
|
) |
| ` [pure virtual]` |

Draw a solid closed polygon provided in CCW order.

| virtual void b2DebugDraw::DrawTransform |
( |
const [b2Transform](../../../../../api-ref/1.0/Box2D/html/structb2_transform/) & |
*xf* | ) |
` [pure virtual]` |

Draw a transform. Choose your own length scale.

**Parameters:**-

| uint32 b2DebugDraw::GetFlags |
( |
| ) |
const |

| void b2DebugDraw::SetFlags |
( |
uint32 |
*flags* | ) |
|


The documentation for this class was generated from the following file: