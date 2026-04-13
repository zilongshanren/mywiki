---
title: 'Box2D: Member List'
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_polygon_shape-members/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is the complete list of members for

[b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/), including all inherited members.

**b2PolygonShape**() (defined in [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/)) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [inline]` |
[Clone](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#ae9ae1676632d6b20f787e1207ed2797f)(b2BlockAllocator *allocator) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
[ComputeAABB](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a00e225b0321bf6bb231a554036ffdf23)(b2AABB *aabb, const b2Transform &transform, int32 childIndex) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
[ComputeMass](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#ad86c4c2a83a7122599462da83bf35389)(b2MassData *massData, float32 density) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
**e_chain** enum value (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**e_circle** enum value (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**e_edge** enum value (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**e_polygon** enum value (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**e_typeCount** enum value (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
[GetChildCount](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#ae844375297d19744e01a37b397a5baba)() const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
[GetType](../../../../../api-ref/1.0/Box2D/html/classb2_shape/#a3b6093f16c18f8a877519a29674abca0)() const | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | ` [inline]` |
[GetVertex](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a88cdb687ec7dc0cbcf4bd25fd37f4da1)(int32 index) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [inline]` |
[GetVertexCount](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#ae220f24c42eff4aef4cd452676ca2ced)() const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [inline]` |
**m_centroid** (defined in [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/)) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
**m_normals** (defined in [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/)) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
**m_radius** (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**m_type** (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**m_vertexCount** (defined in [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/)) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
**m_vertices** (defined in [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/)) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
[RayCast](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#ac13bded10d09c341f64aaa2750dda6b5)(b2RayCastOutput *output, const b2RayCastInput &input, const b2Transform &transform, int32 childIndex) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
[Set](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a8aa13a7584b58f08be4d84181b5a86a8)(const b2Vec2 *vertices, int32 vertexCount) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
[SetAsBox](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a6bb90df8b4a40d1c53b64cc352a855dd)(float32 hx, float32 hy) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
[SetAsBox](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a890690250115483da6c7d69829be087e)(float32 hx, float32 hy, const b2Vec2 ¢er, float32 angle) | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | |
[TestPoint](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/#a69ccc2f671394b3cc1a00a16ef36b12b)(const b2Transform &transform, const b2Vec2 &p) const | [b2PolygonShape](../../../../../api-ref/1.0/Box2D/html/classb2_polygon_shape/) | ` [virtual]` |
**Type** enum name (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | |
**~b2Shape**() (defined in [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/)) | [b2Shape](../../../../../api-ref/1.0/Box2D/html/classb2_shape/) | ` [inline, virtual]` |