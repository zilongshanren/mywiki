---
title: b2Vec3 Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_vec3/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2Vec3 Struct Reference

A 2D column vector with 3 elements.
[More...](#_details)

`#include <`[b2Math.h](../../../box2d-api-reference/API/b2_math_8h_source/)>


[List of all members.](/)


## Detailed Description

A 2D column vector with 3 elements.


## Constructor & Destructor Documentation

| b2Vec3::b2Vec3 |
( |
|
) |
` [inline]` |

Default constructor does nothing (for performance).

Construct using coordinates.


## Member Function Documentation

| void b2Vec3::operator*= |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*s* |
) |
` [inline]` |

Multiply this vector by a scalar.

| void b2Vec3::operator+= |
( |
const [b2Vec3](../../../box2d-api-reference/API/structb2_vec3/) & |
*v* |
) |
` [inline]` |

Add a vector to this vector.

[b2Vec3](../../../box2d-api-reference/API/structb2_vec3/) b2Vec3::operator- |
( |
|
) |
const` [inline]` |

| void b2Vec3::operator-= |
( |
const [b2Vec3](../../../box2d-api-reference/API/structb2_vec3/) & |
*v* |
) |
` [inline]` |

Subtract a vector from this vector.

Set this vector to some specified coordinates.

| void b2Vec3::SetZero |
( |
|
) |
` [inline]` |

Set this vector to all zeros.


## Member Data Documentation


The documentation for this struct was generated from the following file: