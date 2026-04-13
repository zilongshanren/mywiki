---
title: b2Shape Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_shape/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Shape.h](http://www.learn-cocos2d.com/)>

## Public Types | |
| enum |
|

A shape is used for collision detection. You can create a shape however you like. Shapes used for simulation in [b2World](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_world/) are created automatically when a [b2Fixture](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_fixture/) is created.

| b2Shape::b2Shape | ( | ) | ` [inline]` |

| virtual b2Shape::~b2Shape | ( | ) | ` [inline, virtual]` |

Given a transform, compute the associated axis aligned bounding box for this shape.

aabb | returns the axis aligned box. | |
xf | the world transform of the shape. |

Implemented in [b2CircleShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_circle_shape/#a95a1496ea5269befdc59d1b003898057), and [b2PolygonShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_polygon_shape/#a7941f209da41c8737b48cc89cb0d13c1).

Compute the mass properties of this shape using its dimensions and density. The inertia tensor is computed about the local origin.

massData | returns the mass data for this shape. | |
density | the density in kilograms per meter squared. |

Implemented in [b2CircleShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_circle_shape/#a335edea2ef84789e102dde41ca889828), and [b2PolygonShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_polygon_shape/#ad86c4c2a83a7122599462da83bf35389).

Get the type of this shape. You can use this to down cast to the concrete shape.

| virtual bool b2Shape::RayCast | ( |
|

` [pure virtual]`

Cast a ray against this shape.

output | the ray-cast results. | |
input | the ray-cast input parameters. | |
transform | the transform to be applied to the shape. |

Implemented in [b2CircleShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_circle_shape/#a592e0283067365e24681e5f01575229c), and [b2PolygonShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_polygon_shape/#a364b0d326d9a7a61969737331633aed2).

Test a point for containment in this shape. This only works for convex shapes.

xf | the shape world transform. | |
p | a point in world coordinates. |

Implemented in [b2CircleShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_circle_shape/#a77171941cd1633c337fed1efb366bebb), and [b2PolygonShape](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_polygon_shape/#a69ccc2f671394b3cc1a00a16ef36b12b).