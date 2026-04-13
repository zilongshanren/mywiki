---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_constraint/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Opaque [cpConstraint](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_constraint/) struct.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/Chipmunk/html/structcp_constraint/#details)

`#include <cpConstraint.h>`


|

The rate at which joint error is corrected. Defaults to pow(1.0 - 0.1, 60.0) meaning that it will correct 10% of the error every 1/60th of a second.

The maximum rate at which joint error is corrected. Defaults to infinity.

The maximum force that this constraint is allowed to use. Defaults to infinity.

Function called after the solver runs. Use the applied impulse to perform effects like breakable joints.

Function called before the solver runs. Animate your joint anchors, update your motor torque, etc.