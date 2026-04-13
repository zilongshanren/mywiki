---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_space/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Basic Unit of Simulation in Chipmunk.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_space/#details)

`#include <cpSpace.h>`


Basic Unit of Simulation in Chipmunk.

| cpSpace::CP_PRIVATE | ( | int | locked | ) |

Determines how fast overlapping shapes are pushed apart. Expressed as a fraction of the error remaining after each second. Defaults to pow(1.0 - 0.1, 60.0) meaning that Chipmunk fixes 10% of overlap each frame at 60Hz.

Number of frames that contact information should persist. Defaults to 3. There is probably never a reason to change this value.

Amount of encouraged penetration between colliding shapes. Used to reduce oscillating contacts and keep the collision cache warm. Defaults to 0.1. If you have poor simulation quality, increase this number as much as possible without allowing visible amounts of overlap.

Damping rate expressed as the fraction of velocity bodies retain each second. A value of 0.9 would mean that each body's velocity will drop 10% per second. The default value is 1.0, meaning no damping is applied.

Rebuild the contact graph during each step. Must be enabled to use the [cpBodyEachArbiter()](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/group__cp_body/#gacc958b3adad795e718682bea830d4135) function. Disabled by default for a small performance boost. Enabled implicitly when the sleeping feature is enabled.

Speed threshold for a body to be considered idle. The default value of 0 means to let the space guess a good threshold based on gravity.

Time a group of bodies must remain idle in order to fall asleep. Enabling sleeping also implicitly enables the the contact graph. The default value of INFINITY disables the sleeping algorithm.