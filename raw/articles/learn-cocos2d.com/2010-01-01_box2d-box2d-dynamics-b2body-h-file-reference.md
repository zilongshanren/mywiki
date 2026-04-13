---
title: Box2D/Box2D/Dynamics/b2Body.h File Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/b2_body_8h/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# Box2D/Box2D/Dynamics/b2Body.h File Reference

`#include <`[Box2D/Common/b2Math.h](b2_math_8h_source.html)>

`#include <`[Box2D/Collision/Shapes/b2Shape.h](b2_shape_8h_source.html)>

`#include <memory>`

[Go to the source code of this file.](/)


## Enumeration Type Documentation

The body type. static: zero mass, zero velocity, may be manually moved kinematic: zero mass, non-zero velocity set by user, moved by solver dynamic: positive mass, non-zero velocity determined by forces, moved by solver

**Enumerator: **
b2_staticBody |
|
b2_kinematicBody |
|
b2_dynamicBody |
|