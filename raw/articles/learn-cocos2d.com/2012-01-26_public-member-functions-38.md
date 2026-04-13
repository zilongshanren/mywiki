---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_distance_joint_def/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2DistanceJoint.h>`


| void |
|

Distance joint definition. This requires defining an anchor point on both bodies and the non-zero length of the distance joint. The definition uses local anchor points so that the initial configuration can violate the constraint slightly. This helps when saving and loading a game.

| void b2DistanceJointDef::Initialize | ( |
|

Initialize the bodies, anchors, and length using the world anchors.

The mass-spring-damper frequency in Hertz. A value of 0 disables softness.