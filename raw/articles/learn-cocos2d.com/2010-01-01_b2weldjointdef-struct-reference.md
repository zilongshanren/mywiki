---
title: b2WeldJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_weld_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2WeldJoint.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

Weld joint definition. You need to specify local anchor points where they are attached and the relative body angle. The position of the anchor points is important for computing the reaction torque.

| b2WeldJointDef::b2WeldJointDef | ( | ) | ` [inline]` |

Initialize the bodies, anchors, and reference angle using a world anchor point.

The body2 angle minus body1 angle in the reference state (radians).