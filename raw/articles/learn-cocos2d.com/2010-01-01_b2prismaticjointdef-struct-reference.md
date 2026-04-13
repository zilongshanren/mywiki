---
title: b2PrismaticJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_prismatic_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2PrismaticJoint.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

Prismatic joint definition. This requires defining a line of motion using an axis and an anchor point. The definition uses local anchor points and a local axis so that the initial configuration can violate the constraint slightly. The joint translation is zero when the local anchor points coincide in world space. Using local anchors and a local axis helps when saving and loading a game.

| b2PrismaticJointDef::b2PrismaticJointDef | ( | ) | ` [inline]` |

| void b2PrismaticJointDef::Initialize | ( |
|

Initialize the bodies, anchors, axis, and reference angle using the world anchor and world axis.

The constrained angle between the bodies: body2_angle - body1_angle.