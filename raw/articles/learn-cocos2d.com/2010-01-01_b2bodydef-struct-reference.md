---
title: b2BodyDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_body_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Body.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

A body definition holds all the data needed to construct a rigid body. You can safely re-use body definitions. Shapes are added to a body after construction.

| b2BodyDef::b2BodyDef | ( | ) | ` [inline]` |

This constructor sets the body definition default values.

Set this flag to false if this body should never fall asleep. Note that this increases CPU usage.

Angular damping is use to reduce the angular velocity. The damping parameter can be larger than 1.0f but the damping effect becomes sensitive to the time step when the damping parameter is large.

Is this a fast moving body that should be prevented from tunneling through other moving bodies? Note that all bodies are prevented from tunneling through kinematic and static bodies. This setting is only considered on dynamic bodies.

Linear damping is use to reduce the linear velocity. The damping parameter can be larger than 1.0f but the damping effect becomes sensitive to the time step when the damping parameter is large.

The world position of the body. Avoid creating bodies at the origin since this can lead to many overlapping shapes.

The body type: static, kinematic, or dynamic. Note: if a dynamic body would have zero mass, the mass is set to one.