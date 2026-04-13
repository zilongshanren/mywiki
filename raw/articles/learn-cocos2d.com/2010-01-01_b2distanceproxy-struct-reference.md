---
title: b2DistanceProxy Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_distance_proxy/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2DistanceProxy Struct Reference

`#include <`[b2Distance.h](/)>


[List of all members.](/)


## Detailed Description

A distance proxy is used by the GJK algorithm. It encapsulates any shape.


## Constructor & Destructor Documentation

| b2DistanceProxy::b2DistanceProxy |
( |
|
) |
` [inline]` |



## Member Function Documentation

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2DistanceProxy::GetSupport |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex index in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2DistanceProxy::GetSupportVertex |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*d* |
) |
const` [inline]` |

Get the supporting vertex in the given direction.

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2DistanceProxy::GetVertex |
( |
[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) |
*index* |
) |
const` [inline]` |

Get a vertex by index. Used by b2Distance.

[int32](../../../box2d-api-reference/API/b2_settings_8h/#a43d43196463bde49cb067f5c20ab8481) b2DistanceProxy::GetVertexCount |
( |
|
) |
const` [inline]` |

| void b2DistanceProxy::Set |
( |
const [b2Shape](../../../box2d-api-reference/API/classb2_shape/) * |
*shape* |
) |
|

Initialize the proxy using the given shape. The shape must remain in scope while the proxy is in use.


## Member Data Documentation


The documentation for this struct was generated from the following files: