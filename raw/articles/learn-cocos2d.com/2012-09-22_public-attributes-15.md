---
title: Public Attributes
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_mouse_joint_def/
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

`#include <b2MouseJoint.h>`


|

Mouse joint definition. This requires a world target point, tuning parameters, and the time step.

The maximum constraint force that can be exerted to move the candidate body. Usually you will express as some multiple of the weight (multiplier * mass * gravity).

The initial world target point. This is assumed to coincide with the body anchor initially.