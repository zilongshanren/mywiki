---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_prismatic_joint_def/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2PrismaticJoint.h>`


| void |
|

Prismatic joint definition. This requires defining a line of motion using an axis and an anchor point. The definition uses local anchor points and a local axis so that the initial configuration can violate the constraint slightly. The joint translation is zero when the local anchor points coincide in world space. Using local anchors and a local axis helps when saving and loading a game.

| void b2PrismaticJointDef::Initialize | ( |
|

Initialize the bodies, anchors, axis, and reference angle using the world anchor and unit world axis.

The constrained angle between the bodies: bodyB_angle - bodyA_angle.