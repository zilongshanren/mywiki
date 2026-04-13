---
title: b2Vec2 Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_vec2/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2Vec2 Struct Reference

A 2D column vector.
[More...](#_details)

`#include <`[b2Math.h](../../../box2d-api-reference/API/b2_math_8h_source/)>


[List of all members.](/)


## Detailed Description

A 2D column vector.


## Constructor & Destructor Documentation

| b2Vec2::b2Vec2 |
( |
|
) |
` [inline]` |

Default constructor does nothing (for performance).

Construct using coordinates.


## Member Function Documentation

| bool b2Vec2::IsValid |
( |
|
) |
const` [inline]` |

Does this vector contain finite coordinates?

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2Vec2::Length |
( |
|
) |
const` [inline]` |

Get the length of this vector (the norm).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2Vec2::LengthSquared |
( |
|
) |
const` [inline]` |

Get the length squared. For performance, use this instead of [b2Vec2::Length](../../../box2d-api-reference/API/structb2_vec2/#afb1c498214b88874fcb07eb6322374da) (if possible).

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2Vec2::Normalize |
( |
|
) |
` [inline]` |

Convert this vector into a unit vector. Returns the length.

Write to an indexed element.

Read from and indexed element.

| void b2Vec2::operator*= |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*a* |
) |
` [inline]` |

Multiply this vector by a scalar.

| void b2Vec2::operator+= |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*v* |
) |
` [inline]` |

Add a vector to this vector.

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2Vec2::operator- |
( |
|
) |
const` [inline]` |

| void b2Vec2::operator-= |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*v* |
) |
` [inline]` |

Subtract a vector from this vector.

Set this vector to some specified coordinates.

| void b2Vec2::SetZero |
( |
|
) |
` [inline]` |

Set this vector to all zeros.


## Member Data Documentation


The documentation for this struct was generated from the following file: