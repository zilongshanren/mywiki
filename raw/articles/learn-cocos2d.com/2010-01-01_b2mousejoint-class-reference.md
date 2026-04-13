---
title: b2MouseJoint Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_mouse_joint/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# b2MouseJoint Class Reference

`#include <`[b2MouseJoint.h](/)>


[List of all members.](/)


## Detailed Description

A mouse joint is used to make a point on a body track a specified world point. This a soft constraint with a maximum force. This allows the constraint to stretch and without applying huge forces. NOTE: this joint is not documented in the manual because it was developed to be used in the testbed. If you want to learn how to use the mouse joint, look at the testbed.


## Constructor & Destructor Documentation


## Member Function Documentation

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2MouseJoint::GetAnchorA |
( |
|
) |
const` [virtual]` |

[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2MouseJoint::GetAnchorB |
( |
|
) |
const` [virtual]` |

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2MouseJoint::GetDampingRatio |
( |
|
) |
const |


[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2MouseJoint::GetFrequency |
( |
|
) |
const |


[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2MouseJoint::GetMaxForce |
( |
|
) |
const |


[b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) b2MouseJoint::GetReactionForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) b2MouseJoint::GetReactionTorque |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*inv_dt* |
) |
const` [virtual]` |

const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & b2MouseJoint::GetTarget |
( |
|
) |
const |


| void b2MouseJoint::InitVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |

| void b2MouseJoint::SetDampingRatio |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*ratio* |
) |
|

Set/get the damping ratio (dimensionless).

| void b2MouseJoint::SetFrequency |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*hz* |
) |
|

Set/get the frequency in Hertz.

| void b2MouseJoint::SetMaxForce |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*force* |
) |
|

Set/get the maximum force in Newtons.

| void b2MouseJoint::SetTarget |
( |
const [b2Vec2](../../../box2d-api-reference/API/structb2_vec2/) & |
*target* |
) |
|

Use this to update the target point.

| bool b2MouseJoint::SolvePositionConstraints |
( |
[float32](../../../box2d-api-reference/API/b2_settings_8h/#aacdc525d6f7bddb3ae95d5c311bd06a1) |
*baumgarte* |
) |
` [inline, protected, virtual]` |

| void b2MouseJoint::SolveVelocityConstraints |
( |
const [b2TimeStep](../../../box2d-api-reference/API/structb2_time_step/) & |
*step* |
) |
` [protected, virtual]` |


## Friends And Related Function Documentation


## Member Data Documentation


The documentation for this class was generated from the following files: