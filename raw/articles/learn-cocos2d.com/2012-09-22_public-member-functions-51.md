---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_sweep/
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

`#include <b2Math.h>`


| void |
|

This describes the motion of a body/shape for TOI computation. Shapes are defined with respect to the body origin, which may no coincide with the center of mass. However, to support dynamics we must interpolate the center of mass position.

Advance the sweep forward, yielding a new initial state.

| alpha | the new initial time. |

Get the interpolated transform at a specific time.

| beta | is a factor in [0,1], where 0 indicates alpha0. |

Normalize the angles.

Normalize an angle in radians to be between -pi and pi.

Fraction of the current time step in the range [0,1] c0 and a0 are the positions at alpha0.