---
title: b2Sweep Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_sweep/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Math.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_math_8h_source/)>

## Public Member Functions | |
| void |
|

This describes the motion of a body/shape for TOI computation. Shapes are defined with respect to the body origin, which may no coincide with the center of mass. However, to support dynamics we must interpolate the center of mass position.

Advance the sweep forward, yielding a new initial state.

t | the new initial time. |

Get the interpolated transform at a specific time.

alpha | is a factor in [0,1], where 0 indicates t0. |