---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_chain_and_polygon_contact/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](/)

Public Member Functions
|
| **b2ChainAndPolygonContact** ([b2Fixture](../../../../../api-ref/1.0/Box2D/html/classb2_fixture/) *fixtureA, int32 indexA, [b2Fixture](../../../../../api-ref/1.0/Box2D/html/classb2_fixture/) *fixtureB, int32 indexB) |
| void | [Evaluate](../../../../../api-ref/1.0/Box2D/html/classb2_chain_and_polygon_contact/#a8c25ceb49d981797d0a7f8a1ea769442) ([b2Manifold](../../../../../api-ref/1.0/Box2D/html/structb2_manifold/) *manifold, const [b2Transform](../../../../../api-ref/1.0/Box2D/html/structb2_transform/) &xfA, const [b2Transform](../../../../../api-ref/1.0/Box2D/html/structb2_transform/) &xfB) |
| | Evaluate this contact with your own manifold and transforms.
|
Static Public Member Functions
|
static [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) * | **Create** ([b2Fixture](../../../../../api-ref/1.0/Box2D/html/classb2_fixture/) *fixtureA, int32 indexA, [b2Fixture](../../../../../api-ref/1.0/Box2D/html/classb2_fixture/) *fixtureB, int32 indexB, [b2BlockAllocator](../../../../../api-ref/1.0/Box2D/html/classb2_block_allocator/) *allocator) |
static void | **Destroy** ([b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/) *contact, [b2BlockAllocator](../../../../../api-ref/1.0/Box2D/html/classb2_block_allocator/) *allocator) |


## Member Function Documentation

Evaluate this contact with your own manifold and transforms.

Implements [b2Contact](../../../../../api-ref/1.0/Box2D/html/classb2_contact/#ae3c2842e5325b2d4500f8ed1d4de2f72).


The documentation for this class was generated from the following file:

- b2ChainAndPolygonContact.h