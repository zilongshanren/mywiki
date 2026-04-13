---
title: b2AABB Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_a_a_b_b/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2AABB Struct Reference

An axis aligned bounding box.
[More...](#_details)

`#include <`[b2Collision.h](/)>


[List of all members.](/)


## Detailed Description

An axis aligned bounding box.


## Member Function Documentation

| void b2AABB::Combine |
( |
const [b2AABB](../../../box2d-api-reference/API/structb2_a_a_b_b/) & |
*aabb1*, |
|
|
const [b2AABB](../../../box2d-api-reference/API/structb2_a_a_b_b/) & |
*aabb2* | |
|
) |
| | ` [inline]` |

Combine two AABBs into this one.

| bool b2AABB::Contains |
( |
const [b2AABB](../../../box2d-api-reference/API/structb2_a_a_b_b/) & |
*aabb* |
) |
const` [inline]` |

Does this aabb contain the provided AABB.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2AABB::GetCenter |
( |
|
) |
const` [inline]` |

Get the center of the AABB.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2AABB::GetExtents |
( |
|
) |
const` [inline]` |

Get the extents of the AABB (half-widths).

| bool b2AABB::IsValid |
( |
|
) |
const` [inline]` |

Verify that the bounds are sorted.


## Member Data Documentation


The documentation for this struct was generated from the following files: