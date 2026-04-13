---
title: b2JointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2JointDef Struct Reference

Joint definitions are used to construct joints.
[More...](#_details)

`#include <`[b2Joint.h](/)>


[List of all members.](/)

## Public Member Functions |
| | [b2JointDef](../../../box2d-api-reference/API/structb2_joint_def/#a1fdb44829d4fd13c72edb1daacb72f89) () |
## Public Attributes |
[b2JointType](/#a0bb202d8a286c888a11985b07b2272ab) | [type](../../../box2d-api-reference/API/structb2_joint_def/#a470f2879b24adb05facbd49f338856fb) |
| | The joint type is set automatically for concrete joint types.
|
| void * | [userData](../../../box2d-api-reference/API/structb2_joint_def/#a07eb150daaaa52fc09c3bcf402b295fe) |
| | Use this to attach application specific data to your joints.
|
[b2Body](../../../box2d-api-reference/API/classb2_body/) * | [bodyA](../../../box2d-api-reference/API/structb2_joint_def/#a8cd54c93da396be75a9788f2c6897f05) |
| | The first attached body.
|
[b2Body](../../../box2d-api-reference/API/classb2_body/) * | [bodyB](../../../box2d-api-reference/API/structb2_joint_def/#aa4f4dee2fbcd12187b19506b60e68e3d) |
| | The second attached body.
|
| bool | [collideConnected](../../../box2d-api-reference/API/structb2_joint_def/#aef099a1f89b64e230173b6016848ea9b) |
| | Set this flag to true if the attached bodies should collide.
|


## Detailed Description

Joint definitions are used to construct joints.


## Constructor & Destructor Documentation

| b2JointDef::b2JointDef |
( |
|
) |
` [inline]` |



## Member Data Documentation

The second attached body.

Set this flag to true if the attached bodies should collide.

The joint type is set automatically for concrete joint types.

Use this to attach application specific data to your joints.


The documentation for this struct was generated from the following file: