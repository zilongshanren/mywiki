---
title: b2QueryCallback Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_query_callback/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2QueryCallback Class Reference

`#include <`[b2WorldCallbacks.h](../../../box2d-api-reference/API/b2_world_callbacks_8h_source/)>


[List of all members.](/)


## Detailed Description

Callback class for AABB queries. See b2World::Query


## Constructor & Destructor Documentation

| virtual b2QueryCallback::~b2QueryCallback |
( |
|
) |
` [inline, virtual]` |



## Member Function Documentation

| virtual bool b2QueryCallback::ReportFixture |
( |
[b2Fixture](../../../box2d-api-reference/API/classb2_fixture/) * |
*fixture* |
) |
` [pure virtual]` |

Called for each fixture found in the query AABB.

**Returns:**- false to terminate the query.


The documentation for this class was generated from the following file: