---
title: b2DistanceJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_distance_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2DistanceJoint.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

Distance joint definition. This requires defining an anchor point on both bodies and the non-zero length of the distance joint. The definition uses local anchor points so that the initial configuration can violate the constraint slightly. This helps when saving and loading a game.

| b2DistanceJointDef::b2DistanceJointDef | ( | ) | ` [inline]` |

| void b2DistanceJointDef::Initialize | ( |
|

Initialize the bodies, anchors, and length using the world anchors.