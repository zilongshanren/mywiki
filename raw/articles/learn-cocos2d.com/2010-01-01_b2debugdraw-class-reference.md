---
title: b2DebugDraw Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_debug_draw/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2DebugDraw Class Reference

`#include <`[b2WorldCallbacks.h](../../../box2d-api-reference/API/b2_world_callbacks_8h_source/)>


[List of all members.](/)

## Public Types |
| enum | {
[e_shapeBit](../../../box2d-api-reference/API/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3aadd3dbc2b9c41b1ecb1d002d97a210d7) = 0x0001,
[e_jointBit](../../../box2d-api-reference/API/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a97122a80af0336c5f2dee36e305b2efb) = 0x0002,
[e_aabbBit](../../../box2d-api-reference/API/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a1c925b159b060d11a34b08e2a3a108e2) = 0x0004,
[e_pairBit](../../../box2d-api-reference/API/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3a2e9fbd0b7ea527c986f880f8e6021086) = 0x0008,
[e_centerOfMassBit](../../../box2d-api-reference/API/classb2_debug_draw/#a46138efa5acf989200fa1e20092355d3aea9f5f85554f8e08b01a6eb0ad8dba7c) = 0x0010
} |
## Public Member Functions |
| | [b2DebugDraw](../../../box2d-api-reference/API/classb2_debug_draw/#ac8692863187077e24f8ba8fc3d59cdcd) () |
| virtual | [~b2DebugDraw](../../../box2d-api-reference/API/classb2_debug_draw/#aecc6d89f6fb7debf20240f1c7a51fd98) () |
| void | [SetFlags](../../../box2d-api-reference/API/classb2_debug_draw/#ad16f3929a7ae1db79a946aa0cfb97690) ([uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) flags) |
| | Set the drawing flags.
|
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) | [GetFlags](../../../box2d-api-reference/API/classb2_debug_draw/#a2cfd95c027fd25e12e9a28dc1b84683d) () const |
| | Get the drawing flags.
|
| void | [AppendFlags](../../../box2d-api-reference/API/classb2_debug_draw/#a45d471e1e7f42ee05a6d7768786b91d7) ([uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) flags) |
| | Append flags to the current flags.
|
| void | [ClearFlags](../../../box2d-api-reference/API/classb2_debug_draw/#a3a95e31c1c33f9532ec1a703c2b5a475) ([uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) flags) |
| | Clear flags from the current flags.
|
| virtual void | [DrawPolygon](../../../box2d-api-reference/API/classb2_debug_draw/#a6b34d94add9fe6e237efbd63cac9ff1e) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) *vertices, [int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) vertexCount, const [b2Color](../../../box2d-api-reference/API/structb2_color/) &color)=0 |
| | Draw a closed polygon provided in CCW order.
|
| virtual void | [DrawSolidPolygon](../../../box2d-api-reference/API/classb2_debug_draw/#a96f94aef4083fb8492547aa1d04318b4) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) *vertices, [int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) vertexCount, const [b2Color](../../../box2d-api-reference/API/structb2_color/) &color)=0 |
| | Draw a solid closed polygon provided in CCW order.
|
| virtual void | [DrawCircle](../../../box2d-api-reference/API/classb2_debug_draw/#a80bb5da763af96f8216612726b9026d4) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) ¢er, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) radius, const [b2Color](../../../box2d-api-reference/API/structb2_color/) &color)=0 |
| | Draw a circle.
|
| virtual void | [DrawSolidCircle](../../../box2d-api-reference/API/classb2_debug_draw/#a79c7226c17fa669f034e4322b8670961) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) ¢er, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) radius, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &axis, const [b2Color](../../../box2d-api-reference/API/structb2_color/) &color)=0 |
| | Draw a solid circle.
|
| virtual void | [DrawSegment](../../../box2d-api-reference/API/classb2_debug_draw/#a8099b5a99a5f643578b5c5d60c5d3946) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &p1, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &p2, const [b2Color](../../../box2d-api-reference/API/structb2_color/) &color)=0 |
| | Draw a line segment.
|
| virtual void | [DrawTransform](../../../box2d-api-reference/API/classb2_debug_draw/#ad8ae0c5bdde1cddf18746b091923387e) (const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &xf)=0 |
## Protected Attributes |
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) | [m_drawFlags](../../../box2d-api-reference/API/classb2_debug_draw/#aa4acd58eafcb40e3f1c01348557733f2) |


## Detailed Description

Implement and register this class with a [b2World](../../../box2d-api-reference/API/classb2_world/) to provide debug drawing of physics entities in your game.


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



## Constructor & Destructor Documentation

| b2DebugDraw::b2DebugDraw |
( |
|
) |
|


| virtual b2DebugDraw::~b2DebugDraw |
( |
|
) |
` [inline, virtual]` |



## Member Function Documentation

| void b2DebugDraw::AppendFlags |
( |
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) |
*flags* |
) |
|

Append flags to the current flags.

| void b2DebugDraw::ClearFlags |
( |
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) |
*flags* |
) |
|

Clear flags from the current flags.

| virtual void b2DebugDraw::DrawCircle |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*center*, |
|
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*radius*, |
|
|
const [b2Color](../../../box2d-api-reference/API/structb2_color/) & |
*color* | |
|
) |
| | ` [pure virtual]` |

| virtual void b2DebugDraw::DrawPolygon |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) * |
*vertices*, |
|
|
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*vertexCount*, |
|
|
const [b2Color](../../../box2d-api-reference/API/structb2_color/) & |
*color* | |
|
) |
| | ` [pure virtual]` |

Draw a closed polygon provided in CCW order.

| virtual void b2DebugDraw::DrawSegment |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*p1*, |
|
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*p2*, |
|
|
const [b2Color](../../../box2d-api-reference/API/structb2_color/) & |
*color* | |
|
) |
| | ` [pure virtual]` |

| virtual void b2DebugDraw::DrawSolidCircle |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*center*, |
|
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*radius*, |
|
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*axis*, |
|
|
const [b2Color](../../../box2d-api-reference/API/structb2_color/) & |
*color* | |
|
) |
| | ` [pure virtual]` |

| virtual void b2DebugDraw::DrawSolidPolygon |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) * |
*vertices*, |
|
|
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*vertexCount*, |
|
|
const [b2Color](../../../box2d-api-reference/API/structb2_color/) & |
*color* | |
|
) |
| | ` [pure virtual]` |

Draw a solid closed polygon provided in CCW order.

| virtual void b2DebugDraw::DrawTransform |
( |
const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) & |
*xf* |
) |
` [pure virtual]` |

Draw a transform. Choose your own length scale.

**Parameters:**-

[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) b2DebugDraw::GetFlags |
( |
|
) |
const |

| void b2DebugDraw::SetFlags |
( |
[uint32](../../../box2d-api-reference/API/b2_settings_8h/#a1134b580f8da4de94ca6b1de4d37975e) |
*flags* |
) |
|


## Member Data Documentation


The documentation for this class was generated from the following files: