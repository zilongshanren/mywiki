---
title: Public Types
url: http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_shape/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Box2D
2.2
Box2D API Reference for www.kobold2d.com developers
|

`#include <b2Shape.h>`


| enum | Type { e_circle = 0,
e_edge = 1,
e_polygon = 2,
e_chain = 3,
e_typeCount = 4
} |
| virtual
|

A shape is used for collision detection. You can create a shape however you like. Shapes used for simulation in [b2World](http://www.learn-cocos2d.com/) are created automatically when a [b2Fixture](http://www.learn-cocos2d.com/) is created. Shapes may encapsulate a one or more child shapes.

| virtual void
|

` [pure virtual]`

Given a transform, compute the associated axis aligned bounding box for a child shape.

| aabb | returns the axis aligned box. |
| xf | the world transform of the shape. |
| childIndex | the child shape |

Implemented in [b2ChainShape](http://www.learn-cocos2d.com/#a409c21206e4c84f66700809aac5b164c), [b2PolygonShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_polygon_shape/#a00e225b0321bf6bb231a554036ffdf23), [b2EdgeShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_edge_shape/#a30f601c611eb549f9f657eee89d82f9f), and [b2CircleShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_circle_shape/#aa6889a5af85aa1e272547fd0008eb64a).

Compute the mass properties of this shape using its dimensions and density. The inertia tensor is computed about the local origin.

| massData | returns the mass data for this shape. |
| density | the density in kilograms per meter squared. |

Implemented in [b2ChainShape](http://www.learn-cocos2d.com/#a009259d589abebeda27fe580d117b11e), [b2PolygonShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_polygon_shape/#ad86c4c2a83a7122599462da83bf35389), [b2EdgeShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_edge_shape/#a3a305707a07ca3dffa6f2eaff3735dff), and [b2CircleShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_circle_shape/#a335edea2ef84789e102dde41ca889828).

Get the type of this shape. You can use this to down cast to the concrete shape.

| virtual bool
|

` [pure virtual]`

Cast a ray against a child shape.

| output | the ray-cast results. |
| input | the ray-cast input parameters. |
| transform | the transform to be applied to the shape. |
| childIndex | the child shape index |

Implemented in [b2ChainShape](http://www.learn-cocos2d.com/#a85c7a17a15581e0e258c7af561cf5403), [b2PolygonShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_polygon_shape/#ac13bded10d09c341f64aaa2750dda6b5), [b2EdgeShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_edge_shape/#aefbae6b3840f486b22ffecee7d0d15fd), and [b2CircleShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_circle_shape/#a76175079381193917026fdf3702190fa).

Test a point for containment in this shape. This only works for convex shapes.

| xf | the shape world transform. |
| p | a point in world coordinates. |

Implemented in [b2ChainShape](http://www.learn-cocos2d.com/#a4fc27b41ecc556985efacf8e0f91c39f), [b2PolygonShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_polygon_shape/#a69ccc2f671394b3cc1a00a16ef36b12b), [b2EdgeShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_edge_shape/#a28a977f82e4bc1cf60a3143ba5636c22), and [b2CircleShape](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/classb2_circle_shape/#a77171941cd1633c337fed1efb366bebb).