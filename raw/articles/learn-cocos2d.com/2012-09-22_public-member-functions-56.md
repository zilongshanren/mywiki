---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_weld_joint_def/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Box2D
2.2
Box2D API Reference for www.kobold2d.com developers
|

`#include <b2WeldJoint.h>`


| void |
|

Weld joint definition. You need to specify local anchor points where they are attached and the relative body angle. The position of the anchor points is important for computing the reaction torque.

Initialize the bodies, anchors, and reference angle using a world anchor point.

The mass-spring-damper frequency in Hertz. Rotation only. Disable softness with a value of 0.

The bodyB angle minus bodyA angle in the reference state (radians).