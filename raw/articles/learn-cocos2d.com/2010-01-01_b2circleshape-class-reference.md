---
title: b2CircleShape Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_circle_shape/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2CircleShape Class Reference

A circle shape.
[More...](#_details)

`#include <`[b2CircleShape.h](/)>


[List of all members.](/)


## Detailed Description

A circle shape.


## Constructor & Destructor Documentation

| b2CircleShape::b2CircleShape |
( |
|
) |
` [inline]` |



## Member Function Documentation

| void b2CircleShape::ComputeAABB |
( |
[b2AABB](../../../box2d-api-reference/API/structb2_a_a_b_b/) * |
*aabb*, |
|
|
const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) & |
*transform* | |
|
) |
| | const` [virtual]` |

| void b2CircleShape::ComputeMass |
( |
[b2MassData](../../../box2d-api-reference/API/structb2_mass_data/) * |
*massData*, |
|
|
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*density* | |
|
) |
| | const` [virtual]` |

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2CircleShape::GetSupport |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex index in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2CircleShape::GetSupportVertex |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2CircleShape::GetVertex |
( |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*index* |
) |
const` [inline]` |

Get a vertex by index. Used by b2Distance.

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2CircleShape::GetVertexCount |
( |
|
) |
const` [inline]` |

| bool b2CircleShape::TestPoint |
( |
const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) & |
*transform*, |
|
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*p* | |
|
) |
| | const` [virtual]` |


## Member Data Documentation


The documentation for this class was generated from the following files: