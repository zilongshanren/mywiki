---
title: b2PolygonShape Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_polygon_shape/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2PolygonShape Class Reference

`#include <`[b2PolygonShape.h](/)>


[List of all members.](/)

## Public Member Functions |
| | [b2PolygonShape](../../../box2d-api-reference/API/classb2_polygon_shape/#a76d778e6b374e4d22167a609dc0333a4) () |
[b2Shape](../../../box2d-api-reference/API/classb2_shape/) * | [Clone](../../../box2d-api-reference/API/classb2_polygon_shape/#a38cf6a915a85691746465c9dbfc5aeb6) ([b2BlockAllocator](../../../box2d-api-reference/API/classb2_block_allocator/) *allocator) const |
| | Implement [b2Shape](../../../box2d-api-reference/API/classb2_shape/).
|
| void | [Set](../../../box2d-api-reference/API/classb2_polygon_shape/#a8aa13a7584b58f08be4d84181b5a86a8) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) *vertices, [int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) vertexCount) |
| void | [SetAsBox](../../../box2d-api-reference/API/classb2_polygon_shape/#a6bb90df8b4a40d1c53b64cc352a855dd) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) hx, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) hy) |
| void | [SetAsBox](../../../box2d-api-reference/API/classb2_polygon_shape/#a890690250115483da6c7d69829be087e) ([float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) hx, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) hy, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) ¢er, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) angle) |
| void | [SetAsEdge](../../../box2d-api-reference/API/classb2_polygon_shape/#ab6d99dd682d9eff9b35ddb51705717d0) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &v1, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &v2) |
| | Set this as a single edge.
|
| bool | [TestPoint](../../../box2d-api-reference/API/classb2_polygon_shape/#a69ccc2f671394b3cc1a00a16ef36b12b) (const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &transform, const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &p) const |
| bool | [RayCast](../../../box2d-api-reference/API/classb2_polygon_shape/#a364b0d326d9a7a61969737331633aed2) ([b2RayCastOutput](../../../box2d-api-reference/API/structb2_ray_cast_output/) *output, const [b2RayCastInput](../../../box2d-api-reference/API/structb2_ray_cast_input/) &input, const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &transform) const |
| | Implement [b2Shape](../../../box2d-api-reference/API/classb2_shape/).
|
| void | [ComputeAABB](../../../box2d-api-reference/API/classb2_polygon_shape/#a7941f209da41c8737b48cc89cb0d13c1) ([b2AABB](../../../box2d-api-reference/API/structb2_a_a_b_b/) *aabb, const [b2Transform](../../../box2d-api-reference/API/structb2_transform/) &transform) const |
| void | [ComputeMass](../../../box2d-api-reference/API/classb2_polygon_shape/#ad86c4c2a83a7122599462da83bf35389) ([b2MassData](../../../box2d-api-reference/API/structb2_mass_data/) *massData, [float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) density) const |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) | [GetSupport](../../../box2d-api-reference/API/classb2_polygon_shape/#a3a98e5947093b51606190895a43cac49) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &d) const |
| | Get the supporting vertex index in the given direction.
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & | [GetSupportVertex](../../../box2d-api-reference/API/classb2_polygon_shape/#a57672dae6ceb57559dbc8f1efcd6bb2a) (const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) &d) const |
| | Get the supporting vertex in the given direction.
|
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) | [GetVertexCount](../../../box2d-api-reference/API/classb2_polygon_shape/#ae220f24c42eff4aef4cd452676ca2ced) () const |
| | Get the vertex count.
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & | [GetVertex](../../../box2d-api-reference/API/classb2_polygon_shape/#a88cdb687ec7dc0cbcf4bd25fd37f4da1) ([int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) index) const |
| | Get a vertex by index.
|
## Public Attributes |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_centroid](../../../box2d-api-reference/API/classb2_polygon_shape/#ae8f5bd2f13f1e9b741c33350ba19cd9f) |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_vertices](../../../box2d-api-reference/API/classb2_polygon_shape/#a11ee5c107660be5da25f0e164aaccd53) [b2_maxPolygonVertices] |
[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) | [m_normals](../../../box2d-api-reference/API/classb2_polygon_shape/#a97cdcec277321c62ecdf93cb649958ce) [b2_maxPolygonVertices] |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) | [m_vertexCount](../../../box2d-api-reference/API/classb2_polygon_shape/#a45902db31f1a135b259f7967fd05f2f0) |


## Detailed Description

A convex polygon. It is assumed that the interior of the polygon is to the left of each edge.


## Constructor & Destructor Documentation

| b2PolygonShape::b2PolygonShape |
( |
|
) |
` [inline]` |



## Member Function Documentation

| void b2PolygonShape::ComputeAABB |
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

| void b2PolygonShape::ComputeMass |
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

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2PolygonShape::GetSupport |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex index in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2PolygonShape::GetSupportVertex |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2PolygonShape::GetVertex |
( |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*index* |
) |
const` [inline]` |

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2PolygonShape::GetVertexCount |
( |
|
) |
const` [inline]` |

| void b2PolygonShape::Set |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) * |
*vertices*, |
|
|
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*vertexCount* | |
|
) |
| | |

Copy vertices. This assumes the vertices define a convex polygon. It is assumed that the exterior is the the right of each edge.

Build vertices to represent an oriented box.

**Parameters:**-
| *hx* | the half-width. |
| *hy* | the half-height. |
| *center* | the center of the box in local coordinates. |
| *angle* | the rotation of the box in local coordinates. |


Build vertices to represent an axis-aligned box.

**Parameters:**-
| *hx* | the half-width. |
| *hy* | the half-height. |


| void b2PolygonShape::SetAsEdge |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*v1*, |
|
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*v2* | |
|
) |
| | |

Set this as a single edge.

| bool b2PolygonShape::TestPoint |
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