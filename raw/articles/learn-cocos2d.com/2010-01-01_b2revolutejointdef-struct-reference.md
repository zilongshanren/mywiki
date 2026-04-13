---
title: b2RevoluteJointDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_revolute_joint_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2RevoluteJoint.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

Revolute joint definition. This requires defining an anchor point where the bodies are joined. The definition uses local anchor points so that the initial configuration can violate the constraint slightly. You also need to specify the initial relative angle for joint limits. This helps when saving and loading a game. The local anchor points are measured from the body's origin rather than the center of mass because: 1. you might not know where the center of mass will be. 2. if you add/remove shapes from a body and recompute the mass, the joints will be broken.

| b2RevoluteJointDef::b2RevoluteJointDef | ( | ) | ` [inline]` |

Initialize the bodies, anchors, and reference angle using a world anchor point.

The maximum motor torque used to achieve the desired motor speed. Usually in N-m.

The body2 angle minus body1 angle in the reference state (radians).