---
title: b2FrictionJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_friction_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2FrictionJointDef Struct Reference

Friction joint definition.
[More...](#_details)

`#include <`[b2FrictionJoint.h](/)>


[List of all members.](/)


## Detailed Description

Friction joint definition.


## Constructor & Destructor Documentation

| b2FrictionJointDef::b2FrictionJointDef |
( |
|
) |
` [inline]` |



## Member Function Documentation

| void b2FrictionJointDef::Initialize |
( |
[b2Body](../../../box2d-api-reference/API/classb2_body/) * |
*bodyA*, |
|
|
[b2Body](../../../box2d-api-reference/API/classb2_body/) * |
*bodyB*, |
|
|
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*anchor* | |
|
) |
| | |

Initialize the bodies, anchors, axis, and reference angle using the world anchor and world axis.


## Member Data Documentation

The local anchor point relative to bodyA's origin.

The local anchor point relative to bodyB's origin.

The maximum friction force in N.

The maximum friction torque in N-m.


The documentation for this struct was generated from the following files: